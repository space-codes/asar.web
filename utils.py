from models import *
import os
from sqlalchemy.orm import sessionmaker
from sqlalchemy import *
#from back_end import *
from numpy import linalg as LA
import numpy as np
from tensorflow.keras import backend as K
from tensorflow.keras import Model
from tensorflow.keras.layers import Dense, Dropout, MaxPooling2D, Flatten, Input, Conv2D
from tensorflow_addons.layers import SpatialPyramidPooling2D
from phoc_label_generator import phoc_generate_label
from phos_label_generator import phos_generate_label
import cv2

global s
Session = sessionmaker(bind=engine)
s = Session()


# Cosine simialirity * 1000
def similarity(x, y):
    return 1000 * np.dot(x, y) / (LA.norm(x) * LA.norm(y))

def get_comb_label(x):
    phos_labels=phos_generate_label(x)
    phoc_labels=phoc_generate_label(x)
    return np.concatenate((phos_labels,phoc_labels),axis=0)

'''
save image as a thumbnail
'''
def save_thumbnail(user, img):
        # img = cv2.imread(loc)
        max_height = 200
        if(img.shape[0] < img.shape[1]):
            img = np.rot90(img)
        hpercent = (max_height/float(img.shape[0]))
        wsize = int((float(img.shape[1])*float(hpercent)))
        img = cv2.resize(img, (wsize, max_height))
        newname = str(len(os.listdir('static/users/{}/'.format(user)))+1)
        cv2.imwrite('static/users/{}/{}.png'.format(user, newname), img)
        return 'static/users/{}/{}.png'.format(user, newname)

'''
save an image
'''
def save_image(user, img):
    newname = str(len(os.listdir('static/users/{}/'.format(user)))+1)
    cv2.imwrite('static/users/{}/{}.png'.format(user,newname),img)

def ok(username):
    res = s.query(User).filter(User.username==username)
    print(type(res))
    identity = ""
    for r in res:
        identity = r.username
    if identity == username:
        print('ok')
    s.close()


def get_all_transcripts():
    #engine = create_engine('sqlite:///asar.db', echo=True)
    #Session = sessionmaker(bind=engine)
    #s = Session()
    transcripts = s.query(Corpus).with_entities(Corpus.word).all()
    transcripts = [row[0] for row in transcripts]
    s.close()
    return transcripts


def build_phosc_model():
    if K.image_data_format() == 'channels_first':
        input_shapes = (3, 80, 90)
    else:
        input_shapes = (80, 90, 3)
    inp = Input(shape=input_shapes)
    model = Conv2D(64, (3, 3), padding='same', activation='relu')(inp)
    model = Conv2D(64, (3, 3), padding='same', activation='relu')(model)
    model = (MaxPooling2D(pool_size=(2, 2), strides=2))(model)
    model = (Conv2D(128, (3, 3), padding='same', activation='relu'))(model)
    model = (Conv2D(128, (3, 3), padding='same', activation='relu'))(model)
    model = (MaxPooling2D(pool_size=(2, 2), strides=2))(model)
    model = (Conv2D(256, (3, 3), padding='same', activation='relu'))(model)
    model = (Conv2D(256, (3, 3), padding='same', activation='relu'))(model)
    model = (Conv2D(256, (3, 3), padding='same', activation='relu'))(model)
    model = (Conv2D(256, (3, 3), padding='same', activation='relu'))(model)
    model = (Conv2D(256, (3, 3), padding='same', activation='relu'))(model)
    model = (Conv2D(256, (3, 3), padding='same', activation='relu'))(model)
    model = (Conv2D(512, (3, 3), padding='same', activation='relu'))(model)
    model = (Conv2D(512, (3, 3), padding='same', activation='relu'))(model)
    model = (Conv2D(512, (3, 3), padding='same', activation='relu'))(model)
    model = (SpatialPyramidPooling2D([1, 2, 4]))(model)
    model = (Flatten())(model)

    # PHOS component
    phosnet_op = Dense(4096, activation='relu')(model)
    phosnet_op = Dropout(0.5)(phosnet_op)
    phosnet_op = Dense(4096, activation='relu')(phosnet_op)
    phosnet_op = Dropout(0.5)(phosnet_op)
    phosnet_op = Dense(270, activation='relu', name="phosnet")(phosnet_op)

    # PHOC component
    phocnet = Dense(4096, activation='relu')(model)
    phocnet = Dropout(0.5)(phocnet)
    phocnet = Dense(4096, activation='relu')(phocnet)
    phocnet = Dropout(0.5)(phocnet)
    phocnet = Dense(730, activation='sigmoid', name="phocnet")(phocnet)
    model = Model(inputs=inp, outputs=[phosnet_op, phocnet])
    return model