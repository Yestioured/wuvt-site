from functools import wraps
from flask import abort, request
import netaddr
from wuvt import redis_conn

from wuvt import app


def local_only(f):
    @wraps(f)
    def local_wrapper(*args, **kwargs):
        if request.remote_addr not in netaddr.IPSet(app.config['INTERNAL_IPS']):
            abort(403)
        else:
            return f(*args, **kwargs)
    return local_wrapper


def dj_interact(f):
    @wraps(f)
    def dj_wrapper(*args, **kwargs):
        # Call in the function first incase it changes the timeout
        ret = f(*args, **kwargs)

        redis_conn.set('dj_active', 'true')
        # logout/login must delete this dj_timeout
        expire = redis_conn.get('dj_timeout')
        if redis_conn.get('dj_timeout') is None:
            expire = app.config['DJ_TIMEOUT']

        redis_conn.expire('dj_active', int(expire))

        return ret
    return dj_wrapper
