from __future__ import annotations

from dataclasses import dataclass
from html import escape
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parent
OUT = ROOT / "svg-screens"
W = 390
H = 844


COLORS = {
    "bg": "#F8F1EC",
    "surface": "#FFFDFC",
    "surface_soft": "#F3E5DD",
    "text": "#2F2824",
    "muted": "#806B62",
    "line": "#E4D1C8",
    "primary": "#A96F58",
    "primary_dark": "#744637",
    "primary_soft": "#EBD4CB",
    "accent": "#4D7C72",
    "accent_soft": "#DCEBE7",
    "warning": "#C78345",
    "white": "#FFFFFF",
}


@dataclass
class Svg:
    title: str
    parts: list[str]

    def __init__(self, title: str) -> None:
        self.title = title
        self.parts = []

    def add(self, value: str) -> None:
        self.parts.append(value)

    def render(self) -> str:
        return "\n".join(
            [
                f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" fill="none">',
                "  <defs>",
                "    <filter id=\"cardShadow\" x=\"-20%\" y=\"-20%\" width=\"140%\" height=\"140%\">",
                "      <feDropShadow dx=\"0\" dy=\"10\" stdDeviation=\"12\" flood-color=\"#2F2824\" flood-opacity=\"0.10\"/>",
                "    </filter>",
                "    <style>",
                "      text { font-family: Inter, Arial, sans-serif; dominant-baseline: hanging; }",
                "      .small { font-size: 11px; }",
                "      .body { font-size: 13px; }",
                "      .label { font-size: 12px; font-weight: 600; }",
                "      .h1 { font-size: 24px; font-weight: 800; }",
                "      .h2 { font-size: 18px; font-weight: 700; }",
                "      .btn { font-size: 14px; font-weight: 700; }",
                "    </style>",
                "  </defs>",
                f'  <title>{escape(self.title)}</title>',
                f'  <rect width="{W}" height="{H}" rx="28" fill="{COLORS["bg"]}"/>',
                *self.parts,
                "</svg>",
                "",
            ]
        )


def slug(name: str) -> str:
    value = re.sub(r"[^a-zA-Z0-9]+", "_", name.lower()).strip("_")
    return value


def rect(s: Svg, x: float, y: float, w: float, h: float, fill: str, rx: float = 0, stroke: str | None = None,
         sw: float = 1, opacity: float | None = None, shadow: bool = False) -> None:
    extra = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ""
    if opacity is not None:
        extra += f' opacity="{opacity}"'
    if shadow:
        extra += ' filter="url(#cardShadow)"'
    s.add(f'  <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}"{extra}/>')


def circle(s: Svg, cx: float, cy: float, r: float, fill: str, stroke: str | None = None) -> None:
    extra = f' stroke="{stroke}" stroke-width="1"' if stroke else ""
    s.add(f'  <circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}"{extra}/>')


def line(s: Svg, x1: float, y1: float, x2: float, y2: float, color: str = "#FFFFFF", sw: float = 1,
         opacity: float = 1) -> None:
    s.add(
        f'  <line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" '
        f'stroke-width="{sw}" opacity="{opacity}" stroke-linecap="round"/>'
    )


def txt(s: Svg, value: str, x: float, y: float, fill: str = COLORS["text"], size: int = 13,
        weight: int = 400, width: int | None = None, align: str = "start", line_height: int | None = None) -> None:
    lines = wrap(value, width or 10_000, size)
    lh = line_height or round(size * 1.35)
    anchor = {"start": "start", "middle": "middle", "end": "end"}[align]
    class_name = ""
    if size == 11:
        class_name = " small"
    elif size == 12 and weight >= 600:
        class_name = " label"
    elif size == 13:
        class_name = " body"
    elif size == 18 and weight >= 700:
        class_name = " h2"
    elif size == 24 and weight >= 700:
        class_name = " h1"
    s.add(
        f'  <text x="{x}" y="{y}" fill="{fill}" font-size="{size}" font-weight="{weight}" '
        f'text-anchor="{anchor}" class="{class_name.strip()}">'
    )
    for i, item in enumerate(lines):
        dy = 0 if i == 0 else lh
        s.add(f'    <tspan x="{x}" dy="{dy}">{escape(item)}</tspan>')
    s.add("  </text>")


