# Backend part of site with films. Wrote on Django REST framework

Clone this project to your computer:

    $ git clone https://github.com/VolodymyrVdovyn/Movie_REST.git

Navigate to the folder with this project:

    $ cd Movie_REST/

In this project as a Python virtual environment was used pipenv.

If you don't have pipenv on your computer, run the command:

    $ pip install pipenv

To install requirements run:

    $ pipenv shell
    (Movie_REST)$ pipenv install --ignore-pipfile

Navigate to the folder django_movie:

    $ cd django_movie/

Perform migrations:

    (Movie_REST)$ python manage.py makemigrations
    (Movie_REST)$ python manage.py migrate

Create an administrator:

    (Movie_REST)$ python manage.py createsuperuser

Start the local server:

    (Movie_REST)$ python manage.py runserver

Then visit `http://localhost:8000/api/v1/movie/` to view the page with movies.

Or `http://localhost:8000/admin/` to view the admin page.
