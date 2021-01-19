.. _settings:

Settings
========

This project inherits all settings from cookiecutter-django. Please refer to the `Settings of coookiecutter-django`_.

.. _`Settings of coookiecutter-django`: https://cookiecutter-django.readthedocs.io/en/latest/settings.html

There are also additional settings only applicable to the project:

======================================= =========================== ============================================== ======================================================================
Environment Variable                    Django Setting              Development Default                            Production Default
======================================= =========================== ============================================== ======================================================================
GITLAB_URL                              GITLAB_URL                  n/a                                            n/a
REQUESTS_CA_BUNDLE                      REQUESTS_CA_BUNDLE          n/a                                            n/a
PLANTUML_SERVER_URL                     PLANTUML_SERVER_URL         n/a                                            n/a
ARCHITECTURE_TOOL_URL                   ARCHITECTURE_TOOL_URL       n/a                                            n/a
SYNC_TO_CONFLUENCE                      SYNC_TO_CONFLUENCE          False                                          False
CONFLUENCE_URL                          CONFLUENCE_URL              n/a                                            n/a
API_KEY                                 API_KEY                     n/a                                            n/a
CONFLUENCE_USER                         CONFLUENCE_USER             n/a                                            n/a
CONFLUENCE_PASS                         CONFLUENCE_PASS             n/a                                            n/a
SYNC_TO_GITLAB                          SYNC_TO_GITLAB              False                                          False
GITLAB_PROJECT_ID                       GITLAB_PROJECT_ID           n/a                                            n/a
GITLAB_TOKEN                            GITLAB_TOKEN                n/a                                            n/a
======================================= =========================== ============================================== ======================================================================