def wrap(value: str, max_width: int, size: int) -> list[str]:
    if max_width >= 9000:
        return value.split("\n")
    approx = max(8, int(max_width / (size * 0.55)))
    out: list[str] = []
    for source in value.split("\n"):
        words = source.split()
        current = ""
        for word in words:
            candidate = word if not current else f"{current} {word}"
            if len(candidate) <= approx:
                current = candidate
            else:
                if current:
                    out.append(current)
                current = word
        if current:
            out.append(current)
    return out or [""]


def status(s: Svg) -> None:
    txt(s, "9:41", 24, 16, size=13, weight=700)
    rect(s, 300, 18, 42, 12, COLORS["text"], rx=6, opacity=0.18)
    rect(s, 346, 18, 20, 12, COLORS["text"], rx=6, opacity=0.18)


def header(s: Svg, title: str, subtitle: str, back_label: str | None = None, favorite: bool = True) -> None:
    status(s)
    start = 72 if back_label else 20
    if back_label:
        rect(s, 20, 48, 40, 40, COLORS["surface"], rx=14, shadow=True)
        txt(s, "‹", 40, 55, COLORS["primary_dark"], size=24, weight=800, align="middle")
    txt(s, title, start, 46, size=22, weight=800, width=230)
    txt(s, subtitle, start, 76, COLORS["muted"], size=12, width=255)
    if favorite:
        rect(s, 330, 50, 40, 40, COLORS["surface"], rx=14, shadow=True)
        txt(s, "♡", 350, 57, COLORS["primary"], size=18, weight=700, align="middle")


def button(s: Svg, label: str, x: float, y: float, w: float, variant: str = "primary") -> None:
    fill = COLORS["primary"]
    fg = COLORS["white"]
    stroke = None
    if variant == "secondary":
        fill = COLORS["surface"]
        fg = COLORS["primary_dark"]
        stroke = COLORS["line"]
    elif variant == "soft":
        fill = COLORS["primary_soft"]
        fg = COLORS["primary_dark"]
    rect(s, x, y, w, 52, fill, rx=18, stroke=stroke, shadow=variant != "secondary")
    txt(s, label, x + w / 2, y + 17, fg, size=14, weight=700, align="middle")


def section(s: Svg, title: str, y: float) -> None:
    txt(s, title, 20, y, size=17, weight=700)


def chip(s: Svg, label: str, x: float, y: float, w: float, active: bool = False) -> None:
    rect(s, x, y, w, 36, COLORS["primary_soft"] if active else COLORS["surface"], rx=18,
         stroke=None if active else COLORS["line"])
    txt(s, label, x + w / 2, y + 10, COLORS["primary_dark"] if active else COLORS["muted"], size=12,
        weight=700 if active else 500, align="middle")


def chip_grid(s: Svg, labels: list[str], y: float, columns: int = 2, active_mod: int = 3) -> None:
    gutter = 10
    cell = (350 - gutter * (columns - 1)) / columns
    for i, label in enumerate(labels):
        col = i % columns
        row = i // columns
        chip(s, label, 20 + col * (cell + gutter), y + row * 48, cell, i % active_mod == 0)


def room_mock(s: Svg, x: float, y: float, w: float, h: float, mood: str = "warm") -> None:
    rect(s, x, y, w, h, COLORS["surface"], rx=min(22, h / 4), shadow=True)
    main = COLORS["primary_soft"] if mood == "warm" else COLORS["accent_soft"]
    rect(s, x + w * 0.08, y + h * 0.1, w * 0.84, h * 0.46, main, rx=16)
    rect(s, x + w * 0.14, y + h * 0.62, w * 0.34, h * 0.22, "#D6B1A6", rx=9)
    rect(s, x + w * 0.54, y + h * 0.62, w * 0.32, h * 0.22, "#CFA398", rx=9)
    rect(s, x + w * 0.18, y + h * 0.2, w * 0.24, h * 0.22, COLORS["white"], rx=10, opacity=0.6)
    line(s, x + w * 0.5, y + h * 0.16, x + w * 0.5, y + h * 0.88, COLORS["white"], 1, 0.7)


