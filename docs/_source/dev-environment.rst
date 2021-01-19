Dev Environment
===============

.. index:: docker

The steps below will get you up and running with a local development environment.
You may also refer to cookiecutter-django's `Getting Up and Running Locally With Docker`_ for further information.

.. _`Getting Up and Running Locally With Docker`: https://cookiecutter-django.readthedocs.io/en/latest/developing-locally.html

Prerequisites
-------------

* Python3
* Docker; if you don't have it yet, follow the `installation instructions`_;
* Docker Compose; refer to the official documentation for the `installation guide`_.
* GitLab Server (for OAuth2 authentication), GitLab project created (for synchronization)

.. _`installation instructions`: https://docs.docker.com/install/#supported-platforms
.. _`installation guide`: https://docs.docker.com/compose/install/

Code Style Check
----------------
The project also has default integration with `pre-commit`_ for identifying simple issues before submission to code review.

Please run ``pip install pre-commit && pre-commit install`` to set up the git hook scripts before your first commit.

.. _`pre-commit`: https://github.com/pre-commit/pre-commit

Set Up Environment Variables
----------------------------
Create following .project file under .envs/.local folder and put environment variables as described in the ``Settings`` section.
::

  # OAuth2 with Gitlab
  GITLAB_URL=https://<gitlab-url>

  # Set REQUESTS_CA_BUNDLE only when the app needs connection to websites with self-signed certificates
  REQUESTS_CA_BUNDLE=/app/ca-certificates.crt

  # PlantUML
  PLANTUML_SERVER_URL=http://<machine-ip>:8080

  # Architecture Tool
  ARCHITECTURE_TOOL_URL=http://<machine-ip>:8000

  # Confluence (Set to true to enable confluence page update)
  SYNC_TO_CONFLUENCE=False
  # API Gateway for Confluence (Only required when SYNC_TO_CONFLUENCE is True)
  CONFLUENCE_URL=
  API_KEY=
  CONFLUENCE_USER=
  CONFLUENCE_PASS=

  # Synchronize to Gitlab  
  SYNC_TO_GITLAB=True
  # Only required when SYNC_TO_GITLAB is True
  GITLAB_PROJECT_ID=
  GITLAB_TOKEN=

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
---------------------

Add application in Gitlab as per `GitLab as OAuth2 authentication service provider`_.

Perform steps as described in `django-allauth Post-Installation`_.

* Go to GitLab -> Applications, create an application. 

  Name: ``architecture-tool-django-dev``

  Redirect URI: ``http://<machine-ip>:8000/accounts/gitlab/login/callback/``

  Scopes: ``api``
* Visit ``http://<machine-ip>:8000/admin/sites/site/1/change/``, and change site. 

  Domain name: ``<machine-ip>:8000``
  
  Display name: ``Architecture Tool``
* Add social application in ``http://<machine-ip>:8000/admin/socialaccount/socialapp/``. 

  Provider: ``GitLab``

  Name: ``architecture-tool-django-dev``

  Client id: ``<copy from gitlab>``

  Secret key: ``<copy from gitlab>``

  Sites: ``<choose the site in previous step>``


.. _`GitLab as OAuth2 authentication service provider`: https://docs.gitlab.com/ee/integration/oauth_provider.html
.. _`django-allauth Post-Installation`: https://django-allauth.readthedocs.io/en/latest/installation.html#post-installation

Access the Tool
---------------

Please visit the various components of the tool via following URLs.

* Architecture Tool: ``http://<machine-ip>:8000``
* Swagger UI for APIs: ``http://<machine-ip>:8000/swagger/``
* Flower - Celery monitoring tool: ``http://<machine-ip>:5555``
* PlantUML: ``http://<machine-ip>:8080``
* Minio: ``http://<machine-ip>:9000``
* Documentation: ``http://<machine-ip>:7000``
