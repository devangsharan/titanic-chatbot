import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load Titanic dataset
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"
    return pd.read_csv(url)

df = load_data()

# Mapping embarkation port codes to full names
embark_labels = {"S": "Southampton", "C": "Cherbourg", "Q": "Queenstown"}
df["Embarked"] = df["Embarked"].map(embark_labels)

# Streamlit UI
st.title("🚢 Titanic Data Explorer")

# Get user input
question = st.text_input("Enter your question:")

if question:
    # Handle percentage of male passengers
    if "percentage of passengers were male" in question.lower():
        male_percentage = round((df["Sex"].value_counts(normalize=True)["male"] * 100), 2)
        st.write(f"**{male_percentage}%** of passengers were male.")
        
        # Pie chart for gender distribution
        fig, ax = plt.subplots()
        df["Sex"].value_counts().plot.pie(autopct="%1.1f%%", colors=["blue", "pink"], ax=ax)
        ax.set_ylabel("")
        ax.set_title("Gender Distribution")
        st.pyplot(fig)

    # Handle histogram of passenger ages
    elif "histogram of passenger ages" in question.lower():
        st.write("### Age Distribution of Passengers")
        fig, ax = plt.subplots()
        df["Age"].dropna().plot.hist(bins=20, alpha=0.7, color="skyblue", edgecolor="black", ax=ax)
        ax.set_xlabel("Age")
        ax.set_ylabel("Count")
        ax.set_title("Histogram of Passenger Ages")
        st.pyplot(fig)

    # Handle average ticket fare
    elif "average ticket fare" in question.lower():
        avg_fare = round(df["Fare"].mean(), 2)
        st.write(f"**${avg_fare}** was the average ticket fare.")

        # Histogram of ticket fares
        fig, ax = plt.subplots()
        df["Fare"].plot.hist(bins=20, color="green", edgecolor="black", ax=ax)
        ax.set_xlabel("Fare")
        ax.set_ylabel("Count")
        ax.set_title("Distribution of Ticket Fares")
        st.pyplot(fig)

    # Handle number of passengers embarked from each port
    elif "passengers embarked from each port" in question.lower():
        embarked_counts = df["Embarked"].value_counts()
        st.write("### Number of Passengers by Embarkation Port")
        st.write(embarked_counts)

        # Bar chart for embarkation
        fig, ax = plt.subplots()
        embarked_counts.plot(kind="bar", color=["red", "blue", "green"], ax=ax)
        ax.set_xlabel("Embarkation Port")
        ax.set_ylabel("Number of Passengers")
        ax.set_title("Passengers by Embarkation Port")
        st.pyplot(fig)

    else:
        st.write("❌ Sorry, I didn't understand the question. Try rephrasing!")
