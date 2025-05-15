import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO
import base64
from collections import defaultdict

def get_graph():
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')
    buffer.close()
    return graph

def get_plot(date_from, date_to, data, nutrition=None, df=None):
    plt.switch_backend('AGG')

    # Pobranie wszystkich dat w zakresie
    all_dates = pd.date_range(start=date_from, end=date_to).strftime("%d-%m-%Y").tolist()
    
    # Tworzymy domyślny słownik z wartościami 0
    nutrition_data = defaultdict(lambda: {"kcal": 0, "protein": 0, "carbs": 0, "fat": 0})

    # Uzupełnienie wartości z `data`
    for entry in data:
        date = entry.get("date")
        if date:
            nutrition_data[date] = entry

    # Zamiana słownika na listy w poprawnej kolejności
    dates = []
    kcal, protein, carbs, fat = [], [], [], []

    for date in all_dates:
        dates.append(date)
        kcal.append(nutrition_data[date].get("kcal", 0))
        protein.append(nutrition_data[date].get("protein", 0))
        carbs.append(nutrition_data[date].get("carbs", 0))
        fat.append(nutrition_data[date].get("fat", 0))

    # Tworzenie wykresu
    plt.figure(figsize=(8, 5))
    plt.xticks(rotation=45)
    plt.xlabel("Date")
    plt.ylabel("Grams")
    
    if df is not None and not df.empty:
        
        plt.plot(dates, kcal, label="Kcal", marker="o")
        plt.plot(dates, protein, label="Protein", marker="o")
        plt.plot(dates, carbs, label="Carbs", marker="o")
        plt.plot(dates, fat, label="Fat", marker="o")
        plt.legend()
        plt.title("Nutrition over Time")
    if nutrition:
        
        nutrition_values = [nutrition_data[date].get(nutrition, 0) for date in all_dates]
        plt.plot(dates, nutrition_values, label=nutrition.capitalize(), marker="o")
        plt.legend()
        plt.title(f"{nutrition.capitalize()} over Time")
    plt.grid()
    plt.legend()
    chart = get_graph()
    return chart
