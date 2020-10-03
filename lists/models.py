from django.db import models


class List(models.Model):
    pass
    # def save(self):
    #     pass
    

class Item(models.Model):
    text = models.TextField(default='')
    list = models.ForeignKey(List, default=None)
