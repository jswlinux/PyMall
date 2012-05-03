from django.conf.urls.defaults import patterns, include, url
from pymall.views import main, about, contactus
from pymall.shop.views import shop
from pymall.membership.views import Membership
from pymall.blog.views import Blog

urlpatterns = patterns('',
    url(r'^$', 'pymall.views.main', name='main'),
    url('^about/$', about),
	url('^blog/', include('blog.urls')),
    url('^shop/$', shop),
    url('^contactus/$', contactus),
    url('^membership/', include('membership.urls')),
    url('^admin/', include('admin.urls')),
)
