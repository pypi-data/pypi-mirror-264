from sqlalchemy import Column
from sqlalchemy.dialects.mysql import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.declarative import declared_attr

Base = declarative_base()


class BaseFuyaoRunInfoMixin(object):

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id = Column(BIGINT, primary_key=True)
    run_name = Column(TINYTEXT)
    partition = Column(TINYTEXT)
    type = Column(TINYTEXT)
    site = Column(TINYTEXT)
    org = Column(TINYTEXT)
    experiment_id = Column(BIGINT)
    experiment_name = Column(TINYTEXT)
    user_name = Column(TINYTEXT)
    label = Column(TEXT)
    envs = Column(TEXT)
    device_type = Column(TINYTEXT)
    node_count = Column(INTEGER)
    gpus_per_node = Column(INTEGER)
    egpus_per_node = Column(INTEGER)
    cpus_per_node = Column(INTEGER)
    gibs_per_node = Column(INTEGER)
    time_limit = Column(INTEGER)
    time_suspended = Column(INTEGER)
    queuing_strategy = Column(TINYTEXT)
    docker_image = Column(TEXT)
    init_docker_image = Column(TEXT)
    image_id = Column(TINYTEXT)
    source = Column(INTEGER)
    volume = Column(TINYTEXT)
    start_command = Column(TEXT)
    deploy_command = Column(TEXT)
    save_path = Column(TEXT)
    artifact = Column(TEXT)
    enable_sdk = Column(TINYINT)
    enable_launcher = Column(TINYINT)
    enable_entrypoint = Column(TINYINT)
    enable_test_run = Column(TINYINT)
    resource = Column(TEXT)
    node_list = Column(TEXT)
    priority = Column(TINYTEXT)
    priority_score = Column(TEXT)
    state = Column(TEXT)
    time_received = Column(BIGINT)
    time_submit = Column(BIGINT)
    time_start = Column(BIGINT)
    time_end = Column(BIGINT)
    error_json_description = Column(TEXT)
    dbctime = Column(BIGINT)
    dbutime = Column(BIGINT)
    model = Column(TEXT)
    git_url = Column(TEXT)
    git_tag = Column(TEXT)
    git_commit_hash = Column(TEXT)
    git_token = Column(TEXT)
    config_yaml = Column(TEXT)
    jenkins_job = Column(TEXT)
    jenkins_build = Column(BIGINT)
    fuyao_task_id = Column(BIGINT)


class FuyaoRunInfoTbl(Base, BaseFuyaoRunInfoMixin):
    __tablename__ = 'fuyao_run_info'
