.. Architecture Tool documentation master file, created by
   sphinx-quickstart.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Architecture Tool
=================

The architecture tool adopts "diagram as code" approach. Based on the JSON definition of all resources, it generates plain text to draws UML diagrams to model a complex cloud environment. It's especially useful and efficient to manage the drawings when over 20 nodes and relationships are involved. 

The tool can be extended as a configuration and asset management tool and single source of truth for the real IT environment. Here are a few features that the tool can be extended to have.

* Update Confluence pages on node changes
* Update Jira tickets on node changes
* Trigger environment changes. (e.g. create permission groups in another software when the groups are added to the tool)
* Synchronize data from external resources (e.g. person data from ative directory)
* ...

Furthermore, it will provide some lightweight solutions for uses in the future to draw architecture diagrams for their applications in hybird cloud environments.

Functional Features
-------------------
* Sign in with Gitlab or local account
* A GUI to create/update all resources
* JSON schema to define node attributes and constrains
* Generates PlantUML diagrams to define graphical views of the system
* Synchronize data from upstream tools or resources
* Act as single source of truth by pushing data to downstream tools
* Background job to save data to Gitlab to keep track of node change history
* Background job to update document in Confluence whenever a node changes
* Zoom in/out of diagrams
* Export data as zipfile, import/restore data from another architecture tool instance

Technical Summary
-----------------
* Python 3.8, Django 3.0, PostgreSQL
* Django REST framework and Swagger UI for backend APIs
* AdminLTE template, Bootstrap 4
* Project initialized by cookiecutter-django
* Render HTML forms based on JSON schema definition
* OAuth2 authentication with Gitlab
* Asynchronous tasks using Celery and Redis
* Caching using Redis
* Amazon S3 compatible object storage - Minio
* Automated testing using pytest
* Deployment: Docker, Cloud Foundry
* Sphinx for documentation


.. toctree::
   :maxdepth: 2
   :caption: Contents:

   dev-environment
   settings
   deployment-on-cloudfoundry
   deployment-with-docker
   deployment-on-kubernetes
   documentation
   advanced
   changelog


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
