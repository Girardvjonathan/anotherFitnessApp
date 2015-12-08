from django.conf.urls import url, include
from rest_framework import routers
from fit.views import *
from rest_framework.urlpatterns import format_suffix_patterns

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
urlpatterns = [
    url(r'^test1', user_list),
    url(r'^test/(?P<pk>[0-9]+)/$', user_detail),
]
urlpatterns = format_suffix_patterns(urlpatterns)