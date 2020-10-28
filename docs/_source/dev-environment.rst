Dev Environment
=======================

.. index:: docker

The steps below will get you up and running with a local development environment.
You may also refer to cookiecutter-django's `Getting Up and Running Locally With Docker`_ for further information.

.. _`Getting Up and Running Locally With Docker`: https://cookiecutter-django.readthedocs.io/en/latest/developing-locally.html

Prerequisites
-------------

* Docker; if you don't have it yet, follow the `installation instructions`_;
* Docker Compose; refer to the official documentation for the `installation guide`_.
* Gitlab Server (For OAuth2 authentication)

.. _`installation instructions`: https://docs.docker.com/install/#supported-platforms
.. _`installation guide`: https://docs.docker.com/compose/install/

Set up environment variables
----------------------------
Create following .project file under .envs/.local folder and put environment variables as described in the Settings section.
::

  # OAuth2 with Gitlab
  GITLAB_URL=https://<gitlab-url>

  # Set REQUESTS_CA_BUNDLE only when the app needs connection to websites with self-signed certificates
  REQUESTS_CA_BUNDLE=/app/ca-certificates.crt

  # PlantUML
  PLANTUML_SERVER_URL=http://<host-ip>:8080

  # Architecture Tool
  ARCHITECTURE_TOOL_URL=http://<host-ip>:8000

  # Confluence (Set to true to enable confluence page update)
  SYNC_TO_CONFLUENCE=True
  # API Gateway for Confluence (Only required when SYNC_TO_CONFLUENCE is True)
  CONFLUENCE_URL=
  API_KEY=
  CONFLUENCE_USER=
  CONFLUENCE_PASS=

Run the Stack
---------------

This can take a while, especially the first time you run this particular command on your development system::

    $ docker-compose -f local.yml up --build


Execute Management Commands
---------------------------

As with any shell command that we wish to run in our container, this is done using the ``docker-compose -f local.yml run --rm`` command: ::

    $ docker-compose -f local.yml run --rm django python manage.py makemigrations
    $ docker-compose -f local.yml run --rm django python manage.py migrate
    $ docker-compose -f local.yml run --rm django python manage.py createsuperuser
    $ docker-compose -f local.yml run --rm django python manage.py shell

Here, ``django`` is the target service we are executing the commands against.

Gitlab Authentication
---------------------------

Add application in Gitlab as per `GitLab as OAuth2 authentication service provider`_.

Perform steps as described in `django-allauth Post-Installation`_.

.. _`GitLab as OAuth2 authentication service provider`: https://docs.gitlab.com/ee/integration/oauth_provider.html
.. _`django-allauth Post-Installation`: https://django-allauth.readthedocs.io/en/latest/installation.html#post-installation
