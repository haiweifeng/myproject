from django.urls import path

from indexapp import views

urlpatterns = [
    path('view/',views.index_view,name="view"),
    path('bookview/',views.book_view,name="bookview"),
    path('booklistview/',views.booklistview,name="booklistview"),
    path('carview/',views.car_view,name="carview"),
    path('indentview/',views.indent_view,name="indentview"),
    path('indentokview/',views.indentok_view,name="indentokview"),
    path('caradd/',views.ajax_caradd,name="caradd"),
    path('modify/',views.ajax_modify,name="ajax_modify"),
    path('delcart/',views.ajax_delcart,name="ajax_delcart"),
    path('indentlog/',views.indentlog,name="indentlog"),
]