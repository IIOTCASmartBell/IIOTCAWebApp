from django.shortcuts import render
from django.http import HttpResponse
import collections
from collections import abc
collections.MutableMapping = abc.MutableMapping
import firebase_admin
from firebase_admin import storage
from firebase_admin import db
import datetime
import requests
import urllib


url_list = []
green_list = []
black_list = []
display_new_entries = {}

# config = {
# 	'apiKey': "AIzaSyC-DF0lyMXYegJlpKiUrQFzFOMn6QtI_lo",
# 	'authDomain': "smartdoorbell-2382f.firebaseapp.com",
# 	'databaseURL': "https://smartdoorbell-2382f-default-rtdb-firebaseio.com",
#   'storageBucket': "smartdoorbell-2382f.appspot.com"
# }


config = {
	'apiKey': "AIzaSyASpod8P7JnGBYLDz6JO8Q2C3Dbss9YmBw",
	'authDomain': "smartdoorbellfinal.firebaseapp.com",
	'databaseURL': "https://smartdoorbellfinal-default-rtdb.firebaseio.com",
	'storageBucket': "smartdoorbellfinal.appspot.com"
}

# cred = firebase_admin.credentials.Certificate('key.json')
cred = firebase_admin.credentials.Certificate('key2.json')
default_app = firebase_admin.initialize_app(cred, config)
bucket = storage.bucket()
ref_act = db.reference('/actions')
ref_lists = db.reference('/lists')
ref_default = db.reference('/lists/default').get()

default_bucket_list = bucket.list_blobs(prefix="DEFAULT/")
for blob in default_bucket_list:
    img_url = blob.generate_signed_url(datetime.timedelta(seconds=300), method='GET')
    url_list.append(img_url)

# green_bucket_list = bucket.list_blobs(prefix="GREENLIST/")
# for blob in green_bucket_list:
#     img_url = blob.generate_signed_url(datetime.timedelta(seconds=300), method='GET')
#     green_list.append(img_url)

# black_bucket_list = bucket.list_blobs(prefix="BLACKLIST/")
# for blob in black_bucket_list:
#     img_url = blob.generate_signed_url(datetime.timedelta(seconds=300), method='GET')
#     black_list.append(img_url)

def index(request):
    return render(request, 'index.html', {'images_url': url_list[:5]})

def new_entries(request):
    for key, value in ref_default.items():
        for keyval, val in value.items():
            display_new_entries[key] = val
            break

    if request.method == 'POST':
        if 'image_key' in request.POST:
            key_img = request.POST['image_key']
            if 'name_person' in request.POST and 'label_person' in request.POST:
                name = request.POST['name_person']
                label = request.POST['label_person']

                ref_image = db.reference('/lists/default/' + key_img)
                ref_image.update({
                    'person_name': name
                })

    return render(request, 'new-entries.html', {'images_url': display_new_entries})