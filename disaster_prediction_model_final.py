import pandas as pd
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
import joblib
from tkinter import Tk, Label, Entry, Button, StringVar, messagebox, Canvas, Scrollbar, Frame
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
from sklearn.model_selection import train_test_split
import os
import warnings

# Suppress sklearn version warnings
warnings.filterwarnings('ignore', category=UserWarning)

# Global flag for animation control
animations_running = True

# Load the model and dataset
script_dir = os.path.dirname(os.path.abspath(__file__))
model = joblib.load(os.path.join(script_dir, 'refined_disaster_prediction_model.pkl'))
reference_data = pd.read_csv(os.path.join(script_dir, 'processed_disaster_data.csv'))

# Check that the features from the model match the dataset
expected_features = model.feature_names_in_
print(f"Model Features: {expected_features}")
print(f"Dataset Columns: {reference_data.columns}")

# Ensure that the reference data has the correct features
comparison = reference_data[expected_features].mean()

# Tkinter Setup - Futuristic Theme
app = Tk()
app.title("⚡ CLOUDBURST PREDICTION SYSTEM ⚡")
app.geometry("1200x950")
app.config(bg="#0a0e27")  # Deep space blue background
app.resizable(True, True)

logo_path = os.path.join(script_dir, 'logo.ico')
if os.path.exists(logo_path):
    app.iconbitmap(logo_path)

# Modern color scheme - Enhanced for better visibility
BG_COLOR = "#0d1117"  # GitHub dark background
CARD_BG = "#161b22"  # Lighter card background for contrast
CARD_BORDER = "#30363d"  # Subtle border
ACCENT_CYAN = "#58a6ff"  # Brighter cyan
ACCENT_PURPLE = "#bc8cff"  # Brighter purple
ACCENT_GREEN = "#3fb950"  # Brighter green
ACCENT_RED = "#f85149"  # Brighter red
ACCENT_ORANGE = "#ffa657"  # Brighter orange
TEXT_COLOR = "#f0f6fc"  # Very light text for maximum visibility
TEXT_MUTED = "#8b949e"  # Slightly lighter muted text
TEXT_BRIGHT = "#ffffff"  # Pure white for important text


# Canvas and Scrollbar Setup with modern styling
canvas = Canvas(app, bg=BG_COLOR, highlightthickness=0)
scrollbar = ttk.Scrollbar(app, orient="vertical", command=canvas.yview)
canvas.config(yscrollcommand=scrollbar.set)

# Create a frame to hold all widgets - CENTERED
scrollable_frame = Frame(canvas, bg=BG_COLOR)
canvas_window = canvas.create_window((600, 0), window=scrollable_frame, anchor="n")  # Center horizontally
scrollbar.pack(side="right", fill="y")
canvas.pack(side="left", fill="both", expand=True)

# Animation variables
animation_index = 0
animation_colors = [ACCENT_CYAN, ACCENT_PURPLE, ACCENT_GREEN, ACCENT_RED, ACCENT_ORANGE]

# Futuristic Header with Animation
header_frame = Frame(scrollable_frame, bg=BG_COLOR)
header_frame.grid(row=0, column=0, pady=(30, 10))

title_label = Label(header_frame, text="⚡ CLOUDBURST PREDICTION ⚡", 
                    font=("", 36, "bold"), fg=ACCENT_CYAN, bg=BG_COLOR)
title_label.pack()

subtitle_label = Label(header_frame, text="AI-Powered Weather Disaster Analysis System", 
                       font=("", 13), fg=TEXT_COLOR, bg=BG_COLOR)  # Brighter text
subtitle_label.pack(pady=(8, 0))

# Status indicator with pulsing animation
status_label = Label(header_frame, text="● SYSTEM ONLINE", 
                    font=("", 10, "bold"), fg=ACCENT_GREEN, bg=BG_COLOR)
status_label.pack(pady=(5, 0))

