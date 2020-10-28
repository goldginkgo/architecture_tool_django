Deployment on Cloud Foundry
===========================

.. index:: cloud foundry

Prerequisites
-------------

* Postgres service provisioned
* Redis service provisioned 
* PlantUML server provisioned

Prepare manifest.yml
--------------------
Prepare following manifest.yaml file in the root folder and adjust environment variables according to your environment.
::

    ---
    applications:
    - name: architecture-tool
    memory: 1G
    instances: 1
    buildpacks:
    - python_buildpack
    stack: cflinuxfs3
    routes:
        - route: xxxx
    env:
        USE_DOCKER: no
        REDIS_URL: xxxx
        CELERY_BROKER_URL: xxxx
        CELERY_FLOWER_USE: xxxx
        CELERY_FLOWER_PASSWORD: xxxx
        GITLAB_URL: xxxx
        PLANTUML_SERVER_URL: xxxx
        DJANGO_ACCOUNT_ALLOW_REGISTRATION: True
        REQUESTS_CA_BUNDLE: ca-certificates.crt
        ARCHITECTURE_TOOL_URL: xxxx
    services:
    - postgres
    - redis

Push the app
------------

The Procfile indicates that there are 4 processes in the app. Please refer to `Pushing an App with Multiple Processes`_ for a better understanding. After pushing the app, you need to scale up the processes other than the web process.

.. _`Pushing an App with Multiple Processes`: https://docs.cloudfoundry.org/devguide/multiple-processes.html

Create super user 
-----------------
::

    cf enable-ssh architecture-tool
    cf ssh architecture-tool
    /tmp/lifecycle/shell app
    python manage.py createsuperuser


Gitlab Authentication
---------------------------

Add application in Gitlab as per `GitLab as OAuth2 authentication service provider`_.

Perform steps as described in `django-allauth Post-Installation`_.

.. _`GitLab as OAuth2 authentication service provider`: https://docs.gitlab.com/ee/integration/oauth_provider.html
.. _`django-allauth Post-Installation`: https://django-allauth.readthedocs.io/en/latest/installation.html#post-installation
