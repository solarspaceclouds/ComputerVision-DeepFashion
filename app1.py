from flask import Flask, redirect, render_template, request, send_from_directory, url_for
import os
from PIL import Image
import numpy as np
import cv2

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MODIFIED_FOLDER'] = 'modified'

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['MODIFIED_FOLDER'], exist_ok=True)

def change_top_color_hsv(hsv_img, segm, new_hue, new_saturation):
    hsv_img = hsv_img.copy()
    top_label = 1  # Label for 'top'
    mask = segm == top_label
    hsv_img[:, :, 0][mask] = new_hue
    hsv_img[:, :, 1][mask] = new_saturation
    return hsv_img


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)
            return redirect(url_for('modify_image', filename=file.filename))
    return render_template('upload.html')

@app.route('/modify/<filename>', methods=['GET', 'POST'])
def modify_image(filename):
    if request.method == 'POST':
        # Handle color selection
        new_hue = int(request.form.get('hue'))
        new_saturation = int(request.form.get('saturation'))

        # Load the original and segmentation images
        original_img_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        segm_path = os.path.join(app.config['UPLOAD_FOLDER'],  filename[:-4] + "_segm.png")
        
        original_img = np.array(Image.open(original_img_path))
        segm = np.array(Image.open("" + segm_path))
        hsv_img = cv2.cvtColor(original_img, cv2.COLOR_RGB2HSV)

        # Apply the color change function
        modified_hsv_img = change_top_color_hsv(hsv_img, segm, new_hue, new_saturation)
        modified_rgb_img = cv2.cvtColor(modified_hsv_img, cv2.COLOR_HSV2RGB)

        # Save the modified image
        modified_img_path = os.path.join(app.config['MODIFIED_FOLDER'], filename)
        Image.fromarray(modified_rgb_img).save(modified_img_path)
        
        # filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        #     file.save(filepath)
        
        return redirect(url_for('download_image', filename=filename))

    return render_template('modify.html', filename=filename)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/download/<filename>')
def download_image(filename):
    return send_from_directory(app.config['MODIFIED_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)