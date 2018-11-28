from django.urls import path

from myadmin import views

urlpatterns = [
    path('view/',views.myview,name="main"),
    path('add/',views.addbook,name="add"),
    path('dzlist/',views.dzlist,name="dzlist"),
    path('list/',views.list,name="list"),
    path('splb/',views.splb,name="splb"),
    path('zjsp/',views.zjsp,name="zjsp"),
    path('zjzlb/',views.zjzlb,name="zjzlb"),
    path('addlog/',views.addlog,name="addlog"),
    path('addparent/',views.addparent,name="addparent"),
    path('addchild/',views.addchild,name="addchild"),
    path('orderlist/',views.orderlist,name="orderlist"),
    path('bookdel/',views.bookdel,name="bookdel"),
    path('bookclassdel/',views.bookclassdel,name="bookclassdel"),

]