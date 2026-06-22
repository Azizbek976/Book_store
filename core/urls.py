from django.conf.urls.i18n import urlpatterns
from django.contrib import admin
from django.urls import path
from django.urls import include


from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from django.conf.urls.static import static
from django.conf import settings


from rest_framework_simplejwt.views import TokenObtainPairView , TokenRefreshView

from main.views import *

schema_view = get_schema_view(
   openapi.Info(
      title="Book store",
      default_version='v1',
      description="Test holatida",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="Litsenziyam yoq"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('user/register/' , RegisterCreateAPIView.as_view()) ,
    path('user/update/' , UserRetrieveUpdateDestroyAPIView.as_view()) ,
    path('book/' , BookListCreateAPIView.as_view()) ,
    path('book/<int:pk>/' , BookRetrieveUpdateDestroyAPIView.as_view()) ,

]




urlpatterns += [
    path('admin/', admin.site.urls),
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),

    path("auth/", include("rest_framework.urls")) ,

    path('token/', TokenObtainPairView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view()),

]

urlpatterns += static(settings.MEDIA_URL , document_root=settings.MEDIA_ROOT)











