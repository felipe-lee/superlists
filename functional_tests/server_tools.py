# -*- coding: utf-8 -*-
"""
Tools to run on server
"""
from fabric.tasks import execute

from deploy_tools.fabfile import GOOGLE_ELSPETH, create_session, flush_database


def _get_manage_dot_py(host):
    """
    Retrieves a string containing the paths to the python interpreter and the manage.py file for the given host
    :param host: host to find the manage.py file for
    :return: string with paths
    """
    return f'~/sites/{host}/virtualenv/bin/python ~/sites/{host}/manage.py'


def reset_database(host):
    """
    Flush remote db
    :param host: site name
    """
    manage_dot_py = _get_manage_dot_py(host)

    execute(flush_database, manage_dot_py=manage_dot_py)


def create_session_on_server(host, email):
    """
    Creates a session on server
    :param host: site name
    :param email: email to create a session for
    :return: session key
    """
    manage_dot_py = _get_manage_dot_py(host)

    task_info = execute(create_session, manage_dot_py=manage_dot_py, email=email)

    session_key = task_info.get(f'{GOOGLE_ELSPETH}')
    
    return session_key.strip()
