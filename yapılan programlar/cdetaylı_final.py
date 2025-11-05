import pandas as pd
import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox
from scipy.stats import poisson

# CSV yükleme
def load_csv():
    path = filedialog.askopenfilename(title="CSV dosyanızı seçin", filetypes=[("CSV files","*.csv")])
    if not path:
        messagebox.showerror("Hata", "Dosya seçilmedi!")
        return None
    try:
        df = pd.read_csv(path)
        # Eksik sütun varsa varsayılan değer ekle
        defaults = {
            'xG': 1.5, 'GoalsFor': 1.5, 'Corners': 5,
            'Shots': 10, 'ShotsOnTarget': 4, 'Possession': 50,
            'Injuries': 0, 'Weather': 0, 'Referee': 0
        }
        for col, val in defaults.items():
            if col not in df.columns:
                df[col] = val
        return df
    except Exception as e:
        messagebox.showerror("Hata", f"CSV yüklenemedi: {e}")
        return None

# Ağırlıklı lambda hesaplama
def weighted_lambda(row, is_home):
    lam = row['xG']
    lam *= 1.10 if is_home else 0.90
    lam *= 1 + (row['GoalsFor'] - 1.5)/10
    lam *= 1 + (row['ShotsOnTarget']/row['Shots'] - 0.3)/3
    lam *= 1 + (row['Possession']/100 - 0.5)/5
    lam *= 1 - row['Injuries']*0.05
    lam *= 1 - row['Weather']*0.03
    lam *= 1 - row['Referee']*0.02
    return lam

# Poisson ile skor tahmini
def poisson_scores(home_lambda, away_lambda, max_goals=5):
    scores = []
    for h in range(0, max_goals+1):
        for a in range(0, max_goals+1):
            prob = poisson.pmf(h, home_lambda) * poisson.pmf(a, away_lambda)
            scores.append(((h,a), prob))
    scores.sort(key=lambda x: x[1], reverse=True)
    cumulative = 0
    top_scores = []
    for score, prob in scores:
        top_scores.append((score, prob))
        cumulative += prob
        if cumulative >= 0.8:  # %80 güven aralığı
            break
    avg_home = sum(h*prob for (h,a),prob in top_scores)
    avg_away = sum(a*prob for (h,a),prob in top_scores)
    min_home = min(h for (h,a),_ in top_scores)
    max_home = max(h for (h,a),_ in top_scores)
    min_away = min(a for (h,a),_ in top_scores)
    max_away = max(a for (h,a),_ in top_scores)
    return round(avg_home), round(avg_away), (min_home,max_home), (min_away,max_away), top_scores

# Tahmin
def predict_match(df):
    # Team sütunu yoksa HomeTeam ve AwayTeam'den oluştur
    if 'Team' not in df.columns:
        if 'HomeTeam' in df.columns and 'AwayTeam' in df.columns:
            teams = [df.iloc[0]['HomeTeam'], df.iloc[0]['AwayTeam']]
            df = df.copy()
            df.insert(0, 'Team', teams)
        else:
            raise ValueError("CSV'de 'Team' veya 'HomeTeam/AwayTeam' sütunları bulunamadı!")

    home_team = df.iloc[0]['Team']
    away_team = df.iloc[1]['Team']
    home_corners = df.iloc[0].get('Corners', 5)
    away_corners = df.iloc[1].get('Corners', 5)
    home_lambda = weighted_lambda(df.iloc[0], True)
    away_lambda = weighted_lambda(df.iloc[1], False)
    home_goals, away_goals, (min_h,max_h), (min_a,max_a), top_scores = poisson_scores(home_lambda, away_lambda)
    winner = home_team if home_goals>away_goals else away_team if home_goals<away_goals else 'Berabere'
    total_goals = home_goals + away_goals
    over_under_2_5 = 'Üst' if total_goals > 2.5 else 'Alt'
    total_corners = round(home_corners + away_corners)
    corner_8_5 = 'Üst' if total_corners > 8.5 else 'Alt'
    if total_goals <= 1:
        total_goals_range = '0,1 gol'
    elif total_goals <= 3:
        total_goals_range = '2,3 gol'
    elif total_goals <= 5:
        total_goals_range = '4,5 gol'
    else:
        total_goals_range = '6 gol ve üzeri'
    confidence = round(sum(prob for _,prob in top_scores)*100,1)
    return {
        'Tahmini Skor': f"{home_team} {home_goals} - {away_goals} {away_team}",
        'Min-Max Skor Home': f"{min_h}-{max_h}",
        'Min-Max Skor Away': f"{min_a}-{max_a}",
        'Kazanan': winner,
        '2.5 Gol Alt/Üst': over_under_2_5,
        'Toplam Korner': total_corners,
        'Korner 8.5 Alt/Üst': corner_8_5,
        'Toplam Gol Aralığı': total_goals_range,
        'Güven Yüzdesi': f"{confidence}%"
    }

# GUI
def run_prediction():
    df = load_csv()
    if df is not None:
        result = predict_match(df)
        output_text.delete('1.0', tk.END)
        for key, value in result.items():
            output_text.insert(tk.END, f"{key}: {value}\n")

root = tk.Tk()
root.title("Gelişmiş C Modeli Tahmin")
root.geometry("550x450")
load_btn = tk.Button(root, text="CSV Yükle ve Tahmin Et", command=run_prediction)
load_btn.pack(pady=10)
output_text = tk.Text(root, width=65, height=22)
output_text.pack(padx=10, pady=10)
root.mainloop()
