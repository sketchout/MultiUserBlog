import os
import webapp2
import jinja2

import hashlib
import hmac
import random
from module.user.user import User


template_dir = os.path.join(os.path.dirname(__file__), '..', 'templates')
jinja_env = jinja2.Environment(
                            loader=jinja2.FileSystemLoader(template_dir),
                            autoescape=True)


secure_key = "dBqz8+Bbu3KzVK>a"


def make_secure_val(val):
    return "%s|%s" % (val, hmac.new(secure_key, val).hexdigest())


def check_secure_val(secure_val):
    val = secure_val.split('|')[0]
    if secure_val == make_secure_val(val):
        return val


class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

    def set_cookie_val(self, name, val):
        cookie_str = str("%s=%s; Path=/" % (name, val))
        self.response.headers.add_header(
                "Set-Cookie",
                cookie_str)

    def unset_cookie_val(self, name, val):
        self.set_cookie_val(name, val)

    def read_cookie_val(self, name):
        cookie_val = self.request.cookies.get(name)
        return cookie_val and check_secure_val(cookie_val)

    def login(self, u):
        secure_val = make_secure_val(u.name)
        cookie_str = str("%s=%s; Path=/" % ("name", secure_val))
        self.response.headers.add_header("Set-Cookie", cookie_str)

    def login_username(self, username):
        secure_val = make_secure_val(username)
        cookie_str = str("%s=%s; Path=/" % ("name", secure_val))
        self.response.headers.add_header("Set-Cookie", cookie_str)

    def logout(self):
        self.unset_cookie_val("name", "")

    def initialize(self, *a, **kw):
        webapp2.RequestHandler.initialize(self, *a, **kw)
        name = self.read_cookie_val('name')
        self.user = name and User.by_name(name)
