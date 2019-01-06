[![codecov](https://codecov.io/gh/daryavasilyeva/lms/branch/master/graph/badge.svg)](https://codecov.io/gh/daryavasilyeva/lms)
[![Build Status](https://travis-ci.org/daryavasilyeva/lms.svg?branch=master)](https://travis-ci.org/daryavasilyeva/lms)

Final project for PPPoSD

Author: Vasilyeva Darya 

It's a platform for managing study process.

You can:
    * Login with 
        mail: dasha@mail.com; 
        password = 'cat' - as admin; 
    * Create new user (teacher or student), group, course (as admin);
    * After creating teacher or student a special verification code is shown;
    * You can sign up with verification code. You can't sign up with one verification code twice; 
    * As teacher or student you don't have permission to add new users, groups or courses 
    * There is a validation for email field

It can't (now):
    * Check if password is complex or not 
    * Create Materials and Homework
    * Change profile information 
    * 
    
To start:
    * download (or clone) repository
    * run `python setup.py install` 
    * run `flask run` 
    * enter `http://localhost:5000` in a web browser - it's an index page 
    
 Thanks a lot to https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world - really useful blog to get start with web forms, api and html. 
