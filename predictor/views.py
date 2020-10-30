from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.views.generic import ListView
from .apps import PredictorConfig
from .forms import DocumentForm
from .models import Document
from .Metadata import getmetadata
import warnings
from .predict import predict_gen
from django.contrib import messages

from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

import librosa
import os
from pathlib import Path
import simpleaudio as sa

warnings.simplefilter('ignore')

class IndexView(ListView):
    template_name= 'music/index.html'
    def get_queryset(self):
        return True

@csrf_exempt
def model_form_upload(request):

    documents = Document.objects.all()
    if request.method == 'POST':
        if len(request.FILES) == 0:
            messages.error(request,'Upload a file')
            return HttpResponse({'genre':'error please upload a file'}, status=400)

        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            uploadfile = request.FILES['document']
            print(uploadfile.name)
            print(uploadfile.size)
            if not uploadfile.name.endswith('.wav'):
                messages.error(request,'Only .wav file type is allowed')
                return JsonResponse({'genre':'error please upload a wav file'}, status=400)

            #uploadfile = uploadfile.read().decode('utf-8', 'replace')

            #Audio_file = sa.WaveObject.from_wave_file(uploadfile)
            meta = getmetadata(uploadfile)
            genre = predict_gen(meta)
            print(genre)

            context = {'genre':genre}
            return JsonResponse({'genre':genre}, status=200)

    else:
        return JsonResponse({'genre':'error'}, status=400)