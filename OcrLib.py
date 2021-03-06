import numpy
import cv2
import requests
import pytesseract
from PIL import Image
from PIL import ImageFilter
from StringIO import StringIO

class OcrLib(object):
    def __init__(self, crop_vals):
        super(OcrLib, self).__init__()
        self.crop = crop_vals

    def _get_image(self,url):
        return Image.open(StringIO(requests.get(url).content)).convert('RGB')

    def crop_image(self,pil_img):
        cv_img = cv2.cvtColor(numpy.array(pil_img), cv2.COLOR_RGB2GRAY)

        v, bin_img = cv2.threshold(cv_img, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

        cropped = {}
        for f in self.crop:
            params = self.crop[f]
            roi = bin_img[params['y']:(params['y']+params['h']), params['x']:(params['x']+params['w'])] # money
            #cv2.imwrite('%s.png' % f, roi)

            roi = cv2.cvtColor(roi, cv2.COLOR_GRAY2RGB)
            pil_roi = Image.fromarray(roi)
            cropped[f] = pil_roi

        return cropped

    def ocr_img(self,img):
        #img.filter(ImageFilter.SHARPEN)
        text = pytesseract.image_to_string(img, lang='money')
        return ''.join(text.split())

    def process_img(self,img_src):
        croped_rois = self.crop_image(self._get_image(img_src))

        result = {}
        for f in croped_rois:
            ocr_text = self.ocr_img(croped_rois[f])
            result[f] = ocr_text

        return result

if __name__ == "__main__":

    img_src = 'http://oss.aliyuncs.com/quancheng-syt/uploads/picture_caiwu/2015-09-28/56090caf01889.jpg'

    crop_vals = {'money': {'x': 151, 'y': 186, 'w': 126, 'h': 18}, 'account': {'x': 113, 'y': 224, 'w': 210, 'h': 16}, 'recepit_num': {'x': 354, 'y': 362, 'w': 124, 'h': 16},'created': {'x':552,'y':327,'w':65,'h':16}}

    ocr = OcrLib(crop_vals);
    output = ocr.process_img(img_src)
    print output;
