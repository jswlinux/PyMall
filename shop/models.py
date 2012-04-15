from django.db import models
import datetime

# Create your models here.
class categories(models.Model):
#	cat_no = models.IntegerField()
	cat_desc = models.CharField(max_length=200)


class items(models.Model):
#	item_no = models.IntegerField()
	cat_no = models.ForeignKey(categories)
	item_name = models.CharField(max_length=50)
	item_desc = models.CharField(max_length=200)
	item_size = models.CharField(max_length=3)
	item_price = models.DecimalField(max_digits=5, decimal_places=2)
	item_img = models.CharField(max_length=50)

	
class orders(models.Model):
#	order_no = models.IntegerField()
	item_no = models.ForeignKey(items)
	membership_id = models.IntegerField()
	qty = models.IntegerField()
	order_date = models.DateTimeField('Ordered Date')

