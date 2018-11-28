from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
import re
# Create your views here.
from indexapp.models import Book, Bookclass, Booklist
from indexapp.models import MyUser,Address,Order,Orderlist
from django.db import transaction
# 主页面
from tools.tools import GetPostValue, Cart
def index_view(request):
    """
    主页面显示
    :param request:
    :return:
    """
    remember =request.COOKIES.get("username")
    if remember:
        usercook = str(remember.encode("latin-1"), "utf-8")
        logstatus=1
    else:
        usercook =""
        if request.session.get("username"):
            logstatus = 1
        else:
            logstatus = 0

    if request.session.get("id"):
        del request.session["id"]
        del request.session["parentid"]
    totalclass = Bookclass.objects.filter(parent_id=0).values()
    childclass = Bookclass.objects.all().exclude(parent_id=0).values()
    newbook = Book.objects.all().order_by("-addtime").values("id",
                                                              "image","title","writer","booklist__price",
                                                              "booklist__dangprice")[:8]
    editsupportbook = Booklist.objects.all().order_by("-editsupport").values("book_infor__id",
                                                                              "price","dangprice","book_infor__image",
                                                                              "book_infor__writer","book_infor__title")[:8]
    newsellbook = Book.objects.all().order_by("-booklist__sellnumber","-addtime").values("id",
                                                                                            "image","title","writer","booklist__price",
                                                                                            "booklist__dangprice")[:8]
    newsupportbook = Booklist.objects.all().order_by("-editsupport","-book_infor__addtime").values("book_infor__id",
                                                                                                      "price","dangprice","book_infor__image",
                                                                                                      "book_infor__writer","book_infor__title")[:10]
    return render(request,"indexapp/index.html",
                  {"total":totalclass,"child":childclass,
                   "newbook":newbook,"editsupportbook":editsupportbook,
                   "newsellbook":newsellbook,"newsupportbook":newsupportbook,
                   "logstatus":logstatus,"usercook":usercook})
# 图示详细信息页面
def book_view(request):
    """
    书籍详情页面展示
    :param request:
    :return:
    """
    if request.COOKIES.get("username"):
        usercook = str(request.COOKIES.get("username").encode("latin-1"), "utf-8")
        logstatus=1
    else:
        usercook = ""
        if request.session.get("username"):
            logstatus = 1
        else:
            logstatus = 0
    if request.session.get("id"):
        del request.session["id"]
        del request.session["parentid"]
    bookid = request.GET.get("id")
    book = Book.objects.filter(pk=bookid)
    bookchildclass = Bookclass.objects.filter(id=book.values()[0].get("class_id_id"))
    bookparentclass = Bookclass.objects.filter(pk=bookchildclass.values()[0].get("parent_id"))
    booklist = Booklist.objects.filter(book_infor=bookid)

    return render(request,
                  "indexapp/Book details.html",{"book":book.values()[0],"bookchildclass":bookchildclass.values()[0],
                  "booklist":booklist.values()[0],"bookparentclass":bookparentclass.values()[0],
                  "logstatus":logstatus,"usercook":usercook,})
# 图书分类展示页面
def booklistview(request):
    """
    书籍分类展示
    :param request:
    :return:
    """
    if request.COOKIES.get("username"):
        usercook = str(request.COOKIES.get("username").encode("latin-1"), "utf-8")
        logstatus=1
    else:
        usercook = ""
        if request.session.get("username"):
            logstatus = 1
        else:
            logstatus = 0
    totalclass = Bookclass.objects.filter(parent_id=0).values()
    childclass = Bookclass.objects.all().exclude(parent_id=0).values()
    id = request.GET.get("id")  #主键id
    parentid = request.GET.get("parentid")  #关联列id
    print("id",id,"parentid",parentid)
    if not id:
        id = request.session.get("id")
        parentid = request.session.get("parentid")
    else:
        request.session["id"]=id
        request.session["parentid"]=parentid
    if not parentid:
        parentid = 0
    if int(parentid):
        bookchildclass = Bookclass.objects.filter(pk=id)
        bookparentclass = Bookclass.objects.filter(pk=parentid)
        book = Bookclass.objects.filter(id=id).values("book__writer",
                                                             "book__image", "book__press", "book__printtime",
                                                             "book__title", "book__booklist__dangprice", "book__id",
                                                             "book__booklist__price")
    else:
        bookparentclass = Bookclass.objects.filter(pk=id)
        if not Bookclass.objects.filter(parent_id=id):
            bookchildclass = 0
        else:
            bookchildclass = Bookclass.objects.filter(parent_id=id)
        book = Bookclass.objects.filter(parent_id=id).values("book__writer",
                                                             "book__image","book__press","book__printtime",
                                                             "book__title","book__booklist__dangprice","book__id",
                                                             "book__booklist__price")
    book = book.exclude(book__writer=None)
    sort = request.GET.get("sort")
    if sort=='1':
        book = book.order_by("-book__booklist__sellnumber")
    elif sort=='2':
        book = book.order_by("book__booklist__dangprice")
    elif sort=='3':
        book = book.order_by("-book__addtime")
    else:
        sort = 0
    print("sort",sort)
    num = request.GET.get("num")
    if not num:
        num=1
    page=Paginator(book,2).page(num)
    allpage = Paginator(book, 2)
    return render(request,
                    "indexapp/booklist.html",{"total":totalclass,
                    "child":childclass,"bookchild":bookchildclass,"id":id,"parentid":parentid,
                    "bookparent":bookparentclass.values()[0],"pages":page,"allapge":allpage,
                    "sort":sort,"logstatus":logstatus,"usercook":usercook})

