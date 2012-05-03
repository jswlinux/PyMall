#-*- coding: utf-8 -*-
from django.http import HttpResponse
from django.template.loader import get_template
from django.template.context import Context
from membership.models import Membership, Cart
from shop.models import Items

def isNumber(string):
	try:
		int(string)
		return True
	except ValueError:
		return False

def register(request):
	if request.POST.has_key('user_no'):
		Membership.objects.filter(id=request.POST['user_no']).update(**
		{
			'firstname':request.POST['firstname'], 
			'lastname':request.POST['lastname'], 
			'ph':request.POST['ph'], 
			'street1':request.POST['street1'],
			'street2':request.POST['street2'], 
			'city':request.POST['city'], 
			'state':request.POST['state'].upper(), 
			'zipcode':request.POST['zipcode']
		})
		return HttpResponse("<script>window.alert('Edited!');document.location.replace('/membership/myCart/');</script>")
	else:
		# Avoid registering with a duplicated username
		try:
			Membership.objects.get(username=request.POST['username'])
		except:
			if isNumber(request.POST['zip']) == False:
				return HttpResponse("<script>window.alert('Zip code must be numbers. Please try again');window.history.go(-1);</script>")
			elif isNumber(request.POST['ph']) == False:
				return HttpResponse("<script>window.alert('Phone number must be numbers. Please try again');window.history.go(-1);</script>")
			else:
				if request.POST.has_key('admin') == 'yes':
					admin = 'y'
				else:
					admin = 'n'

				signup = Membership(**
				{
					'username':request.POST['username'], 
					'password':request.POST['password'],
					'firstname':request.POST['firstname'], 
					'lastname':request.POST['lastname'],
					'ph':request.POST['ph'], 
					'street1':request.POST['street1'], 
					'street2':request.POST['street2'], 
					'city':request.POST['city'], 
					'state':request.POST['state'].upper(), 
					'zipcode':request.POST['zip'], 
					'admin':admin
				})
				signup.save()

				login = Membership.objects.get(username=request.POST['username'])
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
		login = Membership.objects.get(username=request.POST['username'])
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
		login = Membership.objects.get(username=request.session['username'])
	except:
		return HttpResponse("<script>window.alert('Login Please');document.location.replace('/membership/signin/');</script>")
	else:
		address = login.street1+" "+login.street2+" "+login.city+" "+login.state+" "+login.zipcode
		itemsInCart = Cart.objects.filter(membership_id=request.session['user_no'])
		allItem = Items.objects.all()

		if itemsInCart.count() == 0:
			reset = 'empty'
		else:
			reset = 'notempty'

		return HttpResponse(cartTemplate.render(Context(
		{
			"user_no":request.session['user_no'], 
			"username":login.username, 
			"firstname":login.firstname, 
			"lastname":login.lastname, 
			"ph":login.ph[:3]+'-'+login.ph[3:6]+'-'+login.ph[6:], 
			"address":address, 
			"menu1":"My cart", 
			"address1":"/membership/myCart/", 
			"menu2":"Sign out:"+(request.session['username'].capitalize()), 
			"address2":"/membership/signout/", 
			"itemsInCart":itemsInCart, "allItem":allItem, 
			"reset":reset,
		})))
		

def addCart(request):
	try:
		login = Membership.objects.get(username=request.session['username'])
	except:
		return HttpResponse("<script>window.alert('Login first');document.location.replace('/membership/signin/');</script>")
	else:
		if  request.session.has_key('username'):
			try:
				addToCart = Cart.objects.filter(membership_id=login.id)
			except:	
				addToCart = Cart(** 
				{
					'item_id':int(request.GET['item_no']), 'item_qty':1, 
					'membership_id_id':login.id
				})
				addToCart.save()
			else:
				itemAlreadyInCart = False
				for itemsInCart in addToCart:
					if  itemsInCart.item_id == int(request.GET['item_no']) and itemsInCart.membership_id_id == login.id:
						itemAlreadyInCart = True
						qty = itemsInCart.item_qty+1
						break

				if itemAlreadyInCart == True:
					Cart.objects.filter(** 
					{
						'item_id':request.GET['item_no'], 
						'membership_id':login.id
					}).update(item_qty=qty)
				else:
					addToCart = Cart(**
					{
						'item_id':int(request.GET['item_no']), 
						'item_qty':1,
						'membership_id_id':login.id
					})
					addToCart.save()

			return HttpResponse("<script>document.location.replace('/membership/myCart')</script>")
		else:
			return HttpResponse(u"<script>window.alert('Please sign in');document.location.replace('/membership/signin/')</script>")


