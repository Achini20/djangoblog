# DjangoBlog

A blog application built with Django as a learning project.

## Features
- Post list with pagination, category filter and search
- Create, edit, delete posts (author only)
- Image upload with validation and auto-resize
- Registration, login, logout, password reset
- My Posts dashboard
- Responsive navbar and custom 403 page

## Setup
1. Create a virtual environment and activate it
2. `pip install -r requirements.txt`
3. Create a `.env` file with your settings
4. `python manage.py migrate`
5. `python manage.py runserver`