def card(s: Svg, x: float, y: float, w: float, h: float, title: str, body: str, number: str | None = None) -> None:
    rect(s, x, y, w, h, COLORS["surface"], rx=24, shadow=True)
    if number:
        rect(s, x + 14, y + 14, 42, 42, COLORS["primary_soft"], rx=14)
        txt(s, number, x + 35, y + 25, COLORS["primary_dark"], size=13, weight=800, align="middle")
        tx = x + 14
        ty = y + 68
    else:
        tx = x + 18
        ty = y + 18
    txt(s, title, tx, ty, size=15, weight=700, width=int(w - 28))
    txt(s, body, tx, ty + 28, COLORS["muted"], size=11, width=int(w - 28), line_height=15)


def project_card(s: Svg, y: float, title: str, body: str, tag: str = "совпадает") -> None:
    rect(s, 20, y, 350, 146, COLORS["surface"], rx=28, shadow=True)
    room_mock(s, 34, y + 14, 126, 118, "cool")
    txt(s, title, 178, y + 22, size=17, weight=700, width=150, line_height=23)
    txt(s, body, 178, y + 78, COLORS["muted"], size=12, width=150, line_height=16)
    rect(s, 178, y + 116, 86, 22, COLORS["accent_soft"], rx=11)
    txt(s, tag, 221, y + 120, COLORS["accent"], size=10, weight=700, align="middle")
    txt(s, "›", 340, y + 58, COLORS["primary"], size=22, weight=800, align="middle")


def small_project(s: Svg, y: float, title: str, body: str) -> None:
    rect(s, 20, y, 350, 98, COLORS["surface"], rx=24, shadow=True)
    room_mock(s, 34, y + 14, 86, 70)
    txt(s, title, 136, y + 18, size=16, weight=700, width=180)
    txt(s, body, 136, y + 50, COLORS["muted"], size=12, width=190)
    txt(s, "›", 338, y + 36, COLORS["primary"], size=22, weight=800, align="middle")


def master_card(s: Svg, y: float, name: str, body: str) -> None:
    rect(s, 20, y, 350, 98, COLORS["surface"], rx=24, shadow=True)
    circle(s, 67, y + 49, 29, COLORS["primary_soft"])
    initials = "".join(part[0] for part in name.split()[:2]).upper()
    txt(s, initials, 67, y + 40, COLORS["primary_dark"], size=14, weight=800, align="middle")
    txt(s, name, 104, y + 18, size=17, weight=700, width=175)
    txt(s, body, 104, y + 50, COLORS["muted"], size=12, width=190)
    rect(s, 300, y + 26, 42, 28, COLORS["primary_soft"], rx=14)
    txt(s, "4.9", 321, y + 33, COLORS["primary_dark"], size=12, weight=800, align="middle")


def bottom_nav(s: Svg, active: str) -> None:
    rect(s, 20, 786, 350, 48, COLORS["surface"], rx=22, shadow=True)
    items = [("home", "Дом"), ("catalog", "Каталог"), ("favorites", "Избранное"), ("specialists", "Профи")]
    for i, (key, label) in enumerate(items):
        x = 32 + i * 82
        rect(s, x, 794, 66, 32, COLORS["primary_soft"] if key == active else COLORS["surface"], rx=16)
        txt(s, label, x + 33, 803, COLORS["primary_dark"] if key == active else COLORS["muted"], size=11,
            weight=700 if key == active else 500, align="middle")


def metrics(s: Svg, y: float, items: list[tuple[str, str]]) -> None:
    for i, (value, label) in enumerate(items):
        x = 20 + i * 116
        rect(s, x, y, 106, 70, COLORS["surface"], rx=22, shadow=True)
        txt(s, value, x + 53, y + 16, size=18, weight=800, align="middle")
        txt(s, label, x + 53, y + 44, COLORS["muted"], size=10, align="middle")


def input_box(s: Svg, y: float, label: str, value: str) -> None:
    rect(s, 20, y, 350, 72, COLORS["surface"], rx=20, shadow=True)
    txt(s, label, 38, y + 12, COLORS["muted"], size=11, weight=700)
    txt(s, value, 38, y + 34, size=14, width=290)


