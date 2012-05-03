from django.db import models

# Create your models here.
class Membership(models.Model):
	username = models.CharField(max_length=20, unique=True)
	password = models.CharField(max_length=20)
	firstname = models.CharField(max_length=20)
	lastname = models.CharField(max_length=20)
	ph = models.CharField(max_length=10)
	street1 = models.CharField(max_length=20)
	street2 = models.CharField(max_length=20)
	city = models.CharField(max_length=20)
	state = models.CharField(max_length=2)
	zipcode = models.CharField(max_length=5)
	admin = models.CharField(max_length=1)


class Cart(models.Model):
	item_id = models.IntegerField()
	item_qty = models.IntegerField()
	membership_id = models.ForeignKey(Membership)
