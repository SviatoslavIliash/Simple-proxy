# Simple Django HTTP proxy server

Simple Python HTTP proxy service. It is a Django application with user authentication and simple data analytics.

# Overview

User can log in or create new account. On user page you can see and change some personal information.
Also, user can add websites and their aliases, for opening them with proxy server. 
You can also find simple analytics like incoming data volume and visit counter on the page.

# Installation

1. Setup Python3, pip 
2. Create and activate virtual environment
3. Install from GitHub: (venv)mydir> pip install git+
4. To make migrations in db, run: `python manage.py makemigrations`, `python manage.py migrate`
5. Run using Docker: Install Doker(https://docs.docker.com/get-docker/), clone git repository
6. To build image, run: `docker build . -t myapp`
7. To start  Docker server, run: `docker run -p 127.0.0.1:8000:8000 myapp`

