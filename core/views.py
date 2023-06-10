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
greenlist = []
blacklist = []
display_new_entries = {}
display_greenlist = {}
name_greenlist = {}
date_greenlist = {}

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
ref_greenlist = db.reference('/lists/greenlist').get()

default_bucket_list = bucket.list_blobs(prefix="DEFAULT/")
for blob in default_bucket_list:
    img_url = blob.generate_signed_url(datetime.timedelta(seconds=500000), method='GET')
    url_list.append(img_url)

green_bucket_list = bucket.list_blobs(prefix="GREENLIST/")
for blob in green_bucket_list:
    img_url = blob.generate_signed_url(datetime.timedelta(seconds=500000), method='GET')
    greenlist.append(img_url)

# black_bucket_list = bucket.list_blobs(prefix="BLACKLIST/")
# for blob in black_bucket_list:
#     img_url = blob.generate_signed_url(datetime.timedelta(seconds=300), method='GET')
#     blacklist.append(img_url)

def index(request):
    return render(request, 'index.html', {'images_url': url_list[:5], 'greenlist': greenlist[:5]})

def new_entries(request):
    # special dict for displaying images on website, as well as tracking the image name
    for key, value in ref_default.items():
        for keyval, val in value.items():
            display_new_entries[key] = val
            break

    if request.method == 'POST':
        # making use of the image name
        if 'image_key' in request.POST:
            key_img = request.POST['image_key']
            if 'name_person' in request.POST and 'label_person' in request.POST:
                name = request.POST['name_person']
                label = request.POST['label_person']

                # change the name from "person" to name given as input
                ref_image = db.reference('/lists/default/' + key_img)
                ref_image.update({'person_name': name})

                # move the image to the specified label in the database
                img_dict = ref_image.get()
                ref_move_label = db.reference('/lists/' + label)
                ref_move_label.update({key_img: img_dict})

                # insert image to a specific folder in the storage (DEFAULT / GREENLIST / BLACKLIST)
                local_file_path = 'static/' + key_img + '.jpg'
                img_url = ref_image.get()['img_link']
                urllib.request.urlretrieve(img_url, local_file_path)
                name_path_storage = label.upper() + '/' + key_img + '.jpg'
                blob = bucket.blob(name_path_storage)
                blob.upload_from_filename(local_file_path)
                # change image link in database
                ref_image = db.reference('/lists/' + label + '/' + key_img)
                img_url_new = blob.generate_signed_url(datetime.timedelta(seconds=500000), method='GET')
                ref_image.update({'img_link': img_url_new})

                # delete from default in db and storage (only if they're greenlist/blacklist!)
                if label == 'greenlist' or label == 'blacklist':
                    ref_image.delete()
                    display_new_entries.pop(key_img)
                    blob = bucket.blob('DEFAULT/' + key_img + '.jpg')
                    print(blob)
                    blob.delete()

    return render(request, 'new-entries.html', {'images_url': display_new_entries})


def green_list(request):
    # special dict for displaying images on website, as well as tracking the image name
    for key, value in ref_greenlist.items():
        for keyval, val in value.items():
            display_greenlist[key] = val
            break

    for key, value in ref_greenlist.items():
        for keyval, val in value.items():
            if str(keyval) == 'person_name':
                name_greenlist[key] = val

    for key, value in ref_greenlist.items():
        date_taken = str(key).strip("img_").replace('_', ', ')
        date_taken = date_taken[::-1].replace('-', ':', 1)[::-1]
        date_greenlist[key] = date_taken

    return render(request, 'green-list.html', {'greenlist': display_greenlist, 'name': name_greenlist, 'date': date_greenlist})