from django.conf.urls.defaults import patterns, url
from pymall.admin.views import *

urlpatterns = patterns('',
	url('^$', main),
	url('^add/$', add),
	url('^do_add/$', do_add),
	url('^delete/$', delete),
	url('^edit/$', edit),
	url('^view/$', view),
	url('^categories/$', adminCategories),
	url('^do_addCategories/$', do_addCategories),
	url('^do_editCategories/$', do_editCategories),
	url('^delete_category/$', delete_category),
	url('^upload', upload),
)
