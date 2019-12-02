from django.shortcuts import render
from .models import Photo
import base64
import requests
import json
import os
from django.conf import settings
from django.templatetags.static import static
import re
from dateutil.parser import parse
from django.views import generic


# Create your views here.

def get_URL():
    """URL with API Key"""
    URL =  'https://vision.googleapis.com/v1/images:annotate?key='
    return URL 

def encode_image(image_path):
    """Converts image to base64"""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('ascii')

def image_request(image_path):
    """This function makes a call to Google Vision API"""
    data = {
            "requests":[
                        {
                        "image":{
                            "content":encode_image(image_path)
                                },
                        "features":[
                                    {
                                    "type":"DOCUMENT_TEXT_DETECTION", #other options: LABEL_DETECTION FACE_DETECTION LOGO_DETECTION CROP_HINTS WEB_DETECTION
                                    "maxResults": 10
                                    }
                                   ]
                        }
                    ]
}
    r = requests.post(get_URL(), json = data)
    return r.text

def media_path():
    """Returns the Root Media path but with the word "Media" removed"""
    path = settings.MEDIA_ROOT
    new_path = path [:-6]
    return new_path

def regex(expression):
    """Attempts to extract date from data"""
    # We try a variety of REGEX
    pattern_list  = []
    match = re.search(r"\d{2}-\w{3}-\d{4}", expression)
    if match is not None:
        pattern_list.append(match.group(0))
    
    match = re.search(r"\w{3}-\d{2}-\d{4}", expression)
    if match is not None:
        pattern_list.append(match.group(0))
    
    match  = re.search(r"\d{2}-\d{2}-\d{4}", expression)
    if match is not None:
        pattern_list.append(match.group(0))
    
    match  = re.search(r"\d{2}-\d{2}-\d{2}", expression)
    if match is not None:
        pattern_list.append(match.group(0))

    match = re.search(r"\d{2}\.\w{3}\.\d{4}", expression)
    if match is not None:
        pattern_list.append(match.group(0))
    
    match = re.search(r"\w{3}\.\d{2}\.\d{4}", expression)
    if match is not None:
        pattern_list.append(match.group(0))
    
    match  = re.search(r"\d{2}\.\d{2}\.\d{4}", expression)
    if match is not None:
        pattern_list.append(match.group(0))
    
    match  = re.search(r"\d{2}\.\d{2}\.\d{2}", expression)
    if match is not None:
        pattern_list.append(match.group(0))
    
    match = re.search(r"\d{2}\s\w{3}\s\d{4}", expression)
    if match is not None:
        pattern_list.append(match.group(0))
    
    match = re.search(r"\w{3}\s\d{2}\s\d{4}", expression)
    if match is not None:
        pattern_list.append(match.group(0))
    
    match  = re.search(r"\d{2}\s\d{2}\s\d{4}", expression)
    if match is not None:
        pattern_list.append(match.group(0))
    
    match  = re.search(r"\d{2}\s\d{2}\s\d{2}", expression)
    if match is not None:
        pattern_list.append(match.group(0))
    
    match = re.search(r"\d{2}/\w{3}/\d{4}", expression)
    if match is not None:
        pattern_list.append(match.group(0))
    
    match = re.search(r"\w{3}/\d{2}/\d{4}", expression)
    if match is not None:
        pattern_list.append(match.group(0))
    
    match  = re.search(r"\d{2}/\d{2}/\d{4}",expression )
    if match is not None:
        pattern_list.append(match.group(0))
    
    match  = re.search(r"\d{2}/\d{2}/\d{2}", expression)
    if match is not None:
        pattern_list.append(match.group(0))

    print(pattern_list)
    if not pattern_list:
        return None
    else:
        try:
            # We just use the first element of the list
            # Convert into date
            ext_date = parse(pattern_list[0]).date()
            return ext_date
        except:
            return None

def api_loop(picture_path):
    """Requests a response from VISION API and passes information onto REGEX"""
    data = json.loads(image_request(picture_path))
    extracted_data = data["responses"][0]["textAnnotations"][0]["description"].split('\n')
    cleaned_data = " ".join(extracted_data)
    return regex(cleaned_data)

def index(request):
    """View function for home page of site."""
    # Initialize the Accuracy number
    # Set it to a default value of 0
    check_accuracy = {
            'accuracy': 0,
            'number_images': 0,
            }
    # Calls function to receive the OCR data for the receipt images
    photos = Photo.objects.all()
    for receipts in photos:
        receipts.extracted_date = api_loop(media_path()+receipts.picture.url)
        receipts.save()

    # Compare Actual and Extracted Date
    counter = 0
    match_date = 0
    for receipts in photos:
        counter += 1
        if receipts.actual_date == receipts.extracted_date:
            match_date += 1

    # Avoid division by 0
    # This would be the case when there are no images in the database
    if counter != 0:
        check_accuracy['accuracy'] = (match_date/counter)*100
        check_accuracy['number_images'] = counter

    # Create a context variable for accuracy
    context = {'check_accuracy' : check_accuracy}

    # Render the HTML template index.html 
    return render(request, 'index.html', context)

class PhotoListView(generic.ListView):
    """View function for each Receipt"""
    model = Photo
