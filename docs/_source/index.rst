.. Architecture Tool documentation master file, created by
   sphinx-quickstart.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Architecture Tool
======================================================================

The architecture tool adopts "diagram as text" approach. It draws UML diagrams to model a complex IT environment, and it's especially useful and efficient to manage the drawings when over 20 nodes and relationships are involved. 

The tool can also be extended as a configuration and asset management tool and single source of truth for the real IT environment. For example, if you add a new user in the tool, then the user will be created in your IT environments via a background job.

Furthermore, it will provide some lightweight solutions for uses in the future to draw architecture diagrams for their applications in hybird cloud environments.

Features
--------
* Log in  with Gitlab
* A GUI to create/update all resources
* JSON schema to define node attributes and constrains
* Generates PlantUML diagrams to define graphical views of the system
* Synchronize data from upstream tools or resources
* Act as single source of truth by pushing data to downstream tools
* Background job to save data to Gitlab for traceability of data changes
* Background job to update document in Confluence whenever a node changes
* Zoom in/out of diagrams

Technical Summary
------------------
* Django 3.0, PostgreSQL
* AdminLTE template, Bootstrap 4
* Project initialized by cookiecutter-django
* Render HTML forms based on JSON schema definition
* Django REST framework and Swagger UI for backend APIs
* OAuth2 authentication with Gitlab
* Asynchronous tasks using Celery and Redis
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


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
