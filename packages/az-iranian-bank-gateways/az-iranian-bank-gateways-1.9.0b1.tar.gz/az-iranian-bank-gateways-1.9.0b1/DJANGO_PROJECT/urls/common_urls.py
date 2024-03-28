# -*- coding: utf-8 -*-

"""src URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLConf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.utils.translation import gettext_lazy as _

from azbankgateways.urls import az_bank_gateways_urls
from examples.views import go_to_gateway_view, callback_gateway_view
admin.autodiscover()

admin.site.site_title = _('Admin panel')
admin.site.site_header = _('Admin panel')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('bankgateways/', az_bank_gateways_urls()),
    path('go-to-gateway/', go_to_gateway_view, name='go-to-gateway'),
    path('callback-gateway/', callback_gateway_view, name='callback-gateway'),
]
