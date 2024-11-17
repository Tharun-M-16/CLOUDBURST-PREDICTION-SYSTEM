import pandas as pd
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
import joblib
from tkinter import Tk, Label, Entry, Button, StringVar, messagebox, Canvas, Scrollbar, Frame
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
from sklearn.model_selection import train_test_split

# Load the model and dataset
model = joblib.load(r'D:\WeatherForecast\mainproject\www\refined_disaster_prediction_model.pkl')
reference_data = pd.read_csv(r'D:\WeatherForecast\mainproject\www\processed_disaster_data.csv')

# Check that the features from the model match the dataset
expected_features = model.feature_names_in_
print(f"Model Features: {expected_features}")
print(f"Dataset Columns: {reference_data.columns}")

# Ensure that the reference data has the correct features
comparison = reference_data[expected_features].mean()

# Tkinter Setup
app = Tk()
app.title("Cloudburst Prediction System")
app.geometry("950x900")  # Adjusted window size
app.config(bg="#34495e")  # Darker background for better contrast

app.iconbitmap(r'D:\WeatherForecast\mainproject\www\images\logo.ico')
app.iconbitmap(r'D:\WeatherForecast\mainproject\www\images\logo.ico')


# Canvas and Scrollbar Setup
canvas = Canvas(app, bg="#34495e")
scrollbar = Scrollbar(app, orient="vertical", command=canvas.yview)
canvas.config(yscrollcommand=scrollbar.set)

# Create a frame to hold all widgets
scrollable_frame = Frame(canvas, bg="#34495e")
canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
scrollbar.pack(side="right", fill="y")
canvas.pack(side="left", fill="both", expand=True)

# Title for the Application
title_label = Label(scrollable_frame, text="Cloudburst Prediction System", font=("Helvetica", 20, "bold"), fg="white", bg="#34495e")
title_label.grid(row=0, columnspan=2, pady=20)

# Label Font Style
label_font = ("Helvetica", 12, "bold")
result_font = ("Helvetica", 14, "bold", "underline")

# Input variables
inputs = {feature: StringVar() for feature in expected_features}

# Function to Clear All Input Fields
def clear_inputs():
    for feature in expected_features:
        inputs[feature].set("")

# Function to check if all inputs are filled
def check_inputs():
    missing_fields = [feature for feature in expected_features if not inputs[feature].get()]
    if missing_fields:
        messagebox.showwarning("Input Error", f"Please fill in the following fields: {', '.join(missing_fields)}")
        return False
    return True

# Function to Predict Disaster with improved error handling
def predict_disaster():
    if not check_inputs():
        return
    try:
        input_data = pd.DataFrame([[float(inputs[feature].get() or "0") for feature in expected_features]], columns=expected_features)
        prediction = model.predict(input_data)[0]
        
        # More detailed output based on prediction
        if prediction == 1:
            result_var.set("Disaster Prediction: A potential disaster is likely due to the conditions.")
            messagebox.showwarning("Warning", "Potential disaster conditions detected! Immediate action may be necessary.")
        else:
            result_var.set("Disaster Prediction: No immediate disaster threat detected.")
            messagebox.showinfo("Info", "Conditions are not likely to result in a disaster.")
            
    except ValueError as e:
        messagebox.showerror("Input Error", f"Invalid input: {e}")
    except Exception as e:
        messagebox.showerror("Error", f"An unexpected error occurred: {e}")

# Function to Clear Previous Plot before Creating a New One
def clear_previous_plot():
    for widget in scrollable_frame.grid_slaves():
        if isinstance(widget, FigureCanvasTkAgg):
            widget.get_tk_widget().destroy()

# Function to Show Comparison Plot
def show_comparison_plot():
    clear_previous_plot()
    input_values = [float(inputs[feature].get() or "0") for feature in expected_features]
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar(expected_features, comparison.values, color='#95a5a6', label="Dataset Average")
    ax.bar(expected_features, input_values, color='#e67e22', alpha=0.6, label="Your Input")
    ax.set_xlabel("Feature", fontsize=14, fontweight="bold")
    ax.set_ylabel("Value", fontsize=14, fontweight="bold")
    ax.set_title("Comparison of Input Values vs. Dataset Averages", fontsize=16, fontweight="bold")
    ax.legend()

    canvas_plot = FigureCanvasTkAgg(fig, master=scrollable_frame)
    canvas_plot.draw()
    canvas_plot.get_tk_widget().grid(row=len(expected_features) + 3, columnspan=2, pady=20)
    scrollable_frame.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))

