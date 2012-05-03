from django.db import models

# Create your models here.
class Categories(models.Model):
	cat_desc = models.CharField(max_length=200)


class Items(models.Model):
	cat_no = models.ForeignKey(Categories)
	item_name = models.CharField(max_length=50)
	item_desc = models.CharField(max_length=200)
	item_size = models.CharField(max_length=5)
	item_price = models.DecimalField(max_digits=5, decimal_places=2)
	item_img = models.CharField(max_length=50)

	
class Orders(models.Model):
	item_no = models.ForeignKey(Items)
	membership_id = models.IntegerField()
	qty = models.IntegerField()
	order_date = models.DateTimeField('Ordered Date')

