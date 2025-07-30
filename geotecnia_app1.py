import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Fórmulas do ângulo de atrito
def phi_1(N): return 15 + np.sqrt(24 * N)
def phi_2(N): return 20 + np.sqrt(15.5 * N)
def phi_3(N): return 27.1 + 0.3 * N - 0.00054 * N * N
def phi_4(N): return 28 + 0.4 * N
def phi_5(N): return 27.5 + 9.2 * np.log10(np.maximum(N, 0.1))

# Fórmulas da coesão
def c_1(N): return 10 * N  # Teixeira e Godoy (1996)
def c_2(N): return N / 0.35  # Berberian (2015)

st.title("Estimativa do Ângulo de Atrito e Coesão pelo Nspt")

# Entrada Nspt
Nspt = st.number_input("Digite o valor de Nspt (0 a 30):", min_value=0.0, max_value=30.0, step=0.1)

# Calcular valores
N_vals = np.linspace(0, 30, 300)
phis = [phi_1(N_vals), phi_2(N_vals), phi_3(N_vals), phi_4(N_vals), phi_5(N_vals)]
phi_avg = np.mean(phis, axis=0)

c1_vals = c_1(N_vals)
c2_vals = c_2(N_vals)

phi_input_vals = [f(Nspt) for f in [phi_1, phi_2, phi_3, phi_4, phi_5]]
phi_input_avg = np.mean(phi_input_vals)

c1_input = c_1(Nspt)
c2_input = c_2(Nspt)
c_avg = (c1_input + c2_input) / 2

# Mostrar resultados
st.subheader("Ângulo de Atrito (φ) para Nspt informado")
for i, val in enumerate(phi_input_vals, 1):
    st.write(f"φ{i}: {val:.2f}°")
st.write(f"Média: {phi_input_avg:.2f}°")

st.subheader("Coesão estimada (c) para Nspt informado")
st.write(f"c1 (Teixeira e Godoy, 1996): {c1_input:.2f} kPa")
st.write(f"c2 (Berberian, 2015): {c2_input:.2f} kPa")
st.write(f"Média: {c_avg:.2f} kPa")

# Plotar gráficos
import matplotlib.pyplot as plt

fig, axs = plt.subplots(1, 2, figsize=(12, 5))

# Gráfico ângulo de atrito
autores_phi = [
    "Teixeira (1996)",
    "Hatanaka e Uchida (1996)",
    "Peck, Hanson e Thornburn (1974)",
    "Godoy (1983)",
    "Kulhawy e Chen (2007)"
]
cores_phi = ['blue', 'green', 'orange', 'purple', 'brown']

for i in range(5):
    axs[0].plot(N_vals, phis[i], label=autores_phi[i], linestyle='--', color=cores_phi[i])
    axs[0].scatter(Nspt, phi_input_vals[i], color=cores_phi[i])
axs[0].plot(N_vals, phi_avg, label="Média", color="black", linewidth=2)
axs[0].scatter(Nspt, phi_input_avg, color="red", label="Valor Médio")

axs[0].set_title("Ângulo de Atrito (φ) vs Nspt")
axs[0].set_xlabel("Nspt")
axs[0].set_ylabel("Ângulo de Atrito φ (°)")
axs[0].set_xlim(0, 30)
axs[0].grid(True)
axs[0].legend()

# Gráfico coesão
axs[1].plot(N_vals, c1_vals, label="Teixeira e Godoy (1996) - Argilas saturadas", linestyle='--', color='blue')
axs[1].plot(N_vals, c2_vals, label="Berberian (2015) - Solos não saturados", linestyle='--', color='green')
axs[1].scatter(Nspt, c1_input, color='blue')
axs[1].scatter(Nspt, c2_input, color='green')
axs[1].set_title("Coesão estimada (c) vs Nspt")
axs[1].set_xlabel("Nspt")
axs[1].set_ylabel("Coesão c (kPa)")
axs[1].set_xlim(0, 30)
axs[1].grid(True)
axs[1].legend()

st.pyplot(fig)

st.markdown("""
---
### Fórmulas usadas

**Ângulo de atrito φ (°):**

- φ1 (Teixeira, 1996): φ = 15 + √(24 × Nspt)  
- φ2 (Hatanaka e Uchida, 1996): φ = 20 + √(15.5 × Nspt)  
- φ3 (Peck, Hanson e Thornburn, 1974): φ = 27,1 + 0,3 × Nspt - 0,00054 × Nspt²  
- φ4 (Godoy, 1983): φ = 28 + 0,4 × Nspt  
- φ5 (Kulhawy e Chen, 2007): φ = 27,5 + 9,2 × log₁₀(Nspt)  

**Coesão c (kPa):**

- c1 (Teixeira e Godoy, 1996): c = 10 × Nspt (argilas saturadas)  
- c2 (Berberian, 2015): c = Nspt / 0,35 (solos não saturados)
""")