# Pulsing animation for title and status
def pulse_animation():
    global animation_index, animations_running
    if not animations_running:
        return
    try:
        # Pulse the title between two shades
        current_color = ACCENT_CYAN if animation_index % 2 == 0 else "#4a9eff"
        title_label.config(fg=current_color)
        
        # Pulse the status indicator
        status_color = ACCENT_GREEN if animation_index % 2 == 0 else "#2ea043"
        status_label.config(fg=status_color)
        
        animation_index += 1
        if animations_running:
            app.after(800, pulse_animation)  # Repeat every 800ms
    except:
        animations_running = False

# Start animation
pulse_animation()

# Divider line with gradient effect
divider_frame = Frame(scrollable_frame, bg=BG_COLOR)
divider_frame.grid(row=1, column=0, pady=(15, 30))

divider = Frame(divider_frame, bg=ACCENT_CYAN, height=3, width=800)
divider.pack()

# Animated loading bar effect
loading_bar = Frame(divider_frame, bg=ACCENT_PURPLE, height=1, width=0)
loading_bar.pack()

def animate_divider():
    global animations_running
    if not animations_running:
        return
    try:
        current_width = loading_bar.winfo_width()
        if current_width < 800 and animations_running:
            loading_bar.config(width=current_width + 20)
            app.after(30, animate_divider)
    except:
        animations_running = False

app.after(100, animate_divider)

# Label Font Styles
label_font = ("Arial", 11, "bold")
entry_font = ("Arial", 12)
result_font = ("Arial", 13, "bold")
button_font = ("Arial", 10, "bold")

# Input variables
inputs = {feature: StringVar() for feature in expected_features}

# Carousel state management
current_graph_index = 0
graph_widgets = []  # Store graph canvases
graph_titles = []
carousel_container = None
indicator_labels = []

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
    global graph_widgets, carousel_container, indicator_labels
    # Clear all graph widgets
    for widget in graph_widgets:
        widget.destroy()
    graph_widgets.clear()
    graph_titles.clear()
    
    # Clear carousel container if exists
    if carousel_container:
        carousel_container.destroy()
        carousel_container = None
    
    indicator_labels.clear()

# Function to create carousel container
def create_carousel_container():
    global carousel_container
    if carousel_container:
        carousel_container.destroy()
    
    # Main carousel frame
    carousel_container = Frame(scrollable_frame, bg=BG_COLOR)
    carousel_container.grid(row=5, column=0, pady=20)
    
    return carousel_container

# Function to show specific graph in carousel
def show_graph_in_carousel(index):
    global current_graph_index
    
    if not graph_widgets or index < 0 or index >= len(graph_widgets):
        return
    
    # Hide all graphs
    for i, widget in enumerate(graph_widgets):
        widget.grid_forget()
    
    # Show selected graph
    current_graph_index = index
    graph_widgets[index].grid(row=1, column=0, pady=10)
    
    # Update indicators
    for i, label in enumerate(indicator_labels):
        if i == index:
            label.config(fg=ACCENT_CYAN, text="●")
        else:
            label.config(fg=TEXT_MUTED, text="○")
    
    # Update title
    title_label = carousel_container.grid_slaves(row=0, column=0)
    if title_label:
        title_label[0].config(text=graph_titles[index])
    
    # Update scroll region
    scrollable_frame.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))

# Navigation functions
def next_graph():
    global current_graph_index
    if graph_widgets:
        current_graph_index = (current_graph_index + 1) % len(graph_widgets)
        show_graph_in_carousel(current_graph_index)

def prev_graph():
    global current_graph_index
    if graph_widgets:
        current_graph_index = (current_graph_index - 1) % len(graph_widgets)
        show_graph_in_carousel(current_graph_index)

