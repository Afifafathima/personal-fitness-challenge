from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # 🔥 rename Django admin URL
    path('django-admin/', admin.site.urls),

    # your app routes
    path('', include('core.urls')),
]