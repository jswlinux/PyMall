from django.db import models

class Blog(models.Model):
	title = models.CharField(max_length=100)
	entry = models.TextField()
	date = models.CharField(max_length=10)
	user_no = models.IntegerField()

class Reply(models.Model):
	comment = models.TextField()
	user_no = models.IntegerField()
	date = models.CharField(max_length=10)
	entry_no = models.ForeignKey(Blog)
