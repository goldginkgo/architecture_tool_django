Deployment with Docker
======================

.. index:: deployment, docker, docker-compose

Refer to cookiecutter-django's `Deployment with Docker`_ for further information.

.. _`Deployment with Docker`: https://cookiecutter-django.readthedocs.io/en/latest/deployment-with-docker.html


Prerequisites
-------------

* Create a virtual machine, and install Docker/Docker Compose
* Get a DNS name (e.g. architecture-tool.top) from a domain registrar (e.g. NameSilo)
* Add a record with VM's IP under the DNS
* Search the code, and replace "architecture-tool.top" with your registered DNS
* Add .envs/.production folder and environment variable files (.django, .postgres)
* Add an application in GitLab for OAuth2 authentication 

Deploy with docker-compose 
--------------------------
::

    docker-compose -f production.yml build
    docker-compose -f production.yml up -d
    docker-compose -f production.yml run --rm django python manage.py migrate
    docker-compose -f production.yml run --rm django python manage.py createsuperuser


Gitlab Authentication
---------------------

Add application in Gitlab as per `GitLab as OAuth2 authentication service provider`_.

Perform steps as described in `django-allauth Post-Installation`_.

.. _`GitLab as OAuth2 authentication service provider`: https://docs.gitlab.com/ee/integration/oauth_provider.html
.. _`django-allauth Post-Installation`: https://django-allauth.readthedocs.io/en/latest/installation.html#post-installation

Access the tool
---------------

Please visit the various components of the tool via following URLs.

* Architecture Tool: https://architecture-tool.top
* Swagger UI for APIs: https://architecture-tool.top/swagger/
* Flower - Celery monitoring tool: https://architecture-tool.top:5555
* PlantUML: https://architecture-tool.top:8080
* Minio: https://architecture-tool.top:9000