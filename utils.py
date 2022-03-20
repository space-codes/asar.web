from table_def import *
import os
from sqlalchemy.orm import sessionmaker
from sqlalchemy import *
from back_end import *
from numpy import linalg as LA

global s
Session = sessionmaker(bind=engine)
s = Session()


# Cosine simialirity * 1000
def similarity(x, y):
    return 1000 * np.dot(x, y) / (LA.norm(x) * LA.norm(y))

'''
save image as a thumbnail
'''
def save_thumbnail(user, loc):
        img = cv2.imread(loc)
        max_height = 200
        if(img.shape[0] < img.shape[1]):
            img = np.rot90(img)
        hpercent = (max_height/float(img.shape[0]))
        wsize = int((float(img.shape[1])*float(hpercent)))
        img = cv2.resize(img,(wsize,max_height))
        newname = str(len(os.listdir('static/users/{}/'.format(user)))+1)
        cv2.imwrite('static/users/{}/{}.png'.format(user,newname),img)

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

def get_all_transcripts():
    engine = create_engine('sqlite:///asar.db', echo=True)
    Session = sessionmaker(bind=engine)
    s = Session()
    transcripts = s.query(Corpus).with_entities(Corpus.word).all()
    return transcripts