from django.shortcuts import render
from xml.dom import minidom
from .forms import *
from .models import *
from django.contrib import messages
from django.views.generic import ListView
from django.shortcuts import get_object_or_404, redirect
from django.db.models import Count
from django.urls import reverse_lazy, reverse

import datetime
# Create your views here.


class Faktura_List(ListView):
    model = Faktura
    fields = '__all__'
    template_name =  'faktura_list.html'

    def get_context_data(self,*args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context['faktury'] = Faktura.objects.all().order_by('-data_wystawienia').annotate(lek_len=(Count('lek')))
        return context

class Lek_List_Base(ListView):
    model = Lek
    fields = '__all__'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['sort'] = self.__class__.__name__[9:-2]

        if self.__class__.__name__[-1] == 'A':
            context['stan'] = 'A'
        elif self.__class__.__name__[-1] == 'O':
            context['stan'] = 'O'

        return context

    def post(self, request, *args, **kwargs):
        form = request.POST
        if form.get('bulk'):
            nazwa = form.get('nazwa')
            ilosc = int(form.get('ilosc'))
            if form.get('bulk') == 'bulk_a':
                leki = Lek.all.apteka().filter(nazwa__exact = nazwa).order_by('data_waznosci')[0:ilosc]
            elif form.get('bulk') == 'bulk_o':
                leki = Lek.all.oddzial().filter(nazwa__exact = nazwa).order_by('data_waznosci')[0:ilosc]
            for lek in leki:
                if lek.stan == 'A':
                    lek.stan = 'O'
                    lek.data_wydania = datetime.datetime.today().date()
                elif lek.stan == 'O':
                    lek.stan = 'A'
                    lek.data_wydania = None
                lek.save()
        elif form.get('id'):
            id = form.get('id')
            lek = get_object_or_404(Lek, id=id)
            if lek.stan == 'A':
                lek.stan = 'O'
                lek.data_wydania = datetime.datetime.today().date()
            elif lek.stan == 'O':
                lek.stan = 'A'
                lek.data_wydania = None
            lek.save()


        return redirect(str(self.__class__.__name__).lower())



class Lek_List_Nazwa_Base(Lek_List_Base):
    def get_context_data(self,*args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        if self.__class__.__name__ == 'Lek_List_Nazwa_O':
            dict = Lek.all.oddzial().values('nazwa').annotate(ilosc=(Count('nazwa')))
        elif self.__class__.__name__ == 'Lek_List_Nazwa_A':
            dict = Lek.all.apteka().values('nazwa').annotate(ilosc=(Count('nazwa')))
        for j in dict:
            nazwa = j.get('nazwa')
            if self.__class__.__name__ == 'Lek_List_Nazwa_A':
                list = Lek.all.apteka().filter(nazwa__exact = nazwa)
            elif self.__class__.__name__ == 'Lek_List_Nazwa_O':
                list = Lek.all.oddzial().filter(nazwa__exact = nazwa)
            j['list'] = list
        context['leki'] = dict
        return context




class Lek_List_Nazwa_A(Lek_List_Nazwa_Base):
    template_name =  'lek_list.html'


class Lek_List_Nazwa_O(Lek_List_Nazwa_Base):
    template_name =  'lek_list.html'


class Psychotrop_List(ListView):
    model = Lek
    fields = '__all__'
    template_name =  'psychotrop_list.html'

    def get_context_data(self,*args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['leki'] = Lek.all.psychotrop().order_by('nazwa')
        return context


    def post(self, request, *args, **kwargs):
        form = request.POST

        if form.get('wydane'):
            data_od = datetime.datetime.strptime(form.get('w_data_od'), '%d-%m-%Y').strftime('%Y-%m-%d')
            data_do = datetime.datetime.strptime(form.get('w_data_do'), '%d-%m-%Y').strftime('%Y-%m-%d')
            leki = Lek.all.psychotrop().filter(data_wydania__range = [data_od, data_do]).values('nazwa','BLOZ','kod_kreskowy', 'jednostka').annotate(ilosc=(Count('nazwa')))

            return render(request, 'psychotrop_list.html', {'leki' : leki, 'data_od':form.get('w_data_od'), 'data_do':form.get('w_data_do'), 'stan':'wydane'})

        elif form.get('przyjete'):
            data_od = datetime.datetime.strptime(form.get('p_data_od'), '%d-%m-%Y').strftime('%Y-%m-%d')
            data_do = datetime.datetime.strptime(form.get('p_data_do'), '%d-%m-%Y').strftime('%Y-%m-%d')
            leki = Lek.all.psychotrop().filter(faktura__data_sprzedazy__range = [data_od, data_do]).values('nazwa','BLOZ','kod_kreskowy', 'jednostka').annotate(ilosc=(Count('nazwa')))

            return render(request, 'psychotrop_list.html', {'leki' : leki, 'data_od':form.get('p_data_od'), 'data_do':form.get('p_data_do'), 'stan':'przyjete'})

def lek_list_range_a(request):
    data_od =datetime.datetime.strptime(request.POST.get('p_data_od'),'%d-%m-%Y')
    data_do =datetime.datetime.strptime(request.POST.get('p_data_do'),'%d-%m-%Y')

    dict = Lek.all.apteka().filter(faktura__data_sprzedazy__range=[data_od,data_do]).values('nazwa','BLOZ', 'seria', 'data_waznosci', 'PKWiU', 'kod_kreskowy', 'faktura__nr_faktury','faktura__data_sprzedazy').annotate(ilosc=(Count('nazwa')))
    stan = 'sprzedaz'
    return render(request, 'lek_list_range.html', {'data_od': data_od, 'data_do':data_do, 'dict':dict, 'stan':stan})



def lek_list_range_o(request):
    data_od =datetime.datetime.strptime(request.POST.get('w_data_od'),'%d-%m-%Y')
    data_do =datetime.datetime.strptime(request.POST.get('w_data_do'),'%d-%m-%Y')

    dict = Lek.all.oddzial().filter(data_wydania__range=[data_od,data_do]).values('nazwa','BLOZ', 'seria', 'data_waznosci', 'PKWiU', 'kod_kreskowy', 'faktura__nr_faktury','faktura__data_sprzedazy', 'data_wydania').annotate(ilosc=(Count('nazwa')))
    stan = 'wydanie'
    return render(request, 'lek_list_range.html', {'data_od': data_od, 'data_do':data_do, 'dict':dict, 'stan':stan})



class Lek_List_Faktura_Base(Lek_List_Base):
    def get_context_data(self,*args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        if self.__class__.__name__ == 'Lek_List_Faktura_O':
            dict = Lek.all.oddzial().values('faktura_id').annotate(ilosc=(Count('faktura_id')))
        elif self.__class__.__name__ == 'Lek_List_Faktura_A':
            dict = Lek.all.apteka().values('faktura_id').annotate(ilosc=(Count('faktura_id')))

        for j in dict:
            faktura_id = j.get('faktura_id')
            faktura_nr_faktury = get_object_or_404(Faktura,id=faktura_id).nr_faktury
            if self.__class__.__name__ == 'Lek_List_Faktura_O':
                list = Lek.all.oddzial().filter(faktura_id__exact = faktura_id)
            elif self.__class__.__name__ == 'Lek_List_Faktura_A':
                list = Lek.all.apteka().filter(faktura_id__exact = faktura_id)
            j['list'] = list
            j['faktura_nr_faktury']=faktura_nr_faktury
        context['leki'] = dict
        return context



    def post(self, request, *args, **kwargs):
        form = request.POST
        if form.get('bulk'):
            faktura_id = form.get('faktura_id')
            if form.get('bulk') == 'bulk_a':
                leki = Lek.all.apteka().filter(faktura_id__exact = faktura_id).order_by('data_waznosci')
                for lek in leki:
                    lek.stan = 'O'
                    lek.save()
            elif form.get('bulk') == 'bulk_o':
                leki = Lek.all.oddzial().filter(faktura_id__exact = faktura_id).order_by('data_waznosci')
                for lek in leki:
                    lek.stan = 'A'
                    lek.save()
        else:
            id = form.get('id')
            lek = get_object_or_404(Lek, id=id)
            if lek.stan == 'A':
                lek.stan = 'O'
            elif lek.stan == 'O':
                lek.stan = 'A'
            lek.save()

        return redirect(str(self.template_name).partition('.')[0])


class Lek_List_Faktura_A(Lek_List_Faktura_Base):
    template_name =  'lek_list.html'

class Lek_List_Faktura_O(Lek_List_Faktura_Base):
    template_name =  'lek_list.html'





def upload_faktura(request):
    form = UploadFileForm()
    if request.method == 'POST' and request.FILES:
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
        f = open('documents/' + str(request.FILES['document']), mode='rb')
        tree = minidom.parse(f)

        towary = tree.getElementsByTagName('towar')
        faktura = tree.getElementsByTagName('faktura')[0]
        naglowek = faktura.getElementsByTagName('naglowek')[0]
        pozycje = faktura.getElementsByTagName('pozycja')

        nr_faktury = naglowek.getElementsByTagName('nr-faktury')[0].firstChild.data

        if not (Faktura.objects.all().filter(nr_faktury__exact = nr_faktury)):
            try:
                data_wystawienia = str(naglowek.getElementsByTagName('data-wystawienia')[0].firstChild.data).partition("T")[0]
            except:
                data_wystawienia = False
            try:
                data_sprzedazy = naglowek.getElementsByTagName('data-sprzedazy')[0].firstChild.data
            except:
                data_sprzedazy = False
            try:
                termin_platnosci = naglowek.getElementsByTagName('termin-platnosci')[0].firstChild.data
            except:
                termin_platnosci = False
            try:
                id_sprzedawcy = naglowek.getElementsByTagName('id-sprzedawcy')[0].firstChild.data
            except:
                id_sprzedawcy = False
            try:
                korekta = naglowek.getElementsByTagName('korekta')[0].firstChild.data
            except:
                korekta = False
            try:
                wartosc_netto = naglowek.getElementsByTagName('wartosc-netto')[0].firstChild.data
            except:
             wartosc_netto = False
            try:
                wartosc_brutto = naglowek.getElementsByTagName('wartosc-brutto')[0].firstChild.data
            except:
                wartosc_brutto = False

            _faktura = Faktura(nr_faktury=nr_faktury, data_wystawienia=data_wystawienia, data_sprzedazy=data_sprzedazy,
                       termin_platnosci=termin_platnosci, id_sprzedawcy=id_sprzedawcy, korekta=korekta,
                       wartosc_netto=wartosc_netto, wartosc_brutto=wartosc_brutto)

            _faktura.save()

            for towar in towary:
                _id = towar.getElementsByTagName('id-towaru')[0].firstChild.data

                try:
                    _nazwa = towar.getElementsByTagName('id-towaru')[0].parentNode.getElementsByTagName('nazwa')[
                    0].firstChild.data
                except:
                    _nazwa = 'Brak nazwy'
                try:
                    _BLOZ = towar.getElementsByTagName('id-towaru')[0].parentNode.getElementsByTagName('id-towaru-ks')[
                    0].firstChild.data
                except:
                    _BLOZ = False

                for pozycja in pozycje:
                    ilosc = 0
                    if pozycja.getElementsByTagName('id-towaru')[0].firstChild.data == _id:
                        try:
                            _jednostka = pozycja.getElementsByTagName('jednostka-miary')[0].firstChild.data
                        except:
                            _jednostka = False
                        try:
                            _seria = pozycja.getElementsByTagName('seria')[0].firstChild.data
                        except:
                            _seria = False
                        try:
                            _data_waznosci = pozycja.getElementsByTagName('data-waznosci')[0].firstChild.data
                        except:
                            _data_waznosci = False
                        try:
                            _cena_netto = pozycja.getElementsByTagName('cena-netto')[0].firstChild.data
                        except:
                            _cena_netto = False
                        try:
                            _cena_brutto = pozycja.getElementsByTagName('cena-brutto')[0].firstChild.data
                        except:
                            _cena_brutto = False
                        try:
                            _PKWiU = pozycja.getElementsByTagName('pkwiu')[0].firstChild.data
                        except:
                            _PKWiU = False
                        try:
                            _kod_kreskowy = pozycja.getElementsByTagName('kod-kreskowy')[0].firstChild.data
                        except:
                            _kod_kreskowy = False

                        try:
                            _ilosc = pozycja.getElementsByTagName('ilosc')[0].firstChild.data

                        except:
                            _ilosc = 0
                        ilosc += int(_ilosc)
                        _faktura_nr = _faktura
                    for i in range(ilosc):
                        _lek = Lek(id_towaru=_id, nazwa=_nazwa, BLOZ=_BLOZ, jednostka=_jednostka, seria=_seria,
                                        data_waznosci=_data_waznosci, cena_netto=_cena_netto, cena_brutto=_cena_brutto,
                                        PKWiU=_PKWiU, kod_kreskowy=_kod_kreskowy, faktura=_faktura_nr, stan = 'A')
                        _lek.save()

        else:
            messages.add_message(request, messages.INFO, 'Faktura wczesniej zaladowana')

    return render(request, 'upload_faktura.html', {'form': form})
