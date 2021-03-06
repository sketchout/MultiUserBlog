import os
import jinja2
from module.user.user import User

from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'templates')
jinja_env = jinja2.Environment(
                            loader=jinja2.FileSystemLoader(template_dir),
                            autoescape=True)


def render_str(template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)


class Post(db.Model):
    author = db.StringProperty(required=True)
    subject = db.StringProperty(required=True)
    content = db.TextProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)
    modified = db.DateTimeProperty(auto_now=True)
    liked_count = db.IntegerProperty(default=0)
    liked_user = db.StringListProperty()

    def render(self):
        self._render_text = self.content.replace('\n', '<br>')
        return render_str("blog/rowpost.html", post=self)
