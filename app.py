import os
import logging
from logging import Formatter, FileHandler
from flask import Flask, request, jsonify

#from ocr import process_img

import numpy
import cv2
import requests
import pytesseract
from PIL import Image
from PIL import ImageFilter
from StringIO import StringIO

img_src = 'http://oss.aliyuncs.com/quancheng-syt/uploads/picture_caiwu/2015-09-28/56090caf01889.jpg'

def _get_image(url):
    return Image.open(StringIO(requests.get(url).content)).convert('RGB')

def crop_image(pil_img):
    cv_img = cv2.cvtColor(numpy.array(pil_img), cv2.COLOR_RGB2GRAY)

    v, bin_img = cv2.threshold(cv_img, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

    crop_vals = {'money': {'x': 151, 'y': 186, 'w': 126, 'h': 18}, 'account': {'x': 113, 'y': 224, 'w': 210, 'h': 16}, 'recepit_num': {'x': 354, 'y': 362, 'w': 124, 'h': 16}}

    cropped = {}
    for f in crop_vals:
        params = crop_vals[f]
        roi = bin_img[params['y']:(params['y']+params['h']), params['x']:(params['x']+params['w'])] # money
        #cv2.imwrite('%s.png' % f, roi)

        roi = cv2.cvtColor(roi, cv2.COLOR_GRAY2RGB)
        pil_roi = Image.fromarray(roi)
        cropped[f] = pil_roi

    return cropped

def ocr_img(img):
    #img.filter(ImageFilter.SHARPEN)
    text = pytesseract.image_to_string(img, lang='money')
    return ''.join(text.split())

def process_img(url):
    print '+++processing img: %s' % img_src
    croped_rois = crop_image(_get_image(img_src))

    print 'OCR results:'
    result = {}
    for f in croped_rois:
        ocr_text = ocr_img(croped_rois[f])
        print '%s -> %s' % (f, ocr_text)
        result[f] = ocr_text

    print '---processed img: %s' % img_src
    return result
 
_VERSION = 1

app = Flask(__name__)

@app.route('/v{}/ocr'.format(_VERSION), methods=["POST"])
def ocr():
    try:
        url = request.json['image_url']
        if 'jpg' in url:
            output = process_img(url)
            return jsonify({"output": output})
        else:
            return jsonify({"error": "only .jpg files, please"})
    except Exception as e:
        return jsonify(
            {"error": "Did you mean to send: {'image_url': 'some_jpeg_url'}", "e": str(e)}
        )
    except:
        return jsonify(
            {"error": "Did you mean to send: {'image_url': 'some_jpeg_url'}"}
        )

if __name__ == "__main__":
    app.run()
