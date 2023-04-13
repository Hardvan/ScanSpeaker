from flask import Flask, render_template, request
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import base64
import io
import easyocr
import cv2
import numpy as np
from PIL import Image

app = Flask(__name__)


@app.route('/', methods=["GET", "POST"])
def index():

    if request.method == "POST":
        f = request.files["imageFile"]

        # Load the image
        img = Image.open(io.BytesIO(f.read()))

        # Reading the text from the image
        reader = easyocr.Reader(['en'])
        data = reader.readtext(np.array(img))
        text = data[0][1]

        print(data)  # For debugging

        # Read the image file and convert it to base64 encoding
        f.seek(0)
        image_file = f.read()
        image_base64 = base64.b64encode(image_file).decode('utf-8')

        # Result
        result = {'image': image_base64,
                  'text': text}

        return render_template("index.html", result=result)

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
