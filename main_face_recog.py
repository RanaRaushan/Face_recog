import cv2
import pickle


def main_face_recog():
    face_cascade = cv2.CascadeClassifier('venv\Lib\site-packages\cv2\data/haarcascade_frontalface_alt2.xml')
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read("trainer.yml")

    # labels = {"Person_name": 1}
    with open("labels.pickle", 'rb') as file:
        actual_labels = pickle.load(file)
        labels = {v:k for k,v in actual_labels.items()}

    cap = cv2.VideoCapture(1)

    while (1):
        # Capture frame-by-frame
        ret, frame = cap.read()

        # img1 = cv2.imread("5.jpg", 1)


        # Our operations on the frame come here
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)
        for (x, y, w, h) in faces:
            #print(x, y, w, h)
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = frame[y:y+h, x:x+w]

            id_,conf = recognizer.predict(roi_gray)
            print(conf)
            if conf>=45 and conf<=60:
                # print(id_, conf, sep='------', end='\n')
                # print(labels[id_])
                font = cv2.FONT_HERSHEY_SIMPLEX
                name = labels[id_]
                color = (255, 0, 255)
                thickness = 4
                cv2.putText(frame, name, (x, y+100), font, 1, color, thickness, cv2.LINE_AA)
                end_coord_x = x+w
                end_coord_y = y+h
                rect_color = (255, 0, 0)
                rect_thickness = 4
                cv2.rectangle(frame, (x, y), (end_coord_x, end_coord_y), rect_color, rect_thickness)
                return labels[id_]

        #Display the resulting frame
        cv2.imshow('frame', frame)
        if cv2.waitKey(20) & 0xFF == ord('q'):
            break

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()


# main_face_recog()







