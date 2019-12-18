from django.db import models
from django.forms import ModelForm
from .models import *



class UploadFileForm(ModelForm):
    class Meta:
        model = Document
        fields = ( 'document',)