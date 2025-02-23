from fastapi import FastAPI, Query
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import io
import base64


app = FastAPI()

df = sns.load_dataset("titanic")

@app.get("/")
def home():
    return {"message": "Hello, FastAPI! Titanic API is running"}

@app.get("/query")
def get_titanic_data(question: str = Query(..., description="Ask a question about Titanic dataset")):
    """Answer Titanic-related questions based on user input."""
    question = question.lower()

    if "percentage of passengers were male" in question or "male percentage" in question:
        male_percentage = (df["sex"] == "male").mean() * 100
        return {"answer": f"{male_percentage:.2f}% of passengers were male."}

    elif "histogram of passenger ages" in question:
        image_response = generate_visualization(chart_type="histogram", column="age")
        return {
            "answer": "Here is a histogram of passenger ages.",
            "image": image_response["image"]
        }

    elif "average ticket fare" in question or "average fare" in question:
        avg_fare = df["fare"].mean()
        return {"answer": f"The average ticket fare was ${avg_fare:.2f}."}

    elif "how many passengers embarked from each port" in question:
        embark_counts = df["embark_town"].value_counts().to_dict()
        image_response = generate_visualization(chart_type="countplot", column="embark_town")
        return {
            "answer": "Passenger embarkation distribution",
            "data": embark_counts,
            "image": image_response["image"]
        }

    else:
        return {"answer": "I couldn't understand the question. Try asking about fare, survival rate, class, etc."}

@app.get("/visualization/")
def generate_visualization(chart_type: str = Query("histogram", description="Choose a visualization type"), 
                           column: str = Query("sex", description="Column for visualization")):
    """Generate visualizations for Titanic dataset."""
    
    if column not in df.columns:
        return {"error": "Invalid column name. Choose a valid column from the dataset."}

    plt.figure(figsize=(6, 4))

    if chart_type == "histogram":
        sns.histplot(df[column].dropna(), kde=True)
    elif chart_type == "pie":
        df[column].value_counts().plot.pie(autopct="%1.1f%%")
    elif chart_type == "countplot":
        sns.countplot(x=df[column])
    else:
        return {"error": "Invalid chart type. Choose from histogram, pie, or countplot."}

    img = io.BytesIO()
    plt.savefig(img, format="png")
    img.seek(0)
    encoded_img = base64.b64encode(img.getvalue()).decode()

    return {"image": encoded_img}
