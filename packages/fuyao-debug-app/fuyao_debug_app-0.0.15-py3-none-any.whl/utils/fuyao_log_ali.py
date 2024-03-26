import click
import re
import os
import json
import logging
import multiprocessing
import sys
from urllib.parse import urlencode

import requests
from requests.adapters import HTTPAdapter
from requests.exceptions import ChunkedEncodingError, ConnectionError

from .sigs import *

sys.path.append("..")
from config import config as cfg


def get_fuyao_log(job, log_path):
    tail_flag = False
    sts = int(job['time_start'] // 1000)
    ets = int(job['time_end'] // 1000)
    if sts > 0 and ets - sts > 3600 * 6:
        click.echo(f"job's duration > 6h, using tail to get log.")
        tail_flag = True  # 任务时间太长，只tail日志

    job_name = job.run_name
    node_list = job.node_list
    log_path = os.path.join(log_path, 'log')
    ret = {}
    file_list = gen_file_list(job_name, node_list)
    click.echo(f"Log File List: {file_list}")
    get_fuyao_logs(file_list, tail_flag, log_path)

    node_logname_dict = {}
    # read file content to memory
    index = 0
    for node in node_list.split(','):
        data = ''
        log_file_name = '%s-%s.out.log' % (job_name, str(index))
        err_file_name = '%s-%s.err.log' % (job_name, str(index))
        node_logname_dict[node] = [log_file_name, err_file_name]

        log_file = f'{log_path}/{log_file_name}'
        err_file = f'{log_path}/{err_file_name}'
        if os.path.exists(log_file) or os.path.exists(err_file):
            if os.path.exists(log_file):
                with open(log_file, 'r') as file:
                    data = data + '\n' + file.read()
                    ret[node] = data
                    file.close()
            if os.path.exists(err_file):
                with open(err_file, 'r') as file:
                    data = data + '\n' + file.read()
                    ret[node] = data
                    file.close()
        else:
            ret[node] = ''
        index = index + 1
    return ret, node_logname_dict


def gen_file_list(job_name, node_list):
    nodes = node_list.split(',')
    index = 0
    ret = []
    for node in nodes:
        filename = '%s-%s.err.txt' % (job_name, str(index))
        ret.append(filename)
        filename = '%s-%s.out.txt' % (job_name, str(index))
        ret.append(filename)
        index = index + 1
    return ret


def get_fuyao_logs(file_list, tail_flag, log_path):
    jobs = []
    for i in range(0, len(file_list)):
        p = multiprocessing.Process(target=get_log, args=(file_list[i], 'fuyao', tail_flag, log_path))
        logging.info('write log into file, %s' % file_list[i])
        jobs.append(p)
        p.start()

    for p in jobs:
        p.join()


def get_log(file, site, tail_flag, log_path):
    # Parse out node id.
    tokens = file.split('-')
    job_name = '-'.join(tokens[:-1])
    rank = int(tokens[-1].split('.')[0])
    source = 'stdout' if 'out' in file else 'stderr'
    # head = 0
    # if head > 10000:
    #     print(f"--head MAXIMUM is 10000, now is {head}")
    #     return
    # if tail > 1000:
    #     print(f"--tail MAXIMUM is 1000, now is {tail}")
    #     return
    head = -1
    if tail_flag:
        tail = 1000
    else:
        tail = -1

    start_after = ''
    end_before = ''
    log_host = 'http://8.130.29.99'
    use_timestamps = False
    maximum_idle_second = 1
    # TODO can get namespace from job?
    namespace = "default"
    container = "pytorch"
    pod_name = get_k8s_pod_name(job_name, rank)
    log_name = "fuyao-job"
    is_stream = False
    if is_stream:
        maximum_idle_second = 600
    try:
        # log_path = os.path.join(log_path, 'log')
        if not os.path.exists(log_path):
            os.makedirs(log_path)
        for line in get_logs(
                host=log_host,
                log_name=log_name,
                namespace=namespace,
                pod_name=pod_name,
                container=container,
                source=source,
                maximum_idle_second=maximum_idle_second,
                head=head,
                tail=tail,
                start_after=start_after,
                end_before=end_before,
        ):
            msg = ""
            if use_timestamps:
                msg = line["timestamp"] + " "
            msg += line["content"]
            # filename = '/data/{}.{}.log'.format(file.split('.')[0], file.split('.')[1])
            filename = f'{log_path}/{file.split(".")[0]}.{file.split(".")[1]}.log'
            with open(filename, 'a+') as logfile:
                # Writing data to a file
                logfile.writelines(msg + '\n')
    except KeyboardInterrupt:
        sys.exit(1)
    except ConnectionError as e:
        click.echo("Connection error, please contact the administrator!"
                   f" and paste the following message:\n{e}")
    except ChunkedEncodingError as e:
        if "Connection broken" in e.__str__():
            click.echo("Timeout, please try again later!")
        else:
            click.echo(f"Server Error: Can't fetch logs\n{e}, "
                       "please contact the administrator!")
    except NameError as e:
        click.echo(e)
    except RuntimeError as e:
        click.echo(e)


def get_logs(
        host,
        log_name,
        namespace,
        pod_name,
        source=None,
        container=None,
        maximum_idle_second=1,
        tail=-1,
        head=-1,
        start_after=None,
        end_before=None
):
    url = "{}/api/v1/logs/{index}/scroll".format(
        host,
        index=log_name,
    )
    # streaming log
    if maximum_idle_second > 1:
        url = "{}/api/v1/logs/{index}/index".format(
            host,
            index=log_name,
        )
    query_params = {
        "podname": pod_name,
        "timeout": maximum_idle_second,
        "tail": tail,
        "head": head,
        "namespace": "default" if namespace is None else namespace,
    }
    if source is not None:
        query_params["stream"] = source
    if container is not None:
        query_params["container"] = container
    if start_after:
        query_params["start_after"] = start_after
    if end_before:
        query_params["end_before"] = end_before
    url = "{}?{}".format(url, urlencode(query_params))
    s = requests.Session()
    s.mount(host, HTTPAdapter(max_retries=3))
    with s.get(url, stream=True) as resp:
        if resp.status_code == 200:
            for line in resp.iter_lines():
                res = json.loads(line.decode("utf-8"))
                yield res
        elif resp.status_code == 404:
            raise NameError(f"Not found log name: {log_name}")
        elif resp.status_code == 500:
            raise RuntimeError("Server error, please run wait a moment"
                               " or contact the administrator")


def get_k8s_pod_name(job_name, rank):
    if rank == 0:
        return job_name + "-master-0"
    else:
        return job_name + "-worker-" + str(rank - 1)


def analyze_job_log(log_data, node_logname_dict, process_no=8):
    lv0_excmatch = None
    lv0_matched = False
    lv0_type = ''
    lv1_matched = False
    lv1_type = ''
    detail = ''  # 记录具体原因， 对应数据库中job_failed_subdetail字段，job_failed_detail不使用
    cur_node = ''
    for key in log_data.keys():
        # if already matched an exception, break
        if lv0_excmatch:
            break
        node_log = log_data[key]
        if node_log == '':
            continue

        # step1: search exception
        sig0 = re.sub('\n\s+', '', signatures_lv0_exception['0000'])
        lv0_excmatch = re.search(sig0, node_log)
        # check if there is no exception terminate
        if not lv0_excmatch:  # no traceback in log, no exception
            for lv_key in signatures_lv0_noexception.keys():
                if lv_key == 'type':
                    continue
                sig_noexc = re.sub('\n\s+', '', signatures_lv0_noexception[lv_key])
                lv0_noexcmatch = re.search(sig_noexc, node_log)
                if lv0_noexcmatch:
                    lv0_type = signatures_lv0_noexception['type']
                    lv0_matched = True
                    detail = lv0_noexcmatch.group(0)
                    cur_node = key
                    break

        if lv0_excmatch:  # there is Traceback in log, find exception
            lv0_matched = True
            lv0_noexcmatch = False
            lv0_type = signatures_lv0_exception['type']
            # step2: search lv2 sig
            for lv_key in signatures_lv1_dataloader.keys():
                if lv1_type != '':
                    break
                if lv_key == 'type':
                    continue
                else:
                    sig1 = re.sub('\n\s+', '', signatures_lv1_dataloader[lv_key])
                    lv1_match = re.search(sig1, node_log)

                    if lv1_match:
                        lv1_matched = True
                        lv1_type = signatures_lv1_dataloader['type']
                        detail = lv1_match.group(0)
                        cur_node = key
                        break
            for lv_key in signatures_lv1_cuda.keys():
                if lv1_type != '':
                    break
                if lv_key == 'type':
                    continue
                else:
                    sig1 = re.sub('\n\s+', '', signatures_lv1_cuda[lv_key])
                    lv1_match = re.search(sig1, node_log)
                    if lv1_match:
                        lv1_matched = True
                        lv1_type = signatures_lv1_cuda['type']
                        detail = lv1_match.group(0)
                        cur_node = key
                        break
            for lv_key in signatures_lv1_infra.keys():
                if lv1_type != '':
                    break
                if lv_key == 'type':
                    continue
                else:
                    sig1 = re.sub('\n\s+', '', signatures_lv1_infra[lv_key])
                    lv1_match = re.search(sig1, node_log)
                    if lv1_match:
                        lv1_matched = True
                        lv1_type = signatures_lv1_infra['type']
                        detail = lv1_match.group(0)
                        cur_node = key
                        break
            for lv_key in signatures_lv1_usercode.keys():
                if lv1_type != '':
                    break
                if lv_key == 'type':
                    continue
                else:
                    sig1 = re.sub('\n\s+', '', signatures_lv1_usercode[lv_key])
                    lv1_match = re.search(sig1, node_log)
                    if lv1_match:
                        lv1_matched = True
                        lv1_type = signatures_lv1_usercode['type']
                        detail = lv1_match.group(0)
                        cur_node = key
                        break

    # 有traceback，但是exception不属于任何一种； 没有traceback，也不属于noexception的任何一种
    if not lv0_matched and not lv1_matched:
        lv0_type = 'unknown'
        lv1_type = 'unknown'

    # remove_log_files(job_name)

    # click.echo(cfg.FORMAT_DICT['step_head'] + f"Worker process analyse" + cfg.FORMAT_DICT['step_tail'])
    # # worker process analyse
    # # 1. check initiation
    # initiation = False
    # node_process_no_dict = {}
    # for node, data in log_data.items():
    #     # click.echo(f"Node: {node}, Data: {data}")
    #
    #     sig = re.sub('\n\s+', '', worker_process_exception['0000'])
    #     res = re.findall(sig, data)
    #     node_process_no_dict[node] = len(res)
    # node_process_no_dict['Total'] = sum(node_process_no_dict.values())
    # click.echo(f"Node Process No Dict: {node_process_no_dict}")
    # if (node_process_no_dict['Total'] == process_no or
    #         (node_process_no_dict['Total'] % process_no == 0 and node_process_no_dict['Total'] // process_no > 0)):
    #     initiation = True
    #
    # # 2. check exit
    # has_exit = False
    # exit_node_list = []
    # for node, data in log_data.items():
    #     # click.echo(f"Node: {node}, Data: {data}")
    #
    #     sig = re.sub('\n\s+', '', worker_process_exception['0001'])
    #     exit_match = re.search(sig, data)
    #     if exit_match:
    #         has_exit = True
    #         exit_node_list.append(node)
    # click.echo(f"Exit Node List: {exit_node_list}")

    return {
        'lv0': lv0_type,
        'lv1': lv1_type,
        'detail': detail,
        'node': cur_node,
        'logname': node_logname_dict[cur_node]
    }


def analyze_worker_process(log_data, process_no=8):
    # worker process analyse
    # 1. check initiation
    initiation = False
    node_process_no_dict = {}
    for node, data in log_data.items():
        # click.echo(f"Node: {node}, Data: {data}")
        sig = re.sub('\n\s+', '', worker_process_exception['0000'])
        res = re.findall(sig, data)
        node_process_no_dict[node] = len(res)
    node_process_no_dict['Total'] = sum(node_process_no_dict.values())
    # click.echo(f"Node Process Number Dict: {node_process_no_dict}")
    if (node_process_no_dict['Total'] == process_no or
            (node_process_no_dict['Total'] % process_no == 0 and node_process_no_dict['Total'] // process_no > 0)):
        initiation = True

    # 2. check exit
    has_exit = False
    exit_node_list = []
    for node, data in log_data.items():
        # click.echo(f"Node: {node}, Data: {data}")
        sig = re.sub('\n\s+', '', worker_process_exception['0001'])
        exit_match = re.search(sig, data)
        if exit_match:
            has_exit = True
            exit_node_list.append(node)
    # click.echo(f"Exit Node List: {exit_node_list}")

    return {
        'initiation': initiation,
        'has_exit': has_exit,
        'node_process_no_dict': node_process_no_dict,
        'exit_node_list': exit_node_list
    }
