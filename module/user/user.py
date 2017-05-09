import hashlib
import hmac
import random
import logging

from string import letters
from google.appengine.ext import db


def make_salt(length=5):
    salt = ''.join(random.choice(letters) for x in range(length))
    return salt


# salt="|Ojv2-S9a@q(9Qg"
def make_pw_hash(name, pw, salt=None):
    if not salt:
        salt = make_salt()
    h = hashlib.sha256(name+pw+salt).hexdigest()
    return "%s,%s" % (salt, h)


def valid_pw(name, password, h):
    salt = h.split(',')[0]
    logging.info("~~valid_pw : salt :" + salt)
    return h == make_pw_hash(name, password, salt)


def users_key(group='default'):
    return db.Key.from_path('users', group)


class User(db.Model):
    name = db.StringProperty(required=True)
    pw_hash = db.StringProperty(required=True)
    email = db.StringProperty()

    @classmethod
    def by_id(cls, uid):
        return User.get_by_id(uid, parent=users_key())

    @classmethod
    def by_name(cls, name):
        u = User.all().filter('name =', name).get()
        return u

    @classmethod
    def register(cls, name, pw, email=None):
        pw_hash = make_pw_hash(name, pw)
        return User(parent=users_key(),
                    name=name,
                    pw_hash=pw_hash,
                    email=email)

    @classmethod
    def login(cls, name, pw):
        u = cls.by_name(name)
        logging.info("~~~u.pw_hash :"+u.pw_hash)
        logging.info("~~~ pw :"+pw)
        if u and valid_pw(name, pw, u.pw_hash):
            return u
