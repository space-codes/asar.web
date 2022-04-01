from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array
from utils import similarity, get_all_transcripts, get_comb_label, build_phosc_model
from segmentation import multi_line_ext, words_extract
from tensorflow_addons.layers import SpatialPyramidPooling2D
import numpy as np
import uuid
import cv2
import tensorflow as tf


'''This module is the main back-end, which handles classification and
    word/character extraction.
'''
global model
#if load_phosc_model:
model = build_phosc_model()
model.load_weights('model/phosc-model.h5')
#else:
#    model = load_model('model/phoc-model.h5', custom_objects={'SpatialPyramidPooling2D': SpatialPyramidPooling2D})

def classify(img, transcripts):
    ''' Classify a single word
        To make a prediction

    Args:
        img: The image to be classified
    Returns:
        out: The prediciton
    '''

    img = img_to_array(img)
    img = tf.image.resize(img, [110, 110])
    img = np.expand_dims(img, axis=0)
    y_pred=model.predict(img)
    y_pred=np.squeeze(np.concatenate((y_pred[0],y_pred[1]),axis=1))
    out = ''
    mx = 0
    for k in transcripts:
        temp = similarity(y_pred, get_comb_label(k))
        if temp > mx:
            mx = temp
            out = k
    return out


def get_result(path):
    ''' Classify all features from within an image

    This method classifies an image. It is split into three parts:
        1. detect image lines
        2. segment line to words
        2. classify the detected words using the phoc
        3. format the output
    Args:
        path: the location of the image to be classified
    Returns:
        result: the classified string
    '''
    output = ''
    img = cv2.imread(path)
    if np.mean(img) == 255:
        output = ''
    transcripts = get_all_transcripts()
    lines = multi_line_ext(img)
    for line in lines:
        arr = words_extract(line)
        if line != []:
            for a in arr:
                res = classify(a, transcripts)
                output += ' ' + res
            output += '\n'
    if output == '':
        output = 'Classification error'
    return output


def format_result(arr):
    '''Formats the prediciton result to a readable string

    Args:
        arr:a list of predicted chars sorted into lines

    Returns:
        string: the formatted string
    '''
    string = ''
    for a in arr:
        string += a
        string += '\n'
    string = string.strip()
    return string


def save_thumbnail(user, img):
    ''' Reduce the size of an image and generate a thumbnail.
    The image is saved to the users file. It is used in the hub page to
    display previous predictions.

    Args:
        user: the current user
        img: the image to be resized

    Returns:
        the location of the image
    '''

    max_height = 200
    if img.shape[0] < img.shape[1]:
        img = np.rot90(img)
    hpercent = max_height / float(img.shape[0])
    wsize = int(float(img.shape[1]) * float(hpercent))
    img = cv2.resize(img, (wsize, max_height))
    newname = uuid.uuid4()
    cv2.imwrite('static/users/{}/{}.png'.format(user, newname), img)
    return 'static/users/{}/{}.png'.format(user, newname)


# img = cv2.imread('image.png')
# transcripts = get_all_transcripts()
# lines = multi_line_ext(img)
# output = ''
# for line in lines:
#     output = ''
#     arr = words_extract(line)
#     if line != []:
#         for a in arr:
#             res = classify(a, transcripts)
#             output += ' ' + res


# img = cv2.imread('index.jpg')
# transcripts = get_all_transcripts()
# res = classify(img, transcripts)
# print(res)