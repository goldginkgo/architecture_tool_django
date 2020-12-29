0.8.0-pre
******************
- Fix for django-compose settings
- Production deployment for docker-compose
- Email/SMTP support
- Support token authentication for APIs

0.7.0 (2020-12-25)
******************
- Fix for unnecessary compress tags in HTML files
- Logging for export/import actions
- Use Minio for development environment and object storage for Cloud Foundry deployment
- Node key rename API
- Use production settings for Cloud Foundry deployment


0.6.0 (2020-12-10)
******************

- Use Redis to display recent user actions in timeline section in dashboard page
- Add Minio for object storage in Docker development and production environment
- Export current data to Zip file asynchronously
- Add dropzone.js for uploading file
- Import data from another tool or revert data to previsous status (development environment)

0.5.0 (2020-12-01)
******************

- Edit node json directly
- Fix for issues of existing nodes when node schema is changed
- Set validation error attribute for node/list/graph when schema changes
- Scheduled job to synchronize data to Gitlab as a backup method
- Update Gitlab when nodetype/edgetype/schema/list/graph/nodes changes
- Use logging instead of print

0.4.0 (2020-11-12)
******************

- Smaller edit/delete buttons on nodetypes page
- Remove user related APIs
- Add APIs for all resources supported by Swagger UI
- Add project API documentation
- Migrate APIs implemented in django to drf for all resources
- Add preview button for node attributes
- Move JS in html to dedicated JS files
- Fix issues for changing exsiting edges
- Display errors in node submit page
- Use Django template to render graph
- Initial support for graph detail page
- Restructure FAQ page

0.3.0 (2020-11-06)
******************

- Initial support for List
- Document Update
- Use atlassian-python-api to communicate with Confluence
- Display description in textarea
- Remove keyFormat attribute
- Redirect to details page after create/update
- data validation for list, graph and schema
- Remove unused code for node


0.2.0 (2020-10-28)
******************

- Support for asynchronous tasks
- Update Confluence pages automatically on node changes
- FAQ page
- Update documents

0.1.0 (2020-10-19)
******************