def render_cover() -> Svg:
    s = Svg("00 Обзор прототипа")
    rect(s, 0, 0, W, H, COLORS["surface"], rx=28)
    txt(s, "Дизайн-проект приложения", 28, 48, size=24, weight=800, width=290)
    txt(s, "Для начинающих дизайнеров интерьера", 28, 112, COLORS["muted"], size=15, width=270)
    rect(s, 28, 176, 334, 190, COLORS["surface_soft"], rx=28)
    room_mock(s, 50, 198, 290, 146)
    txt(s, "Основные пользовательские сценарии", 28, 402, size=17, weight=700)
    bullets = [
        "Подбор дизайна по типу жилья, стилю и состоянию",
        "Каталог готовых кейсов и фильтрация",
        "База проверенных дизайнеров и инженеров",
        "Сохранение понравившихся проектов"
    ]
    for i, item in enumerate(bullets):
        y = 444 + i * 44
        circle(s, 40, y + 10, 11, COLORS["accent_soft"])
        txt(s, "✓", 40, y + 4, COLORS["accent"], size=12, weight=800, align="middle")
        txt(s, item, 62, y, size=13, width=285)
    button(s, "Открыть прототип", 44, 716, 302)
    return s


def render_home() -> Svg:
    s = Svg("01 Домашняя страница")
    header(s, "SenseRoom", "Подбор интерьеров для сложных задач", favorite=True)
    rect(s, 20, 112, 350, 156, COLORS["primary_soft"], rx=28)
    txt(s, "Начните с задачи", 40, 136, size=24, weight=800, width=180)
    txt(s, "Выберите комнату, стиль и технические ограничения.", 40, 202, COLORS["primary_dark"], size=13, width=205)
    room_mock(s, 236, 132, 110, 112)
    button(s, "Подобрать дизайн", 40, 284, 176)
    section(s, "Быстрый доступ", 354)
    card(s, 20, 390, 166, 130, "Поиск дизайна", "По объекту, стилю и состоянию", "01")
    card(s, 204, 390, 166, 130, "Каталог идей", "Готовые кейсы и решения", "02")
    card(s, 20, 538, 166, 130, "Специалисты", "Дизайнеры и инженеры", "03")
    card(s, 204, 538, 166, 130, "Избранное", "Сохраненные проекты", "04")
    bottom_nav(s, "home")
    return s


def render_design_search() -> Svg:
    s = Svg("02 Поиск дизайна")
    header(s, "Поиск дизайна", "Алгоритм подбора для начинающих дизайнеров", "home")
    rect(s, 20, 108, 350, 96, COLORS["accent_soft"], rx=24)
    txt(s, "Опишите объект", 40, 128, size=21, weight=800)
    txt(s, "Чем точнее критерии, тем полезнее подборка.", 40, 164, COLORS["muted"], size=13, width=260)
    section(s, "Что проектируем?", 234)
    choice(s, 270, "Отдельную комнату", "Кухня, спальня, детская, санузел", "Комната")
    choice(s, 388, "Жилье целиком", "Студия, квартира, дом, апартаменты", "Жилье")
    section(s, "Нужна помощь с выбором?", 536)
    button(s, "Пройти короткий выбор объекта", 20, 572, 350, "secondary")
    button(s, "Смотреть каталог идей", 20, 640, 350, "soft")
    bottom_nav(s, "home")
    return s


def choice(s: Svg, y: float, title: str, body: str, label: str) -> None:
    rect(s, 20, y, 350, 94, COLORS["surface"], rx=24, shadow=True)
    rect(s, 38, y + 18, 58, 58, COLORS["primary_soft"], rx=20)
    txt(s, label, 67, y + 38, COLORS["primary_dark"], size=10, weight=800, align="middle")
    txt(s, title, 114, y + 20, size=17, weight=700)
    txt(s, body, 114, y + 50, COLORS["muted"], size=12, width=210)
    txt(s, "›", 340, y + 33, COLORS["primary"], size=22, weight=800, align="middle")


def render_object_choice() -> Svg:
    s = Svg("03 Выбор объекта")
    header(s, "Выбор объекта", "Уточните масштаб будущего проекта", "search")
    txt(s, "Выберите вариант, который ближе к задаче клиента.", 24, 112, COLORS["muted"], size=15, width=330)
    object_card(s, 178, "Кухня", "мокрые зоны, хранение, вентиляция", "cool")
    object_card(s, 312, "Студия", "зонирование малого пространства", "warm")
    object_card(s, 446, "Вторичное жилье", "коммуникации и несущие стены", "warm")
    object_card(s, 580, "Сложная комната", "ниши, низкие потолки, старые трубы", "cool")
    bottom_nav(s, "home")
    return s


