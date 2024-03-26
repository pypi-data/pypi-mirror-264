import click
import datetime
import os.path
from db.base_fuyao_db import get_job_info
from utils.fuyao_log_ali import get_fuyao_log, analyze_job_log, analyze_worker_process
from config.config import NODE_LIST, FORMAT_DICT
from utils.utils import send_node_health_check_request, send_collect_ranks_stack_request


@click.group()
def cli():
    pass


# 0. 包含以下1-6所有功能
@cli.command()
@click.option('--job_name', prompt='Job Name',
              help='The name of a job. Checkout a job name by "fuyao view" or "fuyao history".')
@click.option('--env', prompt='Environment', type=click.Choice(['prd', 'dev']),
              help='prd: in pods | dev: at local machine. To determine which DB will be used.')
@click.option('--log_path', default='.', help='The path where tool will put the logs.')
def combo(job_name, env, log_path):
    """All included."""
    click.echo(FORMAT_DICT['step_head'] + f"Start to check job: {job_name}" + FORMAT_DICT['step_tail'])

    click.echo(FORMAT_DICT['step_head'] + f"0. data preparation" + FORMAT_DICT['step_tail'])
    # 0. data preparation
    # 0.1 get job info from db
    # e.g. Job Info: ('bifrost-20240320184129-yuyh2', 1710985425396, 1710986032217,
    # 'cnwlb-a100-p01002,cnwlb-a100-p01008,cnwlb-a100-p01022,cnwlb-a100-p01018', 'JOB_COMPLETE', 'fuyao_b1', 4, 8)
    job_info, code = get_job_info(job_name, env)
    click.echo(f"Job Info: {job_info}, Code: {code}")
    if job_info is None or code != 200:
        click.echo(FORMAT_DICT['warning_head'] + f"Job {job_name} not found or DB error." + FORMAT_DICT['warning_tail'])
        return

    # 0.2 get node_list and node_info_dict from job_info['node_list']
    # e.g. nodes_list: ['cnwlb-a100-p01002', 'cnwlb-a100-p01008', 'cnwlb-a100-p01022', 'cnwlb-a100-p01018']
    # e.g. nodes_info_list: [
    # {'pod_ip': '10.1.0.58', 'node_name': 'cnwlb-a100-p01002'},
    # {'pod_ip': '10.1.0.44', 'node_name': 'cnwlb-a100-p01008'},
    # {'pod_ip': '10.1.0.75', 'node_name': 'cnwlb-a100-p01022'},
    # {'pod_ip': '10.1.0.52', 'node_name': 'cnwlb-a100-p01018'}]
    nodes_list = [node.strip() for node in job_info['node_list'].split(',')]
    # nodes_list = ['cnwlp-gpu-p02084']  # for test
    nodes_info_list = []
    for node in nodes_list:
        if node in NODE_LIST:
            nodes_info_list.append({
                'pod_ip': NODE_LIST[node],
                'node_name': node,
            })
        else:
            click.echo(
                FORMAT_DICT['warning_head'] + f"node: {node} do not exist in NODE_LIST" + FORMAT_DICT['warning_tail'])
            return
    click.echo(f"nodes_list: {nodes_list}")
    click.echo(f"nodes_info_list: {nodes_info_list}")
    if nodes_list is None or len(nodes_list) == 0 or nodes_list[0] == '':
        click.echo(
            FORMAT_DICT['warning_head'] + 'nodes_list is empty, no nodes to check.' + FORMAT_DICT['warning_tail'])
        return

    # 0.3 get start_time and end_time from job_info
    # e.g. time_start: 2024-03-21 01:43:45, time_end: 2024-03-21 01:53:52
    dt_start = datetime.datetime.utcfromtimestamp(job_info['time_start'] // 1000) if job_info[
                                                                                         'time_start'] != 0 else None
    dt_end = datetime.datetime.utcfromtimestamp(job_info['time_end'] // 1000) if job_info['time_end'] != 0 else None
    click.echo(f"time_start: {dt_start}, time_end: {dt_end}")

    # 0.4 get log_data and node_logname_dict from es based on job_info
    # e.g. node_logname_dict: {
    # 'cnwlb-a100-p01002': ['bifrost-20240320184129-yuyh2-0.out.log', 'bifrost-20240320184129-yuyh2-0.err.log'], ...}
    log_data, node_logname_dict = get_fuyao_log(job_info, log_path)
    click.echo(f"node_logname_dict: {node_logname_dict}")

    # 0.5 get devops container url based on job_info['site']
    cluster = job_info['site']
    base_url = ''
    if cluster == 'fuyao':
        base_url = r'http://fuyao-devop-container.xiaopeng.link/'
    elif cluster == 'fuyao_a1':
        # TODO new dn
        base_url = r'http://fuyao-devop-container.a1.xiaopeng.link/'
    elif cluster == 'fuyao_b1':
        # TODO new dn
        base_url = r'http://fuyao-devop-container.b1.xiaopeng.link/'
    flame_url = base_url + 'get_flame_graph'
    rank_url = base_url + 'collect_ranks_stack'

    # 1. 检查设备是否出现异常
    click.echo(FORMAT_DICT['step_head'] + f"1. check_device" + FORMAT_DICT['step_tail'])

    # 1.1. call api to check device health
    url = r'http://fuyao-admin-backend.xiaopeng.link/check-nodes-status'
    data = send_node_health_check_request(url, job_name, nodes_list, dt_start, dt_end)
    click.echo(f"Data: {data}")
    if data is None:
        click.echo(FORMAT_DICT['warning_head'] + f"Error: No node health data returned." + FORMAT_DICT['warning_tail'])

    # 1.2. conclude the result
    unhealthy_nodes = []
    for node, info in data['status'].items():
        node, state = node, info['state']
        click.echo(f"Node: {node}, Status: {state}")
        if state != 'healthy':
            unhealthy_nodes.append(node)

    if len(unhealthy_nodes) > 0:
        click.echo(FORMAT_DICT['warning_head'] + f"Unhealthy Nodes: {unhealthy_nodes}" + FORMAT_DICT['warning_tail'])
    else:
        click.echo(FORMAT_DICT['result_head'] + f"All nodes are healthy." + FORMAT_DICT['result_tail'])

    # 2. 检查所有job相关node的log，是否有exception，分析exception
    click.echo(FORMAT_DICT['step_head'] + f"2. check_log_exception" + FORMAT_DICT['step_tail'])

    click.echo(f"Logs are saved and start to analysis exceptions")
    fail_info = analyze_job_log(log_data, node_logname_dict)
    # log exception result
    click.echo(FORMAT_DICT['result_head'] + f"Exception Info: {fail_info}" + FORMAT_DICT['result_tail'])

    # 3. 检查是否有worker process退出
    click.echo(FORMAT_DICT['step_head'] + f"3. check_workers_exit" + FORMAT_DICT['step_tail'])

    # 3.1 日志检测是否有worker退出
    click.echo(f"Logs are saved and start to analysis worker processes")
    process_no = job_info['node_count'] * job_info['gpus_per_node']
    fail_info = analyze_worker_process(log_data, process_no)
    click.echo(f"Exit node list: {fail_info['exit_node_list']}")
    if fail_info['has_exit']:
        click.echo(FORMAT_DICT['warning_head'] + f"Has exit? {fail_info['has_exit']}" + FORMAT_DICT['warning_tail'])
    else:
        click.echo(FORMAT_DICT['result_head'] + f"Has exit? {fail_info['has_exit']}" + FORMAT_DICT['result_tail'])

    # 3.2 TODO - 检测主进程相关的子进程有没有退出, 比较数量？

    # 4. 检查所有worker是否完成初始化
    click.echo(FORMAT_DICT['step_head'] + f"4. check_workers_initiation" + FORMAT_DICT['step_tail'])

    # 日志检测是否所有worker都完成初始化
    click.echo(f"Node process number: {fail_info['node_process_no_dict']}")
    if fail_info['initiation']:
        click.echo(
            FORMAT_DICT['result_head'] + f"All initialized? {fail_info['initiation']}" + FORMAT_DICT['result_tail'])
    else:
        click.echo(
            FORMAT_DICT['warning_head'] + f"All initialized? {fail_info['initiation']}" + FORMAT_DICT['warning_head'])

    if job_info['state'] != 'JOB_RUNNING':
        click.echo(
            FORMAT_DICT['step_head'] + f"Job state is not running. Can not get flame and rank stack." + FORMAT_DICT[
                'step_head'])
        return

    # 5. 自动收集各节点火焰图
    click.echo(FORMAT_DICT['step_head'] + f"5. collect_flame_graph" + FORMAT_DICT['step_tail'])

    # get graphs from all nodes
    # 5.1 对相应集群的master发起调用
    data = send_collect_ranks_stack_request(flame_url, job_name, nodes_info_list)
    if data is None:
        click.echo(FORMAT_DICT['warning_head'] + f"Error: No rank graph data returned." + FORMAT_DICT['warning_tail'])
    else:
        # 5.2 save stack info to file
        log_folder = f'{log_path}/graphs'
        if not os.path.exists(log_folder):
            os.makedirs(log_folder)

        rank_data_dict = data['rank_data_dict']
        for node_name, rank_data in rank_data_dict.items():
            filename = f'{log_folder}/{node_name}.svg'
            with open(filename, 'w+') as logfile:
                logfile.writelines(rank_data['data'])

        click.echo(FORMAT_DICT['result_head'] + f"Graph saved! See {log_folder}" + FORMAT_DICT['result_tail'])

    # 6. 自动收集各节点rank的stack
    click.echo(FORMAT_DICT['step_head'] + f"6. collect_ranks_stack" + FORMAT_DICT['step_tail'])

    # get stack info from all nodes
    # 6.1 对相应集群的master发起调用
    data = send_collect_ranks_stack_request(rank_url, job_name, nodes_info_list)
    if data is None:
        click.echo(FORMAT_DICT['warning_head'] + f"Error: No rank stack data returned." + FORMAT_DICT['warning_tail'])
    else:
        # 5.2 save stack info to file
        log_folder = f'{log_path}/stacks'
        if not os.path.exists(log_folder):
            os.makedirs(log_folder)

        rank_data_dict = data['rank_data_dict']
        for node_name, rank_data in rank_data_dict.items():
            filename = f'{log_folder}/{node_name}.log'
            with open(filename, 'w+') as logfile:
                for line in rank_data['data']:
                    logfile.write(line + '\n')

        click.echo(FORMAT_DICT['result_head'] + f"Stack saved! See {log_folder}" + FORMAT_DICT['result_tail'])


@cli.command()
@click.option('--job_name', prompt='Job Name',
              help='The name of a job. Checkout a job name by "fuyao view" or "fuyao history".')
@click.option('--env', prompt='Environment', type=click.Choice(['prd', 'dev']),
              help='prd: in pods | dev: at local machine. To determine which DB will be used.')
# 1. 检查设备是否出现异常
def check_device(job_name, env):
    """Check whether the job-related nodes have hardware problems."""
    click.echo(f"Processing Job: {job_name}")

    # 1. get job info from db
    job_info, code = get_job_info(job_name, env)
    click.echo(f"Job Info: {job_info}, Code: {code}")
    if job_info is None or code != 200:
        click.echo(FORMAT_DICT['warning_head'] + f"Job {job_name} not found or DB error." + FORMAT_DICT['warning_tail'])
        return
    nodes_list = [node.strip() for node in job_info['node_list'].split(',')]
    dt_start = datetime.datetime.utcfromtimestamp(job_info['time_start'] // 1000) if job_info[
                                                                                         'time_start'] != 0 else None
    dt_end = datetime.datetime.utcfromtimestamp(job_info['time_end'] // 1000) if job_info['time_end'] != 0 else None
    click.echo(f"node_list: {nodes_list}, time_start: {dt_start}, time_end: {dt_end}")

    if nodes_list is None or len(nodes_list) == 0 or nodes_list[0] == '':
        click.echo(
            FORMAT_DICT['warning_head'] + 'nodes_list is empty, no nodes to check.' + FORMAT_DICT['warning_tail'])
        return

    # 2. call api to check device health
    url = r'http://fuyao-admin-backend.xiaopeng.link/check-nodes-status'
    data = send_node_health_check_request(url, job_name, nodes_list, dt_start, dt_end)
    click.echo(f"Data: {data}")

    if data is None:
        click.echo(FORMAT_DICT['warning_head'] + f"Error: No data returned." + FORMAT_DICT['warning_tail'])
        return

    # 3. conclude the result
    unhealthy_nodes = []
    for node, info in data['status'].items():
        node, state = node, info['state']
        click.echo(f"Node: {node}, Status: {state}")
        if state != 'healthy':
            unhealthy_nodes.append(node)

    if len(unhealthy_nodes) > 0:
        click.echo(FORMAT_DICT['warning_head'] + f"Unhealthy Nodes: {unhealthy_nodes}" + FORMAT_DICT['warning_tail'])
    else:
        click.echo(FORMAT_DICT['result_head'] + f"All nodes are healthy." + FORMAT_DICT['result_tail'])


@cli.command()
@click.option('--job_name', prompt='Job Name',
              help='The name of a job. Checkout a job name by "fuyao view" or "fuyao history".')
@click.option('--env', prompt='Environment', type=click.Choice(['prd', 'dev']),
              help='prd: in pods | dev: at local machine. To determine which DB will be used.')
@click.option('--log_path', default='.', help='The path where tool will put the logs.')
# 2. 检查所有job相关node的log，是否有exception，分析exception
def check_log_exception(job_name, env, log_path):
    """Get and analyze job log, then return if there is an exception and corresponding details."""
    click.echo(f"Processing Job: {job_name}")

    # 1. get job info from db
    job_info, code = get_job_info(job_name, env)
    click.echo(f"Job Info: {job_info}, Code: {code}")
    if job_info is None or code != 200:
        click.echo(FORMAT_DICT['warning_head'] + f"Job {job_name} not found or DB error." + FORMAT_DICT['warning_tail'])
        return

    # 2. get log data
    log_data, node_logname_dict = get_fuyao_log(job_info, log_path)

    # 3. analyze log data
    fail_info = analyze_job_log(log_data, node_logname_dict)
    click.echo(FORMAT_DICT['result_head'] + f"Fail Info: {fail_info}" + FORMAT_DICT['result_tail'])


@cli.command()
@click.option('--job_name', prompt='Job Name',
              help='The name of a job. Checkout a job name by "fuyao view" or "fuyao history".')
@click.option('--env', prompt='Environment', type=click.Choice(['prd', 'dev']),
              help='prd: in pods | dev: at local machine. To determine which DB will be used.')
@click.option('--log_path', default='.', help='The path where tool will put the logs.')
# 3. 检查是否有worker process退出
def check_workers_exit(job_name, env, log_path):
    """Check if any worker process exited."""
    click.echo(f"Processing Job: {job_name}")

    # 日志检测是否所有worker都完成初始化
    # 1. get job info from db
    job_info, code = get_job_info(job_name, env)
    click.echo(f"Job Info: {job_info}, Code: {code}")
    if job_info is None or code != 200:
        click.echo(FORMAT_DICT['warning_head'] + f"Job {job_name} not found or DB error." + FORMAT_DICT['warning_tail'])
        return

    # 2. get log data
    log_data, node_logname_dict = get_fuyao_log(job_info, log_path)

    # 3. analyze log data
    process_no = job_info['node_count'] * job_info['gpus_per_node']
    fail_info = analyze_worker_process(log_data, process_no)
    click.echo(f"Exit node list: {fail_info['exit_node_list']}")
    click.echo(FORMAT_DICT['result_head'] + f"Has exit? {fail_info['has_exit']}" + FORMAT_DICT['result_tail'])

    # TODO - 检测主进程相关的子进程有没有退出, 比较数量？


@cli.command()
@click.option('--job_name', prompt='Job Name',
              help='The name of a job. Checkout a job name by "fuyao view" or "fuyao history".')
@click.option('--env', prompt='Environment', type=click.Choice(['prd', 'dev']),
              help='prd: in pods | dev: at local machine. To determine which DB will be used.')
@click.option('--log_path', default='.', help='The path where tool will put the logs.')
# 4. 检查所有worker是否完成初始化
def check_workers_initiation(job_name, env, log_path):
    """To check if all workers load dataset completed."""
    click.echo(f"Processing Job: {job_name}")

    # 1. get job info from db
    job_info, code = get_job_info(job_name, env)
    click.echo(f"Job Info: {job_info}, Code: {code}")
    if job_info is None or code != 200:
        click.echo(FORMAT_DICT['warning_head'] + f"Job {job_name} not found or DB error." + FORMAT_DICT['warning_tail'])
        return

    # 2. get log data
    log_data, node_logname_dict = get_fuyao_log(job_info, log_path)

    # 3. analyze log data
    process_no = job_info['node_count'] * job_info['gpus_per_node']
    fail_info = analyze_worker_process(log_data, process_no)
    click.echo(f"Node process number: {fail_info['node_process_no_dict']}")
    click.echo(FORMAT_DICT['result_head'] + f"All initialized? {fail_info['initiation']}" + FORMAT_DICT['result_tail'])


@cli.command()
@click.option('--job_name', prompt='Job Name',
              help='The name of a job. Checkout a job name by "fuyao view" or "fuyao history".')
@click.option('--env', prompt='Environment', type=click.Choice(['prd', 'dev']),
              help='prd: in pods | dev: at local machine. To determine which DB will be used.')
@click.option('--log_path', default='.', help='The path where tool will put the logs.')
# 5. 自动收集各节点火焰图
def collect_flame_graph(job_name, env, log_path):
    """Collect flame graph from all nodes."""
    click.echo(f"Processing Job: {job_name}")

    # 1. get job info and nodes info
    job_info, code = get_job_info(job_name, env)
    click.echo(f"Job Info: {job_info}, Code: {code}")
    if job_info is None or code != 200:
        click.echo(FORMAT_DICT['warning_head'] + f"Job {job_name} not found or DB error." + FORMAT_DICT['warning_tail'])
        return
    nodes_list = [node.strip() for node in job_info['node_list'].split(',')]
    # nodes_list = ['cnwlp-gpu-p02084']  # for test
    click.echo(f"node_list: {nodes_list}")

    # 2. get node info dict
    nodes_info_list = []
    for node in nodes_list:
        if node in NODE_LIST:
            nodes_info_list.append({
                'pod_ip': NODE_LIST[node],
                'node_name': node,
            })
        else:
            click.echo(
                FORMAT_DICT['warning_head'] + f"node: {node} do not exist in NODE_LIST" + FORMAT_DICT['warning_tail'])
            return
    nodes_list = nodes_info_list
    click.echo(f"nodes_list after: {nodes_list}")

    if nodes_list is None or len(nodes_list) == 0:
        return

    # 3. get stack info from all nodes
    # 3.1 判断当前集群
    cluster = job_info['site']
    url = ''
    if cluster == 'fuyao':
        url = r'http://fuyao-devop-container.xiaopeng.link/get_flame_graph'
    elif cluster == 'fuyao_a1':
        # TODO new dn
        url = r'http://fuyao-devop-container.a1.xiaopeng.link/get_flame_graph'
    elif cluster == 'fuyao_b1':
        # TODO new dn
        url = r'http://fuyao-devop-container.b1.xiaopeng.link/get_flame_graph'
    # 3.2 对相应集群的master发起调用
    data = send_collect_ranks_stack_request(url, job_name, nodes_list)
    # click.echo(f"Data: {data}")

    # 4. save stack info to file
    log_folder = f'{log_path}/graphs'
    if not os.path.exists(log_folder):
        os.makedirs(log_folder)

    rank_data_dict = data['rank_data_dict']
    for node_name, rank_data in rank_data_dict.items():
        filename = f'{log_folder}/{node_name}.svg'
        with open(filename, 'w+') as logfile:
            logfile.writelines(rank_data['data'])


@cli.command()
@click.option('--job_name', prompt='Job Name',
              help='The name of a job. Checkout a job name by "fuyao view" or "fuyao history".')
@click.option('--env', prompt='Environment', type=click.Choice(['prd', 'dev']),
              help='prd: in pods | dev: at local machine. To determine which DB will be used.')
@click.option('--log_path', default='.', help='The path where tool will put the logs.')
# 6. 自动收集各节点rank的stack
def collect_ranks_stack(job_name, env, log_path):
    """Collect stack info from all nodes."""
    click.echo(f"Processing Job: {job_name}")

    # 1. get job info and nodes info
    job_info, code = get_job_info(job_name, env)
    click.echo(f"Job Info: {job_info}, Code: {code}")
    if job_info is None or code != 200:
        click.echo(FORMAT_DICT['warning_head'] + f"Job {job_name} not found or DB error." + FORMAT_DICT['warning_tail'])
        return
    nodes_list = [node.strip() for node in job_info['node_list'].split(',')]
    # nodes_list = ['cnwlp-gpu-p02021']  # for test
    click.echo(f"node_list: {nodes_list}")

    # 2. get node info dict
    nodes_info_list = []
    for node in nodes_list:
        if node in NODE_LIST:
            nodes_info_list.append({
                'pod_ip': NODE_LIST[node],
                'node_name': node,
            })
        else:
            click.echo(
                FORMAT_DICT['warning_head'] + f"node: {node} do not exist in NODE_LIST" + FORMAT_DICT['warning_tail'])
            return
    nodes_list = nodes_info_list
    click.echo(f"nodes_list after: {nodes_list}")

    if nodes_list is None or len(nodes_list) == 0:
        return

    # 3. get stack info from all nodes
    # 3.1 判断当前集群
    cluster = job_info['site']
    url = ''
    if cluster == 'fuyao':
        url = r'http://fuyao-devop-container.xiaopeng.link/collect_ranks_stack'
    elif cluster == 'fuyao_a1':
        # TODO new dn
        url = r'http://fuyao-devop-container.a1.xiaopeng.link/collect_ranks_stack'
    elif cluster == 'fuyao_b1':
        # TODO new dn
        url = r'http://fuyao-devop-container.b1.xiaopeng.link/collect_ranks_stack'
    # 3.2 对相应集群的master发起调用
    data = send_collect_ranks_stack_request(url, job_name, nodes_list)
    # click.echo(f"Data: {data}")

    # 4. save stack info to file
    log_folder = f'{log_path}/stacks'
    if not os.path.exists(log_folder):
        os.makedirs(log_folder)

    rank_data_dict = data['rank_data_dict']
    for node_name, rank_data in rank_data_dict.items():
        filename = f'{log_folder}/{node_name}.log'
        with open(filename, 'w+') as logfile:
            for line in rank_data['data']:
                logfile.write(line + '\n')


# # 0. 包含以下1-6所有功能
# @cli.command()
# @click.option('--job_name', prompt='Job Name',
#               help='The name of a job. Checkout a job name by "fuyao view" or "fuyao history".')
# @click.option('--env', prompt='Environment', type=click.Choice(['prd', 'dev']),
#               help='prd: in pods | dev: at local machine. To determine which DB will be used.')
# @click.option('--log_path', default='.', help='The path where tool will put the logs.')
# def combo(job_name, env, log_path):
#     """All included."""
#     click.echo(FORMAT_DICT['step_head'] + f"Start to check job: {job_name}" + FORMAT_DICT['step_tail'])
#
#     # 1. check log exception, include exception, worker process exit & initiation
#     # 1.1 get job info from db
#     job_info, code = get_job_info(job_name, env)
#     click.echo(f"Job Info: {job_info}, Code: {code}")
#     if job_info is None or code != 200:
#         click.echo(FORMAT_DICT['warning_head'] + f"Job {job_name} not found or DB error." + FORMAT_DICT['warning_tail'])
#     else:
#         # 1.2 get log data
#         log_data, node_logname_dict = get_fuyao_log(job_info, log_path)
#         click.echo(
#             FORMAT_DICT['step_head'] + f"Logs are saved and start to analysis exceptions" + FORMAT_DICT['step_tail'])
#
#         # 1.3 analyze log data
#         process_no = job_info['node_count'] * job_info['gpus_per_node']
#         fail_info = analyze_job_log(log_data, node_logname_dict, process_no)
#         # log exception result
#         click.echo(FORMAT_DICT['result_head'] + f"Exception Info: {fail_info}" + FORMAT_DICT['result_tail'])
#         # worker process exit & initiation result
#         click.echo(FORMAT_DICT['step_head'] + f"Start to analyse worker processes" + FORMAT_DICT['step_tail'])
#         worker_process_info = analyze_worker_process(log_data, process_no)
#         click.echo(FORMAT_DICT['result_head'] + f"{worker_process_info}" + FORMAT_DICT['result_tail'])
#
#     # 2. collect ranks stack
#     click.echo(FORMAT_DICT['step_head'] + f"Start to collect rank0 stack at all nodes" + FORMAT_DICT['step_tail'])
#
#     # 2.1 get node info dict
#     nodes_list = [node.strip() for node in job_info['node_list'].split(',')]
#     nodes_list = ['cnwlp-gpu-p02021']
#     click.echo(f"Nodes need to be collected: {nodes_list}")
#
#     if len(nodes_list) == 0:
#         # _, nodes_list = get_nodes_by_job(job_name)
#         # 不会有job没有node_list吧？
#         pass
#     else:
#         nodes_info_list = []
#         for node in nodes_list:
#             if node in NODE_LIST:
#                 nodes_info_list.append({
#                     'pod_ip': NODE_LIST[node],
#                     'node_name': node,
#                 })
#             else:
#                 click.echo(f"!!! node: {node} do not exist in NODE_LIST !!!")
#                 return
#         nodes_list = nodes_info_list
#     click.echo(f"nodes_list after: {nodes_list}")
#
#     if nodes_list is not None and len(nodes_list) != 0:
#         # 3. get stack info from all nodes
#         # 3.1 判断当前集群
#         cluster = job_info['site']
#         url = ''
#         if cluster == 'fuyao':
#             url = r'http://fuyao-devop-container.xiaopeng.link/collect_ranks_stack'
#         elif cluster == 'fuyao_a1':
#             # TODO new dn
#             url = r'http://fuyao-devop-container.xiaopeng.link/collect_ranks_stack'
#         elif cluster == 'fuyao_b1':
#             # TODO new dn
#             url = r'http://fuyao-devop-container.xiaopeng.link/collect_ranks_stack'
#
#         # 3.2 对相应集群的master发起调用
#         click.echo('start to collect ranks stack')
#         data = send_collect_ranks_stack_request(url, job_name, nodes_list)
#         click.echo(f"Data: {data}")
#
#         # 4. save stack info to file
#         log_folder = f'{log_path}/log'
#         if not os.path.exists(log_folder):
#             os.makedirs(log_folder)
#
#         rank_data_dict = data['rank_data_dict']
#         for node_name, rank_data in rank_data_dict.items():
#             filename = f'{log_folder}/{node_name}.log'
#             with open(filename, 'w+') as logfile:
#                 for line in rank_data['data']:
#                     logfile.write(line + '\n')

if __name__ == '__main__':
    cli()
