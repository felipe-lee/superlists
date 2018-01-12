# -*- coding: utf-8 -*-
"""
Tools to run on server
"""
from fabric.api import run
from fabric.context_managers import settings


def _get_manage_dot_py(host):
    """
    Retrieves a string containing the paths to the python interpreter and the manage.py file for the given host
    :param host: host to find the manage.py file for
    :return: string with paths
    """
    return f'~/sites/{host}/virtualenv/bin/python ~/sites/{host}/source/manage.py'


def reset_database(host):
    """
    Flush remote db
    :param host: site name
    """
    manage_dot_py = _get_manage_dot_py(host)
    
    with settings(use_ssh_config=True, hosts=['google-superlists-elspeth']):
        run(f'{manage_dot_py} flush --noinput')


def create_session_on_server(host, email):
    """
    Creates a session on server
    :param host: site name
    :param email: email to create a session for
    :return: session key
    """
    manage_dot_py = _get_manage_dot_py(host)
    
    with settings(use_ssh_config=True, hosts=['google-superlists-elspeth']):
        session_key = run(f'{manage_dot_py} create_session {email}')
        
        return session_key.strip()