def object_card(s: Svg, y: float, title: str, body: str, mood: str) -> None:
    rect(s, 20, y, 350, 108, COLORS["surface"], rx=24, shadow=True)
    room_mock(s, 38, y + 18, 76, 72, mood)
    txt(s, title, 132, y + 24, size=18, weight=700)
    txt(s, body, 132, y + 56, COLORS["muted"], size=12, width=190)
    txt(s, "›", 340, y + 42, COLORS["primary"], size=22, weight=800, align="middle")


def render_room_design() -> Svg:
    s = Svg("04 Дизайн комнаты")
    header(s, "Дизайн комнаты", "Фильтры под специфику помещения", "object")
    section(s, "Тип комнаты", 104)
    chip_grid(s, ["Кухня", "Гостиная", "Спальня", "Детская", "Санузел", "Рабочая зона"], 140, 2)
    section(s, "Технические проблемы", 276)
    chip_grid(s, ["старые коммуникации", "узкая площадь", "низкий потолок", "много жильцов"], 312, 2, 2)
    section(s, "Рекомендуемые решения", 444)
    small_project(s, 480, "Кухня 8 м² с переносом хранения", "Сканди + инженерные ограничения")
    small_project(s, 602, "Детская для двоих", "Зонирование, хранение, тихая зона")
    button(s, "Показать 24 варианта", 20, 724, 350)
    return s


def render_housing_design() -> Svg:
    s = Svg("05 Дизайн жилья")
    header(s, "Дизайн жилья", "Подбор решения для квартиры или дома", "object")
    section(s, "Тип жилья", 104)
    chip_grid(s, ["Студия", "1-комн.", "2-комн.", "Дом", "Апартаменты", "Комната"], 140, 3)
    section(s, "Состояние", 254)
    chip_grid(s, ["новостройка", "вторичка", "старый фонд", "без ремонта"], 290, 2)
    section(s, "Фокус проекта", 404)
    wide_filter(s, 440, "Зонирование малой площади", "Для студий и семей с разным режимом дня")
    wide_filter(s, 536, "Много скрытого хранения", "Шкафы до потолка, антресоли, ниши")
    wide_filter(s, 632, "Бюджетная реализация", "Материалы и мебель из доступных линеек")
    button(s, "Сформировать подборку", 20, 738, 350)
    return s


def wide_filter(s: Svg, y: float, title: str, body: str) -> None:
    rect(s, 20, y, 350, 76, COLORS["surface"], rx=22, shadow=True)
    txt(s, title, 40, y + 16, size=16, weight=700, width=250)
    txt(s, body, 40, y + 44, COLORS["muted"], size=12, width=270)
    txt(s, "›", 340, y + 26, COLORS["primary"], size=22, weight=800, align="middle")


def render_catalog() -> Svg:
    s = Svg("06 Каталог идей")
    header(s, "Каталог идей", "Готовые кейсы для быстрого подбора", "home")
    small_filter(s, 20, "Стиль", "Japandi")
    small_filter(s, 142, "Класс", "Комфорт")
    small_filter(s, 264, "Критерии", "4")
    project_card(s, 172, "Студия 29 м² для пары", "Japandi, хранение, светлая палитра")
    project_card(s, 344, "Санузел в старом фонде", "коммуникации, влагостойкие материалы")
    project_card(s, 516, "Гостиная-кабинет", "зонирование без перегородок")
    bottom_nav(s, "catalog")
    return s


def small_filter(s: Svg, x: float, title: str, value: str) -> None:
    rect(s, x, 104, 106, 50, COLORS["surface"], rx=18, shadow=True)
    txt(s, title, x + 14, 112, COLORS["muted"], size=10)
    txt(s, value, x + 14, 128, size=13, weight=700)


def render_style_filter() -> Svg:
    s = Svg("07 Фильтр по стилям")
    header(s, "Фильтр по стилям", "Выберите визуальное направление", "catalog")
    section(s, "Популярные стили", 104)
    style_tile(s, 20, 142, "Сканди", COLORS["primary_soft"])
    style_tile(s, 204, 142, "Japandi", COLORS["accent_soft"])
    style_tile(s, 20, 310, "Минимализм", "#EDE9DF")
    style_tile(s, 204, 310, "Современный", "#E6DDD8")
    section(s, "Настроение", 500)
    chip_grid(s, ["теплый", "нейтральный", "контрастный", "натуральный"], 536, 2)
    button(s, "Применить стиль", 20, 722, 350)
    return s


