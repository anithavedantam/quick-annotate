import os
import csv
from flask import Flask, url_for, render_template

app = Flask(__name__)

ANNOTATIONS_PATH = "annotations.csv"

# draw bounding boxes on images
# def draw_bounding_boxes(image, annotations):
#     pass

# save annotations to csv
# def save_annotations(annotations):
#     pass

@app.route("/")
def index():
    image_url = url_for("static", filename="sample.jpeg")
    return render_template("index.html", image_url=image_url)

def main():
    app.run(debug=True)


if __name__ == "__main__":
    main()