# Function to Show Confusion Matrix
def show_confusion_matrix():
    clear_previous_plot()
    data = pd.read_csv(r'D:\WeatherForecast\mainproject\www\processed_disaster_data.csv')
    features = expected_features
    target = 'disaster'
    X = data[features]
    y = data[target]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    y_pred = model.predict(X_test)
    cm = confusion_matrix(y_test, y_pred)
    fig, ax = plt.subplots(figsize=(6, 6))
    ConfusionMatrixDisplay(cm, display_labels=['No Disaster', 'Disaster']).plot(cmap='Blues', ax=ax)
    ax.set_title("Confusion Matrix", fontsize=16, fontweight="bold")

    canvas_cm = FigureCanvasTkAgg(fig, master=scrollable_frame)
    canvas_cm.draw()
    canvas_cm.get_tk_widget().grid(row=len(expected_features) + 4, columnspan=2, pady=20)
    scrollable_frame.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))

# Function to Show Weather Data Graphs
def show_weather_graphs():
    clear_previous_plot()
    data = pd.read_csv(r'D:\WeatherForecast\mainproject\www\processed_disaster_data.csv')
    data['time'] = pd.to_datetime(data['time'])
    fig, ax = plt.subplots(2, 2, figsize=(12, 8))

    ax[0, 0].plot(data['time'], data['temp'], label='Temperature (°C)', color='#f39c12')
    ax[0, 0].set_title('Temperature Over Time', fontsize=14, fontweight="bold")
    ax[0, 0].grid(True)
    ax[0, 0].legend()

    ax[0, 1].plot(data['time'], data['wspd'], label='Wind Speed (m/s)', color='#2980b9')
    ax[0, 1].set_title('Wind Speed Over Time', fontsize=14, fontweight="bold")
    ax[0, 1].grid(True)
    ax[0, 1].legend()

    ax[1, 0].plot(data['time'], data['rhum'], label='Humidity (%)', color='#27ae60')
    ax[1, 0].set_title('Humidity Over Time', fontsize=14, fontweight="bold")
    ax[1, 0].grid(True)
    ax[1, 0].legend()

    ax[1, 1].plot(data['time'], data['pres'], label='Pressure (hPa)', color='#8e44ad')
    ax[1, 1].set_title('Pressure Over Time', fontsize=14, fontweight="bold")
    ax[1, 1].grid(True)
    ax[1, 1].legend()

    plt.tight_layout()
    canvas_weather = FigureCanvasTkAgg(fig, master=scrollable_frame)
    canvas_weather.draw()
    canvas_weather.get_tk_widget().grid(row=len(expected_features) + 5, columnspan=2, pady=20)
    scrollable_frame.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))

# Create Input Fields with Specific Label Text
label_texts = ["Temperature (°C)", "Wind Speed (km/hr)", "Humidity (%)", "Pressure (hPa)"]

for i, feature in enumerate(expected_features[:4]):  # Only show the first four features
    Label(scrollable_frame, text=f"Enter {label_texts[i]} value:", font=label_font, fg="white", bg="#34495e").grid(row=i+1, column=0, padx=20, pady=12, sticky="w")
    Entry(scrollable_frame, textvariable=inputs[feature], font=("Helvetica", 12), fg="#34495e", bg="white").grid(row=i+1, column=1, padx=20, pady=12)

# Prediction Result Label
result_var = StringVar()
Label(scrollable_frame, textvariable=result_var, font=result_font, fg="white", bg="#34495e").grid(row=len(expected_features)+1, columnspan=2, pady=20)

# Button Frame - Centered
button_frame = Frame(scrollable_frame, bg="#34495e")
button_frame.grid(row=len(expected_features) + 2, column=0, columnspan=2, pady=20)

# Buttons - Centered and spaced evenly
Button(button_frame, text="Predict Disaster", font=label_font, command=predict_disaster, bg="#e74c3c", fg="white", width=15).grid(row=0, column=0, padx=10, pady=5)
Button(button_frame, text="Show Comparison", font=label_font, command=show_comparison_plot, bg="#3498db", fg="white", width=15).grid(row=0, column=1, padx=10, pady=5)
Button(button_frame, text="Confusion Matrix", font=label_font, command=show_confusion_matrix, bg="#2ecc71", fg="white", width=15).grid(row=0, column=2, padx=10, pady=5)
Button(button_frame, text="Show Graphs", font=label_font, command=show_weather_graphs, bg="#9b59b6", fg="white", width=15).grid(row=0, column=3, padx=10, pady=5)
Button(button_frame, text="Clear All", font=label_font, command=clear_inputs, bg="#95a5a6", fg="white", width=15).grid(row=0, column=4, padx=10, pady=5)


# Update Scroll Region
scrollable_frame.update_idletasks()
canvas.config(scrollregion=canvas.bbox("all"))

app.mainloop()
