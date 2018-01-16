# -*- coding: utf-8 -*-
"""
Tools to run on server
"""
from fabric.api import env, run
from fabric.tasks import execute

env.use_ssh_config = True
env.hosts = ['google-superlists-elspeth']


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
    execute(lambda: run('ls'))
    execute(lambda: run(f'{manage_dot_py} flush --noinput'))


def create_session_on_server(host, email):
    """
    Creates a session on server
    :param host: site name
    :param email: email to create a session for
    :return: session key
    """
    manage_dot_py = _get_manage_dot_py(host)

    task_info = execute(lambda: run(f'{manage_dot_py} create_session {email}'))

    session_key = task_info.get(f'{env.hosts[0]}')
    
    return session_key.strip()
