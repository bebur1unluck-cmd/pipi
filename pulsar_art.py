import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# 1. Конфигурация интерфейса (Минимализм без ИИ-эмодзи)
st.set_page_config(
    page_title="Астрофизический архив: Пульсар",
    layout="centered"
)

st.title("📟 Радиоинтерферометрия PSR")
st.caption("Симуляция ленточного самописца аналоговой обсерватории (Стиль: Архив / Ретро-наука).")

# 2. Панель калибровки приборов (Ретро-параметры)
st.sidebar.header("🎛️ Калибровка сигнала")
num_pulses = st.sidebar.slider("Плотность записи (строки)", 20, 100, 50, 5)
drift_factor = st.sidebar.slider("Дрейф фазы (нестабильность)", 0.0, 2.0, 0.8, 0.1)
decay_factor = st.sidebar.slider("Затухание сигнала к краям", 0.1, 2.0, 1.0, 0.1)
interference_freq = st.sidebar.slider("Частота сетевой наводки (Гц)", 1, 10, 3, 1)

style_preset = st.sidebar.selectbox("Режим визуализации", ["Архивная бумага", "Зеленый фосфор", "Инверсия (Чернила)"])

regenerate = st.sidebar.button("📡 Перехватить новый сигнал")

if regenerate or 'seed' not in st.session_state:
    st.session_state.seed = np.random.randint(0, 100000)

np.random.seed(st.session_state.seed)

# 3. Математическая модель аналогового сигнала
points_per_pulse = 400
x = np.linspace(-15, 15, points_per_pulse)

# Настройка цветовых пресетов (Уходим от кислотного неона)
if style_preset == "Архивная бумага":
    bg_color, line_color, grid_color = '#F4F1EA', '#2B2A27', '#D1C6B4'
elif style_preset == "Зеленый фосфор":
    bg_color, line_color, grid_color = '#0D1B0E', '#4AF626', '#1B3B1E'
else: # Инверсия
    bg_color, line_color, grid_color = '#111111', '#FFFFFF', '#333333'

fig, ax = plt.subplots(figsize=(10, 12), facecolor=bg_color)
ax.set_facecolor(bg_color)

# Добавляем координатную сетку как на миллиметровке для эффекта документа
ax.grid(True, color=grid_color, linestyle='--', linewidth=0.5, zorder=0)

# Базовый дрейф центра для всей серии импульсов
global_drift = np.sin(np.linspace(0, np.pi * 2, num_pulses)) * drift_factor

for i in range(num_pulses):
    y_base = i * 2.0
    
    # Сложная форма импульса: основной всплеск + смещение фазы
    center = global_drift[i] + np.random.normal(0, 0.2)
    width = np.random.uniform(0.8, 1.5)
    amplitude = np.random.uniform(5, 12)
    
    # Гауссиана + затухание огибающей к краям (настоящая физика антенны)
    envelope = np.exp(-(x ** 2) / (2 * (8 * decay_factor) ** 2))
    gauss = amplitude * np.exp(-((x - center) ** 2) / (2 * width ** 2)) * envelope
    
    # Аналоговые помехи: белый шум + низкочастотная наводка 50Гц
    line_noise = np.random.normal(0, 0.2, points_per_pulse)
    hum_noise = 0.4 * np.sin(x * interference_freq + i * 0.5)
    
    y = y_base + gauss + line_noise + hum_noise
    
    # Непрозрачная подложка для эффекта наложения (скрывает задние линии)
    ax.fill_between(x, y_base, y, color=bg_color, zorder=i + 1)
    
    # Отрисовка линии самописца (без градиентов, чистая линия)
    ax.plot(x, y, color=line_color, linewidth=1.2, alpha=0.9, zorder=i + 1.1)

# Стилизация осей под технический график
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_color(grid_color)
ax.spines['bottom'].set_color(grid_color)
ax.tick_params(colors=line_color, labelsize=8)
ax.set_xlabel("Время задержки (мс)", color=line_color, fontsize=9)
ax.set_ylabel("Индекс суб-импульса", color=line_color, fontsize=9)

plt.tight_layout()

# 4. Вывод холста
st.pyplot(fig)
