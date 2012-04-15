from django.db import models

# Create your models here.
class membership(models.Model):
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

class cart(models.Model):
	item_id = models.CharField(max_length=2)
	item_qty = models.IntegerField()
	membership_id = models.ForeignKey(membership)
