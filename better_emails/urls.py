from django.conf.urls.defaults import patterns, url
from . import views
urlpatterns = patterns("",
    url(r"^confirmation/(?P<operation>(email|signup))/(?P<key>\w+)/$", 
        views.confirmation, name="confirmation"),
)
