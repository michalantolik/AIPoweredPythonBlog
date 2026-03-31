# AIPoweredPythonBlog
AIPoweredPythonBlogEngine is a Django-based blogging platform built with Python that combines a fully custom UI system with AI-driven content workflows. Designed and implemented from scratch, it demonstrates backend architecture, clean design, and practical AI integration for developer-focused publishing.


## Prerequisites






```powershell
#################################################################
# Install PyCharm Community edition
#################################################################

choco install pycharm-community -y

#################################################################
# Install Python 3 via Chocolatey (in PyCharm terminal)
#################################################################

choco install python -y
python --version
pip --version

python --version
pip --version

#################################################################
# Install Django (in PyCharm terminal)
#################################################################

python -m pip install django

django-admin --version
```





## Create and run Django project

```powershell
#################################################################
# Create Django project (in PyCharm terminal)
#################################################################

django-admin startproject ai_powered_blog

#################################################################
# Run Django development web server (in PyCharm terminal)
#################################################################

cd ai_powered_blog

python manage.py runserver
```

## Create Django App

```powershell
################################################################################
# Create and run Django App (Web Page)
################################################################################

cd ai_powered_blog

python manage.py startapp website

## DECLARE Django App 'website' as a part of Django Project 'ai_powered_blog'

# --> open "settings.py"
# --> scroll down to INSTALLED_APPS
# --> add 'website' to INSTALLED_APPS array
```

1. Remove from `website` folder: `migrations`, `admin.py`, `apps.py`, `models.py`, `tests.py`
2. Keep in `website` folder: `views.py`, `__init__.py`
3. Paste in `views.py` *(so called view function)*

```python
from django.http import HttpResponse
from django.shortcuts import render

def welcome(request):
    return HttpResponse("Welcome to the AI Powered Python Blog!")

```

4. Open `ulrs.py` and find the `urlpatterns` array *(which contains URL mappings)*
5. Import the implemented `welcome` view function above the `urlpattern` URL mappings like this

```python
from website.views import welcome
```

6. Solve the `unresolved reference errors for #5
   
👉 right-click on "ai_powered_blog" Django project 👉 Mark Directory as 👉 Source Root

7. Add the following URL mapping in the `urlpattern` array

```python
path('welcome.html', welcome)
```

8. ...
