Advanced Topics
===============

.. index:: confluence gitlab backup restore

How to enable automated document update in Confluence when node changes?
--------------------------------------------------------------

* Define the confluence related environment variables as described in the ``Settings`` page.


How to enable synchronization with Gitlab for all the resources?
----------------------------------------------------------------
The database is the primary source of truth of all data. The reason is that direct commit to Gitlab may have lots of validation errors. By using the tool it’s forced to correct the errors before submit.

But the data will also be synchronized to a Gitlab repository. It can be seen as a backup method. So whenever there are changes in the tool, a background job will commit the changes to the node file in the repository. Then the repository keeps track of who changed what.

The tool will also have the feature to export/import data to/from Gitlab repository. It's just like a software upgrade, we import all backup data to the new installed software. This would be helpful during the initial setup of the tool when there is already a repository conforming to the format the tool requires.

We will tag the source code and data repository at the same time so that it's consistent. When the database is broken or we want to revert to the data state of a specific point of time, we can cleanup all data in the tool and import data from Gitlab. Cleaning up all data is as easy as deleting all schemas.

Steps:

* Create a project in GitLab
* Create an personal access token of a user who has maintainer permission to the GitLab project, it's the default user to sync data
* Define `SYNC_TO_GITLAB`, `GITLAB_PROJECT_ID`, `GITLAB_TOKEN` as environment variable and restart the application

How to import data from another architecture tool instance or restore the data to previous status?
--------------------------------------------------------------------------------------------------

* Cleanup all resource data in the tool. Just delete all schemas will delete all the data. Not required if it's a fresh installation.
* Disable automated synchronization to GitLab and automated update to Confluence, and restart the application. You may need to deploy a prevous version of the app that is consistent with the data if required.
* Import and upload data from the exported data file.
* Enable the automated synchronization again if needed.
