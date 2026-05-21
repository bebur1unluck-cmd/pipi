# SVG-макеты для импорта в Figma

Этот каталог содержит готовые SVG-экраны мобильного приложения **SenseRoom** по теме:

> «Разработка мобильного приложения дизайна интерьеров для начинающих дизайнеров».

## Как использовать в Figma

### Вариант 1: импорт всех экранов сразу

1. Откройте Figma Design file.
2. Перетащите файл `_all_screens_board.svg` на canvas.
3. Разгруппируйте импортированный SVG при необходимости.
4. Если Figma сохранила SVG-ссылки как link-области, проверьте их в Present/Preview.
5. Если Figma импортировала их только как вектор, используйте невидимые hotspot-прямоугольники как основу для Prototype-связей.

### Вариант 2: импорт по одному экрану

1. Создайте в Figma фреймы iPhone/Android размером **390x844**.
2. Перетащите SVG-файл нужного экрана внутрь соответствующего фрейма.
3. Повторите для всех экранов.
4. Проверьте импортированные hotspot-зоны поверх кнопок и карточек.
5. При необходимости во вкладке **Prototype** назначьте им `On click -> Navigate to` по карте ниже.

## Кликабельность в SVG

В каждый SVG добавлены реальные ссылки `<a href="...svg">` поверх кнопок, карточек, фильтров, стрелок назад и нижней навигации.  
Проверить их можно напрямую: откройте `00_overview.svg` или любой другой экран в браузере и нажимайте на кнопки.

Ограничение Figma: SVG-ссылки и Figma Prototype-связи — разные механики. Если Figma не превращает `<a href>` в native Prototype-переходы автоматически, выделите импортированные hotspot-прямоугольники и назначьте им переходы вручную по карте ниже.

## Список файлов

- `00_overview.svg` — обзор прототипа.
- `01_home.svg` — домашняя страница.
- `02_design_search.svg` — поиск дизайна.
- `03_object_choice.svg` — выбор объекта.
- `04_room_design.svg` — дизайн комнаты.
- `05_housing_design.svg` — дизайн жилья.
- `06_idea_catalog.svg` — каталог идей.
- `07_style_filter.svg` — фильтр по стилям.
- `08_class_filter.svg` — фильтр по классу.
- `09_criteria_filter.svg` — фильтр по критериям.
- `10_project_card.svg` — карточка проекта.
- `11_favorites.svg` — избранное.
- `12_specialists.svg` — специалисты.
- `13_problem_search.svg` — поиск по проблеме.
- `14_engineers.svg` — инженеры.
- `15_designers.svg` — дизайнеры.
- `16_master_profile.svg` — профиль мастера.
- `17_specialist_request.svg` — заявка специалисту.
- `_all_screens_board.svg` — все экраны на одном полотне.

## Карта переходов для Figma Prototype

### Нижняя навигация

- `Дом` -> `01_home`.
- `Каталог` -> `06_idea_catalog`.
- `Избранное` -> `11_favorites`.
- `Профи` -> `12_specialists`.

### Основной сценарий подбора дизайна

- `00_overview` / кнопка `Открыть прототип` -> `01_home`.
- `01_home` / `Подобрать дизайн` -> `02_design_search`.
- `01_home` / карточка `Поиск дизайна` -> `02_design_search`.
- `02_design_search` / `Отдельную комнату` -> `04_room_design`.
- `02_design_search` / `Жилье целиком` -> `05_housing_design`.
- `02_design_search` / `Пройти короткий выбор объекта` -> `03_object_choice`.
- `03_object_choice` / `Кухня` или `Сложная комната` -> `04_room_design`.
- `03_object_choice` / `Студия` или `Вторичное жилье` -> `05_housing_design`.
- `04_room_design` / карточки решений или `Показать 24 варианта` -> `10_project_card` или `06_idea_catalog`.
- `05_housing_design` / `Сформировать подборку` -> `06_idea_catalog`.

### Каталог и фильтры

- `01_home` / карточка `Каталог идей` -> `06_idea_catalog`.
- `06_idea_catalog` / `Стиль` -> `07_style_filter`.
- `06_idea_catalog` / `Класс` -> `08_class_filter`.
- `06_idea_catalog` / `Критерии` -> `09_criteria_filter`.
- `07_style_filter` / `Применить стиль` -> `06_idea_catalog`.
- `08_class_filter` / `Показать проекты класса Комфорт` -> `06_idea_catalog`.
- `09_criteria_filter` / `Найти подходящие кейсы` -> `10_project_card`.
- `06_idea_catalog` / любая карточка проекта -> `10_project_card`.
- `10_project_card` / `Сохранить` -> `11_favorites`.

### Специалисты

- `01_home` / карточка `Специалисты` -> `12_specialists`.
- `10_project_card` / `Найти профи` -> `12_specialists`.
- `12_specialists` / `Поиск по проблеме` -> `13_problem_search`.
- `12_specialists` / `Инженеры` -> `14_engineers`.
- `12_specialists` / `Дизайнеры` -> `15_designers`.
- `13_problem_search` / `Старые коммуникации` или `Несущие стены` -> `14_engineers`.
- `13_problem_search` / `Мало места для жильцов` -> `15_designers`.
- `14_engineers` или `15_designers` / карточка специалиста -> `16_master_profile`.
- `16_master_profile` / `Оставить заявку` -> `17_specialist_request`.
- `16_master_profile` / `В избранное` -> `11_favorites`.
- `17_specialist_request` / `Отправить заявку` -> `11_favorites`.

## Рекомендация по кликабельным зонам

После импорта SVG в Figma удобно создавать прозрачные прямоугольники поверх кнопок и карточек:

1. Нарисуйте Rectangle поверх кнопки/карточки.
2. Установите Fill opacity `0%`.
3. Во вкладке Prototype задайте `On click -> Navigate to`.
4. Назовите слой, например `hotspot_to_catalog`.
