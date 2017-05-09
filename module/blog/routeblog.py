import webapp2
import time

from module.handler import Handler
from post import Post
from comment import Comment
from google.appengine.ext import db


def blog_key(name='default'):
    return db.Key.from_path('blogs', name)


class BlogListPage(Handler):
    def get(self):
        # posts = db.GqlQuery("select * from Post order by created desc")
        username = self.read_cookie_val('name')
        posts = Post.all().order('-created')
        if not username:
            return self.redirect('/user/login')
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

class LikeBlogPage(Handler):
    def post(self,blog_id):
        username = self.read_cookie_val('name')
        if not username:
            return self.redirect('/user/login')
        key = db.Key.from_path(
                        'Post',
                        int(blog_id),
                        parent=blog_key())
        post = db.get(key)
        if not post:
            self.error(404)
            return

        if username == post.author:
            self.write("You can't like your own post!")
        else:
            if username in post.liked_user:
                self.write("You can olny like a post once")
            else:
                post.liked_user.append(username)
                post.liked_count += 1
                post.put()
                time.sleep(0.1)
                self.redirect("/blog/")


class NewPostPage(Handler):
    def get(self):
        username = self.read_cookie_val('name')
        if not username:
            return self.redirect('/user/login')
        self.render("blog/newpost.html")

    def post(self):
        username = self.read_cookie_val('name')
        if not username:
            return self.redirect('/user/login')

        if "cancel" in self.request.POST:
            self.redirect('/blog/')
            return

        if "save" in self.request.POST:
            author = username
            subject = self.request.get("subject")
            content = self.request.get("content")

            if subject and content:
                p = Post(
                        parent=blog_key(),
                        subject=subject,
                        content=content,
                        author=author
                        )
                p.put()
                self.redirect('/blog/%s' % str(p.key().id()))
            else:
                error = 'subject and content, please!'
                self.render('blog/newpost.html', subject=subject,
                            content=content, error=error)


class EditPostPage(Handler):
    def get(self, blog_id):
        username = self.read_cookie_val('name')
        if not username:
            return self.redirect('/user/login')

        key = db.Key.from_path(
                        'Post',
                        int(blog_id),
                        parent=blog_key())
        post = db.get(key)
        if not post:
            self.error(404)
            return

        if username == post.author:
            self.render("blog/editpost.html", post=post)
        else:
            self.write("You can't edit other User's posts!")

    def post(self, blog_id):
        username = self.read_cookie_val('name')
        if not username:
            return self.redirect('/user/login')

        subject = self.request.get("subject")
        content = self.request.get("content")

        uptPost = Post.get_by_id(int(blog_id), parent=blog_key())
        if not uptPost:
            return self.error(404)

        if "cancel" in self.request.POST:
            self.redirect('/blog/%s' % str(uptPost.key().id()))
            return

        if "update" in self.request.POST:
            if subject and content:
                uptPost.subject = subject
                uptPost.content = content
                uptPost.put()
                self.redirect('/blog/%s' % str(uptPost.key().id()))
            else:
                error = 'subject and content, please!'
                self.render('blog/editpost.html',
                        subject=subject,
                        content=content,
                        error=error)

        if "delete" in self.request.POST:
            self.redirect('/blog/deletepost/%s' % str(uptPost.key().id()))


class DeletePostPage(Handler):
    def get(self, blog_id):
        username = self.read_cookie_val('name')
        if not username:
            return self.redirect('/user/login')
        key = db.Key.from_path(
                        'Post',
                        int(blog_id),
                        parent=blog_key())
        post = db.get(key)
        if not post:
            return self.error(404)
        self.render("blog/delpost.html",post=post);

    def post(self, blog_id):
        username = self.read_cookie_val('name')
        if not username:
            return self.redirect('/user/login')

        if "yes" in self.request.POST:
            key = db.Key.from_path(
                            'Post',
                            int(blog_id),
                            parent=blog_key())
            post = db.get(key)
            if not post:
                return self.error(404)
            post.delete()
            time.sleep(0.1)
            return self.redirect("/blog")

        if "no" in self.request.POST:
            return self.redirect("/blog")



class NewCommentPage(Handler):
    def get(self, blog_id):
        key = db.Key.from_path(
                        'Post',
                        int(blog_id),
                        parent=blog_key())
        post = db.get(key)
        if not post:
            return self.error(404)

        comments = db.GqlQuery(
            "select * from Comment where blog_id=:1", str(blog_id)
            )
        if not comments:
            return self.error(404)

        self.render("blog/newcomment.html",
                    post=post,
                    comments=comments)

    def post(self, blog_id):
        username = self.read_cookie_val('name')
        if not username:
            return self.redirect('/user/login')

        if "cancel" in self.request.POST:
            return self.redirect("/blog/%s" % str(blog_id))

        if "submit" in self.request.POST:
            content = self.request.get('content')
            author = username
            if content:
                c = Comment(
                    blog_id=blog_id,
                    content=content,
                    author=author)
                c.put()
                time.sleep(0.1)
                return self.redirect('/blog/newcomment/%s' % str(blog_id))
            else:
                key = db.Key.from_path(
                                'Post',
                                int(blog_id),
                                parent=blog_key())
                post = db.get(key)
                if not post:
                    return self.error(404)

                comments = db.GqlQuery(
                    "select * from Comment where blog_id=:1", str(blog_id)
                    )
                if not comments:
                    return self.error(404)

                error = 'comment, please!'
                self.render("blog/newcomment.html",
                            post=post,
                            comments=comments,
                            error=error)


class EditCommentPage(Handler):
    def get(self, comment_id):
        username = self.read_cookie_val('name')
        if not username:
            return self.redirect('/user/login')

        key = db.Key.from_path(
                        'Comment',
                        int(comment_id)
                        )
        comment = db.get(key)
        if not comment:
            return self.error(404)

        if username == comment.author:
            self.render("blog/editcomment.html", comment=comment)
        else:
            self.write("You can't edit other User's comments!")

    def post(self, comment_id):
        username = self.read_cookie_val('name')
        if not username:
            return self.redirect('/user/login')

        content = self.request.get('content')
        uptComment = Comment.get_by_id(int(comment_id))

        if "cancel" in self.request.POST:
            return self.redirect("/blog/newcomment/%s" % str(uptComment.blog_id))

        if "update" in self.request.POST:
            if content:
                uptComment.content = content
                uptComment.put()
                time.sleep(0.1)
                return self.redirect("/blog/newcomment/%s" % str(uptComment.blog_id))

        if "delete" in self.request.POST:
            self.redirect('/blog/deletecomment/%s' % str(comment_id))


class DeleteCommentPage(Handler):
    def get(self, comment_id):
        username = self.read_cookie_val('name')
        if not username:
            return self.redirect('/user/login')

        key = db.Key.from_path(
                        'Comment',
                        int(comment_id)
                        )
        comment = db.get(key)
        if not comment:
            return self.error(404)

        self.render("blog/delcomment.html",comment=comment);

    def post(self, comment_id):
        username = self.read_cookie_val('name')
        if not username:
            return self.redirect('/user/login')

        uptComment = Comment.get_by_id(int(comment_id))

        if "no" in self.request.POST:
            return self.redirect("/blog/newcomment/%s" % str(uptComment.blog_id))

        if "yes" in self.request.POST:
            key = db.Key.from_path(
                            'Comment',
                            int(comment_id)
                            )
            comment = db.get(key)
            if not comment:
                return self.error(404)
            comment.delete()
            time.sleep(0.1)
            return self.redirect("/blog/newcomment/%s" % str(uptComment.blog_id))

