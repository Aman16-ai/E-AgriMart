from .measureGrainShape import measure
from .predict_diease import predict

# Conditions : {
#   Good ---> No diease and w >= 70px and h >= 155px
#   medium ---> No diease and w < 70px and h < 155px
#   low ---> contain diease 
# }

def get_crop_quality(main_img,single_img):
    diease = predict(main_img)
    width, height = measure(single_img)

    if diease == 'Healthy Wheat' and width >= 70 and height >= 155:
        return "Good"

    elif diease == 'Healthy Wheat' and width < 70 and height < 155:
        return "Medium"
    
    else:
        return "Low"