# 购物车页面
def car_view(request):
    remember = request.COOKIES.get("username")
    if remember:
        usercook = str(remember.encode("latin-1"), "utf-8")
        logstatus = 1
    else:
        usercook = ""
        if request.session.get("username"):
            logstatus = 1
        else:
            logstatus = 0
    cart = request.session.get("cart")
    if not  cart:
        cartlsit = 0
        return render(request, "indexapp/car.html",{"logstatus":logstatus,"usercook":usercook})
    cartlist = cart.cartlist
    totalprice=cart.total_price
    saveprice=cart.save_price
    print("logstatus",logstatus)
    return render(request,"indexapp/car.html",{"cart":cartlist,"totalprice":totalprice,
            "saveprice":saveprice,"logstatus":logstatus,"usercook":usercook})

# 地址填写页面

def ajax_caradd(request):
    bookid = request.POST.get("bookid")
    number = int(request.POST.get("number"))
    print("bookid",bookid,type(bookid),"number",number,type(number))
    cart = request.session.get("cart")
    print(cart)
    if cart:
        for i in cart.cartlist:
            print("bookid",i.book.get("id"),type(i.book.get("id")))
            print("id",bookid,type(bookid))
            if int(i.book.get("id"))==int(bookid):
                print(i.number,type(i.number),"i.number")
                num = i.number
                num=int(num)+number
                i.number=num
                cart.modifycart(bookid,num)
                print("############",i.number)
                request.session["cart"] = cart
                return HttpResponse("ok")
        else:
            cart.addcart(bookid,number)
            print("*********")
            request.session["cart"] = cart
            return HttpResponse("ok")

    else:
        car = Cart()
        car.addcart(bookid, number)
        print("++++++++++++++++")
        request.session["cart"] = car
    return HttpResponse("ok")


def ajax_modify(request):
    bookid = request.POST.get("bookid")
    number = int(request.POST.get("number"))
    print("bookid", bookid, type(bookid), "number", number, type(number))
    cart = request.session.get("cart")
    print(cart)
    if cart:
        cart.modifycart(bookid,number)
        request.session["cart"] = cart
        return HttpResponse("ok")
    return HttpResponse("no")

def ajax_delcart(request):
    bookid = request.POST.get("bookid")
    cart = request.session.get("cart")
    if cart:
        cart.delcart(bookid)
        request.session["cart"] = cart
        if not cart.cartlist:
            return HttpResponse("none")
        return HttpResponse("ok")

    return HttpResponse("no")
def indent_view(request):
    fromcart = request.GET.get("fromcart")
    if fromcart:
        request.session["fromcart"]=fromcart
    remember = request.COOKIES.get("username")
    sessionusername = request.session.get("username")
    if not remember and not sessionusername:
        return redirect("log:logview")
    if remember:
        usercook = str(remember.encode("latin-1"), "utf-8")
    else:
        usercook = sessionusername
    cart = request.session.get("cart")
    if not cart:
        return redirect("index:view")
    print("sessionusername",sessionusername)

    myadress = MyUser.objects.filter(username=usercook).values("address__name","address__zipcode",
                                                               "address__cellphone","address__phone","address__address")
    myadress=myadress.exclude(address__name=None)
    print(myadress,"myadress")
    totalprice = cart.total_price
    saveprice = cart.save_price
    cartlist = cart.cartlist
    return render(request,"indexapp/indent.html",
                  {"usercook":usercook,"totalprice":totalprice,"saveprice":saveprice,"cartlist":cartlist,"myadress":myadress})

def indentlog(request):
    l=GetPostValue(request,"user","username","adress","ecode","cellphone","phone","country","province","city","town")
    print(l)
    l[2]=l[6]+" " +l[7]+" "+l[8]+" "+l[9]+" "+l[2]  #地址拼接
    rulecode = "[0-9]{6}"
    rulephone = "^[1][3,4,5,7,8][0-9]{9}$"
    cart = request.session.get("cart")
    if l[0] and cart:
        user = MyUser.objects.get(username=l[0])
        if not (not l[1]) and len(l[2])<6 and (not re.match(rulecode,l[3]) and (not re.match(rulephone,l[4]))) :
            return redirect("index:indentview")
        with transaction.atomic():
            alladress = Address.objects.filter(user_address=user.id)
            for i in alladress:
                if i.name==l[1] and i.address==l[2] and i.zipcode==l[3] and i.cellphone==l[4] and i.phone==l[5]:
                    break
            else:
                Address(name=l[1],address=l[2],zipcode=l[3],cellphone=l[4],phone=l[5],user_address=user).save()
            myorder = Order(name=l[1],address=l[2],cellphone=l[4],phone=l[5],totalprice=cart.total_price,order_user=user)
            myorder.save()
            for i in cart.cartlist:
                bookid = Book.objects.get(pk=i.book.get("id"))
                Orderlist(count=i.number,price=i.book.get("booklist__price"),
                         dangprice=i.book.get("booklist__dangprice"),book_id=bookid,order_id=myorder).save()
        request.session["orderid"] = myorder.id
        del request.session["cart"]
        return redirect("index:indentokview")
    return redirect("log:logview")


# 下单成功页面
def indentok_view(request):
    count = 0
    remember = request.COOKIES.get("username")
    sessionusername = request.session.get("username")
    if remember:
        usercook = str(remember.encode("latin-1"), "utf-8")
    else:
        usercook = sessionusername
    orderid = request.session.get("orderid")
    if orderid:
        del request.session["orderid"]
        with transaction.atomic():
            order = Order.objects.get(pk=orderid)
            orderlist = Orderlist.objects.filter(order_id=orderid)
            for i in orderlist:
                count += i.count

    return render(request,"indexapp/indent ok.html",{"usercook":usercook,"order":order,"count":count})
















