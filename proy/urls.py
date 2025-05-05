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
from proy import views
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    #esta es la url que redirige una vez accedido al sitio "respaldosuv.mx" directamente al login
    path('', RedirectView.as_view(url='/login/', permanent=False)),
    path('login/', views.login_view),
    path('index/', views.index),
    path('alta/', views.dar_alta),
    path('logout/',views.logout_v),
    #path('actualiza/', views.get_server_choices),
    path('logs/', views.ver_logs),
    path('agregar/', views.crear_respaldo, name='agregar'),
    path('baja/', views.ver_configuraciones_respaldo, name='ver_configuraciones_respaldo'),
    path('cronlog/', views.cron_log_view, name='cron_log_view'),
    path('ajax-cron-log/', views.ajax_cron_log, name='ajax_cron_log'),
    path('captcha/', include('captcha.urls')),   
]
