from django.http import HttpResponse
from django.template.loader import get_template
from django.template.context import Context
from blog.models import Blog, Reply
from membership.models import Membership
import time

def view(request):
	blogTemplate = get_template('blog.html')

	if request.session.has_key('username'):
		menu1 = "My cart"
		menu2 = "Sign out:"+(request.session['username'])
		address1 = "/membership/myCart/"
		address2 = "/membership/signout/"
		currentuser = request.session['user_no']
	else:
		menu1 = "Sign in"
		menu2 = "Sign up"
		address1 = "/membership/signin/"
		address2 = "/membership/signup/"
		currentuser = ''

	try:
		page = int(request.GET['page'])
	except:
		page = 1
	
	perPage = 5
	startPos = (int(page)-1)*perPage
	endPos = startPos+perPage

	return HttpResponse(blogTemplate.render(Context(
	{	
		"menu1":menu1, "address1":address1,
		"menu2":menu2, "address2":address2,
		"blog":Blog.objects.all().order_by('-id')[startPos:endPos],
		"reply":Reply.objects.all().order_by('-id'),
		"login":Membership.objects.all(),
		"page":page,
		"currentuser":currentuser
	})))
	
def write(request):	
	if request.session.has_key('username'):
		blogWriteTemplate = get_template('write.html')
		return HttpResponse(blogWriteTemplate.render(Context(
		{
			"menu1":"My cart", "address1":"/membership/myCart/",
			"menu2":"Sign out:"+(request.session['username']), 
			"address2":"/membership/signout/",
		})))
	else:
		return HttpResponse("<script>window.alert('Login Please');document.location.replace('/membership/signin/');</script>")

def edit(request):
	Blog.objects.filter(id=request.POST['blogid']).update(**
	{
		'title':request.POST['title'], 
		'entry':request.POST['entry']
	})
	return HttpResponse("<script>window.alert('Edited');document.location.replace('/blog/view/');</script>")

def useredit(request):
	editTemplate = get_template('blogedit.html')

	blogEntry = Blog.objects.get(id=request.POST['blogid'])
	print blogEntry.entry
	print blogEntry.title

	return HttpResponse(editTemplate.render(Context(
	{
		"menu1":"My cart", "address1":"/membership/myCart/",
		"menu2":"Sign out:"+(request.session['username']), 
		"address2":"/membership/signout/",
		"blogentry":blogEntry.entry,
		"blogtitle":blogEntry.title,
		"blogid":request.POST['blogid']
	})))

def delete(request):
	Blog.objects.filter(id=request.POST['blogid']).delete()
	return HttpResponse("<script>window.alert('Deleted');document.location.replace('/blog/view/');</script>")

def save(request):
	if len(request.POST['title']) == 0 or len(request.POST['entry']) == 0:
		return HttpResponse("<script>window.alert('No empty box is allowed. Please try again');history.back();</script>")
	else:
		# Get today
		now = time.localtime()

		if now.tm_mon < 10:
			month = '0'+str(now.tm_mon)
		else:
			month = str(now.tm_mon)

		blogTime = str(now.tm_year)+'/'+month+'/'+str(now.tm_mday)

		saveBlog = Blog(**
		{
			'title':request.POST['title'], 
			'date':blogTime, 
			'entry':request.POST['entry'], 
			'user_no':request.session['user_no']
		})
		saveBlog.save()

		return HttpResponse("<script>window.alert('Posted');document.location.replace('/blog/view/');</script>")

def addReply(request):
	if request.session.has_key('username'):
		now = time.localtime()

		if now.tm_mon < 10:
			month = '0'+str(now.tm_mon)
		else:
			month = str(now.tm_mon)
		if now.tm_mday < 10:
			mday = '0'+str(now.tm_mday)
		else:
			mday = str(now.tm_mday)

		replyTime = str(now.tm_year)+'/'+month+'/'+mday

		saveReply = Reply(**
		{
			'comment':request.POST['reply'], 
			'date':replyTime, 
			'user_no':request.session['user_no'],
			'entry_no_id':request.POST['blogid']
		})
		saveReply.save()
		
		return HttpResponse("<script>window.alert('Comment added');document.location.replace('/blog/view/');</script>")
	else:
		return HttpResponse("<script>window.alert('Login Please');document.location.replace('/membership/signin/');</script>")
