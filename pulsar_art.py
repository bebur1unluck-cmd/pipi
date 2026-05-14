import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Настройка интерфейса в строгом академическом стиле
st.set_page_config(
    page_title="Radio Astronomy Data Plot",
    page_icon="░",
    layout="centered"
)

# Оформление текстовых блоков (без эмодзи и маркетинговых описаний)
st.title("Визуализация сигналов периодических источников")
st.caption("Математическое моделирование серии радиоимпульсов с использованием функций Гаусса и стохастического шума.")

# Компактная боковая панель управления
st.sidebar.markdown("### Параметры симуляции")
num_pulses = st.sidebar.slider("Число профилей (N)", min_value=20, max_value=100, value=50, step=5)
line_width = st.sidebar.slider("Толщина линии (pt)", min_value=0.5, max_value=2.0, value=1.0, step=0.1)
noise_level = st.sidebar.slider("Амплитуда шума (σ)", min_value=0.0, max_value=0.8, value=0.2, step=0.05)

st.sidebar.markdown("---")
color_theme = st.sidebar.selectbox(
    "Цветовое решение холста", 
    ["Монохром (Архивный черный)", "Глубокий синий (Индиго)", "Светлая бумага (Инверсия)"]
)

# Генерация и фиксация состояния
regenerate = st.sidebar.button("Пересчитать матрицу сигналов")

if regenerate:
    st.session_state.seed = np.random.randint(0, 100000)
if 'seed' not in st.session_state:
    st.session_state.seed = 1979  # Отсылка к году выхода альбома Unknown Pleasures

np.random.seed(st.session_state.seed)

# Математические параметры сетки
points_per_pulse = 400
x = np.linspace(-8, 8, points_per_pulse)

# Конфигурация стилей отображения в зависимости от темы
if color_theme == "Монохrom (Архивный черный)":
    bg_color = "#111111"
    line_color = "#FFFFFF"
elif color_theme == "Глубокий синий (Индиго)":
    bg_color = "#0B132B"
    line_color = "#48CAE4"
else:
    bg_color = "#F4F4F6"
    line_color = "#1A1A1A"

# Инициализация холста
fig, ax = plt.subplots(figsize=(9, 11), facecolor=bg_color)
ax.set_facecolor(bg_color)

# Отрисовка сигналов сверху вниз (для правильного эффекта наложения)
for i in range(num_pulses):
    # Рассчитываем индекс от дальнего плана к ближнему
    idx = num_pulses - i
    y_base = idx * 1.5
    
    # Генерация основного импульса (Асимметричный Гаусс)
    center = np.random.uniform(-1.5, 1.5)
    width = np.random.uniform(0.5, 1.2)
    amplitude = np.random.uniform(3.5, 7.5)
    gauss = amplitude * np.exp(-((x - center) ** 2) / (2 * width ** 2))
    
    # Редкие вторичные эхо-сигналы
    if np.random.rand() > 0.6:
        echo_center = center + np.random.uniform(1.0, 2.5)
        echo_width = np.random.uniform(0.3, 0.7)
        gauss += (amplitude * 0.3) * np.exp(-((x - echo_center) ** 2) / (2 * echo_width ** 2))
        
    # Модуляция шума (шум затухает к краям графика для чистоты композиции)
    noise_envelope = np.exp(-(x ** 2) / 32)
    raw_noise = np.random.normal(0, noise_level, points_per_pulse)
    cosmic_noise = raw_noise * noise_envelope
    
    y = y_base + gauss + cosmic_noise
    
    # Эффект перекрытия нижележащих линий (маскирование)
    ax.fill_between(x, -5, y, color=bg_color, zorder=i * 2)
    
    # Отрисовка чистого контура графика
    ax.plot(x, y, color=line_color, linewidth=line_width, zorder=i * 2 + 1, solid_capstyle='round')

# Тонкая настройка границ отображения и скрытие осей
ax.set_xlim(-7.5, 7.5)
ax.axis('off')
plt.tight_layout()

# Вывод итоговой графики
st.pyplot(fig)
