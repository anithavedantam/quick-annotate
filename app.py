import os
import csv
from flask import Flask, url_for, render_template, jsonify, request
from datetime import datetime

app = Flask(__name__)

ANNOTATIONS_PATH = "annotations.csv"

# Create annotations file if it doesn't exist
if not os.path.exists(ANNOTATIONS_PATH):
    with open(ANNOTATIONS_PATH, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(['timestamp', 'image_name', 'x', 'y', 'width', 'height'])

@app.route("/")
def index():
    image_url = url_for("static", filename="sample.jpeg")
    return render_template("index.html", image_url=image_url)

@app.route('/save_annotation', methods=['POST'])
def save_annotation():
    data = request.json
    timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")
    image_name = data.get('image_name', 'sample.jpeg')
    x = data['x']
    y = data['y']
    width = data['width']
    height = data['height']

    with open(ANNOTATIONS_PATH, mode='a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([timestamp, image_name, x, y, width, height])

    return jsonify(status='success')

def main():
    app.run(debug=True)


if __name__ == "__main__":
    main()
