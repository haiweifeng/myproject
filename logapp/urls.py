from django.urls import path

from logapp import views

urlpatterns = [
    path('logview/',views.login_view,name="logview"),
    path('loglogic/',views.log_logic,name="loglogic"),
    path('regview/',views.regist_view,name="regview"),
    path('reglogic/',views.reg_logic,name="reglogic"),
    path('regok/',views.registok_view,name="registok"),
    path('getcaptcha/',views.getcaptcha,name="getcaptcha"),
    path('ajax_captcha/',views.ajax_captcha,name="ajax_captcha"),
    path('ajax_username/',views.ajax_username,name="ajax_username"),
    path('ajax_email/',views.ajax_email,name="ajax_email"),
    path('logexit/',views.log_exit,name="logexit"),
    path('email_confirm/',views.email_confirm,name="email_confirm"),

]
