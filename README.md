
# Multi User Blog 

This project is a python example for blog system(application) using Google App Engine. 
And it use the template engine which is jinja 2 ( http://jinja.pocoo.org/ ).

If user registered in this system, user could login & write posts.
Each post has a unique key which could use with url.

# Sample Site URL ( Temporary Operation ) 

    https://norse-blade-166616.appspot.com

# Page Map

    /welcome : link to login or signup

    /user/signup : register user to blog system
    /user/login  : login to blog system

    /blog/          : shows all blog
    /blog/[1234]    : shows each blog with unique blog key
    /blog/newpost   : edit new post to save 

    /user/logout : redirect to /welcome page
        
# Source Directoy

    / : main route code
    
    /static : css code
    
    /templates : html template code 
    
    /module :  use and blog request handling code


# Setup for this project ( from udacity.com ) 

    •	Install Python if necessary
    •	Install Google App Engine SDK.
    •	Sign Up for a Google App Engine Account.
    •	When developing locally, you can use dev_appserver.py to run a copy of your app 
        on your own computer, and access it at http://localhost:8080/.
    •	Create a new project in Google’s Developer Console using a unique name.
    •	Deploy your project with gcloud app deploy.

# Screen Shot - signup
![screenshot](./screenshot_signup.png)

