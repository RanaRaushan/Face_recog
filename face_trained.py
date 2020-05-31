import cv2
import os
import numpy as np
from PIL import Image
import pickle


def main_train():

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    image_DIR = os.path.join(BASE_DIR,'to_train_image')

    face_cascade = cv2.CascadeClassifier('venv\Lib\site-packages\cv2\data/haarcascade_frontalface_alt2.xml')
    recognizer = cv2.face.LBPHFaceRecognizer_create()


    def face_train():
        current_id = 0
        label_ids = {}
        y_labels = []
        x_train = []
        for root, dirs, files in os.walk(image_DIR):
            for file in files:
                if file.endswith('png') or file.endswith('jpg'):
                    path = os.path.join(root, file)
                    label = os.path.basename(root).lower() # or label = os.path.basename(os.path.dirname(path)).lower()
                    #print(label, '----',path)
                    if not label in label_ids:
                        label_ids[label] = current_id
                        current_id += 1
                    id_ = label_ids[label]
                    # print(id_)
                    # print(label_ids)
                    # y_labels.append(label)
                    # x_train.append(path)
                    pil_image = Image.open(path).convert("L") #grayscale
                    size = (800, 800)
                    final_image = pil_image.resize(size, Image.ANTIALIAS)
                    image_array = np.array(final_image, "uint8")
                    #print(image_array)
                    faces = face_cascade.detectMultiScale(image_array, scaleFactor=1.05, minNeighbors=5)

                    for x,y,w,h  in faces:
                        roi = image_array[y:y+h, x:x+w]
                        x_train.append(roi)
                        # print(x_train)
                        # print(y_labels)
                        y_labels.append(id_)
                        ch = "Training..."
                        print(ch)
        return label_ids, x_train, y_labels

    # print(x_train)
    # print(y_labels)
    label_ids, x_train, y_labels = face_train()
    with open("labels.pickle", 'wb') as file:
        pickle.dump(label_ids, file)

    recognizer.train(x_train, np.array(y_labels))
    recognizer.save("trainer.yml")
    print("Successfully Trained")


main_train()