from django.urls import path

from .views import *

urlpatterns = [
    path('upload_faktura/', upload_faktura, name='upload_faktura'),
    path('faktura_list/', FakturaList.as_view(), name='faktura_list'),

    path('lek_list_nazwa_a/', LekList_Nazwa_A.as_view(), name='lek_list_nazwa_a'),
    path('lek_list_nazwa_o/', LekList_Nazwa_O.as_view(), name='lek_list_nazwa_o'),

    path('lek_list_faktura_a/', LekList_Faktura_A.as_view(), name='lek_list_faktura_a'),
    path('lek_list_faktura_o/', LekList_Faktura_O.as_view(), name='lek_list_faktura_o'),

]
