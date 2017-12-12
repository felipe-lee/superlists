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
* use `sudo nginx -t` to check your config files
* you can also read the logs using `sudo cat /var/log/nginx/error.log`

## Systemd service

* see gunicorn-systemd.template.service
* replace SITENAME with, e.g., staging.my-domain.com
* place in /etc/systemd/system/gunicorn-<SITENAME>.service
* run `sudo systemctl daemon-reload`
* run `sudo systemctl enable gunicorn-<SITENAME>`
  * This purposely doesn't have the ".service" part of it.
* run `sudo systemctl start gunicorn-<SITENAME>`
  * If it was pre-existing, you can run `sudo systemctl restart gunicorn-<SITENAME>` 
* use `systemd-analyze verify /path/to/my.service` to verify config files
* you can look at the log using `sudo journalctl -u gunicorn-<SITENAME>`

## Folder structure:
Assume we have a user account at /home/username

/home/username \
* ├── sites 
  *  ├── SITENAME 
     *    ├── database \
         ├── source \
         ├── static \
         ├── virtualenv