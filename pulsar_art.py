import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# 1. Настройка конфигурации веб-страницы
st.set_page_config(
    page_title="Pulsar Space Data Art",
    page_icon="🌌",
    layout="centered"
)

# Стилизация заголовков веб-интерфейса
st.title("🌌 Космический Дата-Арт")
st.caption("Генеративная визуализация радиоизлучения пульсаров в реальном времени.")

# 2. Боковая панель управления (Интерактивные параметры)
st.sidebar.header("🎛️ Настройки графики")
num_pulses = st.sidebar.slider("Количество линий (сигналов)", min_value=10, max_value=80, value=40, step=5)
line_width = st.sidebar.slider("Толщина светящихся линий", min_value=0.5, max_value=3.0, value=1.6, step=0.1)
noise_level = st.sidebar.slider("Уровень космических помех", min_value=0.0, max_value=1.0, value=0.25, step=0.05)
color_theme = st.sidebar.selectbox("Цветовая схема", ["Неоновый бирюзовый", "Огненный красный", "Космический зеленый"])

# Кнопка для мгновенной перегенерации случайных данных
regenerate = st.sidebar.button("🔄 Сгенерировать новый паттерн")

# Фиксируем или сбрасываем зерно рандома при нажатии кнопки
if regenerate:
    st.session_state.seed = np.random.randint(0, 100000)
if 'seed' not in st.session_state:
    st.session_state.seed = 42

np.random.seed(st.session_state.seed)

# 3. Математическое ядро визуализации
points_per_pulse = 300
x = np.linspace(-10, 10, points_per_pulse)

# Инициализация темного холста
fig, ax = plt.subplots(figsize=(10, 12), facecolor='#0B0C10')
ax.set_facecolor('#0B0C10')

for i in range(num_pulses):
    y_base = i * 1.8
    
    # Генерация всплесков (Функция Гаусса)
    center = np.random.uniform(-2.5, 2.5)
    width = np.random.uniform(0.6, 1.8)
    amplitude = np.random.uniform(4, 10)
    gauss = amplitude * np.exp(-((x - center) ** 2) / (2 * width ** 2))
    
    # Вторичные гармоники и шум
    secondary_noise = 1.5 * np.exp(-((x - (center + 3)) ** 2) / 0.8) if np.random.rand() > 0.4 else 0
    cosmic_noise = np.random.normal(0, noise_level, points_per_pulse)
    
    y = y_base + gauss + secondary_noise + cosmic_noise
    
    # Эффект 3D-перекрытия: заливка под графиком в цвет фона
    ax.fill_between(x, y_base, y, color='#0B0C10', zorder=num_pulses - i)
    
    # Расчет цвета на основе выбранной темы
    progress = i / num_pulses
    if color_theme == "Неоновый бирюзовый":
        line_color = (0.1, 0.8 * progress, 0.9, 0.8)
    elif color_theme == "Огненный красный":
        line_color = (0.9, 0.3 * progress, 0.1, 0.8)
    else: # Зеленый
        line_color = (0.2, 0.9, 0.4 * progress, 0.8)
        
    # Отрисовка контура
    ax.plot(x, y, color=line_color, linewidth=line_width, zorder=num_pulses - i + 0.1)

ax.axis('off')
plt.tight_layout()

# 4. Вывод готового холста в браузер
st.pyplot(fig)
