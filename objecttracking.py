
import dlib
import cv2

cap = cv2.VideoCapture(0)
tolerance=0.05
toleran=0.1
tracked = False
x_dev=0
y_dev=0


def first():
    while True:
        k,frame = cap.read()
        height, width, channels = frame.shape
        cv2.imshow("Tracking",frame)
    
        k = cv2.waitKey(1)
        if k == 27 :
            break
    cv2.destroyWindow("Tracking")

first()
k,frame = cap.read()
bbox= cv2.selectROI(frame)
gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
gray = cv2.GaussianBlur(gray, (5, 5), 0)
topLeftX, topLeftY,w,h = bbox

bottomRightX = topLeftX + w
bottomRightY = topLeftY + h
tracker = dlib.correlation_tracker()
dlib_rect = dlib.rectangle(topLeftX, topLeftY, bottomRightX,bottomRightY )

tracker.start_track(gray, dlib_rect)
cv2.namedWindow("Tracker")
while (True):
        cv2.destroyWindow("ROI selector")
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (5, 5), 0)

        ok = tracker.update(gray)
        img = cv2.cvtColor(gray, cv2.COLOR_BGR2RGB)
        if ok :
                timer = cv2.getTickCount()
                if tracked == True:
                    tracker.update(frame)
                    objectPosition = tracker.get_position()
                    x0  = int(objectPosition.left())
                    y0  = int(objectPosition.top())
                    x1 = int(objectPosition.right())
                    y1 = int(objectPosition.bottom())
                    cv2.rectangle(frame, (x0, y0), (x1, y1), (0, 0, 255), 2)
                    #garis tengah
                    frame = cv2.rectangle(frame, (0,int(480/2)-1), (640, int(480/2)+1), (127,127,127), -1)
                    frame = cv2.rectangle(frame, (int(640/2)-1,0), (int(640/2)+1,480), (127,127,127), -1)
                    #titik tengah
                    frame = cv2.circle(frame, (320,240), 7, (0,0,255), -1)
                    cv2.line(frame,(int(x0),int(y0)),(int(x1),int(y1)), (255,0,255),2)
                    cv2.line(frame,(int(x0),int(y1)),(int(x1),int(y0)), (255,0,255),2)
                    X=int((x0+x1)/2.0)
                    Y=int((y0+y1)/2.0)


                    x_dev=X-320
                    str_x='X: {}'.format(x_dev)
                    frame = cv2.putText(frame, str_x, (110, 460),cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
    
                    y_dev=240-Y
                    str_y='Y: {}'.format(y_dev)
                    frame = cv2.putText(frame, str_y, (330, 460),cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)    
               
               
                if (x_dev < 355 and x_dev > -355 and y_dev < 240 and y_dev > -240  ):
                    tracked = True
                else:
                    tracked = False
                cv2.putText(frame, "Fps:", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,0,255), 2);


                fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer);
                if fps>60: myColor = (20,230,20)
                elif fps>20: myColor = (230,20,20)
                else: myColor = (20,20,230)
                cv2.putText(frame,str(int(fps)), (75, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, myColor, 2);
        else:
            cv2.putText(frame, "Lost", (100, 75), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        cv2.imshow('Tracker',frame)
        
        ch = 0xFF & cv2.waitKey(1)
        if ch == ord("r"):
            cv2.destroyWindow("Tracker")
            k,frame = cap.read()
            bbox= cv2.selectROI(frame)

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray = cv2.GaussianBlur(gray, (5, 5), 0)


            topLeftX, topLeftY,w,h = bbox

            bottomRightX = topLeftX + w
            bottomRightY = topLeftY + h
            dlib_rect = dlib.rectangle(topLeftX, topLeftY, bottomRightX,bottomRightY )

            tracker = dlib.correlation_tracker()
            tracker.start_track(gray, dlib_rect)
            tracked = True
            
            
        if ch == ord("q"):
                break
        
         
cv2.destroyAllWindows()
    
