from django.urls import path

from .views import *

urlpatterns = [
    path('upload_faktura/', upload_faktura, name='upload_faktura'),
    path('faktura_list/', Faktura_List.as_view(), name='faktura_list'),

    path('', Lek_List_Nazwa_A.as_view(), name='lek_list_nazwa_a'),
    path('lek_list_nazwa_o/', Lek_List_Nazwa_O.as_view(), name='lek_list_nazwa_o'),

    path('lek_list_faktura_a/', Lek_List_Faktura_A.as_view(), name='lek_list_faktura_a'),
    path('lek_list_faktura_o/', Lek_List_Faktura_O.as_view(), name='lek_list_faktura_o'),

]
