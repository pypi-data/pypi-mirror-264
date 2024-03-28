# django-fitbit-healthkit

django-fitbit-healthkit is a Django Fitbit App with HealthKit-friendly API

Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add "fitbit" to your INSTALLED_APPS setting like this:

```
INSTALLED_APPS = [
    ...,
    "django_fitbit_healthkit",
]
```

2. Include the fitbit URLconf in your project urls.py like this:

```
path("fitbit/", include("django_fitbit_healthkit.urls")),
```

3. Run ``python manage.py migrate`` to create the models.

4. Visit the ``/fitbit/login`` URL to sign in with Fitbit.
