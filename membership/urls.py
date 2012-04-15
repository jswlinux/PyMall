from django.conf.urls.defaults import patterns, url
from pymall.membership.views import *

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
	url('^addCart/$', addCart),
	url('^myCart/$', myCart),
	url('^resetCart/$', resetCart),
	url('^qty/$', editQty),
	url('^deleteItem/$', deleteItem),
)
