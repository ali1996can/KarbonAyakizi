import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
import joblib
import os

def train_and_save_model(csv_path="results/usage_log.csv", model_path="utils/emission_model.pkl", encoder_path="utils/city_encoder.pkl"):
    if not os.path.exists(csv_path):
        print("❌ CSV dosyası bulunamadı.")
        return

    df = pd.read_csv(csv_path)

    # Eksik verileri temizle
    df.dropna(inplace=True)

    if "city" not in df.columns:
        print("❌ 'city' sütunu CSV dosyasında bulunamadı.")
        return

    # Kullanılacak sütunlar (motorcycle ve flight eklendi)
    feature_columns = ["beef", "chicken", "car", "electricity", "motorcycle", "flight", "city"]

    # Eksik sütun var mı kontrol et
    for col in feature_columns:
        if col not in df.columns:
            print(f"❌ '{col}' sütunu CSV dosyasında bulunamadı.")
            return

    # Giriş ve çıkışlar
    X = df[feature_columns]
    y = df["total_emission"]

    # Şehir sütununu One-Hot Encode et
    encoder = OneHotEncoder(sparse_output=False, handle_unknown="ignore")
    city_encoded = encoder.fit_transform(X[["city"]])
    city_df = pd.DataFrame(city_encoded, columns=encoder.get_feature_names_out(["city"]))

    # city sütununu çıkarıp diğer sütunlarla birleştir
    X_encoded = pd.concat([X.drop(columns=["city"]), city_df], axis=1)

    # Eğitim/test bölünmesi
    X_train, X_test, y_train, y_test = train_test_split(X_encoded, y, test_size=0.2, random_state=42)

    # Modeli eğit
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Modeli ve encoder'ı kaydet
    joblib.dump(model, model_path)
    joblib.dump(encoder, encoder_path)

    print("✅ Model ve encoder başarıyla kaydedildi.")

if __name__ == "__main__":
    train_and_save_model()
