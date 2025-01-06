import streamlit as st
import pickle
import pandas as pd

# Header
st.sidebar.title('Car Price Prediction')
html_temp = """
<div style="background-color:#008080;padding:5px">
<h2 style="color:white;text-align:center;">Auto Scout Car Prices Prediction Project:<br> Web App</h2>
</div>"""
st.markdown(html_temp,unsafe_allow_html=True)

# Variables
make_model = st.sidebar.selectbox("Select make of the car:",
('audi_a3',
 'audi_a1',
 'opel_insignia',
 'opel_astra',
 'opel_corsa',
 'renault_clio',
 'renault_espace'))
year=st.sidebar.selectbox("Select year of the car:",(2016,2017,2018,2019))
age = 2019 - year
weight=st.sidebar.slider("Weight of car", 800,2400, step=100)
hp=st.sidebar.slider("Car engine horse power:", 50, 150, step=10)
displacement=st.sidebar.slider("Displacement of car:", 800, 3000, step=50)
consumption_comb=st.sidebar.slider("Combined consumption (litres of petrol for 100 km):", 0, 14, step=1)
co2_emission=st.sidebar.slider("Carbon dioxide emission (CO2/km):", 0, 200, step=5)
gearing_type=st.sidebar.radio('Select gear type',('Manual','Not Manual'))
gearing_type_manual = 1*(gearing_type=='Manual')
new_used=st.sidebar.selectbox("Select condition of the car", ("New", "Used"))
prev_owner = 0
if new_used == "Used":
    prev_owner=st.sidebar.slider("Select no. of previous owners", 0, 4, step=1)
km=st.sidebar.slider("Km on car odometer", 0,250000, step=1000)
warr=st.sidebar.slider("Months of warranty", 0,72, step=3)


# confirm entries with user
conf = {"Make":make_model,
        "Age (Yrs)": age,
        "Wt (Kg)": weight,
        "HP": hp,
        "Disp. (cc)":displacement,
        "Cons. (comb)":consumption_comb,
        "CO2 (g/km)":co2_emission,
        "Gearing":gearing_type,
        "New/Used":new_used,
        "Prev Owners":prev_owner,
        "KM": km,
        "Warranty (months)": warr,
        } 

conf_df = pd.DataFrame.from_dict([conf])
st.header("The configuration of your car:")
st.table(conf_df)
st.subheader("Press predict if configuration is okay")


# Data frame for prediction
pred = {'make_model': make_model,
 'age': age,
 'co2_emission':co2_emission,
 'consumption_comb': consumption_comb,
 'displacement': displacement,
 'hp': hp,
 'km': km,
 'warranty_mo': warr,
 'weight': weight,
 'gearing_type_manual': gearing_type_manual,
 'prev_owner':prev_owner
        }
df = pd.DataFrame.from_dict([pred])


# load model and predict
model=pickle.load(open("model.pkl","rb"))
if st.button("Predict"):
    prediction = model.predict(df)
    st.success("The estimated price of your car is €{} +/- {}.".format(
                             int(prediction[0]), int(0.0936*prediction[0])))
