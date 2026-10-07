import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix


# -----------------------------
# 1. Load Dataset
# -----------------------------

df = pd.read_csv("kochi_weather_2023_2025.csv")

print("Dataset shape:", df.shape)


# -----------------------------
# 2. Convert Weather Code
#    into Weather Class
# -----------------------------

def classify_weather(code):

    if code in [0, 1]:
        return "Clear"

    elif code in [2, 3]:
        return "Cloudy"

    elif code in [51, 53, 55]:
        return "Drizzle"

    elif code in [61, 63, 65]:
        return "Rain"

    else:
        return "Other"


df["weather_class"] = df["weather_code"].apply(classify_weather)

# Remove unwanted classes
df = df[df["weather_class"] != "Other"]


# -----------------------------
# 3. Select Features
# -----------------------------

features = [
    "temperature",
    "humidity",
    "precipitation",
    "cloud_cover",
    "wind_speed",
    "surface_pressure"
]

target = "weather_class"

X = df[features]
y = df[target]


# -----------------------------
# 4. Train/Test Split
# -----------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)


# -----------------------------
# 5. Create Decision Tree
# -----------------------------

model = DecisionTreeClassifier(
    max_depth=8,
    random_state=42,
    class_weight="balanced"
)


# -----------------------------
# 6. Train Model
# -----------------------------

model.fit(X_train, y_train)


# -----------------------------
# 7. Test Model
# -----------------------------

y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)

print("\nAccuracy:", round(accuracy * 100, 2), "%")

print("\nClassification Report:")
print(classification_report(y_test, y_pred))

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))


# -----------------------------
# 8. Save Model
# -----------------------------

joblib.dump(model, "weather_decision_tree.pkl")

print("\nModel saved as weather_decision_tree.pkl")