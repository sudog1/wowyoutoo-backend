from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("admin/", admin.site.urls),
    path("english/", include("english.urls")),
    path("payments/", include("payments.urls")),
    path("service/", include("service.urls")),
    path("accounts/", include("accounts.urls")),
    path("accounts/", include("allauth.urls")),
    path("accounts/", include("dj_rest_auth.urls")),
    # path("emails/", include("allauth.urls")),
]
