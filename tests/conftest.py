from django.conf import settings
import django
import sys
import os


def pytest_configure():
    sys.path.append(
        os.path.dirname(__file__),
    )
    settings.configure(
        DEBUG=True,
        STATIC_URL="/static/",
        INSTALLED_APPS=(
            "app",
        ),
        TEMPLATES=[
            {
                "BACKEND": 'django.template.backends.django.DjangoTemplates',
                "APP_DIRS": True,
                "OPTIONS": {
                    "debug": True,
                },
            },
        ]
    )
    django.setup()
