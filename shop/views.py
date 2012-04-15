#-*- coding: utf-8 -*-
from django.http import HttpResponse
from django.template.loader import get_template
from django.template.context import Context

def shop(request):
	shopTemplate = get_template('shop.html')
	if request.session.has_key('username'):
		menu1 = "My cart"
		address1 = "# onClick=nextweek();"
		menu2 = "Sign out:"+(request.session['username'].capitalize())
		address2 = "/membership/signout/"
	else:
	 	menu1 = "Sign in"
	 	address1 = "/membership/signin/"
		menu2 = "Sign up"
		address2 = "/membership/signup/"


	return HttpResponse(shopTemplate.render(Context({
		"menu1":menu1, "address1":address1, "menu2":menu2, "address2":address2
		})))
