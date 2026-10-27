"""
URL configuration for vegetablesfruits project.
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView
from django.conf import settings
from django.conf.urls.static import static # ✅ IMPORTANT

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('vegetables_fruits.urls')),
    path('home/', TemplateView.as_view(template_name='index.html'), name='home'),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns

    # ✅ SERVIR LES FICHIERS MÉDIA EN DÉVELOPPEMENT
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)