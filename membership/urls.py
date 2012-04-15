from django.conf.urls.defaults import patterns, include, url
from pymall.membership.views import signup, register, mypage, signin, signout, cart, login

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	url('^mypage/$', mypage),
	url('^signup/$', signup),
	url('^register/$', register),
	url('^signin/$', signin),
	url('^signout/$', signout),
	url('^cart/$', cart),
	url('^login/$', login),
)