def style_tile(s: Svg, x: float, y: float, title: str, fill: str) -> None:
    rect(s, x, y, 166, 144, COLORS["surface"], rx=26, shadow=True)
    rect(s, x + 14, y + 14, 138, 82, fill, rx=20)
    room_mock(s, x + 26, y + 28, 114, 52)
    txt(s, title, x + 16, y + 108, size=16, weight=700)


def render_class_filter() -> Svg:
    s = Svg("08 Фильтр по классу")
    header(s, "Фильтр по классу", "Уровень бюджета и материалов", "catalog")
    tariff(s, 124, "Базовый", "доступные материалы, простая мебель", "от 45 тыс. ₽")
    tariff(s, 276, "Комфорт", "кастомное хранение и долговечные покрытия", "от 90 тыс. ₽")
    tariff(s, 428, "Премиум", "сложная столярка, авторские детали", "от 180 тыс. ₽")
    button(s, "Показать проекты класса Комфорт", 20, 724, 350)
    return s


def tariff(s: Svg, y: float, title: str, body: str, price: str) -> None:
    rect(s, 20, y, 350, 124, COLORS["surface"], rx=26, shadow=True)
    txt(s, title, 42, y + 20, size=20, weight=800)
    txt(s, body, 42, y + 54, COLORS["muted"], size=13, width=225)
    rect(s, 250, y + 22, 96, 36, COLORS["primary_soft"], rx=16)
    txt(s, price, 298, y + 32, COLORS["primary_dark"], size=11, weight=700, align="middle")
    txt(s, "›", 334, y + 76, COLORS["primary"], size=22, weight=800, align="middle")


def render_criteria_filter() -> Svg:
    s = Svg("09 Фильтр по критериям")
    header(s, "Фильтр по критериям", "Технические и бытовые ограничения", "catalog")
    section(s, "Площадь", 104)
    chip_grid(s, ["до 12 м²", "12-25 м²", "25-45 м²", "45+ м²"], 140, 2)
    section(s, "Жильцы", 254)
    chip_grid(s, ["1 человек", "пара", "семья", "дети", "питомцы", "аренда"], 290, 3)
    section(s, "Особенности конструкций", 420)
    chip_grid(s, ["несущие стены", "старые трубы", "мало света", "низкий потолок"], 456, 2)
    button(s, "Найти подходящие кейсы", 20, 724, 350)
    return s


def render_project() -> Svg:
    s = Svg("10 Карточка проекта")
    header(s, "Карточка проекта", "Готовый кейс с техническими подсказками", "catalog")
    rect(s, 20, 94, 350, 220, COLORS["surface_soft"], rx=28)
    room_mock(s, 38, 116, 314, 170)
    txt(s, "Студия 29 м²: светлое зонирование", 20, 340, size=24, weight=800, width=320)
    txt(s, "Решение для пары: спальная ниша, рабочее место у окна и система хранения до потолка.",
        20, 412, COLORS["muted"], size=14, width=335)
    metrics(s, 490, [("29 м²", "площадь"), ("комфорт", "класс"), ("Japandi", "стиль")])
    section(s, "Почему подходит", 592)
    for i, item in enumerate(["зонирование без капитальных перегородок", "сценарии света для работы и отдыха",
                              "шкафы маскируют неровные стены"]):
        y = 628 + i * 34
        circle(s, 32, y + 9, 9, COLORS["accent_soft"])
        txt(s, "✓", 32, y + 4, COLORS["accent"], size=10, weight=800, align="middle")
        txt(s, item, 50, y, size=13, width=300)
    button(s, "Сохранить", 20, 724, 164)
    button(s, "Найти профи", 196, 724, 174, "secondary")
    return s


def render_favorites() -> Svg:
    s = Svg("11 Избранное")
    header(s, "Избранное", "Проекты и специалисты, которые понравились", "home")
    segmented(s, 100, ["Проекты", "Профи"], 0)
    project_card(s, 162, "Студия 29 м² для пары", "сохранено сегодня, 3 критерия совпали")
    master_card(s, 346, "Мария Климова", "дизайнер малых квартир")
    rect(s, 20, 520, 350, 126, COLORS["accent_soft"], rx=24)
    txt(s, "Совет", 40, 544, size=16, weight=700)
    txt(s, "Сохраняйте 3-5 решений, чтобы сравнить планировки, материалы и стоимость реализации.",
        40, 580, COLORS["muted"], size=14, width=286)
    bottom_nav(s, "favorites")
    return s