# Function to add graph to carousel
def add_graph_to_carousel(fig, title):
    global graph_widgets, carousel_container
    
    if not carousel_container:
        create_carousel_container()
        
        # Add title at top
        title_frame = Frame(carousel_container, bg=BG_COLOR)
        title_frame.grid(row=0, column=0, pady=(0, 10))
        
        Label(title_frame, text=title, font=("", 16, "bold"), 
              fg=ACCENT_CYAN, bg=BG_COLOR).pack()
    
    # Create canvas for this graph
    canvas_widget = FigureCanvasTkAgg(fig, master=carousel_container)
    canvas_widget.draw()
    graph_widgets.append(canvas_widget.get_tk_widget())
    graph_titles.append(title)
    
    # Show the first graph
    if len(graph_widgets) == 1:
        canvas_widget.get_tk_widget().grid(row=1, column=0, pady=10)
    
    # Update navigation controls
    update_carousel_controls()
    
    # Force scroll region update
    scrollable_frame.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))
    
    # Scroll to show the new content
    canvas.yview_moveto(0)

def update_carousel_controls():
    global carousel_container, indicator_labels
    
    if not carousel_container:
        return
    
    # Clear old controls
    for widget in carousel_container.grid_slaves(row=2):
        widget.destroy()
    for widget in carousel_container.grid_slaves(row=3):
        widget.destroy()
    
    # Only show navigation if there are multiple graphs
    if len(graph_widgets) < 2:
        scrollable_frame.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))
        return
    
    # Navigation buttons
    nav_frame = Frame(carousel_container, bg=BG_COLOR)
    nav_frame.grid(row=2, column=0, pady=15)
    
    Button(nav_frame, text="◀ Previous", font=("", 11, "bold"), command=prev_graph,
           bg=ACCENT_PURPLE, fg=TEXT_BRIGHT, activebackground="#9b73d9",
           relief="flat", padx=20, pady=10, cursor="hand2").pack(side="left", padx=10)
    
    Button(nav_frame, text="Next ▶", font=("", 11, "bold"), command=next_graph,
           bg=ACCENT_PURPLE, fg=TEXT_BRIGHT, activebackground="#9b73d9",
           relief="flat", padx=20, pady=10, cursor="hand2").pack(side="left", padx=10)
    
    # Indicators
    indicator_frame = Frame(carousel_container, bg=BG_COLOR)
    indicator_frame.grid(row=3, column=0, pady=10)
    
    indicator_labels.clear()
    for i in range(len(graph_widgets)):
        indicator = Label(indicator_frame, text="○", font=("", 20), 
                         fg=TEXT_MUTED, bg=BG_COLOR, cursor="hand2")
        indicator.pack(side="left", padx=5)
        indicator.bind("<Button-1>", lambda e, idx=i: show_graph_in_carousel(idx))
        indicator_labels.append(indicator)
    
    # Set first indicator as active
    if indicator_labels:
        indicator_labels[0].config(fg=ACCENT_CYAN, text="●")
    
    scrollable_frame.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))

# Function to Show Comparison Plot
def show_comparison_plot():
    if not check_inputs():
        return
    
    clear_previous_plot()
    input_values = [float(inputs[feature].get() or "0") for feature in expected_features]
    
    # Modern dark theme for plot
    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(10, 6), facecolor='#1a1f3a')
    ax.set_facecolor('#1a1f3a')
    
    x = range(len(expected_features))
    width = 0.35
    
    bars1 = ax.bar([i - width/2 for i in x], comparison.values, width, 
                    color=ACCENT_CYAN, label="Dataset Average", alpha=0.8)
    bars2 = ax.bar([i + width/2 for i in x], input_values, width, 
                    color=ACCENT_ORANGE, label="Your Input", alpha=0.8)
    
    ax.set_xlabel("Weather Parameters", fontsize=12, fontweight="bold", color=TEXT_COLOR)
    ax.set_ylabel("Value", fontsize=12, fontweight="bold", color=TEXT_COLOR)
    ax.set_title("📊 Input Comparison Analysis", fontsize=16, fontweight="bold", 
                 color=ACCENT_CYAN, pad=20)
    ax.set_xticks(x)
    ax.set_xticklabels(expected_features, color=TEXT_COLOR)
    ax.tick_params(colors=TEXT_COLOR)
    ax.legend(facecolor='#2a2f4a', edgecolor=ACCENT_CYAN, labelcolor=TEXT_COLOR)
    ax.grid(True, alpha=0.2, color=TEXT_MUTED, linestyle='--')
    
    plt.tight_layout()
    add_graph_to_carousel(fig, "📊 Input Comparison Analysis")

