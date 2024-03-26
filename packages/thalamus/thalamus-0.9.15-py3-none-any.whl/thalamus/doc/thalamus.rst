.. SPDX-FileCopyrightText: 2017-2024 GNU Solidario <health@gnusolidario.org>
.. SPDX-FileCopyrightText: 2017-2024 Luis Falcón <falcon@gnuhealth.org>
..
.. SPDX-License-Identifier: CC-BY-SA-4.0 

|thalamus|

The GNU Health Message and Authentication Server
==========================================================

.. Note:: This document is licensed under Creative Commons
    Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)

:Author: Luis Falcon
:Contact: info@gnuhealth.org
:Version: 0.9.15

.. contents:: Contents
   :local:
   :depth: 2

Introduction
------------
The Thalamus project provides a RESTful API hub to all the GNU Health 
Federation nodes. The main functions are:

#. **Message server**: A concentrator and message relay from and to  
   the participating nodes in the GNU Health Federation and the GNU Health
   Information System (PgSQL). Some of the participating nodes include 
   the GNU Health HMIS, MyGNUHealth mobile PHR application,
   laboratories, research institutions and civil offices.

#. **Authentication Server**: Thalamus also serves as an authentication and
   authorization server to interact with the GNUHealth Information System


Thalamus is part of the GNU Health project, but it is a self contained, 
independent server that can be used in different health related scenarios.

.. image:: ./images/federation_components.png
    :scale: 70%
    :align: center

Technology
----------
RESTful API: Thalamus uses a REST (Representional State Transfer) 
architectural style, powered by 
`Flask <https://en.wikipedia.org/wiki/Flask_(web_framework)>`_ technology

Thalamus will perform CRUD (Create, Read, Update, Delete) operations. They
will be achieved via the following methods upon resources and their instances.

* **GET** : Read
 
* **POST** : Create
 
* **PATCH** : Update
 
* **DELETE** : Delete.

The DELETE operations will be minimal.
  

JSON: The information will be encoded in `JSON <https://en.wikipedia.org/wiki/JSON>`_ format.

Resources
---------

Some resources and end-points are:

* People (/people)

* Pages of Life (/pols)

* DomiciliaryUnits (/domiciliary-units)

* PersonalDocs (/personal_docs)

Installation
------------
Create a new user thalamus with PostgreSQL permissions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
* Install PostgreSQL and create an operating system user called thalamus
* Locate the pg_hba.conf file and add the following line::

    local all all trust

  If you don't find the file refer to 'Verify PostgreSQL authentication method'
  in the HMIS node installation guide.


* Restart PostgreSQL::

    $ sudo systemctl restart postgresql.service

* Give permissions to the newly created thalamus user::

    $ sudo su - postgres -c "createuser --createdb --no-createrole --no-superuser thalamus"

Installing Thalamus
~~~~~~~~~~~~~~~~~~~

Thalamus is a flask application, and is pip installable. Using the thalamus
operating system user, install Thalamus server locally::

    $ pip3 install --user wheel $ pip3 install --user thalamus
    $ pip3 install --user flask-cors

Initializing PostgreSQL for the HIS and Person Master Index
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The following documentation applies to a demo / test database, that we will call
"federation"

#. Create the database::

    $ createdb federation

#. Locate thalamus::

    $ pip3 show thalamus
    $ cd /path/thalamus/demo/

#. Create the Federation HIS schema. Inside the "demo" directory in Thalamus
execute the following SQL script::

        $ psql -d federation < federation_schema.sql

#. Set the PostgreSQL URI for demo data: In import_pg.py adjust the
variable PG_URI to fit your needs. It could be sufficient to just
put "dbname='federation'" into psycopg2.connect(...) if your setup fits the
default settings.

#. Initialize the Federation Demo database::

    $ bash ./populate.sh

#. Set the PostgreSQL URI for runtime: Just like in the second step
modify POSTGRESQL_URI in etc/thalamus.cfg

At this point you can run and test Thalamus directly from the Flask Werkzeug
server::

    $ python3 ./thalamus.py

This is ok for development and testing environments, but for production sites,
always run Thalamus from a WSGI container, as described in the next section.


