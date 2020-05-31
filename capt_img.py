import cv2
from datetime import datetime
import pickle



face_cascade = cv2.CascadeClassifier('venv\Lib\site-packages\cv2\data/haarcascade_frontalface_alt2.xml')
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("trainer.yml")



with open("labels.pickle", 'rb') as file:
    actual_labels = pickle.load(file)
    print(actual_labels.items)
    labels = {v:k for k,v in actual_labels.items()}


cap= cv2.VideoCapture(1)
while (True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    now = datetime.now()
    pic_num = now.strftime("%d%m%y_%H%M%S")

    # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # faces = face_cascade.detectMultiScale(gray, scaleFactor=1.05, minNeighbors=5)
    # for (x, y, w, h) in faces:
    #     print(x, y, w, h)
    #     roi_gray = gray[y:y+h, x:x+w]
    #     roi_color = frame[y:y+h, x:x+w]
    #
    #     #id_,conf = recognizer.predict(roi_gray)
    #     # if conf>=45 and conf<=85:
    #     # print(id_, conf, sep='------', end='\n')
    #     # print(labels[id_])
    #     # font = cv2.FONT_HERSHEY_SIMPLEX
    #     # name = labels[id_]
    #     # color = (255, 0, 255)
    #     # thickness = 4
    #     # cv2.putText(frame, name, (x,y), font, 1, color, thickness, cv2.LINE_AA)
    #
    #     end_coord_x = x + w
    #     end_coord_y = y + h
    #     rect_color = (255, 255, 255)
    #     rect_thickness = 4
    #     cv2.rectangle(gray, (x, y), (end_coord_x, end_coord_y), rect_color, rect_thickness)
    img_item = "capture_image\ IMG_" + str(pic_num) + ".png"
    cv2.imwrite(img_item, frame)

    cv2.imshow('frame', frame)
    if cv2.waitKey(20) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()


''' for video capturing'''

# cap = cv2.VideoCapture(0 or 1)
#
# # Get the Default resolutions
# frame_width = int(cap.get(3))
# frame_height = int(cap.get(4))
#
# # Define the codec and filename.
# out = cv2.VideoWriter('output.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 10, (frame_width,frame_height))
#
# while(cap.isOpened()):
#     ret, frame = cap.read()
#     if ret==True:
#
#         # write the  frame
#         out.write(frame)
#
#         cv2.imshow('frame',frame)
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break
#     else:
#         break
#
# # Release everything if job is finished
# cap.release()
# out.release()
# cv2.destroyAllWindows()