import cv2
path2img = 'chessPieces/BBB.jpg'
image = cv2.imread(path2img)
blur = cv2.pyrMeanShiftFiltering(image, 11, 21)
gray = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY)
thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cv2.imshow('thresh',thresh)
cv2.imshow('gray',gray)
cv2.imshow('cnts',blur)
cv2.waitKey()