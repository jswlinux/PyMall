from django.conf.urls.defaults import patterns, include, url
from pymall.views import main, about, blog, contactus
from pymall.shop.views import shop
from pymall.membership.views import membership

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^pymall/', include('pymall.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'pymall.views.main', name='main'),
    url('^about/$', about),
    url('^blog/$', blog),
    url('^shop/$', shop),
    url('^contactus/$', contactus),
    url('^membership/', include('membership.urls')),
)
