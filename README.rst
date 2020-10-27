Architecture Tool
=================

.. image:: https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg
     :target: https://github.com/pydanny/cookiecutter-django/
     :alt: Built with Cookiecutter Django
.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
     :target: https://github.com/ambv/black
     :alt: Black code style

:License: MIT

The architecture tool adopts "diagram as text" approach. It draws UML diagrams to model a complex IT environment, and it's especially useful and efficient to manage the drawings when over 20 nodes and relationships are involved.

The tool can also be extended as a configuration management tool and single source of truth for the real IT environment. For example, if you add a new user in the tool, then the user will be created in your IT environments.

Furthermore, it will provide some lightweight solutions for uses to draw architecture diagrams for their applications in cloud environments.

Functional Features
-------------------
* Log in  with Gitlab.
* A GUI to create/update all resources.
* JSON schema to define node attributes and constrains.
* Generates PlantUML diagrams to define graphical views of the system.
* Synchronize data from upstream tools or resources.
* Act as single source of truth by pushing data to downstream tools.
* Background job to save data to Gitlab for traceability of data changes.
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


Concepts
--------

* Schema: JSON schema to define the attributes of a node, or the schema for a list or graph.
* Node: An entity in the IT environment, can be a hardware, software, application, user or anything.
* Node Type: Define the type of a kind of nodes and other related attributes.
* Edge: Relationships between different nodes. Every node defines its outbound edges.
* List: A list is created by selecting attributes and node selection criteria to display similar nodes in a HTML table. (e.g. a list of technical users or open source software)
* Graph: Similar to a list but displayed in a diagram. (e.g. a diagram of dependency tree of all components )


Settings
--------

Moved to settings_.

.. _settings: http://cookiecutter-django.readthedocs.io/en/latest/settings.html

Basic Commands
--------------

Setting Up Your Users
^^^^^^^^^^^^^^^^^^^^^

* To create a **normal user account**, just go to Sign Up and fill out the form. Once you submit it, you'll see a "Verify Your E-mail Address" page. Go to your console to see a simulated email verification message. Copy the link into your browser. Now the user's email should be verified and ready to go.

* To create an **superuser account**, use this command::

    $ python manage.py createsuperuser

For convenience, you can keep your normal user logged in on Chrome and your superuser logged in on Firefox (or similar), so that you can see how the site behaves for both kinds of users.

Type checks
^^^^^^^^^^^

Running type checks with mypy:

::

  $ mypy architecture_tool_django

Test coverage
^^^^^^^^^^^^^

To run the tests, check your test coverage, and generate an HTML coverage report::

    $ coverage run -m pytest
    $ coverage html
    $ open htmlcov/index.html

Running tests with py.test
~~~~~~~~~~~~~~~~~~~~~~~~~~

::

  $ pytest

Live reloading and Sass CSS compilation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Moved to `Live reloading and SASS compilation`_.

.. _`Live reloading and SASS compilation`: http://cookiecutter-django.readthedocs.io/en/latest/live-reloading-and-sass-compilation.html



Celery
^^^^^^

This app comes with Celery.

To run a celery worker:

.. code-block:: bash

    cd architecture_tool_django
    celery -A config.celery_app worker -l info

Please note: For Celery's import magic to work, it is important *where* the celery commands are run. If you are in the same folder with *manage.py*, you should be right.




Email Server
^^^^^^^^^^^^

In development, it is often nice to be able to see emails that are being sent from your application. For that reason local SMTP server `MailHog`_ with a web interface is available as docker container.

Container mailhog will start automatically when you will run all docker containers.
Please check `cookiecutter-django Docker documentation`_ for more details how to start all containers.

With MailHog running, to view messages that are sent by your application, open your browser and go to ``http://127.0.0.1:8025``

.. _mailhog: https://github.com/mailhog/MailHog



Deployment
----------

The following details how to deploy this application.



Docker
^^^^^^

See detailed `cookiecutter-django Docker documentation`_.

.. _`cookiecutter-django Docker documentation`: http://cookiecutter-django.readthedocs.io/en/latest/deployment-with-docker.html


Acknowledgments
---------------

* AdminLTE_
* django-dashboard-adminlte_
* django-adminlte3_

.. _AdminLTE: https://github.com/ColorlibHQ/AdminLTE
.. _django-adminlte3: https://github.com/d-demirci/django-adminlte3
.. _django-dashboard-adminlte: https://github.com/app-generator/django-dashboard-adminlte
