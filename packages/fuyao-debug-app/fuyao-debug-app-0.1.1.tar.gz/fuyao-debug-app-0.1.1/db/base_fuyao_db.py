import configparser
import os
import logging
import traceback
import click

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker

from sqlalchemy import and_
from sqlalchemy.exc import SQLAlchemyError
from .fuyao_run_info_tbl import FuyaoRunInfoTbl

import sys

sys.path.append("..")
from config import config as cfg

config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(__file__), '../config', 'config.properties'))
# prd env session
PRD_DB_URI_FUYAO_MGMT = config['DB_INFO']['PRD_FUYAO_MGMT_DB_SERVER']
prd_db_engine_fuyao_mgmt = create_engine(PRD_DB_URI_FUYAO_MGMT)
Prd_session_fuyao_mgmt = sessionmaker(bind=prd_db_engine_fuyao_mgmt)
prd_session_fuyao_mgmt = scoped_session(Prd_session_fuyao_mgmt)
# dev env session
DEV_DB_URI_FUYAO_MGMT = config['DB_INFO']['DEV_FUYAO_MGMT_DB_SERVER']
dev_db_engine_fuyao_mgmt = create_engine(DEV_DB_URI_FUYAO_MGMT)
Dev_session_fuyao_mgmt = sessionmaker(bind=dev_db_engine_fuyao_mgmt)
dev_session_fuyao_mgmt = scoped_session(Dev_session_fuyao_mgmt)


def get_job_info(job_name, env):
    try:
        db_session = prd_session_fuyao_mgmt() if env == 'prd' else dev_session_fuyao_mgmt()
        job_info = (
            db_session.query(
                FuyaoRunInfoTbl.run_name,
                FuyaoRunInfoTbl.time_start,
                FuyaoRunInfoTbl.time_end,
                FuyaoRunInfoTbl.node_list,
                FuyaoRunInfoTbl.state,
                # site to determine which cluster to send request
                FuyaoRunInfoTbl.site,
                # node_count * gpus_per_node to determine how many processes need to be checked
                FuyaoRunInfoTbl.node_count,
                FuyaoRunInfoTbl.gpus_per_node,
            )
            .filter(and_(FuyaoRunInfoTbl.run_name == job_name))
            .order_by(FuyaoRunInfoTbl.time_start.asc())
            .first()
        )
        db_session.close()

        return job_info, 200
    except SQLAlchemyError as e:
        db_session.rollback()
        click.echo(cfg.FORMAT_DICT['warning_head'] + f"SQLAlchemyError: {e}" + cfg.FORMAT_DICT['warning_tail'])
        return None, 500
    except Exception:
        click.echo(cfg.FORMAT_DICT['warning_head'] + f"{str(traceback.format_exc())}" + cfg.FORMAT_DICT['warning_tail'])
        return None, 400
