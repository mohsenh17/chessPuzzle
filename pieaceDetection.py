import glob
import numpy as np
from PIL import Image
from keras.preprocessing.image import load_img
from keras.preprocessing.image import img_to_array
from keras.models import Sequential
from keras.layers import Dense, Conv2D, Flatten
pieces2OneHotDict = {
    'black_bishop':[0,0,0,0,0,0,0,0,0,0,0,0,1],
    'black_king':[0,0,0,0,0,0,0,0,0,0,0,1,0],
    'black_knight':[0,0,0,0,0,0,0,0,0,0,1,0,0],
    'black_pawn':[0,0,0,0,0,0,0,0,0,1,0,0,0],
    'black_queen':[0,0,0,0,0,0,0,0,1,0,0,0,0],
    'black_rook':[0,0,0,0,0,0,0,1,0,0,0,0,0],
    'empty':[0,0,0,0,0,0,1,0,0,0,0,0,0],
    'white_bishop':[0,0,0,0,0,1,0,0,0,0,0,0,0],
    'white_king':[0,0,0,0,1,0,0,0,0,0,0,0,0],
    'white_knight':[0,0,0,1,0,0,0,0,0,0,0,0,0],
    'white_pawn':[0,0,1,0,0,0,0,0,0,0,0,0,0],
    'white_queen':[0,1,0,0,0,0,0,0,0,0,0,0,0],
    'white_rook':[1,0,0,0,0,0,0,0,0,0,0,0,0],
}

embd2pieces = ['black_bishop',
    'black_king',
    'black_knight',
    'black_pawn',
    'black_queen',
    'black_rook',
    'empty',
    'white_bishop',
    'white_king',
    'white_knight',
    'white_pawn',
    'white_queen',
    'white_rook',
]
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
            img = load_img(item, color_mode="grayscale")
            X_train.append(img_to_array(img))
        elif portion == 9:
            y_val.append(pieces2OneHotDict[piece])
            img = load_img(item, color_mode="grayscale")
            X_val.append(img_to_array(img))
        else:
            y_test.append(pieces2OneHotDict[piece])
            img = load_img(item, color_mode="grayscale")
            X_test.append(img_to_array(img))
    portion = 0
    for item in glob.glob('dataset/white_square/{}/*'.format(piece)):
        if portion == 10:
            portion = 0
        portion+=1
        if portion < 9:
            y_train.append(pieces2OneHotDict[piece])
            img = load_img(item, color_mode="grayscale")
            X_train.append(img_to_array(img))
        elif portion == 9:
            y_val.append(pieces2OneHotDict[piece])
            img = load_img(item, color_mode="grayscale")
            X_val.append(img_to_array(img))
        else:
            y_test.append(pieces2OneHotDict[piece])
            img = load_img(item, color_mode="grayscale")
            X_test.append(img_to_array(img))

#create model
model = Sequential()
#add model layers
model.add(Conv2D(64, kernel_size=3, activation='relu', input_shape=(32,32,1)))
model.add(Conv2D(32, kernel_size=3, activation='relu'))
model.add(Flatten())
model.add(Dense(13, activation='softmax'))
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
model.fit(np.array(X_train), np.array(y_train), validation_data=(np.array(X_val), np.array(y_val)), epochs=5)

for item in glob.glob('chessPieces/*.jpg'):

    img = load_img(item, target_size=(32,32), color_mode="grayscale")
    test = img_to_array(img).reshape(1,32,32,1)
    pred = model.predict(test)[0]
    pred = np.where(np.array(pred) > 0.5, 1, 0)
    predPiece = embd2pieces[12-np.argmax(pred)]
    print(predPiece, item, pred)
