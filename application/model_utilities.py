import numpy as np
import cv2
from keras.models import load_model
import tensorflow as tf

global graph
graph = tf.get_default_graph()

model = load_model('../trained_model/model_weight.hdf5')

def predict(image):
    """
    :param img_path: str, path of image
    :return: json, prediction on image
    """

    # img = cv2.imread(img_path)
    img = np.copy(image)
    print(np.shape(img))
    img = resize_image(img, (224, 224))
    img = normalize(img)

    result = {}
    with graph.as_default():
        result = model.predict(img)

    p = result[0]
    p = np.sort(p)
    l = max(float(format(p[0], '.2f')), 1)
    h = min(float(format(p[-1], '.2f')), 10)
    m = float(format(p[1], '.2f'))
    # print("Prediction:" + str(((result[0]))))

    return {'Pessimistic': l, 'Optimistic': h, 'real': m}


def resize_image(img, size):
    img = cv2.resize(img, size)
    return img


def normalize(img):
    img = np.float64(img)
    img = np.expand_dims(img, axis=0)
    img = img / 255.0
    return img

if __name__ == '__main__':
    a = predict('./tests/img.jpg')
    print(a)
