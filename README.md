
# Multi User Blog 

This project is a python example for blog system(application) using Google App Engine. 
And it use the template engine which is jinja 2.

If user registered in this system, user could login & write posts.
Each post has a unique key which could use with url.


# Site Map

    /welcome : link to login or signup

        /user/signup : register user to blog system

        /user/login  : login to blog system

            /blog/          : shows all blog
            /blog/[1234]    : shows each blog with unique blog key
            /blog/newpost   : edit new post to save 

        /user/logout : redirect to /welcome page



