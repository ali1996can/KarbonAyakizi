def generate_advice(details):
    advice = []

    for category, (value, emission) in details.items():
        if category == "beef" and emission > 8:
            advice.append(
                "🥩 Dana eti tüketiminiz yüksek. Hayvansal protein yerine nohut, mercimek gibi bitkisel kaynaklara yönelerek "
                "yılda yüzlerce kilogram CO₂ tasarruf edebilirsiniz."
            )

        elif category == "chicken" and emission > 6:
            advice.append(
                "🍗 Tavuk tüketiminiz oldukça fazla. Haftalık tüketimi sınırlamak ve sebze ağırlıklı beslenmeye yönelmek emisyonunuzu azaltabilir."
            )

        elif category == "car" and emission > 10:
            advice.append(
                "🚗 Araba kullanımınız yoğun görünüyor. Haftada birkaç gün toplu taşıma, bisiklet veya yürüyüşle ulaşım sağlayarak "
                "karbon ayak izinizi önemli ölçüde azaltabilirsiniz."
            )

       

        elif category == "electricity" and emission > 25:
            advice.append(
                "💡 Elektrik tüketiminiz yüksek. Enerji tasarruflu LED ampuller, A+++ cihazlar ve fişleri prizden çekmek "
                "gibi küçük alışkanlıklar büyük fark yaratabilir."
            )

        

    if not advice:
        advice.append("🌱 Harika! Karbon ayak izinizi düşük tutuyorsunuz. Bu bilinçli yaklaşımı sürdürmeniz çevre için çok değerli.")

    return advice

