from django.conf.urls.defaults import patterns, url
from pymall.membership.views import *

urlpatterns = patterns('',
	url('^mypage/$', mypage),
	url('^signup/$', signup),
	url('^register/$', register),
	url('^signin/$', signin),
	url('^signout/$', signout),
	url('^login/$', login),
	url('^addCart/$', addCart),
	url('^myCart/$', myCart),
	url('^resetCart/$', resetCart),
	url('^qty/$', editQty),
	url('^deleteItem/$', deleteItem),
	url('^resetPassword/$', resetPassword),
	url('^do_ResetPassword/$', do_ResetPassword),
	url('^editInfo/$', editInfo),
)
