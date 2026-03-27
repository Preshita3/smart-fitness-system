import pandas as pd
import matplotlib.pyplot as plt

import streamlit as st
import sqlite3

# Functions
def calculate_bmi(weight, height):
    height_m = height / 100
    return weight / (height_m ** 2)

def bmi_category(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif bmi < 25:
        return "Normal"
    elif bmi < 30:
        return "Overweight"
    else:
        return "Obese"

def water_intake(weight):
    return round(weight * 0.033, 2)

def walking_recommendation(bmi):
    if bmi < 18.5:
        return 3
    elif bmi < 25:
        return 5
    elif bmi < 30:
        return 7
    else:
        return 9


# UI
st.title("🏃 Smart Fitness Recommendation System")

age = st.number_input("Enter Age", min_value=10, max_value=100)
height = st.number_input("Enter Height (cm)")
weight = st.number_input("Enter Weight (kg)")

if st.button("Get Recommendation"):
    bmi = calculate_bmi(weight, height)
    category = bmi_category(bmi)
    water = water_intake(weight)
    walking = walking_recommendation(bmi)

    st.success(f"BMI: {round(bmi,2)} ({category})")
    st.info(f"💧 Recommended Water Intake: {water} litres/day")
    st.info(f"🚶 Recommended Walking: {walking} km/day")

    # Save to database
    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO users (age, height, weight, bmi, category, water_intake, walking_km)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (age, height, weight, bmi, category, water, walking))

    conn.commit()
    conn.close()