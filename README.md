# Notes App 📝

## Overview
Notes App is a straightforward yet robust application developed with Django, a high-level Python web framework. It features a powerful API built on the Django Rest Framework, ensuring seamless integration with various front-end or mobile applications.

## Features
- **User Authentication:** A secure user authentication system guarantees data privacy.
- **CRUD Operations (Create, Read, Update, Delete):** Effortlessly manage your notes with comprehensive CRUD functionality.
- **API Integration:** Utilize the Django Rest Framework for smooth integration with other applications.

## Technologies
- Python 3.x
- Django
- Django Rest Framework

## Getting Started
To run the Notes App locally, follow these steps:

- First clone the repository from Github and switch to the new directory:

    $ git clone git@github.com/guisecreator/notes.git
    $ cd notes
    
Activate the virtualenv for your project.
    
Install project dependencies:

    $ pip install -r requirements/local.txt
    
    
Then simply apply the migrations:

    $ python manage.py migrate
    

You can now run the development server:

    $ python manage.py runserver
