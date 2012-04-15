#-*- coding: utf-8 -*-
from django.http import HttpResponse
from django.template.loader import get_template
from django.template.context import Context
from shop.models import items, categories

def shop(request):
	shopTemplate = get_template('shop.html')
	detailTemplate = get_template('detail.html')

	if request.session.has_key('username'):
		menu1 = "My cart"
		address1 = "/membership/myCart/"
		menu2 = "Sign out:"+(request.session['username'].capitalize())
		address2 = "/membership/signout/"
	else:
	 	menu1 = "Sign in"
	 	address1 = "/membership/signin/"
		menu2 = "Sign up"
		address2 = "/membership/signup/"

	if request.GET.has_key('item_no'):
		item = items.objects.get(id=request.GET['item_no'])
		category = categories.objects.get(id=item.cat_no_id)

		return HttpResponse(detailTemplate.render(Context(
		{
			"item_no":item.id, "item_name":item.item_name, "item_img":item.item_img, "item_desc":item.item_desc, "item_price":item.item_price, "item_size":item.item_size, "category":category.cat_desc, "menu1":menu1, "address1":address1, "menu2":menu2, "address2":address2, "currentItemNo":request.GET['item_no'],
		})))
	else:
		return HttpResponse(shopTemplate.render(Context(
		{
			"item":items.objects.all(), "menu1":menu1, "address1":address1, "menu2":menu2, "address2":address2
		})))
		