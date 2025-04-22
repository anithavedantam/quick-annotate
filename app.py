import os
import csv
import json
from flask import Flask, url_for, render_template, jsonify, request, redirect
from datetime import datetime
import uuid

app = Flask(__name__)
IMAGE_FOLDER = "static/images"
ANNOTATIONS_PATH = "annotations.csv"

# Create annotations file if it doesn't exist
if not os.path.exists(ANNOTATIONS_PATH):
    with open(ANNOTATIONS_PATH, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(['image_name','id', 'timestamp', 'class','x', 'y', 'width', 'height'])

@app.route("/")
def index():
    images = os.listdir(IMAGE_FOLDER)
    # Get the index of the image to display
    img_index = int(request.args.get('img_index', 0))
    
    # If the index is out of range, set it to first image
    if img_index < 0:
        img_index = 0
    # If the index is out of range, set it to last image
    if img_index >= len(images):
        img_index = len(images) - 1
    
    # Get the image name
    image_name = images[img_index]
    
    # Get the image url
    image_url = url_for("static", filename=f'images/{image_name}')

    # Render the index.html template with the image url
    return render_template("index.html", 
                           image_url=image_url,
                           image_name=image_name,
                           img_index=img_index,
                           total_images=len(images))

@app.route('/save_annotation', methods=['POST'])
def save_annotation():
    data = request.json
    timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")
    image_name = data.get('image_name', 'unknown.jpeg')
    label = data.get('label', 'vehicle')
    x = data['x']
    y = data['y']
    width = data['width']
    height = data['height']
    annotation_id = data.get('id', str(uuid.uuid4()))

    with open(ANNOTATIONS_PATH, mode='a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([image_name, annotation_id, timestamp, label, x, y, width, height])

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
                    data['image_name'],
                    annotation_id,
                    datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f"),
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

@app.route('/delete_annotation', methods=['POST'])
def delete_annotation():
    data = request.json
    annotataion_id = data['id']
    updated_rows = []

    # Filter out the annotation to be deleted
    with open(ANNOTATIONS_PATH, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)

        for row in reader:
            if row[0] != annotataion_id:
                updated_rows.append(row)
    
    # Write updated rows back to the file
    with open(ANNOTATIONS_PATH, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(updated_rows)
    
    return jsonify(status='deleted')

@app.route('/save_annotations_per_image', methods=['POST'])
def save_annotations_per_image():
    data = request.json
    image_name = data['image_name']
    annotations = data['annotations']

    updated_rows = []
    exists = False

    with open(ANNOTATIONS_PATH, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)

        for row in reader:
            if row[0] == image_name:
                updated_rows.append(row)
                exists = True
                updated_rows.append([image_name, json.dumps(annotations)])
            else:
                updated_rows.append(row)
    
    if not exists:
        updated_rows.append([image_name, json.dumps(annotations)])
    
    # Write updated rows back to the file
    with open(ANNOTATIONS_PATH, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(updated_rows)
    
    return jsonify(status='saved')
    

def main():
    app.run(debug=True)


if __name__ == "__main__":
    main()
