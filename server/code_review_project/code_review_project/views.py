import os
from django.conf import settings
from django.http import HttpResponse
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


def index_view(request):
    """
    Renders the homepage, no matter the URL it's called from
    """

    try:
        index_html = ""
        with open(os.path.join(settings.STATIC_ROOT, 'index.html'), 'r') as f:
            index_html = f.read()

        return HttpResponse(index_html)
    except Exception as e:
        print('Error occurred while fetching index.html', e)


def swagger_schema_view():
    schema_view = get_schema_view(
        openapi.Info(
            title="GitHub Repo Analyser",
            default_version='v1',
            description="Find all the APIs here.",
            terms_of_service="https://www.google.com/policies/terms/",
            contact=openapi.Contact(email="aviroop.paul@think41.com"),
            license=openapi.License(name="BSD License"),
        ),
        public=True,
        permission_classes=(permissions.AllowAny,),
    )

    return schema_view