def segmented(s: Svg, y: float, labels: list[str], active: int) -> None:
    rect(s, 20, y, 350, 48, COLORS["surface_soft"], rx=18)
    cell = 350 / len(labels)
    for i, label in enumerate(labels):
        rect(s, 24 + i * cell, y + 4, cell - 8, 40, COLORS["surface"] if i == active else COLORS["surface_soft"], rx=15)
        txt(s, label, 20 + i * cell + cell / 2, y + 16, COLORS["text"] if i == active else COLORS["muted"],
            size=13, weight=700, align="middle")


def render_specialists() -> Svg:
    s = Svg("12 Специалисты")
    header(s, "Специалисты", "Проверенные дизайнеры и инженеры", "home")
    button(s, "Поиск по проблеме", 20, 104, 350, "secondary")
    pro_category(s, 184, "Инженеры", "перепланировки, коммуникации, конструктив", "12 профилей", "ИН")
    pro_category(s, 324, "Дизайнеры", "малые площади, стиль, подбор мебели", "28 профилей", "ДЗ")
    section(s, "Рекомендуемые", 492)
    master_card(s, 528, "Мария Климова", "малые квартиры и студии")
    master_card(s, 650, "Антон Ветров", "инженер по перепланировкам")
    bottom_nav(s, "specialists")
    return s


def pro_category(s: Svg, y: float, title: str, body: str, count: str, icon: str) -> None:
    rect(s, 20, y, 350, 112, COLORS["surface"], rx=26, shadow=True)
    rect(s, 38, y + 18, 62, 62, COLORS["accent_soft"] if icon == "ИН" else COLORS["primary_soft"], rx=22)
    txt(s, icon, 69, y + 40, COLORS["accent"] if icon == "ИН" else COLORS["primary_dark"], size=12, weight=800,
        align="middle")
    txt(s, title, 120, y + 18, size=19, weight=800)
    txt(s, body, 120, y + 50, COLORS["muted"], size=12, width=190)
    txt(s, count, 120, y + 82, COLORS["primary"], size=11, weight=700)
    txt(s, "›", 340, y + 43, COLORS["primary"], size=22, weight=800, align="middle")


def render_problem_search() -> Svg:
    s = Svg("13 Поиск по проблеме")
    header(s, "Поиск по проблеме", "Специалист под конкретный риск", "specialists")
    section(s, "Что нужно решить?", 104)
    wide_filter(s, 140, "Старые коммуникации", "нужен инженер и дизайнер санузла")
    wide_filter(s, 236, "Несущие стены", "проверить возможность перепланировки")
    wide_filter(s, 332, "Мало места для жильцов", "планировка и хранение")
    section(s, "Подходящие профили", 468)
    master_card(s, 504, "Антон Ветров", "конструктив и согласования")
    master_card(s, 626, "Мария Климова", "зонирование малых площадей")
    return s


def render_engineers() -> Svg:
    s = Svg("14 Инженеры")
    header(s, "Инженеры", "Проверенные эксперты по конструктиву", "specialists")
    chip_grid(s, ["перепланировка", "коммуникации", "старый фонд", "согласование"], 104, 2)
    master_card(s, 244, "Антон Ветров", "12 лет, согласования и несущие стены")
    master_card(s, 366, "Ирина Соколова", "водоснабжение и вентиляция")
    master_card(s, 488, "Павел Громов", "обследование старого фонда")
    button(s, "Заполнить задачу для инженера", 20, 724, 350)
    return s


def render_designers() -> Svg:
    s = Svg("15 Дизайнеры")
    header(s, "Дизайнеры", "Специализация на сложных квартирах", "specialists")
    chip_grid(s, ["малые площади", "семьи", "Japandi", "бюджет"], 104, 2)
    master_card(s, 244, "Мария Климова", "студии и квартиры до 45 м²")
    master_card(s, 366, "Олег Нестеров", "современный стиль и хранение")
    master_card(s, 488, "Вера Лисина", "детские и многофункциональные комнаты")
    button(s, "Подобрать дизайнера", 20, 724, 350)
    return s


