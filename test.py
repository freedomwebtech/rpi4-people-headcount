import cv2
import numpy as np
from tracker import*
import cvzone
import time

bg_subtractor = cv2.createBackgroundSubtractorMOG2(history=200, varThreshold=40)

# Open a video capture
video_capture = cv2.VideoCapture('headcount2.mp4')
def RGB(event, x, y, flags, param):
    if event == cv2.EVENT_MOUSEMOVE :  
        point = [x, y]
        print(point)
  
        

cv2.namedWindow('RGB')
cv2.setMouseCallback('RGB', RGB)
tracker=Tracker()
cy1=253  
cy2=223
cy3=121

offset=6

going_in={}
counter1=[]
going_out={}
counter2=[]


count=0
while True:
    ret, frame = video_capture.read()
    if not ret:
        break
    count += 1
    if count % 3 != 0:
        continue
    
    frame=cv2.resize(frame,(600,480))
  
    mask = bg_subtractor.apply(frame)
    _, mask = cv2.threshold(mask, 245, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    list=[]
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 500:
#           cv2.drawContours(frame, [cnt], -1, (0, 255, 0), 2)
           x, y, w, h = cv2.boundingRect(cnt)
           list.append([x,y,w,h])
    bbox_idx=tracker.update(list)
    for bbox in bbox_idx:
        x1,y1,x2,y2,id=bbox
        cx=int(x1+x1+x2)//2
        cy=int(y1+y1+y2)//2
#        cv2.rectangle(frame, (x1, y1), (x2+x1, y2+y1), (255, 0, 0), 3)
#        cvzone.putTextRect(frame,f'{id}',(x1,y1),2,2)
#        cv2.circle(frame,(cx,cy),4,(255,0,255),-1)
        
        
        if cy1<(cy+offset) and cy1>(cy-offset):
           going_out[id]=(cx,cy)
        if id in going_out:
           if cy3<(cy+offset) and cy3>(cy-offset):
              cv2.rectangle(frame, (x1, y1), (x2+x1, y2+y1), (255, 0, 255), 3)
              cvzone.putTextRect(frame,f'{id}',(x1,y1),2,2)
              cv2.circle(frame,(cx,cy),4,(255,0,255),-1)
              counter1.append(id)
        if cy2<(cy+offset) and cy2>(cy-offset):      
           going_in[id]=(cx,cy)
        if id in going_in:
           if cy1<(cy+offset) and cy1>(cy-offset):
              cv2.rectangle(frame, (x1, y1), (x2+x1, y2+y1), (0, 0, 255), 3)
              cvzone.putTextRect(frame,f'{id}',(x1,y1),2,2)
              cv2.circle(frame,(cx,cy),4,(255,0,255),-1)
              counter2.append(id)
    cv2.line(frame,(10,cy1),(598,cy1),(255,255,255),2)
    cv2.line(frame,(8,cy2),(598,cy2),(255,255,255),2)
    cv2.line(frame,(10,cy3),(596,cy3),(255,255,255),2)
    
    cvzone.putTextRect(frame,f'line1',(10,253),1,1)
    cvzone.putTextRect(frame,f'line2',(288,225),1,1)
    cvzone.putTextRect(frame,f'line3',(552,118),1,1)


    p_out=len(counter1)
    p_in=len(counter2)
    cvzone.putTextRect(frame,f'P_OUT:-{p_out}',(50,60),1,1)
    cvzone.putTextRect(frame,f'P_IN:-{p_in}',(428,56),1,1)


    cv2.imshow('RGB', frame)
    time.sleep(0.1)
    if cv2.waitKey(1) & 0xFF == 27:  # Press 'Esc' to exit
        break

# Release the video capture and close windows
video_capture.release()
cv2.destroyAllWindows()