def resetCart(request):
	cartTemplate = get_template('mypage.html')
	Cart.objects.filter(membership_id=request.session['user_no']).delete()

	return HttpResponse(cartTemplate.render(Context(
	{
		"reset":"empty","menu1":"My cart", "address1":"/membership/myCart/", "menu2":"Sign out",
		"address2":"/membership/signout/",
	})))


def editQty(request):
	if request.POST['qty'] == '0':
		Cart.objects.filter(**
		{
			'item_id':request.POST['item_no'], 
			'membership_id':request.session['user_no']
		}).delete()
	else:
		Cart.objects.filter(**
		{
			'item_id':request.POST['item_no'], 
			'membership_id':request.session['user_no']
		}).update(item_qty=request.POST['qty'])

	return HttpResponse("<script>document.location.replace('/membership/myCart')</script>")


def deleteItem(request):
	Cart.objects.filter(**
	{
		'item_id':request.GET['item_no'], 
		'membership_id':request.session['user_no']
	}).delete()
	return HttpResponse("<script>document.location.replace('/membership/myCart')</script>")


def resetPassword(request):
	resetPasswordTemplate = get_template('resetPassword.html')
	if request.session.has_key('username'):
		return HttpResponse(resetPasswordTemplate.render(Context(
		{	
			"menu1":"My cart", "address1":"/membership/myCart/",
			"menu2":"Sign out", "address2":"/membership/signout/",
		})))
	else:
		return HttpResponse(resetPasswordTemplate.render(Context(
		{
			"menu1":"Sign in", "address1":"/membership/signin/", 
			"menu2":"Sign up", "address2":"/membership/signup/"
		})))


def do_ResetPassword(request):
	if request.POST['newpassword1'] != request.POST['newpassword2']:
		return HttpResponse("<script>window.alert('Password is different.');history.back();</script>")
	else:
		try:
			resetUser = Membership.objects.get(**
			{
				'username':request.POST['username'], 
				'firstname':request.POST['firstname'],
				'lastname':request.POST['lastname']
			})
		except:
			return HttpResponse("<script>window.alert('No exist user\\nUsername: "+request.POST['username']+"\\nFirst name: "+request.POST['firstname']+"\\nLast name: '"+request.POST['lastname']+");history.back();</script>")
		else:
			Membership.objects.filter(id=resetUser.id).update(password=request.POST['newpassword2'])
			if request.POST['alreadyLogin'] == 'yes':
				return HttpResponse("<script>window.alert('Password reset!');document.location.replace('/membership/myCart/');</script>")
			else:
				return HttpResponse("<script>window.alert('Password reset!');document.location.replace('/membership/signin/');</script>")


def editInfo(request):
	if request.POST['requested'] == 'editInfo':
		editInfoTemplate = get_template('editInfo.html')
		if request.session.has_key('username'):
			return HttpResponse(editInfoTemplate.render(Context(
			{	
				"menu1":"My cart", "address1":"/membership/myCart/",
				"menu2":"Sign out", "address2":"/membership/signout/",
				"userInfo":Membership.objects.get(id=request.session['user_no'])
			})))
		else:
			return HttpResponse("<script>window.alert('Login please');document.location.replace('/membership/signin/');</script>")
	else:
		resetPasswordTemplate = get_template('resetPassword.html')
		userInfo = Membership.objects.get(id=request.session['user_no'])
		return HttpResponse(resetPasswordTemplate.render(Context(
			{	
				"menu1":"My cart", "address1":"/membership/myCart/",
				"menu2":"Sign out", "address2":"/membership/signout/",
				"has_userinfo":"yes",
				"username":userInfo.username,
				"firstname":userInfo.firstname,
				"lastname":userInfo.lastname,
			})))
