#-*- coding: utf-8 -*-
from django.http import HttpResponse
from django.template.loader import get_template
from django.template.context import Context
from membership.models import membership, cart
from shop.models import items, categories

def register(request):
	# Avoid registering with a duplicated username
	try:
		login = membership.objects.get(username=username)
	except:
		signup = membership(username = request.POST['username'], password = request.POST['password'], firstname = request.POST['firstname'], lastname = request.POST['lastname'], ph = request.POST['ph'], street1 = request.POST['street1'], street2 = request.POST['street2'], city = request.POST['city'], state = request.POST['state'], zipcode = request.POST['zip'])
		signup.save()

		login = membership.objects.get(username=request.POST['username'])
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
	if request.session.has_key('username'):
		return HttpResponse(signinTemplate.render(Context(
		{	
			"menu1":"My cart", "address1":"/membership/myCart/",
			"menu2":"Sign out", "address2":"/membership/signout/",
		})))
	else:
		return HttpResponse(signinTemplate.render(Context(
		{
			"menu1":"Sign in", "address1":"/membership/signin/", 
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


def myCart(request):
	cartTemplate = get_template('mypage.html')

	try:
		login = membership.objects.get(username=request.session['username'])
	except:
		return HttpResponse("<script>window.alert('Login Please');document.location.replace('/membership/signin/');</script>")
	else:
		address = login.street1+" "+login.street2+" "+login.city+" "+login.state+" "+login.zipcode
		itemsInCart = cart.objects.filter(membership_id=request.session['user_no'])
		allItem = items.objects.all()

		if itemsInCart.count() == 0:
			reset = 'empty'
		else:
			reset = 'notempty'

		return HttpResponse(cartTemplate.render(Context({"user_no":request.session['user_no'], "username":login.username, "firstname":login.firstname, "lastname":login.lastname, "ph":login.ph[:3]+'-'+login.ph[3:6]+'-'+login.ph[6:], "address":address, "menu1":"My cart", "address1":"/membership/myCart/", "menu2":"Sign out:"+(request.session['username'].capitalize()), "address2":"/membership/signout/", "itemsInCart":itemsInCart, "allItem":allItem, "reset":reset,
			})))
		

def addCart(request):
	cartTemplate = get_template('mypage.html')

	try:
		login = membership.objects.get(username=request.session['username'])
	except:
		return HttpResponse("<script>window.alert('Login first');document.location.replace('/membership/signin/');</script>")
	else:
		if  request.session.has_key('username'):
			address = login.street1+" "+login.street2+" "+login.city+" "+login.state+" "+login.zipcode
			
			try:
				addToCart = cart.objects.get(item_id=request.GET['item_no'])
			except:	
				addToCart = cart(item_id = request.GET['item_no'], item_qty = 1, membership_id_id = login.id)
			else:
				if  addToCart.item_id == int(request.GET['item_no']):
					addToCart.item_qty += 1
				else:
					addToCart = cart(item_id = request.GET['item_no'], item_qty = 1, membership_id_id = login.id)

			addToCart.save()


			return HttpResponse("<script>document.location.replace('/membership/myCart')</script>")
			#return HttpResponse(cartTemplate.render(Context({"user_no":request.session['user_no'], "username":login.username, "firstname":login.firstname, "lastname":login.lastname, "ph":login.ph, "address":address, "menu1":"My cart", "address1":"/membership/myCart/", "menu2":"Sign out:"+(request.session['username'].capitalize()), "address2":"/membership/signout/", "currentItemNo":cart.objects.all(),#"item_id":inCart.item_id, "item_qty":inCart.item_qty,
			#})))
		else:
			return HttpResponse(u"<script>window.alert('Please sign in');document.location.replace('/membership/signin/')</script>")


def resetCart(request):
	cartTemplate = get_template('mypage.html')
	resetAllItems = cart.objects.filter(membership_id = request.session['user_no']).delete()

	return HttpResponse(cartTemplate.render(Context({"reset":"empty","menu1":"My cart", "address1":"/membership/myCart/", "menu2":"Sign out", "address2":"/membership/signout/",})))


def editQty(request):
	if request.POST['qty'] == '0':
		cart.objects.filter(item_id=request.POST['item_no'], membership_id=request.session['user_no']).delete()
	else:
		cart.objects.filter(item_id=request.POST['item_no'], membership_id=request.session['user_no']).update(item_qty=request.POST['qty'])

	return HttpResponse("<script>document.location.replace('/membership/myCart')</script>")


def deleteItem(request):
	cart.objects.filter(item_id=request.GET['item_no'], membership_id=request.session['user_no']).delete()
	return HttpResponse("<script>document.location.replace('/membership/myCart')</script>")