# Function to Show Confusion Matrix
def show_confusion_matrix():
    clear_previous_plot()
    data = pd.read_csv(os.path.join(script_dir, 'processed_disaster_data.csv'))
    features = expected_features
    target = 'disaster'
    X = data[features]
    y = data[target]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    y_pred = model.predict(X_test)
    cm = confusion_matrix(y_test, y_pred)
    
    # Futuristic styling
    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(8, 7), facecolor='#1a1f3a')
    ax.set_facecolor('#1a1f3a')
    
    disp = ConfusionMatrixDisplay(cm, display_labels=['No Disaster', 'Disaster'])
    disp.plot(cmap='viridis', ax=ax, colorbar=True, values_format='d')
    ax.set_title("🔮 Model Performance Matrix", fontsize=16, fontweight="bold", 
                 color=ACCENT_PURPLE, pad=20)
    ax.set_xlabel("Predicted Label", fontsize=12, color=TEXT_COLOR, fontweight="bold")
    ax.set_ylabel("True Label", fontsize=12, color=TEXT_COLOR, fontweight="bold")
    ax.tick_params(colors=TEXT_COLOR)
    
    plt.tight_layout()
    add_graph_to_carousel(fig, "🔮 Model Performance Matrix")

# Function to Show Weather Data Graphs
def show_weather_graphs():
    clear_previous_plot()
    data = pd.read_csv(os.path.join(script_dir, 'processed_disaster_data.csv'))
    data['time'] = pd.to_datetime(data['time'])
    
    # Futuristic dark theme
    plt.style.use('dark_background')
    fig, ax = plt.subplots(2, 2, figsize=(14, 10), facecolor='#1a1f3a')
    
    # Temperature plot
    ax[0, 0].set_facecolor('#1a1f3a')
    ax[0, 0].plot(data['time'], data['temp'], label='Temperature (°C)', 
                  color=ACCENT_RED, linewidth=2, alpha=0.9)
    ax[0, 0].fill_between(data['time'], data['temp'], alpha=0.2, color=ACCENT_RED)
    ax[0, 0].set_title('🌡️ Temperature Trends', fontsize=13, fontweight="bold", 
                       color=ACCENT_RED, pad=10)
    ax[0, 0].grid(True, alpha=0.2, color=TEXT_MUTED, linestyle='--')
    ax[0, 0].legend(facecolor='#2a2f4a', edgecolor=ACCENT_RED, labelcolor=TEXT_COLOR)
    ax[0, 0].tick_params(colors=TEXT_COLOR)
    
    # Wind Speed plot
    ax[0, 1].set_facecolor('#1a1f3a')
    ax[0, 1].plot(data['time'], data['wspd'], label='Wind Speed (m/s)', 
                  color=ACCENT_CYAN, linewidth=2, alpha=0.9)
    ax[0, 1].fill_between(data['time'], data['wspd'], alpha=0.2, color=ACCENT_CYAN)
    ax[0, 1].set_title('💨 Wind Speed Patterns', fontsize=13, fontweight="bold", 
                       color=ACCENT_CYAN, pad=10)
    ax[0, 1].grid(True, alpha=0.2, color=TEXT_MUTED, linestyle='--')
    ax[0, 1].legend(facecolor='#2a2f4a', edgecolor=ACCENT_CYAN, labelcolor=TEXT_COLOR)
    ax[0, 1].tick_params(colors=TEXT_COLOR)
    
    # Humidity plot
    ax[1, 0].set_facecolor('#1a1f3a')
    ax[1, 0].plot(data['time'], data['rhum'], label='Humidity (%)', 
                  color=ACCENT_GREEN, linewidth=2, alpha=0.9)
    ax[1, 0].fill_between(data['time'], data['rhum'], alpha=0.2, color=ACCENT_GREEN)
    ax[1, 0].set_title('💧 Humidity Levels', fontsize=13, fontweight="bold", 
                       color=ACCENT_GREEN, pad=10)
    ax[1, 0].grid(True, alpha=0.2, color=TEXT_MUTED, linestyle='--')
    ax[1, 0].legend(facecolor='#2a2f4a', edgecolor=ACCENT_GREEN, labelcolor=TEXT_COLOR)
    ax[1, 0].tick_params(colors=TEXT_COLOR)
    
    # Pressure plot
    ax[1, 1].set_facecolor('#1a1f3a')
    ax[1, 1].plot(data['time'], data['pres'], label='Pressure (hPa)', 
                  color=ACCENT_PURPLE, linewidth=2, alpha=0.9)
    ax[1, 1].fill_between(data['time'], data['pres'], alpha=0.2, color=ACCENT_PURPLE)
    ax[1, 1].set_title('📊 Atmospheric Pressure', fontsize=13, fontweight="bold", 
                       color=ACCENT_PURPLE, pad=10)
    ax[1, 1].grid(True, alpha=0.2, color=TEXT_MUTED, linestyle='--')
    ax[1, 1].legend(facecolor='#2a2f4a', edgecolor=ACCENT_PURPLE, labelcolor=TEXT_COLOR)
    ax[1, 1].tick_params(colors=TEXT_COLOR)
    
    fig.suptitle('📈 Weather Data Analysis Dashboard', fontsize=16, fontweight="bold", 
                 color=TEXT_COLOR, y=0.995)
    
    plt.tight_layout()
    add_graph_to_carousel(fig, "📈 Weather Data Analysis Dashboard")

