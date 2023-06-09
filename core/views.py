from django.shortcuts import render
from django.http import HttpResponse
import collections
from collections import abc
collections.MutableMapping = abc.MutableMapping
import firebase_admin
from firebase_admin import storage
import datetime
import requests
import urllib


url_list = []

config = {
	'apiKey': "AIzaSyC-DF0lyMXYegJlpKiUrQFzFOMn6QtI_lo",
	'authDomain': "smartdoorbell-2382f.firebaseapp.com",
	'databaseURL': "https://smartdoorbell-2382f-default-rtdb-firebaseio.com",
  'storageBucket': "smartdoorbell-2382f.appspot.com"
}

cred = firebase_admin.credentials.Certificate('key.json')
default_app = firebase_admin.initialize_app(cred, config)
bucket = storage.bucket()
bucket_list = bucket.list_blobs(prefix="DEFAULT/")
for blob in bucket_list:
    img_url = blob.generate_signed_url(datetime.timedelta(seconds=300), method='GET')
    url_list.append(img_url)

def index(request):

    return render(request, 'index.html', {'images_url': url_list[1:6]})
