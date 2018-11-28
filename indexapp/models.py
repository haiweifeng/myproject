# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

class MyUser(models.Model):
    username = models.CharField(max_length=20)
    emal = models.CharField(max_length=20)
    password = models.CharField(max_length=100)
    code = models.CharField(max_length=100)
    active = models.BooleanField(default=False)
    regtime = models.DateTimeField(auto_now=True)
    modifytime = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 't_user'

class Address(models.Model):
    name = models.CharField(max_length=20)
    address = models.CharField(max_length=20)
    zipcode = models.CharField(max_length=20)
    phone = models.CharField(max_length=20)
    cellphone = models.CharField(max_length=20)
    addtime = models.DateTimeField(auto_now=True)
    modifytime = models.DateTimeField(auto_now_add=True)
    user_address = models.ForeignKey(MyUser, db_column='user_address',on_delete=models.CASCADE)

    class Meta:
        db_table = 't_address'


class Bookclass(models.Model):
    classname = models.CharField(max_length=20)
    createtime = models.DateTimeField(auto_now=True)
    modifytime = models.DateTimeField(auto_now_add=True)
    parent_id = models.IntegerField(default=0)

    class Meta:
        db_table = 't_bookclass'

class Book(models.Model):
    image = models.FileField(upload_to="bookhead")    #
    title = models.CharField(max_length=50)            #
    writer = models.CharField(max_length=50,null=True) #
    press = models.CharField(max_length=50,null=True)   #
    pubtime = models.DateField(null=True)               #
    edition = models.IntegerField(null=True ,default='1')
    printtime = models.DateField(null=True)
    impress = models.IntegerField(null=True,default=1000)
    isbn = models.CharField(db_column='ISBN', max_length=50, null=True,default='123454321')  # Field name made lowercase.
    words = models.CharField(max_length=50, null=True)    #
    pages = models.IntegerField(null=True,default="12345") #
    format = models.CharField(max_length=20 ,null=True,default='16')
    paper = models.CharField(max_length=20 ,null=True,default="轻纸型")
    packaging = models.CharField(max_length=20, null=True,default="平装-胶订")
    addtime = models.DateTimeField(auto_now=True)     #
    version = models.CharField(max_length=1,default=1)
    class_id = models.ForeignKey(Bookclass, db_column="book_id", on_delete=models.CASCADE) #
    class Meta:
        db_table = 't_book'





class Booklist(models.Model):
    book_infor = models.ForeignKey(Book,db_column='book_infor', on_delete=models.CASCADE)
    price = models.FloatField()
    dangprice = models.FloatField()
    sellnumber = models.IntegerField(default=999)
    inventory = models.IntegerField()
    version = models.CharField(max_length=1,default=1)
    editsupport = models.IntegerField(null=True)
    class Meta:
        db_table = 't_booklist'


class Order(models.Model):
    name = models.CharField(max_length=20)
    totalprice = models.FloatField(blank=True, null=True)
    address = models.CharField(max_length=20)
    cellphone = models.CharField(max_length=20)
    phone = models.CharField(max_length=20)
    order_user = models.ForeignKey(MyUser, db_column='order_user', on_delete=models.CASCADE)
    ordertime = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 't_order'


class Orderlist(models.Model):
    book_id = models.ForeignKey(Book,db_column="book_id",on_delete=models.CASCADE)
    order_id = models.ForeignKey(Order,db_column="order_id",on_delete=models.CASCADE)
    count = models.IntegerField()
    price = models.FloatField()
    dangprice = models.FloatField()

    class Meta:
        db_table = 't_orderlist'




