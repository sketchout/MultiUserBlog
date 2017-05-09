import webapp2

import re

from module import printlog

from module.handler import Handler
from user import User

PrintLog = printlog.PrintLog()

username_valid_error_msg = """
That's not a valid username.
"""
password_valid_error_msg = """
That wasn't a valid password.
"""
password_match_error_msg = """
Your passwords didn't match.
"""
email_valid_error_msg = """
That's not a valid email.
"""

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
PASSWORD_RE = re.compile(r"^.{3,20}$")
EMAIL_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")


def valid_username(username):
    return USER_RE.match(username)


def valid_password(password):
    return PASSWORD_RE.match(password)


def valid_email(email):
    return EMAIL_RE.match(email)


class RootPage(Handler):
    def get(self):
        self.redirect("/welcome")


class WelcomePage(Handler):
    def get(self):
        PrintLog.out("WelcomePage", "Started")
        username = self.read_cookie_val('name')
        if username:
            self.render("welcome.html", username=username)
        else:
            self.redirect("/user/signup")


class LogoutPage(Handler):
    def get(self):

        self.logout()
        self.redirect("/welcome")


class LoginPage(Handler):
    def get(self):
        self.render("user/login.html", error_login="")

    def post(self):
        username = self.request.get("username")
        password = self.request.get("password")

        if not (username and password):
            msg = "Invalid login"
            return self.render("user/login.html", error_login=msg)

        u = User.login(username, password)
        if u:
            self.login(u)
            self.redirect("/blog")
        else:
            msg = "Invalid login"
            return self.render("user/login.html", error_login=msg)

        # self.login_username(username)
        # self.redirect("/blog")


class SignUpPage(Handler):
    def get(self):
        self.render("user/signup.html")

    def post(self):
        username_valid_result = ""
        password_valid_result = ""
        password_match_result = ""
        email_valid_result = ""

        cookie_name = self.request.cookies.get('name')

        username = self.request.get("username")

        if username == "":
            username_valid_result = username_valid_error_msg
        elif not valid_username(username):
            username_valid_result = username_valid_error_msg

        password = self.request.get("password")
        # if password is None or not valid_password(password):
        if password == "" or not valid_password(password):
            password_valid_result = password_valid_error_msg

        verify = self.request.get("verify")
        if password != "" and valid_password(password):
            if password != verify:
                password_match_result = password_match_error_msg

        email = self.request.get("email")
        if email != "" and not valid_email(email):
            email_valid_result = email_valid_error_msg

        if (username_valid_result == "" and
                password_valid_result == "" and
                password_match_result == "" and
                email_valid_result == ""):
            u = User.by_name(username)
            # cookie_str = str( "name=%s; Path=/" % username  )
            # self.response.headers.add_header("Set-Cookie", cookie_str)
            # self.done(self)
            # set_cookie_val("name", username)
            # self.redirect("/welcome?username="+ username)

            if u:
                msg = "That user already exists."
                self.render('user/signup.html', username_valid_result=msg)
            else:
                u = User.register(username, password, email)
                u.put()

                self.login(u)

                # cookie_str = str( "%s=%s; Path=/" % ("name", secure_val) )
                # self.response.headers.add_header("Set-Cookie", cookie_str)

                self.redirect("/blog")
        else:
            self.render(
                "user/signup.html",
                username=username,
                email=email,
                username_valid_result=username_valid_result,
                password_valid_result=password_valid_result,
                password_match_result=password_match_result,
                email_valid_result=email_valid_result)
