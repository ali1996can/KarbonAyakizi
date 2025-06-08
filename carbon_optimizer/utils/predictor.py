# utils/predictor.py

import joblib
import pandas as pd

def load_model(model_path="utils/emission_model.pkl"):
    return joblib.load(model_path)

def load_encoder(encoder_path="utils/city_encoder.pkl"):
    return joblib.load(encoder_path)

def predict_emission(model, input_data, encoder):
    df = pd.DataFrame([input_data])
    
    # Şehir bilgisini encode et
    city_encoded = encoder.transform(df[["city"]])
    city_df = pd.DataFrame(city_encoded, columns=encoder.get_feature_names_out(["city"]))

    # Şehir sütununu düşür ve encode edilmiş sütunları ekle
    df = pd.concat([df.drop(columns=["city"]), city_df], axis=1)

    return model.predict(df)[0]
