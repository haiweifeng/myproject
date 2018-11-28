from django import template
register=template.Library()

#简单过滤器  takes_context表示是否取views.py传递过来的参数.如果等于True,则取，否则则不取。
@register.simple_tag()
def discount(newprice,oldprice):
    return format(float(newprice) *float(10)/ float(oldprice), '.1f')