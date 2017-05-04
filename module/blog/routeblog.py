import webapp2

from module.handler import Handler
from post import Post
from google.appengine.ext import db


def blog_key(name='default'):
    return db.Key.from_path('blogs', name)


class BlogListPage(Handler):
    def get(self):
        # posts = db.GqlQuery("select * from Post order by created desc")
        username = self.read_cookie_val('name')
        posts = Post.all().order('-created')
        self.render("blog/bloglist.html", posts=posts, username=username)


class BlogPage(Handler):
    def get(self, blog_id):
        key = db.Key.from_path(
                        'Post',
                        int(blog_id),
                        parent=blog_key())
        post = db.get(key)
        if not post:
            self.error(404)
            return

        self.render("blog/blogpost.html", post=post)


class NewPostPage(Handler):
    def get(self):
        self.render("blog/newpost.html")

    def post(self):
        subject = self.request.get("subject")
        content = self.request.get("content")

        if subject and content:
            p = Post(
                    parent=blog_key(),
                    subject=subject,
                    content=content)
            p.put()
            self.redirect('/blog/%s' % str(p.key().id()))
        else:
            error = 'subject and content, please!'
            self.render('blog/newpost.html', subject=subject,
                        content=content, error=error)
