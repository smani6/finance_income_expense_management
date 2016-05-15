from django.conf.urls import url

from views import *

urlpatterns = [
 	url(r'^login/$', Login.as_view(), name='login'),
 	url(r'^dashboard/$', Dashboard.as_view(), name='dashboard'),
 	url(r'^transaction/$', Transaction.as_view(),name='transaction'),

]