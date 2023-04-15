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
# import os

app = Flask(__name__)


def getResult(img, f):

    # Read the image file and convert it to base64 encoding
    f.seek(0)
    image_file = f.read()
    image_base64 = base64.b64encode(image_file).decode('utf-8')

    # Reading the text from the image
    reader = easyocr.Reader(['en'])
    data = reader.readtext(np.array(img))
    print(data)  # For debugging

    # Reading text & Putting rectangles
    result_text = []
    result_image = np.array(img)
    for detection in data:
        top_left = tuple([int(val) for val in detection[0][0]])
        bottom_right = tuple([int(val) for val in detection[0][2]])
        result_text.append(detection[1])

        result_image = cv2.rectangle(
            result_image, top_left, bottom_right, (0, 255, 0), 5)
        result_image = cv2.putText(result_image, result_text[-1], top_left, cv2.FONT_HERSHEY_SIMPLEX,
                                   2, (255, 255, 255), 2, cv2.LINE_AA)
    result_text = " ".join(result_text)

    # Convert the image from BGR to RGB
    result_image = cv2.cvtColor(result_image, cv2.COLOR_BGR2RGB)

    # Encode result_image as base64 string
    _, result_image_buffer = cv2.imencode('.jpg', result_image)
    result_image_base64 = base64.b64encode(
        result_image_buffer).decode('utf-8')

    # Converting to speech
    language = 'en'
    speech = gTTS(text=result_text, lang=language, slow=False)

    # On local machine
    # speech.save("speech.mp3")
    # os.system("start speech.mp3")

    # Save the speech to memory as bytes
    speech_file = io.BytesIO()
    speech.write_to_fp(speech_file)
    speech_bytes = speech_file.getvalue()
    speech_base64 = base64.b64encode(speech_bytes).decode('utf-8')

    # Result
    result = {'image': image_base64,
              'result_image': result_image_base64,
              'text': result_text,
              'speech': speech_base64
              }

    return result


@app.route('/', methods=["GET", "POST"])
def index():

    if request.method == "POST":
        f = request.files["imageFile"]

        # Load the image
        try:
            img = PIL.Image.open(io.BytesIO(f.read()))

        except PIL.UnidentifiedImageError:
            return render_template("index.html", error="Invalid Image")

        result = getResult(img, f)

        return render_template("index.html", result=result)

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
