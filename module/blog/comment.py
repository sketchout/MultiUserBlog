import os
import jinja2
from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'templates')
jinja_env = jinja2.Environment(
                            loader=jinja2.FileSystemLoader(template_dir),
                            autoescape=True)


def render_str(template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)


class Comment(db.Model):
    content = db.TextProperty(required=True)
    author = db.StringProperty(required=True)
    blog_id = db.StringProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)
    modified = db.DateTimeProperty(auto_now=True)

    def render(self):
        self._render_text = self.content.replace('\n', '<br>')
        return render_str("blog/rowcomment.html", comment=self)
