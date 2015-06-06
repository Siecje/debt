from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^api/v1.0/', include('api.urls')),
    url(r'^docs/', include('rest_framework_swagger.urls')),
    url(r'^admin/', include(admin.site.urls)),
]
