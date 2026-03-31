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
# Install Django and verify (in PyCharm terminal)
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
