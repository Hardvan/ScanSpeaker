from flask import Flask, render_template, request
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import base64
import io
import easyocr
import cv2
import numpy as np
import PIL
from gtts import gTTS
import os

app = Flask(__name__)


@app.route('/', methods=["GET", "POST"])
def index():

    if request.method == "POST":
        f = request.files["imageFile"]

        # Load the image
        try:
            img = PIL.Image.open(io.BytesIO(f.read()))

        except PIL.UnidentifiedImageError:
            return render_template("index.html", error="Invalid Image (Not an image)")

        # Reading the text from the image
        reader = easyocr.Reader(['en'])
        data = reader.readtext(np.array(img))

        # For one line of text
        # text = data[0][1]

        # For multiple lines
        text = ""
        for i in range(len(data)):
            text += data[i][1] + " "

        print(data)  # For debugging

        # Converting to speech
        language = 'en'
        speech = gTTS(text=text, lang=language, slow=False)

        # On local machine
        # speech.save("speech.mp3")
        # os.system("start speech.mp3")

        # Save the speech to memory as bytes
        speech_file = io.BytesIO()
        speech.write_to_fp(speech_file)
        speech_bytes = speech_file.getvalue()
        speech_base64 = base64.b64encode(speech_bytes).decode('utf-8')

        # Read the image file and convert it to base64 encoding
        f.seek(0)
        image_file = f.read()
        image_base64 = base64.b64encode(image_file).decode('utf-8')

        # Result
        result = {'image': image_base64,
                  'text': text,
                  'speech': speech_base64
                  }

        return render_template("index.html", result=result)

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
