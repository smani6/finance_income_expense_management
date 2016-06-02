from django.conf.urls import url

from views import *

urlpatterns = [
    url(r'^$', Website.as_view(), name='website'),
    url(r'^signup$', SignUp.as_view(), name='signup'),
    url(r'^login/$', Login.as_view(), name='login'),
    url(r'^dashboard/$', Dashboard.as_view(), name='dashboard'),
    url(r'^transaction/$', Transaction.as_view(), name='transaction'),
    url(r'^get_chart/$', CharView.as_view(), name='chart'),

]
