## CLI Commands

### Start application

```powershell
python manage.py runserver
```

### Create & apply migrations

```powershell
python manage.py makemigrations

python manage.py migrate
```

### Run unit & integration tests

```powershell

python manage.py test

python manage.py test -v 2

python manage.py test posts
python manage.py test api

python manage.py test posts.tests.test_models
```


### Run playwright tests

```powershell
pytest tests/playwright

pytest tests/playwright -v

pytest tests/playwright --headed
```
