
from django.contrib import admin
from django.urls import path, include
import myapp.views as myapp
from django.conf import settings
from django.conf.urls.static import static
import debug_toolbar

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('myapp.urls')),
    # path('accounts/', include('allauth.urls')),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += [path('__debug__/', include(debug_toolbar.urls))]