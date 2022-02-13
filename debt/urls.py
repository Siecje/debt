from django.contrib import admin
from django.urls import include, path
from rest_framework_swagger.views import get_swagger_view


schema_view = get_swagger_view(title='Debt API')

urlpatterns = [
    path('api/v1.0/', include('api.urls')),
    # path('docs/', rest_framework_swagger.urls),
    path('docs/', schema_view),
    path('admin/', admin.site.urls),
]
