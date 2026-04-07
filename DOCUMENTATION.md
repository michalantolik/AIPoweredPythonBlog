# Documentation

## Start application

```powershell
python manage.py runserver
```

## Run unit tests & integration tests

```powershell

python manage.py test

python manage.py test -v 2

python manage.py test posts
python manage.py test api

python manage.py test posts.tests.test_models
```


## Run Playwright tests

```powershell
pytest tests/playwright

pytest tests/playwright -v

pytest tests/playwright --headed
```
