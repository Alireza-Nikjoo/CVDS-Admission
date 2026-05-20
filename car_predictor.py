import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import OneHotEncoder
import customtkinter  as ctk


def get_data_from_csv(filepath):
    data = pd.read_csv(filepath)
    return data


data = get_data_from_csv("csvfile.csv")
data['price'] = data['price'].astype(int)
data['mileage'] = data['mileage'].astype(int)
data['year'] = data['year'].astype(int)

encoder = OneHotEncoder()
colors_encoded = encoder.fit_transform(data[['color']])


X = data[['price']].values  
y_color = data['color']  
y_model = data['year'].values  
y_kilometer = data['mileage'].values 

X_train, X_test, y_train_color, y_test_color = train_test_split(X, y_color, test_size=0.2, random_state=42)
X_train_model, X_test_model, y_train_model, y_test_model = train_test_split(X, y_model, test_size=0.2, random_state=42)
X_train_km, X_test_km, y_train_km, y_test_km = train_test_split(X, y_kilometer, test_size=0.2, random_state=42)

color_classifier = RandomForestClassifier()
color_classifier.fit(X_train, y_train_color)

model_regressor = RandomForestRegressor()
model_regressor.fit(X_train_model, y_train_model)

km_regressor = RandomForestRegressor()
km_regressor.fit(X_train_km, y_train_km)

def predict_car(price):
    input_data = np.array([[price]])
    
    predicted_color = color_classifier.predict(input_data)[0]
    predicted_model = int(round(model_regressor.predict(input_data)[0]))
    predicted_kilometer = int(round(km_regressor.predict(input_data)[0]))
    
    return predicted_color, predicted_model, predicted_kilometer

def find_closest_car(price):
    data['price_diff'] = (data['price'] - price).abs()
    
    closest_index = data['price_diff'].idxmin()
    closest_record = data.loc[closest_index]
    
    closest_record = closest_record.drop('price_diff')
    
    record_dict = closest_record.to_dict()
    output = record_dict['urls']

    return output

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")
app = ctk.CTk()
app.geometry("720x380")
app.title("MY Program")
app.resizable(False,False)
frame = ctk.CTkFrame(master=app,width=600,height=340)
frame.grid(pady=20, padx=20)
label = ctk.CTkLabel(master=frame, text="What is your budget?", font=("Verdana",18))
label.grid(pady=12, padx=10,row = 0, column =0)
textbox = ctk.CTkTextbox(master=frame, width=120, height=25, font=("Verdana",18))
textbox.grid(row=0, column=1,padx=(0,30))

def btn_do():
    price = int(textbox.get("0.0","end"))
    predicted_color, predicted_model, predicted_kilometer = predict_car(price)
    closest_record = find_closest_car(price)
    txtbox1.delete("0.0","end")
    txtbox2.delete("0.0","end")
    txtbox3.delete("0.0","end")
    txtbox4.delete("0.0","end")
    txtbox1.insert("0.0", predicted_color)
    txtbox2.insert("0.0", predicted_model)
    txtbox3.insert("0.0", predicted_kilometer)
    txtbox4.insert("0.0", closest_record)

button = ctk.CTkButton(master=frame, text="Find",command=btn_do,width=75)
button.grid(pady=15, row=1, column=0)
txtbox1=ctk.CTkTextbox(master=frame, width=120, height=25, font=("Verdana",18))
txtbox2=ctk.CTkTextbox(master=frame, width=120, height=25, font=("Verdana",18))
txtbox3=ctk.CTkTextbox(master=frame, width=120, height=25, font=("Verdana",18))
txtbox4=ctk.CTkTextbox(master=frame, width=350, height=25, font=("Verdana",10))
lbl1 = ctk.CTkLabel(master=frame, text="predicted color: ", font=("Verdana",12))
lbl2 = ctk.CTkLabel(master=frame, text="predicted year: ", font=("Verdana",12))
lbl3 = ctk.CTkLabel(master=frame, text="predicted mileage: ", font=("Verdana",12))
lbl4 = ctk.CTkLabel(master=frame, text="You Can Buy: ", font=("Verdana",12))
lbl1.grid(row=2,column=0)
txtbox1.grid(pady=10,padx=(0,30),row=2,column=1)
lbl2.grid(row=3,column=0)
txtbox2.grid(pady=10,padx=(0,30),row=3,column=1)
lbl3.grid(row=4,column=0)
txtbox3.grid(pady=10,padx=(0,30),row=4,column=1)
lbl4.grid(row=5,column=0)
txtbox4.grid(pady=10,padx=(0,25),row=5, column=1)

app.mainloop()