import joblib
import pandas as pd
import os

def predict_emission(input_data, model_path="utils/emission_model.pkl", encoder_path="utils/city_encoder.pkl"):
    # Model ve encoder dosyalarının var olup olmadığını kontrol et
    if not os.path.exists(model_path):
        print("❌ Model dosyası bulunamadı.")
        return None
    if not os.path.exists(encoder_path):
        print("❌ Encoder dosyası bulunamadı.")
        return None

    # Model ve encoder'ı yükle
    model = joblib.load(model_path)
    encoder = joblib.load(encoder_path)

    # Şehir bilgisini one-hot encode et
    city_encoded = encoder.transform([[input_data["city"]]])

    # Diğer sayısal veriler
    numeric_data = [[
        input_data["beef"],
        input_data["chicken"],
        input_data["car"],
        input_data["electricity"]
    ]]

    # Hepsini birleştir (sayısal + şehir verisi)
    final_input = pd.DataFrame([numeric_data[0] + list(city_encoded[0])])

    # Tahmin yap
    prediction = model.predict(final_input)[0]
    return round(prediction, 2)
