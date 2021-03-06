from tensorflow.keras.applications import ResNet50
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.applications import imagenet_utils
from PIL import Image
import numpy as np
import flask
import io


app = flask.Flask(__name__)
model = None

def load_model():
    """Use global variable model to initialize it with ResNet50 model"""
    global model
    model = ResNet50(weights='imagenet')


def prepare_image(image, target):
    if image.mode != 'RGB':
        image = image.convert('RGB')
    image = image.resize(target)
    image = img_to_array(image)
    image = np.expand_dims(image, axis=0)
    image = imagenet_utils.preprocess_input(image)
    return image


@app.route('/predict', methods=['POST'])
def predict():
    data = {
        'success': False
    }

    if flask.request.method == 'POST':
        if flask.request.files.get("image"):

            # read the image in PIL format
            image = flask.request.files["image"].read()
            image = Image.open(io.BytesIO(image))

            # preprocess the image and prepare it for classification
            image = prepare_image(image, target=(224, 224))

            # classify the input image and then initialize the list
            # of predictions to return to the client

            preds = model.predict(image)
            results = imagenet_utils.decode_predictions(preds)
            data['predictions'] = []

            for imageID, label, prob in results[0]:
                r = {
                    'label': label,
                    'prob': float(prob)
                }
                data['predictions'].append(r)

            data['success'] = True

    return flask.jsonify(data)


if __name__ == "__main__":
    print(("* Loading Keras model and Flask starting server..."
           "please wait until server has fully started"))
    load_model()
    app.run()

