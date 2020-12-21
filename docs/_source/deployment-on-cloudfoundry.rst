Deployment on Cloud Foundry
===========================

.. index:: cloud foundry

Prerequisites
-------------

* Postgres service provisioned
* Redis service provisioned 
* Object storage provisioned, and bucket created
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
        REDIS_URL: xxx
        CELERY_BROKER_URL: xxx
        CELERY_FLOWER_USE: xxx
        CELERY_FLOWER_PASSWORD: xxx
        GITLAB_URL: xxxx
        PLANTUML_SERVER_URL: xxx
        REQUESTS_CA_BUNDLE: ca-certificates.crt
        ARCHITECTURE_TOOL_URL: xxxx
        SYNC_TO_GITLAB: True
        GITLAB_PROJECT_ID: 1103
        GITLAB_TOKEN: xxx
        DJANGO_AWS_S3_ENDPOINT_URL: xxxx
        DJANGO_AWS_ACCESS_KEY_ID: xxx
        DJANGO_AWS_SECRET_ACCESS_KEY: xxx
        DJANGO_AWS_STORAGE_BUCKET_NAME: mybucket
      services:
      - postgres
      - redis
      - object_storage

    - name: architecture-tool-docs
      memory: 256M
      instances: 1
      buildpacks:
      - staticfile_buildpack
      stack: cflinuxfs3
      path: docs/_build/html

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