Running Thalamus from a WSGI Container
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
In production settings, for performance reasons you should use a HTTP server. We
have chosen `uWSGI <http://projects.unbit.it/uwsgi>`_ , but you can use any WSGI
server. We have also included the configuration file for Gunicorn if you prefer
it instead of uWSGI.

Running Thalamus from uWSGI
"""""""""""""""""""""""""""
We have included a uwsgi sample configuration file (etc/thalamus_uwsgi.ini). In
order to test uWSGI with HTTP it should look like this:

.. code-block::

    [uwsgi] master = 1
    # https = 0.0.0.0:8443, /opt/gnuhealth/certs/gnuhealthfed.crt,/opt/gnuhealth/certs/gnuhealthfed.key
    http = 0.0.0.0:8080
    wsgi-file = thalamus.py
    callable = app
    processes = 4
    threads = 2
    block-size = 32000
    stats = 127.0.0.1:9191
    plugins = http,python

To execute Thalamus with the default configuration file::

  $ uwsgi --ini etc/thalamus_uwsgi.ini

All these arguments can also be passed to the command line.

Enable SSL for encrypted communication
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Either get an official certificate or generate a self-signed certificate and
private key::

    $ sudo openssl req -newkey rsa:2048 -new -x509 -days 3650 -nodes -out
      gnuhealthfed.crt -keyout gnuhealthfed.key

If uWSGI should handle HTTPS, place the certificate (gnuhealthfed.crt) and
private key (gnuhealthfed.key) in a directory where the thalamus user has read
permissions. Afterwards change etc/thalamus_uwsgi from HTTP to HTTPS using the
correct paths. Keep a backup of them in a safe place. Alternatively keep uWSGI
as internal HTTP server and configure a HTTPS reverse proxy. Using apache2 you
can create a file thalamus.conf as site with the following content:

.. code-block::

    <IfModule mod_ssl.c>
    <VirtualHost *:443>
        SSLEngine on
        SSLCertificateFile /etc/ssl/certs/gnuhealthfed.crt
        SSLCertificateKeyFile /etc/ssl/private/gnuhealthfed.key
        ServerName domain
        ProxyPass / http://your_host:8080/
        ProxyPassReverse / http://your_host:8080/
    </VirtualHost>
    </IfModule>

Depending on the operating system place this inside /etc/apache2/vhosts.d/
(openSUSE) or /etc/apache2/sites-available/ (Debian/Ubuntu). For the last case
enable it afterwards using the a2ensite command. Finally enable some modules and
restart apache::

    $ sudo a2enmod headers ssl proxy proxy_http
    $ sudo systemctl restart apache2.service

Create a systemd service
~~~~~~~~~~~~~~~~~~~~~~~~
In order to control Thalamus with systemctl and enable it to be activated after
startup create a service file thalamus.service with the following content:

.. code-block::

    [Unit]
    Description=Thalamus Server
    After=network.target

    [Service]
    User=gnuhealth
    WorkingDirectory=/home/gnuhealth/.local/lib/python3.9/site-packages/thalamus
    ExecStart=uwsgi --ini etc/thalamus_uwsgi.ini
    Restart=on-abort
    Type=notify
    KillSignal=SIGQUIT
    StandardError=syslog

    [Install]
    WantedBy=multi-user.target


.. Note::
    Replace the value of the **WorkingDirectory** to fit your needs.

Put this in the appropriate directory for your operating system: For example
/etc/systemd/system/ on Debian/Ubuntu and openSUSE.
Afterwards start and enable the service::

    $ sudo systemctl start thalamus.service
    $ sudo systemctl enable thalamus.service

Using a virtual environment
~~~~~~~~~~~~~~~~~~~~~~~~~~~
If you want to use a virtual environment create and activate the virtual
environment before installing Thalamus::

    $ python3 -m venv /home/thalamus/venv
    $ source /home/thalamus/venv/bin/activate

Besides add the following line to etc/thalamus_uwsgi.ini::

    venv = /home/thalamus/venv/


Examples
--------
**Command-line, using httpie**

Retrieve the demographic information of person::

  $ http --verify no --auth ITAPYT999HON:gnusolidario https://localhost:8443/people/ESPGNU777ORG

Yields to::

    HTTP/1.1 200 OK
    Connection: close
    Content-Length: 411
    Content-Type: application/json
    Date: Fri, 21 Apr 2017 16:22:38 GMT
    Server: gunicorn/19.7.1

    {
        "_id": "ESPGNU777ORG",
        "active": true,
        "biological_sex": "female",
        "dob": "Fri, 04 Oct 1985 13:05:00 GMT",
        "education": "tertiary",
        "ethnicity": "latino",
        "gender": "female",
        "lastname": "Betz",
        "marital_status": "married",
        "name": "Ana",
        "password": "$2b$12$cjrKVGYEKUwCmVDCtEnwcegcrmECTmeBz526AAD/ZqMGPWFpHJ4FW",
        "profession": "teacher",
        "roles": [
        "end_user"
        ]
        
    }

**Retrieve the demographics information globally**::

  $ http --verify no --auth ITAPYT999HON:gnusolidario
    https://localhost:8443/people

Yields to::

    HTTP/1.1 200 OK
    Connection: close
    Content-Length: 933
    Content-Type: application/json
    Date: Fri, 21 Apr 2017 16:31:23 GMT
    Server: gunicorn/19.7.1

    [
        {
            "_id": "ITAPYT999HON",
            "active": true,
            "biological_sex": "female",
            "dob": "Fri, 05 Oct 1984 09:00:00 GMT",
            "education": "tertiary",
            "ethnicity": "latino",
            "gender": "female",
            "lastname": "Cordara",
            "marital_status": "married",
            "name": "Cameron",
            "password": "$2b$12$Y9rX7PoTHRXhTO1H78Tan.8mVmyayGAUIveiYxu2Qeo0ZDRvJQ8/2",
            "profession": "teacher",
            "roles": [
            "end_user",
            "health_professional"
            ]
            
        },
        
        {
            "_id": "ESPGNU777ORG",
            "active": true,
            "biological_sex": "female",
            "dob": "Fri, 04 Oct 1985 13:05:00 GMT",
            "education": "tertiary",
            "ethnicity": "latino",
            "gender": "female",
            "lastname": "Betz",
            "marital_status": "married",
            "name": "Ana",
            "password": "$2b$12$cjrKVGYEKUwCmVDCtEnwcegcrmECTmeBz526AAD/ZqMGPWFpHJ4FW",
            "profession": "teacher",
            "roles": [
            "end_user"
            ]
            
        }
        
    ]
    

**Using Python requests**::

  >>> import requests
  >>> person = requests.get('https://localhost:8443/people/ESPGNU777ORG', auth=('ITAPYT999HON', 'gnusolidario'), verify=False)
  >>> person.json()
    {'_id': 'ESPGNU777ORG', 'active': True, 'biological_sex': 'female','dob': 'Fri, 04 Oct 1985 13:05:00 GMT',
    'education': 'tertiary', 'ethnicity': 'latino', 'gender': 'female', 'lastname': 'Betz', 'marital_status': 'married',
    'name': 'Ana', 'password': '$2b$12$cjrKVGYEKUwCmVDCtEnwcegcrmECTmeBz526AAD/ZqMGPWFpHJ4FW', 'profession': 'teacher',
    'roles': ['end_user']}

**Note on roles**
The demo user "ITAPYT999HON" is a health professional (health_professional role),
so she has global access to demographic information. 

The user "ARGBUE111FAV" with the password "freedom" is the "root" user for
thedemo database.

Check the ``roles.cfg`` file for examples information about roles and ACLs.


Development
-----------
Thalamus is part of the GNU Health project.

The development will be done on GNU Savannah, using the Mercurial repository.

Tasks, bugs and mailing lists will be on health-dev@gnu.org , for development.

General questions can be done on health@gnu.org mailing list.

Homepage
--------
https://www.gnuhealth.org


Release Cycle
-------------
Thalamus, as other GNU Health components, will follow its own release process.


.. |Thalamus| image:: ./images/thalamus.png
    :scale: 60%

.. |FederationComponents| image:: ./images/federation_components.png
    :scale: 70%


