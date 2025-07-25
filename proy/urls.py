"""
URL configuration for proy project.

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
from backend import views
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url='/login/', permanent=False)),
    path('index/', views.index, name='index'),
    path('logout/',views.logout_view, name='logout'),
    path('captcha/', include('captcha.urls')),
    path("login/", views.login_view, name="login"),
    path("verificar-otp/", views.otp_verification_view, name="otp_verification"),
    path('servidores/', views.servidor_listar, name='servidor_listar'),
    path('servidores/registrar/', views.servidor_crear, name='servidor_crear'),
    path('servidores/<int:pk>/eliminar/', views.servidor_eliminar, name='servidor_eliminar'),
    path('servidores/<int:servidor_pk>/detalle/', views.servidor_detalle, name='servidor_detalle'),
    path('servidores/<int:servidor_pk>/servicios/configurar/', views.servicio_configurar_crear, name='servicio_configurar_crear'),
    path('servicios/<int:servicio_pk>/accion/<str:accion>/', views.servicio_accion, name='servicio_accion'),
    path('api/dashboard-status/', views.api_dashboard_status, name='api_dashboard_status'),
]
