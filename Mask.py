import cv2
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array
import imutils

face_cascade = cv2.CascadeClassifier("D:\Python\LB ML\CV\Open CV\Smile\haarcascade_frontalface_default.xml")


def detect(gray, frame):
    faces = face_cascade.detectMultiScale(gray, 1.3,5)
    for (x,y,w,h) in faces:
        face = frame[y:y+h,x:x+w]
        face = cv2.cvtColor(face,cv2.COLOR_BGR2RGB)
        face = cv2.resize(face,(224,224))
        face = img_to_array(face,dtype='float32')
        face = face.reshape(1,224,224,3)/255.0
        model = load_model("D:\\Python\\LB ML\\DL\\CNN\\Face_Mask.h5")
        pred = model.predict(face)
        pred = pred[0,0]
        label = f'{pred*100:2.2f}'
        if pred > 0.5:
            cv2.putText(frame,label+ " Please Wear Mask",(x,y),cv2.FONT_HERSHEY_SIMPLEX, 0.45,(0,0,255),1)
            cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),2)
        else:
            cv2.putText(frame,label+ "  Good",(x,y),cv2.FONT_HERSHEY_SIMPLEX, 0.45,(0,255,0),1)
            cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
        
    return frame

video = cv2.VideoCapture(0)

while True:
    success,frame = video.read()
    frame = imutils.resize(frame, width=400)
    if not success:
        break
    else:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        canvas = detect(gray,frame)
        cv2.imshow('Face',canvas)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

video.release()
cv2.destroyAllWindows()
