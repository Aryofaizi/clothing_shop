"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import TemplateView
app_name = "config"

urlpatterns = [
    path('admin/', admin.site.urls),
    #third-party 
    path('accounts/', include('allauth.urls')),
    path("__debug__/", include("debug_toolbar.urls")),
    path("rosetta/", include("rosetta.urls")),
    path("ckeditor5/", include('django_ckeditor_5.urls'), name="ck_editor_5_upload_file"),
    #local
    path("", include("store.urls")),
    path("cart/", include("cart.urls")),
    path("order/", include("orders.urls")),
    path("payment/", include("payment.urls")),
    path('404/', TemplateView.as_view(template_name='404.html'), name='404'),
    path("sitemap/", TemplateView.as_view(template_name="sitemap.xml"), name="sitemap"),
    path("pages/", include("pages.urls")),
    #media urls
] + static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)
