from django.conf.urls.defaults import patterns, url

urlpatterns = patterns("",
    url(r"^confirmation/(?P<operation>(email|signup))/(?P<key>\w+)/$", 
        'better.emails.views.confirmation', 
        name="confirmation"),
)
