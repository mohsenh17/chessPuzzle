import glob
from PIL import Image
from keras.preprocessing.image import load_img
from keras.preprocessing.image import img_to_array
pieces2OneHotDict = {
    'black_bishop':[0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    'black_king':[0,0,0,0,0,0,0,0,0,0,0,0,1,0],
    'black_knight':[0,0,0,0,0,0,0,0,0,0,0,1,0,0],
    'black_pawn':[0,0,0,0,0,0,0,0,0,0,1,0,0,0],
    'black_queen':[0,0,0,0,0,0,0,0,0,1,0,0,0,0],
    'black_rook':[0,0,0,0,0,0,0,0,1,0,0,0,0,0],
    'empty':[0,0,0,0,0,0,0,1,0,0,0,0,0,0],
    'white_bishop':[0,0,0,0,0,0,1,0,0,0,0,0,0,0],
    'white_king':[0,0,0,0,0,1,0,0,0,0,0,0,0,0],
    'white_knight':[0,0,0,0,1,0,0,0,0,0,0,0,0,0],
    'white_pawn':[0,0,0,1,0,0,0,0,0,0,0,0,0,0],
    'white_queen':[0,0,1,0,0,0,0,0,0,0,0,0,0,0],
    'white_rook':[0,1,0,0,0,0,0,0,0,0,0,0,0,0],
    'other':[1,0,0,0,0,0,0,0,0,0,0,0,0,0]
}
X_train = []
X_val = []
X_test = []

y_train = []
y_val = []
y_test = []
for piece in pieces2OneHotDict.keys():
    portion = 0
    for item in glob.glob('dataset/black_square/{}/*'.format(piece)):
        if portion == 10:
            portion = 0
        portion+=1
        if portion < 9:
            y_train.append(pieces2OneHotDict[piece])
            img = load_img(item)
            X_train.append(img_to_array(img))
        elif portion == 9:
            y_val.append(pieces2OneHotDict[piece])
            img = load_img(item)
            X_val.append(img_to_array(img))
        else:
            y_test.append(pieces2OneHotDict[piece])
            img = load_img(item)
            X_test.append(img_to_array(img))
    portion = 0
    for item in glob.glob('dataset/white_square/{}/*'.format(piece)):
        if portion == 10:
            portion = 0
        portion+=1
        if portion < 9:
            y_train.append(pieces2OneHotDict[piece])
            img = load_img(item)
            X_train.append(img_to_array(img))
        elif portion == 9:
            y_val.append(pieces2OneHotDict[piece])
            img = load_img(item)
            X_val.append(img_to_array(img))
        else:
            y_test.append(pieces2OneHotDict[piece])
            img = load_img(item)
            X_test.append(img_to_array(img))

