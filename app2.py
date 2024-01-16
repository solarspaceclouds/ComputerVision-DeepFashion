from flask import Flask, render_template, request, send_from_directory, url_for
import os
from PIL import Image
import numpy as np

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['PROCESSED_FOLDER'] = 'processed'

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['PROCESSED_FOLDER'], exist_ok=True)

def process_images(shirt_image_path, artprint_image_path, output_path):
    # Load the original shirt image
    original_img = Image.open(shirt_image_path)
    original_img = np.array(original_img)

    # Load the segmentation map, assuming it's named similarly to the shirt image
    segm_path = shirt_image_path.replace('.jpg', '_segm.png')
    segm = Image.open(segm_path)
    segm = np.array(segm)

    # Define the label for the 'top' (shirt)
    top_label = 1

    # Create a mask for the 'top' label
    top_mask = (segm == top_label)

    # Invert the 'top' mask to get the non-'top' (background) mask
    background_mask = ~top_mask

    # Apply the background mask to the original image
    shirt_with_non_top_bg = original_img.copy()
    shirt_with_non_top_bg[background_mask] = 0  # Set background pixels to black

    # Load the art print image
    print_img = Image.open(artprint_image_path)
    print_img = np.array(print_img)

    # Resize the print image to match the size of the original shirt image
    print_img = Image.fromarray(print_img)
    print_img = print_img.resize((original_img.shape[1], original_img.shape[0]))

    # Convert the print image to a NumPy array
    print_img = np.array(print_img)[:,:,:3]

    # Overlay the shirt on top of the print image
    overlayed_img = print_img.copy()
    overlayed_img[top_mask] = original_img[top_mask]

    # Save the overlayed image
    overlayed_img = Image.fromarray(overlayed_img)
    overlayed_img.save(output_path)
    
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        shirt_image_file = request.files['shirt_image']
        artprint_image_file = request.files['artprint_image']

        shirt_image_path = os.path.join(app.config['UPLOAD_FOLDER'], shirt_image_file.filename)
        artprint_image_path = os.path.join(app.config['UPLOAD_FOLDER'], artprint_image_file.filename)

        shirt_image_file.save(shirt_image_path)
        artprint_image_file.save(artprint_image_path)

        return render_template('preview2.html', 
                               shirt_image=shirt_image_file.filename, 
                               artprint_image=artprint_image_file.filename)
    return render_template('upload2.html')

@app.route('/process', methods=['POST'])
def process():
    shirt_image = request.form['shirt_image']
    artprint_image = request.form['artprint_image']

    shirt_image_path = os.path.join(app.config['UPLOAD_FOLDER'], shirt_image)
    artprint_image_path = os.path.join(app.config['UPLOAD_FOLDER'], artprint_image)
    processed_image_path = os.path.join(app.config['PROCESSED_FOLDER'], 'processed_image.png')

    process_images(shirt_image_path, artprint_image_path, processed_image_path)

    return render_template('display2.html', filename='processed_image.png')


@app.route('/processed/<filename>')
def processed_file(filename):
    return send_from_directory(app.config['PROCESSED_FOLDER'], filename)



if __name__ == '__main__':
    app.run(debug=True)
