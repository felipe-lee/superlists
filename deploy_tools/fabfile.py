# -*- coding: utf-8 -*-
"""
Fabfile to automate provisioning on server
"""
import random

from fabric.api import cd, env, local, run
from fabric.contrib.files import append, exists, sed

env.use_ssh_config = True
env.hosts = ['google-superlists-elspeth']
REPO_URL = 'bb:felipe_lee/superlists.git'


def deploy(production='False'):
    """
    Run deployment provisioning commands.
    :param production: Running for production?
    """
    if production == 'True':
        SITENAME = 'superlists.knightsofhaven.net'
    else:
        SITENAME = 'superlists-staging.knightsofhaven.net'
    
    site_folder = f'/home/{env.user}/sites/{SITENAME}'
    
    run(f'mkdir -p {site_folder}')
    
    with cd(site_folder):
        _get_latest_source()
        _update_settings(site_name=SITENAME)
        _update_virtualenv()
        _update_static_files()
        _update_database()


def _get_latest_source():
    if exists('.git'):
        run('git fetch')
    else:
        run(f'git clone {REPO_URL} .')
    
    current_commit = local("git log -n l --format=%H", capture=True)
    run(f'git reset --hard {current_commit}')


def _update_settings(site_name):
    settings_path = 'superlists/settings.py'
    
    sed(settings_path, 'DEBUG = True', 'DEBUG = False')
    sed(settings_path,
        'ALLOWED_HOSTS =.+$',
        f'ALLOWED_HOSTS = ["{site_name}"]'
        )
    
    secret_key_file = 'superlists/secret_key.py'
    
    if not exists(secret_key_file):
        chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
        key = ''.join(random.SystemRandom().choices(chars, k=50))
        append(secret_key_file, f'SECRET_KEY = "{key}"')
    
    append(settings_path, '\nfrom .secret_key import SECRET_KEY')


def _update_virtualenv():
    if not exists('virtualenv/bin/pip'):
        run(f'python3.6 -m venv virtualenv')
    
    run('./virtualenv/bin/pip install -r requirements.txt')


def _update_static_files():
    run('./virtualenv/bin/python manage.py collectstatic --noinput')


def _update_database():
    run('./virtualenv/bin/python manage.py migrate --noinput')