# Create Input Fields with Futuristic Card Design - CENTERED
label_texts = ["Temperature (°C)", "Wind Speed (km/hr)", "Humidity (%)", "Pressure (hPa)"]
icons = ["🌡️", "💨", "💧", "📊"]
colors = [ACCENT_RED, ACCENT_CYAN, ACCENT_GREEN, ACCENT_PURPLE]

# Input container frame - Centered with fixed width
input_container = Frame(scrollable_frame, bg=BG_COLOR)
input_container.grid(row=2, column=0, pady=20)

for i, feature in enumerate(expected_features[:4]):
    # Card frame for each input with border
    card_outer = Frame(input_container, bg=colors[i], relief="flat", bd=0)
    card_outer.grid(row=i//2, column=i%2, padx=15, pady=15)
    
    card = Frame(card_outer, bg=CARD_BG, relief="flat", bd=0)
    card.pack(padx=2, pady=2)  # Creates border effect
    
    # Configure card padding
    card_inner = Frame(card, bg=CARD_BG)
    card_inner.pack(padx=25, pady=20, fill="both", expand=True)
    
    # Icon and label
    label_frame = Frame(card_inner, bg=CARD_BG)
    label_frame.pack(anchor="w")
    
    Label(label_frame, text=icons[i], font=("", 20), bg=CARD_BG).pack(side="left", padx=(0, 10))
    Label(label_frame, text=label_texts[i], font=("", 12, "bold"), 
          fg=colors[i], bg=CARD_BG).pack(side="left")
    
    # Styled entry field with better visibility
    entry = Entry(card_inner, textvariable=inputs[feature], font=("", 13), 
                  bg="#0d1117", fg=TEXT_BRIGHT, insertbackground=ACCENT_CYAN,
                  relief="solid", bd=1, width=25)
    entry.config(highlightthickness=1, highlightbackground=CARD_BORDER, highlightcolor=colors[i])
    entry.pack(fill="x", pady=(12, 0), ipady=10)
    
# Prediction Result Display with Futuristic Styling - CENTERED
result_var = StringVar()
result_outer = Frame(scrollable_frame, bg=ACCENT_GREEN, relief="flat", bd=0)
result_outer.grid(row=3, column=0, pady=30)

result_frame = Frame(result_outer, bg=CARD_BG, relief="flat", bd=0)
result_frame.pack(padx=2, pady=2)  # Border effect

result_inner = Frame(result_frame, bg=CARD_BG)
result_inner.pack(padx=30, pady=25, fill="both")

Label(result_inner, text="📡 PREDICTION RESULT", font=("", 11, "bold"), 
      fg=TEXT_COLOR, bg=CARD_BG).pack(anchor="w", pady=(0, 12))  # Brighter label

result_label = Label(result_inner, textvariable=result_var, font=("", 15, "bold"), 
                     fg=TEXT_BRIGHT, bg=CARD_BG, wraplength=700, justify="center")  # Brighter result text
result_label.pack(fill="x")

# Futuristic Button Panel - CENTERED
button_frame = Frame(scrollable_frame, bg=BG_COLOR)
button_frame.grid(row=4, column=0, pady=(20, 30))

# Button configurations with modern colors and icons
buttons_config = [
    ("🎯 Predict Disaster", predict_disaster, ACCENT_RED, "#cc3d3d"),
    ("📊 Show Comparison", show_comparison_plot, ACCENT_CYAN, "#4a8ad9"),
    ("🔮 Confusion Matrix", show_confusion_matrix, ACCENT_PURPLE, "#9b73d9"),
    ("📈 Show Graphs", show_weather_graphs, ACCENT_GREEN, "#32933f"),
    ("🗑️ Clear All", clear_inputs, ACCENT_ORANGE, "#d98843")
]

button_widgets = []  # Store button references for animation

for i, (text, cmd, bg, active_bg) in enumerate(buttons_config):
    btn = Button(button_frame, text=text, font=("", 11, "bold"), command=cmd, 
                 bg=bg, fg=TEXT_BRIGHT, activebackground=active_bg, 
                 activeforeground=TEXT_BRIGHT, relief="flat", bd=0,
                 padx=22, pady=14, cursor="hand2")
    btn.grid(row=0, column=i, padx=10, pady=5)
    button_widgets.append((btn, bg, active_bg))
    
    # Hover effect simulation using enter/leave events
    def on_enter(e, button=btn, color=active_bg):
        button.config(bg=color)
    
    def on_leave(e, button=btn, color=bg):
        button.config(bg=color)
    
    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)

# Button glow animation
def button_glow_animation():
    global animations_running
    if not animations_running:
        return
    try:
        import random
        if button_widgets:
            btn, original_bg, hover_bg = random.choice(button_widgets)
            current_bg = btn.cget('bg')
            # Subtle glow effect
            if current_bg == original_bg:
                btn.config(bg=hover_bg)
                if animations_running:
                    app.after(150, lambda: btn.config(bg=original_bg) if animations_running else None)
        if animations_running:
            app.after(3000, button_glow_animation)  # Random glow every 3 seconds
    except:
        animations_running = False

app.after(2000, button_glow_animation)


# Update Scroll Region
scrollable_frame.update_idletasks()
canvas.config(scrollregion=canvas.bbox("all"))

# Window close handler to stop animations gracefully
def on_closing():
    global animations_running
    animations_running = False
    app.after(100, app.destroy)  # Give animations time to stop

app.protocol("WM_DELETE_WINDOW", on_closing)

app.mainloop()
