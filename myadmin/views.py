import json

from django.core.paginator import Paginator
from django.db import transaction
from django.forms import model_to_dict
from django.http import HttpResponse
from django.shortcuts import render, redirect


# Create your views here.

from indexapp.models import Book, Booklist, Bookclass, Address,Order,Orderlist
from tools.tools import GetPostValue


def myview(request):
    return render(request,"admin/index.html")

def addbook(request):
    parentclass = Bookclass.objects.filter(parent_id=0)
    childclass  = Bookclass.objects.exclude(parent_id=0)
    return render(request,"admin/main/add.html",{"parentclass":parentclass,"childclass":childclass})

def dzlist(request):
    myadress = Address.objects.get_queryset().order_by('id').values("id","name","address",
                                      "cellphone","phone","zipcode","addtime","user_address__username")
    num = request.GET.get("num")
    if not num:
        num = 1
    page = Paginator(myadress, 2).page(num)
    allpage = Paginator(myadress, 2)
    return render(request,"admin/main/dzlist.html",{"pages":page,"allpage":allpage})

def orderlist(request):
    order = Order.objects.get_queryset().order_by('id').values("id","name","totalprice",
        "address","cellphone","phone","order_user__username","ordertime")
    num = request.GET.get("num")
    if not num:
        num = 1
    page = Paginator(order, 4).page(num)
    allpage = Paginator(order, 4)
    return render(request,"admin/main/orderlist.html",{"pages":page,"allpage":allpage})

def list(request):
    num = request.GET.get("num")
    if not num:
        num = 1
    parentclass = Bookclass.objects.filter(parent_id=0)
    childclass = Bookclass.objects.exclude(parent_id=0)
    books = Book.objects.get_queryset().order_by('id').values("id","title","image","writer","press",
                                      "booklist__price","booklist__dangprice",
                                      "booklist__inventory","booklist__sellnumber","class_id")
    page = Paginator(books, 8).page(num)
    allpage = Paginator(books, 8)


    return render(request,"admin/main/list.html",{"pages":page,"allpage":allpage,
                                                  "parentclass":parentclass,"childclass":childclass})

def splb(request):
    parent = Bookclass.objects.filter(parent_id=0)
    child = Bookclass.objects.exclude(parent_id=0)
    return render(request,"admin/main/splb.html",{"parent":parent,"child":child})

def zjsp(request):
    return render(request,"admin/main/zjsp.html")

def zjzlb(request):
    parent = Bookclass.objects.filter(parent_id=0)
    return render(request,"admin/main/zjzlb.html",{"parents":parent})

def addlog(request):
    book = GetPostValue(request,"title","inventory","writer","press","pubtime",
                        "words","pages","printtime","price","dangprice","classname")
    print("book",book)
    image = request.FILES.get("headimg")
    with transaction.atomic():

        bookclass = Bookclass.objects.get(pk=book[10])
        print("hahahahhahahahahahahha",bookclass)
        mybook = Book(title=book[0],image=image,writer=book[2],press=book[3],
                      pubtime=book[4],words=book[5],pages=book[6],printtime=book[7],class_id=bookclass)
        print("mybook",mybook)
        mybook.save()
        print("mybook", mybook)
        Booklist(book_infor=mybook,price=book[8],dangprice=book[9],inventory=book[1]).save()


    return redirect("myadmin:add")

def addparent(request):
    parentclass = request.POST.get("parentclass")
    if Bookclass.objects.filter(classname=parentclass):
        return HttpResponse("double")
    else:
        Bookclass(classname=parentclass).save()
        return HttpResponse("ok")

def addchild(request):
    childclass = request.POST.get("childclass")
    print("child",childclass)
    parentid = request.POST.get("parentid")
    print("parent", parentid)
    if parentid=='0':
        return HttpResponse("no")
    if Bookclass.objects.filter(classname=childclass):
        return HttpResponse("double")
    else:
        fatherid = Bookclass.objects.get(pk=parentid).id
        Bookclass(classname=childclass,parent_id=fatherid).save()
        return HttpResponse("ok")


def bookdel(request):
    bookid = request.POST.get("bookid")
    if Book.objects.filter(pk=bookid):
        with transaction.atomic():
            book = Book.objects.get(pk=bookid)
            book.delete()
        return HttpResponse("ok")
    return HttpResponse("no")

def bookclassdel(request):
    classid = request.POST.get("classid")
    if Bookclass.objects.filter(pk=classid):
        with transaction.atomic():
            bookclass = Bookclass.objects.get(pk=classid)
            bookclass.delete()
        return HttpResponse("ok")
    return HttpResponse("no")




























