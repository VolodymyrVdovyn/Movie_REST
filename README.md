# Backend part of site with films. Wrote on Django REST framework

Clone this project to your computer:

    $ git clone https://github.com/VolodymyrVdovyn/Movie_REST.git

Navigate to the folder with this project.
In this project as a Python virtual environment was used pipenv.

If you don't have pipenv on your computer, run the command:

    $ pip install pipenv

To install requirements run:

    $ pipenv shell
    $ pipenv install --ignore-pipfile

Perform migrations:

    $ python manage.py makemigrations
    $ python manage.py migrate

Create an administrator:

    $ python manage.py createsuperuser

Start the local server:

    $ python manage.py runserver
