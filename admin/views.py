# Create your views here.
#-*- coding: utf-8 -*-
from django.http import HttpResponse
from django.template.loader import get_template
from django.template.context import Context
from shop.models import Items, Categories
import os

def main(request):
	adminMainTemplate = get_template('admin_main.html')
	if request.session.has_key('username'):
		return HttpResponse(adminMainTemplate.render(Context(
		{	
			"menu1":"My cart", "address1":"/membership/myCart/",
			"menu2":"Sign out:"+(request.session['username']), 
			"address2":"/membership/signout/",
		})))
	else:
		return HttpResponse("<script>window.alert('Login please');document.location.replace('/membership/signin/');</script>")


def add(request):
	adminAddTemplate = get_template('admin_add.html')

	if request.session.has_key('username'):
		if request.GET.has_key('filename'):
			return HttpResponse(adminAddTemplate.render(Context(
			{	
				"menu1":"My cart", "address1":"/membership/myCart/",
				"menu2":"Sign out:"+(request.session['username']), 
				"address2":"/membership/signout/",
				"categories":Categories.objects.all(),
				"image":"yes",
				"imagePath":str(request.GET['filename']),
			})))
		else:
			return HttpResponse(adminAddTemplate.render(Context(
			{	
				"menu1":"My cart", "address1":"/membership/myCart/",
				"menu2":"Sign out:"+(request.session['username']), 
				"address2":"/membership/signout/",
				"categories":Categories.objects.all(),
			})))
	else:
		return HttpResponse("<script>window.alert('Login please');document.location.replace('/membership/signin/');</script>")


def do_add(request):
	if request.POST['item_type'] == "" or request.POST['item_name'] == "" or request.POST['item_desc'] == "" or request.POST['item_price'] == "" or request.POST['item_size'] == "":
		return HttpResponse("<script>window.alert('Fill all boxes please.');history.back();</script>")
	else:
		newItem = Items(**
		{
			'cat_no_id':request.POST['item_type'], 
			'item_name':request.POST['item_name'], 
			'item_desc':request.POST['item_desc'], 
			'item_price':request.POST['item_price'], 
			'item_size':request.POST['item_size'], 
			'item_img':request.POST['filename']
		})
		newItem.save()

		return HttpResponse("<script>window.alert('Item type: "+request.POST['item_type']+"\\nItem name: "+request.POST['item_name'].replace('\'', '\\\'')+"\\nItem price: "+request.POST['item_price']+"\\nDescription: "+request.POST['item_desc'].replace('\'', '\\\'')+"\\nItem Size: "+request.POST['item_size']+"\\nImage file: "+request.POST['filename']+"');document.location.replace('/shop/?category="+request.POST['item_type']+"');</script>")
		

def delete(request):
	Items.objects.filter(id=request.GET['item_id']).delete()
	return HttpResponse("<script>window.alert('Deleted');document.location.replace('/admin/view/');</script>")


def edit(request):
	if request.POST['item_type'] == '' or request.POST['item_name'] == '' or request.POST['item_desc'] == '' or request.POST['item_price'] == '' or request.POST['item_size'] == '':
		return HttpResponse("<script>window.alert('No blank box allowed. Please try again.');history.back();</script>")
	else:
		Items.objects.filter(id=request.POST['item_id']).update(**
		{
			'cat_no':request.POST['item_type'], 
			'item_name':request.POST['item_name'], 
			'item_desc':request.POST['item_desc'], 
			'item_price':request.POST['item_price'], 
			'item_size':request.POST['item_size']
		})

		return HttpResponse("<script>window.alert('Edited');document.location.replace('/admin/view/');</script>")


def view(request):
	adminViewTemplate = get_template('admin_view.html')
	if request.session.has_key('username'):
		allItem = Items.objects.all().order_by('id')

		return HttpResponse(adminViewTemplate.render(Context(
		{
			"menu1":"My cart", "address1":"/membership/myCart/", 
			"menu2":"Sign out:"+(request.session['username'].capitalize()), 
			"allItem":allItem, 
			"categories":Categories.objects.all(),
		})))
	else:
		return HttpResponse("<script>window.alert('Login please');document.location.replace('/membership/signin/');</script>")


def adminCategories(request):
	adminCategoriesTemplate = get_template('admin_categories.html')

	if request.session.has_key('username'):
		return HttpResponse(adminCategoriesTemplate.render(Context(
		{	
			"menu1":"My cart", "address1":"/membership/myCart/",
			"menu2":"Sign out:"+(request.session['username']), 
			"address2":"/membership/signout/",
			"categories":Categories.objects.all(),
		})))
	else:
		return HttpResponse("<script>window.alert('Login please');document.location.replace('/membership/signin/');</script>")


def do_editCategories(request):
	requestedCatID = Categories.objects.get(id=request.POST['cat_id'])
	return HttpResponse("<script>window.alert('Requested category, "+str(requestedCatID.id)+" has been successfully edited to "+request.POST['cat_desc'].lower().capitalize()+" edited');document.location.replace('/admin/categories/');</script>")


def do_addCategories(request):
	addCategory = Categories(cat_desc=request.POST['cat_desc'].lower().capitalize())
	addCategory.save()

	return HttpResponse("<script>window.alert('New category, "+request.POST['cat_desc'].lower().capitalize()+" added');document.location.replace('/admin/categories/');</script>")


def delete_category(request):
	if request.session.has_key('username'):
		Categories.objects.filter(id=request.GET['cat_id']).delete()
		return HttpResponse("<script>window.alert('Category, "+str(request.GET['desc'])+" deleted');document.location.replace('/admin/categories/');</script>")
	else:
		return HttpResponse("<script>window.alert('Login please');document.location.replace('/membership/signin/');</script>")
	
	
def upload(request):
	if request.method == 'POST':
		if 'file' in request.FILES:
			file = request.FILES['file']
			filename = file._name
			destination = '/app/pymall/static'
			#destination = '/home/jswlinux/pymall/static'

			fp = open('%s/_%s' % (destination, filename), 'wb')
			for chunk in file.chunks():
				fp.write(chunk)

			fp.close()
			try:
				os.system('convert -resize 202x250! '+destination+'/_'+str(filename)+' '+destination+'/'+str(filename)+' && rm -f '+destination+'/_'+str(filename))
			except:
				return HttpResponse("<script>window.alert('This is not an image file. Please try again.');document.location.replace('/admin/add/');</script>")
			else:
				return HttpResponse("<script>window.alert('Image file uploaded');document.location.replace('/admin/add/?filename="+str(filename)+"');</script>")
		else:
			return HttpResponse("<script>window.alert('Please choose an image file');history.back();</script>")


