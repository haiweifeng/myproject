import hashlib

import datetime

from django.core.mail import EmailMultiAlternatives
from django.http import request

# 从POST请求中取值
from indexapp.models import Book

def hash_code(s, salt='#*00'):
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())
    return h.hexdigest()



def send_mail(email,code):
    subject, from_email, to = '邮箱验证', '15309869720@sina.cn',email,
    text_content = code
    # html_content = '<p>感谢注册<a href="http://{}/log/email_confirm/?code={}"target = _blank > 点我激活... < / a >，\欢迎你来验证你的邮箱，验证结束你就可以登录了！ < / p > '.format('172.16.8.136:8000',code)
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    # msg.attach_alternative(html_content, "text/html")
    msg.send()



def GetPostValue(request,*a):
    b=[]
    for i in a:
        b.append(request.POST.get(i))
    return b
# 从GET请求中取值
def GetGetValue(request,*a):
    b=[]
    for i in a:
        b.append(request.GET.get(i))
    return b
class Cartiems():
    def __init__(self,book,number):
        self.book = book
        self.number = number
class Cart():
    def __init__(self):
        self.total_price = 0
        self.save_price = 0
        self.cartlist = []
    def sums(self):
        self.total_price = 0
        self.save_price = 0
        for i in self.cartlist:
            self.total_price += float(i.book.get("booklist__dangprice")) * i.number
            self.save_price += (float(i.book.get("booklist__price"))-float(i.book.get("booklist__dangprice")))*i.number
    def addcart(self,bookid,number):
        for i in self.cartlist:
            if i.book.get("id") ==int(bookid):
                i.number+=int(number)
                self.sums()
                return
        if  Book.objects.filter(pk=bookid):
            book = Book.objects.filter(pk=bookid).values("image", "id",
                                                         "title", "booklist__dangprice", "booklist__price",
                                                         "booklist__sellnumber","press")[0]
            print("book", book)
            self.cartlist.append(Cartiems(book, number))
            self.sums()
            return
    def modifycart(self,bookid,number):
        for i in self.cartlist:
            if i.book.get("id")==int(bookid):
                i.number=int(number)
                print("#######",i.number)
        self.sums()
        print("total_price",self.total_price,self.save_price)
        return
    def delcart(self,bookid):
        print("************","bookid",bookid,type(bookid))
        for i in self.cartlist:
            print("&&&&&&&&&&&&&",i.book.get("id"),type(i.book.get("id")))
            print("this is i",i)
            if i.book.get("id") ==int(bookid):
                print("cartlist",self.cartlist)
                self.cartlist.remove(i)
                print("cartlist", self.cartlist)
        self.sums()
        return

























