# -*- coding: utf-8 -*-
"""
Tools to run on server
"""
from fabric.api import run


def _get_manage_dot_py(host):
    return f'~/sites/{host}/virtualenv/bin/python ~/sites/{host}/source/manage.py'


def reset_database(host):
    manage_dot_py = _get_manage_dot_py(host)
    
    run(f'{manage_dot_py} flush --noinput')


def create_session_on_server(host, email):
    manage_dot_py = _get_manage_dot_py(host)
    
    session_key = run(f'{manage_dot_py} create_session {email}')
    
    return session_key.strip()
