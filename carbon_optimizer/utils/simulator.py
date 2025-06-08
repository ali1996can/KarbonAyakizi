# utils/simulator.py

from utils.calculator import calculate_emission

def simulate_scenarios(current_input, emission_factors):
    scenarios = []

    # Orijinal emisyonu hesapla
    original_emission, _ = calculate_emission(current_input, emission_factors)

    # 1. Dana etini %50 azalt
    input1 = current_input.copy()
    input1["beef"] *= 0.5
    em1, _ = calculate_emission(input1, emission_factors)
    scenarios.append(("🥩 Dana etini %50 azalt", em1))

    # 2. Tavuk etini %30 azalt
    input2 = current_input.copy()
    input2["chicken"] *= 0.7
    em2, _ = calculate_emission(input2, emission_factors)
    scenarios.append(("🍗 Tavuk etini %30 azalt", em2))

    # 3. Elektrik kullanımını %25 azalt
    input3 = current_input.copy()
    input3["electricity"] *= 0.75
    em3, _ = calculate_emission(input3, emission_factors)
    scenarios.append(("⚡ Elektrik kullanımını %25 azalt", em3))

    # 4. Araba kullanımını %50 azalt
    input4 = current_input.copy()
    input4["car"] *= 0.5
    em4, _ = calculate_emission(input4, emission_factors)
    scenarios.append(("🚗 Araba kullanımını %50 azalt", em4))

    

    # 6. Elektrikli araca geçiş (kendi hesaplamamız)
    input6 = current_input.copy()
    km = input6.get("car", 0)
    electric_car_factor = 0.04  # tahmini sabit
    em6 = (
        input6.get("beef", 0) * emission_factors.get("beef", 0) +
        input6.get("chicken", 0) * emission_factors.get("chicken", 0) +
        input6.get("electricity", 0) * emission_factors.get("electricity", 0) +
        input6.get("flight", 0) * emission_factors.get("flight", 0) +
        km * electric_car_factor
    )
    scenarios.append(("🔋 Elektrikli araca geçiş", em6))

    return scenarios

