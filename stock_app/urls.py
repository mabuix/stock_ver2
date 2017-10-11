from django.conf.urls import url

from . import views

urlpatterns = [
    # /stock_app
    url(r'^$', views.index, name='index'),
    # /stock_app/get_daily_data/
    url(r'^get_daily_data/$', views.get_daily_data, name='get_daily_data'),
    # /stock_app/create_spreadsheet_data/
    url(r'^create_spreadsheet_data/$', views.create_spreadsheet_data, name='create_spreadsheet_data'),
]