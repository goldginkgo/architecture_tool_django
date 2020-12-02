import json
from datetime import datetime

from django_redis import get_redis_connection


def display_users_name(user):
    if user.get_full_name():
        return user.get_full_name()
    else:
        return user.username


def log_user_action(user, action, rc_type, resource):
    action = {
        "action": action,
        "message": f"{display_users_name(user)} {action}s {rc_type} {resource}",
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC"),
    }
    con = get_redis_connection("default")
    con.lpush("user_actions", json.dumps(action))


def recent_user_actions():
    con = get_redis_connection("default")
    user_actions = con.lrange("user_actions", 0, 4)
    return [json.loads(i) for i in user_actions]
