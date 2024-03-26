import logging
import requests
import click
import json


def send_node_health_check_request(url, job_name, nodes_list, dt_start, dt_end):
    headers = {
        "Content-type": "application/json"
    }
    begin_time = dt_start.strftime("%Y-%m-%d %H:%M:%S") if dt_start else None
    end_time = dt_end.strftime("%Y-%m-%d %H:%M:%S") if dt_end else None
    data = {
        "jobName": job_name,
        "nodeList": nodes_list,
        "beginTime": begin_time,
        "endTime": end_time
    }
    # click.echo(f"Data: {data}")
    try:
        resp = requests.post(url, data=json.dumps(data), headers=headers, timeout=10)
        # click.echo(f"Returns: {resp}")
        return resp.json()
    except Exception as e:
        click.echo(f"Error: {e}")
        return None


def send_collect_ranks_stack_request(url, job_name, nodes_list):
    logging.debug('collect ranks stack start!')

    headers = {
        "Content-type": "application/json"
    }
    data = {
        'jobName': job_name,
        'nodesList': nodes_list
    }
    try:
        resp = requests.post(url, json=data, headers=headers, timeout=60)
        logging.info(f"Returns: {resp}")
        # click.echo(f"Returns: {resp.json()}")
        return resp.json()
    except Exception as e:
        logging.warning(f"{e}")
        return None
