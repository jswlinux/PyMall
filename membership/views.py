#-*- coding: utf-8 -*-
from django.http import HttpResponse
from django.template.loader import get_template
from django.template.context import Context
from membership.models import membership

def register(request):
	username = request.POST['username']
	password = request.POST['password']

	firstname = request.POST['firstname']
	lastname = request.POST['lastname']
	ph = request.POST['ph']
	street1 = request.POST['street1']
	street2 = request.POST['street2']
	city = request.POST['city']
	state = request.POST['state']
	zipcode = request.POST['zip']
	signup = request.POST['signup']

	# Avoid registering with a duplicated username
	try:
		login = membership.objects.get(username=username)
	except:
		signup = membership(username = username, password = password, firstname = firstname, lastname = lastname, ph = ph, street1 = street1, street2 = street2, city = city, state = state, zipcode = zipcode)
		signup.save()

		login = membership.objects.get(username=username)
		request.session['username'] = request.POST['username']
		request.session['user_no'] = login.id
		request.session.get_expire_at_browser_close()

		return HttpResponse("<script>window.alert('Thank you for visiting PyMall!\\nEnjoy your shopping!');document.location.replace('/');</script>")
	else:
		return HttpResponse("<script>window.alert('This username has already been taken.\\nPlease choose another username.');history.back();</script>")
		

def signup(request):
	signupTemplate = get_template('signup.html')
	return HttpResponse(signupTemplate.render(Context({})))


def signin(request):
	signinTemplate = get_template('signin.html')
	if request.session.has_key('user'):
		return HttpResponse(signinTemplate.render(Context(
		{	
			"menu1":"My cart", "address1":"# onClick=nextweek();",
			"menu2":"Sign out", "address2":"/membership/signout/",
		})))
	else:
		return HttpResponse(signinTemplate.render(Context(
		{
			"menu1":"Sign in", "address1":"# onClick=nextweek();", 
			"menu2":"Sign up", "address2":"/membership/signup/"
		})))


def signout(request):
	if not request.session.has_key('username'):
		return HttpResponse("<script>window.alert('You have not been logged in');document.location.replace('/membership/signin');</script>")
	else:
		del request.session['username']
		del request.session['user_no']
		return HttpResponse("<script>window.alert('Thank you! Come again!');document.location.replace('/');</script>")


def login(request):
	request.session['username'] = request.POST['username']
	request.session['password'] = request.POST['password']

	try:
		login = membership.objects.get(username=request.POST['username'])
	except:
		del request.session['username']
		return HttpResponse("<script>window.alert('Username, "+request.POST['username']+" does not exist. Please try again');history.back();</script>")
	else:
		if login.username == request.POST['username'] and login.password == request.POST['password']:
			request.session['username'] = request.POST['username']
			request.session['user_no'] = login.id
			request.session.get_expire_at_browser_close()
			return HttpResponse("<script>window.alert('Welcome back, "+login.firstname+" "+login.lastname+"!');document.location.replace('/');</script>")
		else:
			return HttpResponse("<script>window.alert('Wrong password');history.back();</script>")

	
def mypage(request):
	return HttpResponse("My Page")


def cart(request):
	cartTemplate = get_template('mypage.html')
	login = membership.objects.get(username=request.session['username'])
	address = login.street1+" "+login.street2+" "+login.city+" "+login.state+" "+login.zipcode

	if request.session.has_key('username'):
		return HttpResponse(cartTemplate.render(Context({"user_no":request.session['user_no'], "username":login.username, "firstname":login.firstname, "lastname":login.lastname, "ph":login.ph, "address":address, "menu1":"My cart", "address1":"/membership/cart/", "menu2":"Sign out:"+(request.session['username'].capitalize()), "address2":"/membership/signout/",
})))
#return HttpResponse(u"Login ID: " + str(request.session['user_no']))# + u", Item#: " + str(request.GET['item_no']))
	else:
		return HttpResponse(u"<script>window.alert('Please sign in');document.location.replace('/membership/signin/')</script>")

