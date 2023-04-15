from flask import Flask, render_template, request
import io
import PIL

# Custom imports
import Analyze

app = Flask(__name__)


@app.route('/', methods=["GET", "POST"])
def index():

    page = "index.html"

    if request.method == "POST":

        # Get the image file from the request
        f = request.files["imageFile"]

        # Load the image
        try:
            img = PIL.Image.open(io.BytesIO(f.read()))
        except PIL.UnidentifiedImageError:
            return render_template(page, error="Invalid Image")
        except Exception:
            return render_template(page, error="Unknown Error")

        result = Analyze.getResult(img, f)

        return render_template(page, result=result)

    return render_template(page)


if __name__ == "__main__":
    app.run(debug=True)
