import pickle
import numpy as np
import pandas as pd

# def predict_crop_production(features):
#     with open("crop_model_pkl.pkl","rb") as files:
#         model = pickle.load(files)
#         model.predict(features)
#         # print(prediction)
# if __name__ == "__main__":
def predict_crop_production(features):
    data = pd.DataFrame(features)
    model = pickle.load(open("crop_model_pkl.pkl","rb"))
    return model.predict(data)
    
test_data = {"State_Name":["Bihar"],"Crop_Year":[2022],"Season":["Kharif"],"Crop":["Tomato"],"Temperature":[48],"humidity":[32],"soil moisture":[40]," area":[4000]}
data = {"State_Name":["Andaman and Nicobar Islands"],"Crop_Year":[2000],"Season":["Kharif"],"Crop":["Arecanut"],"Temperature":[36],"humidity":[35],"soil moisture":[45]," area":[1245.0]}
    # predict_crop_production(pd.DataFrame(data))
    # print(pd.DataFrame(test_data))

model = pickle.load(open("crop_model_pkl.pkl","rb"))
print(model.predict(pd.DataFrame(test_data)))

