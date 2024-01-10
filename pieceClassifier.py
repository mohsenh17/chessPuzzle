import glob
import numpy as np
from PIL import Image
import keras
from keras.preprocessing.image import load_img, img_to_array
from keras.models import Sequential
from keras.layers import Dense, Conv2D, Flatten
from keras.callbacks import ModelCheckpoint
from chess_game import *

class ChessPieceClassifier:
    def __init__(self):
        self.pieces2OneHotDict = {
            'black_bishop': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            'black_king':[0,0,0,0,0,0,0,0,0,0,0,0,1,0],
            'black_knight':[0,0,0,0,0,0,0,0,0,0,0,1,0,0],
            'black_pawn':[0,0,0,0,0,0,0,0,0,0,1,0,0,0],
            'black_queen':[0,0,0,0,0,0,0,0,0,1,0,0,0,0],
            'black_rook':[0,0,0,0,0,0,0,0,1,0,0,0,0,0],
            'empty_black':[0,0,0,0,0,0,0,1,0,0,0,0,0,0],
            'white_bishop':[0,0,0,0,0,0,1,0,0,0,0,0,0,0],
            'white_king':[0,0,0,0,0,1,0,0,0,0,0,0,0,0],
            'white_knight':[0,0,0,0,1,0,0,0,0,0,0,0,0,0],
            'white_pawn':[0,0,0,1,0,0,0,0,0,0,0,0,0,0],
            'white_queen':[0,0,1,0,0,0,0,0,0,0,0,0,0,0],
            'white_rook':[0,1,0,0,0,0,0,0,0,0,0,0,0,0],
            'empty_white':[1,0,0,0,0,0,0,0,0,0,0,0,0,0]
        }

        self.embd2pieces = [
            'black_bishop', 'black_king', 'black_knight', 'black_pawn',
            'black_queen', 'black_rook', 'empty_black', 'white_bishop',
            'white_king', 'white_knight', 'white_pawn', 'white_queen',
            'white_rook', 'empty_white'
        ]

        self.X_train = []
        self.X_val = []
        self.X_test = []

        self.y_train = []
        self.y_val = []
        self.y_test = []

        self.model = None

    def load_images(self, directory):
        for piece in self.pieces2OneHotDict.keys():
            portion = 0
            for item in glob.glob('dataset/{}/{}/*'.format(directory, piece)):
                if portion == 10:
                    portion = 0
                portion += 1
                self.y_train.append(self.pieces2OneHotDict[piece])
                img = load_img(item, color_mode="grayscale")
                self.X_train.append(img_to_array(img))

                if portion < 9:
                    pass
                elif portion == 9:
                    self.X_val.append(img_to_array(img))
                    self.y_val.append(self.pieces2OneHotDict[piece])
                else:
                    self.X_test.append(img_to_array(img))
                    self.y_test.append(self.pieces2OneHotDict[piece])
        print(len(self.X_train),len(self.X_val),len(self.X_test))
    def train(self):
        self.load_images('black_square')
        self.load_images('white_square')

        self.model = Sequential()
        self.model.add(Conv2D(64, kernel_size=3, activation='relu', input_shape=(32, 32, 1)))
        self.model.add(Conv2D(32, kernel_size=3, activation='relu'))
        self.model.add(Flatten())
        self.model.add(Dense(14, activation='softmax'))
        self.model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

        mc = ModelCheckpoint("models/CNN2piece", monitor='val_loss', mode='min', verbose=1, save_best_only=True)
        self.model.fit(np.array(self.X_train), np.array(self.y_train),
                       validation_data=(np.array(self.X_val), np.array(self.y_val)),
                       callbacks=[mc], shuffle=True, epochs=8)
    def detect(self, pieceImg):
        loaded_model = keras.saving.load_model("models/CNN2piece")
        test = img_to_array(pieceImg).reshape(1, 32, 32, 1)
        pred = loaded_model.predict(test)[0]
        pred = np.where(np.array(pred) > 0.5, 1, 0)
        if sum(pred)==0 or self.embd2pieces[13-np.argmax(pred)] == 'empty_white' or self.embd2pieces[13-np.argmax(pred)] == 'empty_black':
            predPiece = 'empty'
        else:
            predPiece = self.embd2pieces[13-np.argmax(pred)]
        print(predPiece)

# Create an instance of the class and process images
chess_classifier = ChessPieceClassifier()
chess_classifier.detect(load_img('chessPieces/BBB.jpg', target_size=(32,32), color_mode="grayscale"))
chess_classifier.detect(load_img('chessPieces/WRW.jpg', target_size=(32,32), color_mode="grayscale"))
