from OcrLib import OcrLib
from flask import Flask, request, jsonify

_VERSION = 1

crop_vals = {'money': {'x': 151, 'y': 186, 'w': 126, 'h': 18}, 'account': {'x': 113, 'y': 224, 'w': 210, 'h': 16}, 'recepit_num': {'x': 354, 'y': 362, 'w': 124, 'h': 16},'created': {'x':552,'y':327,'w':65,'h':16}}

app = Flask(__name__)

@app.route('/v{}/ocr'.format(_VERSION), methods=["POST"])
def ocr():
    try:
        url = request.form.get('image_url')
        if 'jpg' in url:
            ocr    = OcrLib(crop_vals)
            output = ocr.process_img(url)
            return jsonify({"data": output})
        else:
            return jsonify({"error": "only .jpg files, please"})
    except Exception as e:
        return jsonify({"error": "Did you mean to send: {'image_url': 'some_jpeg_url'}", "e": str(e)})
    except:
        return jsonify({"error": "Did you mean to send: {'image_url': 'some_jpeg_url'}"})

if __name__ == "__main__":
    app.run()
