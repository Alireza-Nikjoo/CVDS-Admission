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

# Convert Columns to numeric types
data = get_data_from_csv("csvfile.csv")
data['price'] = data['price'].astype(int)
data['mileage'] = data['mileage'].astype(int)
data['year'] = data['year'].astype(int)

encoder = OneHotEncoder()
colors_encoded = encoder.fit_transform(data[['color']])

# Define features and targets
X = data[['price']].values  
y_color = data['color']  
y_year = data['year'].values  
y_mileage = data['mileage'].values 

#Split data for different prediction tasks
X_train, X_test, y_train_color, y_test_color = train_test_split(X, y_color, test_size=0.2, random_state=42)
X_train_year, X_test_year, y_train_year, y_test_year = train_test_split(X, y_year, test_size=0.2, random_state=42)
X_train_mileage, X_test_mileage, y_train_mileage, y_test_mileage = train_test_split(X, y_mileage, test_size=0.2, random_state=42)

# Train classifier for predicting car color
color_classifier = RandomForestClassifier()
color_classifier.fit(X_train, y_train_color)

# Manual implementation of simple linear regression
def train_linear_regression(X, y):
    X = X.flatten()
    
    mean_x = np.mean(X)
    mean_y = np.mean(y)
    
    numerator = np.sum((X - mean_x) * (y - mean_y))
    denominator = np.sum((X - mean_x) ** 2)
    
    a = numerator / denominator
    b = mean_y - a * mean_x
    
    return a, b

# Predict value using learned linear model
def predict_linear(a, b, price):
    return a * price + b


a_year, b_year = train_linear_regression(X_train_year, y_train_year)

# Train model for predicting mileage
mileage_regressor = RandomForestRegressor()
mileage_regressor.fit(X_train_mileage, y_train_mileage)

# Main prediction function
def predict_car(price):
    input_data = np.array([[price]])
    
    predicted_color = color_classifier.predict(input_data)[0]
    
    # Use manual linear regression for year prediction
    predicted_year = int(round(predict_linear(a_year, b_year, price)))
    
    # Use RandomForest for mileage prediction
    predicted_mileage = int(round(mileage_regressor.predict(input_data)[0]))
    
    return predicted_color, predicted_year, predicted_mileage

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
app.title("Car Recommender")
app.resizable(False,False)
frame = ctk.CTkFrame(master=app,width=600,height=340)
frame.grid(pady=20, padx=20)
label = ctk.CTkLabel(master=frame, text="What is your budget?", font=("Verdana",18))
label.grid(pady=12, padx=10,row = 0, column =0)
textbox = ctk.CTkTextbox(master=frame, width=200, height=25, font=("Verdana",18))
textbox.grid(row=0, column=1,padx=(0,30))

def btn_do():
    price = int(textbox.get("0.0","end"))
    predicted_color, predicted_year, predicted_mileage = predict_car(price)
    closest_record = find_closest_car(price)
    txtbox1.delete("0.0","end")
    txtbox2.delete("0.0","end")
    txtbox3.delete("0.0","end")
    txtbox4.delete("0.0","end")
    txtbox1.insert("0.0", predicted_color)
    txtbox2.insert("0.0", predicted_year)
    txtbox3.insert("0.0", predicted_mileage)
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