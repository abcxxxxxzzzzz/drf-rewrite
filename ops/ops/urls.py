"""ops URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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

from django.urls import path, re_path, include
from rest_framework.documentation import include_docs_urls
from rest_framework.routers import DefaultRouter
from domain.router import dm_router
from domain.views import rewrites
from rest_framework_jwt.views import obtain_jwt_token


router = DefaultRouter()


router.registry.extend(dm_router.registry)


urlpatterns = [
    re_path(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    re_path(r'^docs/', include_docs_urls("开源运维平台")),
    re_path(r'^$', rewrites), # 跳转的url

    # 线上
    re_path(r'^api/v1/', include(router.urls)),
    re_path(r'^api/api-token-auth/$', obtain_jwt_token),

    # 开发
    # re_path(r'^v1/', include(router.urls)),
    # re_path(r'^api-token-auth/$', obtain_jwt_token),
]



