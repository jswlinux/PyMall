from django.conf.urls.defaults import patterns, url
from pymall.blog.views import *

urlpatterns = patterns('',
	url('^view/$', view),
	url('^write/$', write),
	url('^save/$', save),
	url('^useredit/$', useredit),
	url('^edit/$', edit),
	url('^delete/$', delete),
	url('^reply/$', addReply),
)