def render_master_profile() -> Svg:
    s = Svg("16 Профиль мастера")
    header(s, "Профиль мастера", "Проверенный специалист", "specialists")
    rect(s, 20, 104, 350, 188, COLORS["surface"], rx=28, shadow=True)
    circle(s, 81, 171, 39, COLORS["primary_soft"])
    txt(s, "МК", 81, 158, COLORS["primary_dark"], size=15, weight=800, align="middle")
    txt(s, "Мария Климова", 138, 132, size=22, weight=800)
    txt(s, "Дизайнер интерьера", 138, 168, COLORS["muted"], size=14)
    chip(s, "малые площади", 138, 206, 124, True)
    chip(s, "студии", 270, 206, 74)
    metrics(s, 318, [("4.9", "рейтинг"), ("84", "проекта"), ("6 лет", "опыт")])
    section(s, "Кейсы специалиста", 426)
    small_project(s, 462, "Студия с рабочим местом", "29 м², Japandi")
    small_project(s, 584, "Кухня в старом фонде", "8 м², коммуникации")
    button(s, "Оставить заявку", 20, 724, 166)
    button(s, "В избранное", 198, 724, 172, "secondary")
    return s


def render_request() -> Svg:
    s = Svg("17 Заявка специалисту")
    header(s, "Заявка", "Короткое ТЗ для специалиста", "profile")
    input_box(s, 112, "Объект", "Студия 29 м², вторичное жилье")
    input_box(s, 204, "Проблема", "Нужно зонирование и хранение")
    input_box(s, 296, "Бюджет", "Комфорт, до 120 тыс. ₽ на реализацию")
    input_box(s, 388, "Комментарий", "Старые коммуникации на кухне, мало естественного света")
    rect(s, 20, 530, 350, 96, COLORS["accent_soft"], rx=24)
    txt(s, "После отправки специалист получит сохраненные проекты и критерии подбора.",
        40, 558, COLORS["text"], size=14, width=290)
    button(s, "Отправить заявку", 20, 724, 350)
    return s


RENDERERS = [
    ("00_overview", render_cover),
    ("01_home", render_home),
    ("02_design_search", render_design_search),
    ("03_object_choice", render_object_choice),
    ("04_room_design", render_room_design),
    ("05_housing_design", render_housing_design),
    ("06_idea_catalog", render_catalog),
    ("07_style_filter", render_style_filter),
    ("08_class_filter", render_class_filter),
    ("09_criteria_filter", render_criteria_filter),
    ("10_project_card", render_project),
    ("11_favorites", render_favorites),
    ("12_specialists", render_specialists),
    ("13_problem_search", render_problem_search),
    ("14_engineers", render_engineers),
    ("15_designers", render_designers),
    ("16_master_profile", render_master_profile),
    ("17_specialist_request", render_request),
]


def build_board(rendered: list[tuple[str, str]]) -> str:
    gap_x = 72
    gap_y = 96
    cols = 4
    board_w = cols * W + (cols - 1) * gap_x + 80
    rows = (len(rendered) + cols - 1) // cols
    board_h = rows * H + (rows - 1) * gap_y + 96
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{board_w}" height="{board_h}" viewBox="0 0 {board_w} {board_h}" fill="none">',
        '  <rect width="100%" height="100%" fill="#1F1F1F"/>',
        '  <style>text { font-family: Inter, Arial, sans-serif; dominant-baseline: hanging; }</style>',
    ]
    for i, (name, svg) in enumerate(rendered):
        col = i % cols
        row = i // cols
        x = 40 + col * (W + gap_x)
        y = 56 + row * (H + gap_y)
        title = name.replace("_", " ")
        parts.append(f'  <text x="{x}" y="{y - 28}" fill="#9A9A9A" font-size="16" font-weight="700">{escape(title)}</text>')
        inner = svg.split(">", 1)[1].rsplit("</svg>", 1)[0]
        parts.append(f'  <g transform="translate({x},{y})">{inner}</g>')
    parts.append("</svg>\n")
    return "\n".join(parts)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    rendered: list[tuple[str, str]] = []
    for name, renderer in RENDERERS:
        svg = renderer().render()
        (OUT / f"{name}.svg").write_text(svg, encoding="utf-8")
        rendered.append((name, svg))
    (OUT / "_all_screens_board.svg").write_text(build_board(rendered), encoding="utf-8")


if __name__ == "__main__":
    main()
