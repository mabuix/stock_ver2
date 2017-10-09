from django.conf.urls import url

from . import views

urlpatterns = [
    # /stock_app
    url(r'^$', views.index, name='index'),
    # /stock_app/get_daily_data/
    url(r'^get_daily_data/$', views.get_daily_data, name='get_daily_data'),
]