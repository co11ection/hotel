from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework.routers import SimpleRouter
from booking import urls
from rooms.views import RoomViewSet
from category.views import CategoryViewSet
from django.conf.urls.static import static
from django.conf import settings

router = SimpleRouter()
router.register('rooms', RoomViewSet)
router.register('categories', CategoryViewSet)

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
   openapi.Info(
      title="Hotel Tima",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)



urlpatterns = [
   re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
   path('api/v1/docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
   re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
   path('admin/', admin.site.urls),
   path('api/v1/', include(router.urls)),
   path('api/v1/booking/', include('booking.urls')),
   path('api/v1/account/', include('account.urls')),
#    path('api/v1/booking/', include('booking.urls')),
   path('api/v1/', include('rooms.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)