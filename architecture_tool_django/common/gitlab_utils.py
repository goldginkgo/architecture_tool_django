import json
import logging

import gitlab
from django.conf import settings
from gitlab.exceptions import GitlabGetError

logger = logging.getLogger(__name__)


def ordered(obj):  # compare json
    if isinstance(obj, dict):
        return sorted((k, ordered(v)) for k, v in obj.items())
    if isinstance(obj, list):
        return sorted(ordered(x) for x in obj)
    else:
        return obj


def get_project(token=None):
    if token is None:
        gl = gitlab.Gitlab(settings.GITLAB_URL, oauth_token=settings.GITLAB_TOKEN)
        project = gl.projects.get(settings.GITLAB_PROJECT_ID)
    else:
        gl = gitlab.Gitlab(settings.GITLAB_URL, oauth_token=token)
        project = gl.projects.get(settings.GITLAB_PROJECT_ID)

    return project


def sync_file(project, filepath, new_content_json):
    new_content = json.dumps(new_content_json, indent=2)
    try:
        f = project.files.get(file_path=filepath, ref="master")
        old_content = json.loads(f.decode())
        json.loads(f.decode())

        if ordered(old_content) == ordered(new_content_json):
            logger.info(f"{filepath} is update to date.")
        else:
            logger.info(f"sync {filepath}")
            f.content = new_content
            f.save(branch="master", commit_message=f"sync {filepath}")
    except GitlabGetError:
        logger.info(f"sync {filepath}")
        project.files.create(
            {
                "file_path": filepath,
                "branch": "master",
                "content": new_content,
                "commit_message": f"sync {filepath}",
            }
        )


def cleanup_files(project, path, allowed_files):
    for item in project.repository_tree(path, all=True):
        filename = item["name"]
        if filename not in allowed_files:
            delete_file(project, path, filename)


def delete_file(project, path, filename):
    logger.info(f"deleting {path}/{filename}")
    project.files.delete(
        file_path=f"{path}/{filename}",
        commit_message=f"delete {path}/{filename}",
        branch="master",
    )
