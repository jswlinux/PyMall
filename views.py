#-*- coding: utf-8 -*-
from django.http import HttpResponse
from django.template.loader import get_template
from django.template.context import Context


def main(request):
	mainTemplate = get_template('index.html')
	if request.session.has_key('username'):
		return HttpResponse(mainTemplate.render(Context(
		{	
			"menu1":"My cart", "address1":"/membership/myCart/",
			"menu2":"Sign out:"+(request.session['username']), 
			"address2":"/membership/signout/",
		})))
	else:
		return HttpResponse(mainTemplate.render(Context(
		{
			"menu1":"Sign in", "address1":"/membership/signin/", 
			"menu2":"Sign up", "address2":"/membership/signup/"
		})))

def about(request):
	aboutTemplate = get_template('about.html')
	if request.session.has_key('username'):
		return HttpResponse(aboutTemplate.render(Context(
		{	
			"menu1":"My cart", "address1":"/membership/myCart/",
			"menu2":"Sign out:"+(request.session['username']), 
			"address2":"/membership/signout/",
		})))
	else:
		return HttpResponse(aboutTemplate.render(Context(
		{
			"menu1":"Sign in", "address1":"/membership/signin/", 
			"menu2":"Sign up", "address2":"/membership/signup/"
		})))


def contactus(request):
	contactusTemplate = get_template('contact-us.html')
	if request.session.has_key('username'):
		return HttpResponse(contactusTemplate.render(Context(
		{	
			"menu1":"My cart", "address1":"/membership/myCart/",
			"menu2":"Sign out:"+(request.session['username']), 
			"address2":"/membership/signout/",
		})))
	else:
		return HttpResponse(contactusTemplate.render(Context(
		{
			"menu1":"Sign in", "address1":"/membership/signin/", 
			"menu2":"Sign up", "address2":"/membership/signup/"
		})))
