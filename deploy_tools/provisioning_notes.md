# Provisioning a new site
=========================

## Required packages

* nginx
* Python 3.6
* virtualenv + pip
* Git

e.g. on Ubuntu:

sudo add-apt-repository ppa:fkrull/deadsnakes
    sudo apt-get update
    sudo apt-get install nginx git python36 python3.6-venv

## Nginx Virtual Host config

* see nginx.template.conf
* replace SITENAME with, e.g., staging.my-domain.com
* place in /etc/nginx/sites-available/<SITENAME>
* run `sudo ln -s /etc/nginx/sites-available/<SITENAME> /etc/nginx/sites-enabled/<SITENAME>` to create a symlink
* remove the default config by running `sudo rm /etc/nginx/sites-enabled/default`
* reload nginx `sudo systemctl reload nginx` (or start it if you haven't: `sudo systemctl start nginx`)

## Systemd service

* see gunicorn-systemd.template.service
* replace SITENAME with, e.g., staging.my-domain.com
* place in /etc/systemd/system/gunicorn-<SITENAME>.service
* run `sudo systemctl daemon-reload`
* run `sudo systemctl enable gunicorn-<SITENAME>`
* run `sudo systemctl start gunicorn-<SITENAME>`

## Folder structure:
Assume we have a user account at /home/username

/home/username
└── sites
    └── SITENAME
         ├── database
         ├── source
         ├── static
         └── virtualenv