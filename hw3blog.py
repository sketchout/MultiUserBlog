import webapp2

from module.blog import routeblog
from module.user import routeuser


#################################
app = webapp2.WSGIApplication([
    ('/blog/?', routeblog.BlogListPage),
    ('/blog/(\d+)', routeblog.BlogPage),
    ('/blog/newpost', routeblog.NewPostPage),
    ('/', routeuser.RootPage),
    ('/welcome', routeuser.WelcomePage),
    ('/user/signup', routeuser.SignUpPage),
    ('/user/login', routeuser.LoginPage),
    ('/user/logout', routeuser.LogoutPage)],
    debug=True)
