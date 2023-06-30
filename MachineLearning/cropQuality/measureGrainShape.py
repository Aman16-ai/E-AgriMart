import cv2
from django.core.files.storage import default_storage

def measure(grain_image):
    file_name = default_storage.save(grain_image.name,grain_image)
    file_url = default_storage.path(file_name)
    img = cv2.imread(file_url)
    img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(img,100,200)
    img = img[0:250,:]

    contours, _ = cv2.findContours(edges,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

    # cv2.drawContours(img,contours,-1,(0,255,0),2)
    # for cnt in contours:
    #     area = cv2.contourArea(cnt)
    #     x, y, w, h = cv2.boundingRect(cnt)
    #     print("Area:", area)
    #     print("Width and height: ",w,h)

    # set minimum threshold 50
    min_area = 50
    width = None
    height = None
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > min_area:
            cv2.drawContours(img,[cnt],-1,(0,255,0),2)
            x,y,w,h = cv2.boundingRect(cnt)
            width = w
            height = h
            cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
            cv2.putText(img,f"Width: {w} px",(x,y-10),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,255,0),2)
            cv2.putText(img,f"Height: {h} px",(x,y+h+20),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,255,0),2)
            print('Area',area)
            print("Width and height: ",w,h)

    return width,height