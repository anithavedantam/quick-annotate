import os
import csv
from flask import Flask, url_for, render_template, jsonify, request
from datetime import datetime
import uuid

app = Flask(__name__)

ANNOTATIONS_PATH = "annotations.csv"

# Create annotations file if it doesn't exist
if not os.path.exists(ANNOTATIONS_PATH):
    with open(ANNOTATIONS_PATH, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(['id', 'timestamp', 'image_name', 'class','x', 'y', 'width', 'height'])

@app.route("/")
def index():
    image_url = url_for("static", filename="sample.jpeg")
    return render_template("index.html", image_url=image_url)

@app.route('/save_annotation', methods=['POST'])
def save_annotation():
    data = request.json
    timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")
    image_name = data.get('image_name', 'sample.jpeg')
    label = data.get('label', 'vehicle')
    x = data['x']
    y = data['y']
    width = data['width']
    height = data['height']
    annotation_id = data.get('id', str(uuid.uuid4()))

    with open(ANNOTATIONS_PATH, mode='a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([annotation_id, timestamp, image_name, label, x, y, width, height])

    return jsonify(status='success')

@app.route('/update_annotation', methods=['POST'])
def update_annotation():
    data = request.json
    annotation_id = data['id']

    updated_rows = []
    with open(ANNOTATIONS_PATH, mode='r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            if row[0] == annotation_id:
                updated_rows.append([
                    annotation_id,
                    datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f"),
                    data['image_name'],
                    data['label'],
                    data['x'],
                    data['y'],
                    data['width'],
                    data['height']
                ])
            else:
                updated_rows.append(row)
    
    # Write updated rows back to the file
    with open(ANNOTATIONS_PATH, mode='w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(updated_rows)
    return jsonify(status='updated')


def main():
    app.run(debug=True)


if __name__ == "__main__":
    main()
