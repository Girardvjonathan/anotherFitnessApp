from rest_framework import routers
from django.conf.urls import url
from fit.views import *
from rest_framework.urlpatterns import format_suffix_patterns

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
urlpatterns = [
    url(r'^test1', user_list.as_view()),
    url(r'^test/(?P<pk>[0-9]+)/$', user_detail.as_view()),
]
urlpatterns = format_suffix_patterns(urlpatterns)
