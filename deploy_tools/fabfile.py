# -*- coding: utf-8 -*-
"""
Fabfile to automate provisioning on server
"""
import random

from fabric.api import cd, env, local, run
from fabric.contrib.files import append, exists, sed

GOOGLE_ELSPETH = 'google-superlists-elspeth'
env.use_ssh_config = True
env.hosts = [GOOGLE_ELSPETH]
REPO_URL = 'bb:felipe_lee/superlists.git'


def deploy(production='False', email_password=''):
    """
    Run deployment provisioning commands.
    :param production: Running for production?
    :param email_password: Password for email host. Only needed if provisioning for first time.
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

        first_time_provisioning = False
        if not exists(f'/etc/nginx/sites-available/{SITENAME}'):
            if not email_password:
                raise NotImplementedError('You need to pass in an email password in order to provision the server')
    
            first_time_provisioning = True
    
            run(f'sed "s/SITENAME/{SITENAME}/g; s/EMAILPASSWORD/{email_password}/g" '
                f'./deploy_tools/nginx.template.conf | sudo tee /etc/nginx/sites-available/{SITENAME}')
    
            run(f'sudo ln -s /etc/nginx/sites-available/{SITENAME} /etc/nginx/sites-enabled/{SITENAME}')
    
            run(f'sed "s/SITENAME/{SITENAME}/g" ./deploy_tools/gunicorn-systemd.template.service | '
                f'sudo tee /etc/systemd/system/gunicorn-{SITENAME}')

        run('sudo systemctl daemon-reload')

        if first_time_provisioning:
            run('sudo systemctl reload nginx')
            run(f'sudo systemctl enable gunicorn-{SITENAME}')
            run(f'sudo systemctl start gunicorn-{SITENAME}')
        else:
            run(f'sudo systemctl restart gunicorn-{SITENAME}')


def _get_latest_source():
    if exists('.git'):
        run('git fetch')
    else:
        run(f'git clone {REPO_URL} .')

    current_commit = local("git log -n 1 --format=%H", capture=True)
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


def flush_database(manage_dot_py):
    """
    Flushes server database to start fresh (note, this does not drop tables).
    :param manage_dot_py: path to correct python exec and manage.py
    """
    run(f'{manage_dot_py} flush --noinput')


def create_session(manage_dot_py, email):
    """
    Creates a session on the server to mimic user having logged in previously.
    :param manage_dot_py: path to correct python exec and manage.py
    :param email: email of user to log in
    :return: session key
    """
    return run(f'{manage_dot_py} create_session {email}')
