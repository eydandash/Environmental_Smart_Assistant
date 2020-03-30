from django.contrib import admin
from django.urls import include,path

urlpatterns = [
    path(r'', include('Nile_App.urls')),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
]
