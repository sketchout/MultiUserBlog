import webapp2

from module.blog import routeblog
from module.user import routeuser


#################################
app = webapp2.WSGIApplication([
    ('/blog/?', routeblog.BlogListPage),
    ('/blog/(\d+)', routeblog.BlogPage),
    ('/blog/(\d+)/like', routeblog.LikeBlogPage),
    ('/blog/newpost', routeblog.NewPostPage),
    ('/blog/editpost/(\d+)', routeblog.EditPostPage),
    ('/blog/deletepost/(\d+)', routeblog.DeletePostPage),
    ('/blog/newcomment/(\d+)', routeblog.NewCommentPage),
    ('/blog/editcomment/(\d+)', routeblog.EditCommentPage),
    ('/blog/deletecomment/(\d+)', routeblog.DeleteCommentPage),
    ('/', routeuser.RootPage),
    ('/welcome', routeuser.WelcomePage),
    ('/user/signup', routeuser.SignUpPage),
    ('/user/login', routeuser.LoginPage),
    ('/user/logout', routeuser.LogoutPage)],
    debug=True)
