"""
Login and logout views for the browsable API.

Add these to your root URLconf if you're using the browsable API and
your API requires authentication:

    urlpatterns = [
        ...
        path('auth/', include('rest_framework_admin.urls'))
    ]

You should make sure your authentication settings include `SessionAuthentication`.
"""

__all__ = ['loads_urlpatterns']
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path

from rest_framework_util.decorators import login_exempt
from rest_framework_util.urls import load_urlpatterns


def load_doc_urlpatterns():
    from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
    urlpatterns = [
        path(
            'docs/schema/',
            login_exempt(SpectacularAPIView.as_view()), name='schema'),
        path(
            'docs/schema/swagger-ui/',
            login_exempt(SpectacularSwaggerView.as_view(url_name='schema')), name='swagger-ui'),
        path(
            'docs/schema/redoc/',
            login_exempt(SpectacularRedocView.as_view(url_name='schema')), name='redoc'),
    ]
    return urlpatterns


DEFAULT_PREFIX = {
    'rest_framework_admin.user': 'user',
    'rest_framework_admin.role': 'role',
    'rest_framework_admin.system': 'system',
    'rest_framework_admin.auth': 'auth',
}


def loads_urlpatterns(user_prefix=None, **kwargs):
    DEFAULT_PREFIX.update(user_prefix or {})
    urlpatterns = load_urlpatterns(
        settings.BACKEND_INSTALLED_APPS,
        user_prefix=DEFAULT_PREFIX, **kwargs)
    if settings.DEBUG:
        urlpatterns += load_doc_urlpatterns()
    urlpatterns += static(
        settings.STATIC_URL,
        document_root=settings.STATIC_ROOT)
    return urlpatterns
