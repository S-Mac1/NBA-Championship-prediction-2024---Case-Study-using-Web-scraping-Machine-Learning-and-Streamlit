# Import der Module für das Vorhersagemodell
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report

# Datenbank aller Saisons außer der Saison 2024 laden
df = pd.read_csv("exclude_2024.csv")

# DataFrame bereinigen für den Train-Test-Split
df = df.drop("team", axis = 1)
df = df[df['season'] >= 1980]
df = df.drop("Unnamed: 0.1", axis = 1)
df = df.drop("Unnamed: 0", axis = 1)

# Features
X = df.drop("champion", axis = 1)

# Labels
y = df["champion"]

# Train-Test-Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.33, random_state = 42)

# Modell laden
logisReg = LogisticRegression()

# Modell trainieren
logisReg.fit(X_train, y_train)

# Modell testen
predictions = logisReg.predict(X_test)

# Auswertung erstellen
print(classification_report(y_test, predictions))

# Datenbank der Saison 2024 laden für die Vorhersage der aktuellen Teams in Streamlit.py
predict_df = pd.read_csv("season_2024.csv")