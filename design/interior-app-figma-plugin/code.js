const MOBILE_W = 390;
const MOBILE_H = 844;
const GAP_X = 72;
const GAP_Y = 96;

const COLORS = {
  bg: "#F8F1EC",
  surface: "#FFFDFC",
  surfaceSoft: "#F3E5DD",
  text: "#2F2824",
  muted: "#8A756C",
  line: "#E4D1C8",
  primary: "#A96F58",
  primaryDark: "#744637",
  primarySoft: "#EBD4CB",
  accent: "#4D7C72",
  accentSoft: "#DCEBE7",
  warning: "#C78345",
  white: "#FFFFFF"
};

const FONTS = {
  regular: { family: "Inter", style: "Regular" },
  medium: { family: "Inter", style: "Medium" },
  semi: { family: "Inter", style: "Semi Bold" },
  bold: { family: "Inter", style: "Bold" }
};

const SCREEN_DEFS = [
  ["cover", "00 Обзор прототипа"],
  ["home", "01 Домашняя страница"],
  ["designSearch", "02 Поиск дизайна"],
  ["objectChoice", "03 Выбор объекта"],
  ["roomDesign", "04 Дизайн комнаты"],
  ["housingDesign", "05 Дизайн жилья"],
  ["catalog", "06 Каталог идей"],
  ["styleFilter", "07 Фильтр по стилям"],
  ["classFilter", "08 Фильтр по классу"],
  ["criteriaFilter", "09 Фильтр по критериям"],
  ["project", "10 Карточка проекта"],
  ["favorites", "11 Избранное"],
  ["specialists", "12 Специалисты"],
  ["problemSearch", "13 Поиск по проблеме"],
  ["engineers", "14 Инженеры"],
  ["designers", "15 Дизайнеры"],
  ["masterProfile", "16 Профиль мастера"],
  ["request", "17 Заявка специалисту"]
];

const ui = `
<style>
  body {
    margin: 0;
    font-family: Inter, Arial, sans-serif;
    color: #2F2824;
    background: #F8F1EC;
  }
  main { padding: 24px; }
  h1 { margin: 0 0 8px; font-size: 22px; line-height: 1.2; }
  p { margin: 0 0 16px; color: #6E5A51; line-height: 1.45; }
  ul { padding-left: 18px; color: #6E5A51; line-height: 1.45; }
  button {
    width: 100%;
    border: 0;
    border-radius: 16px;
    padding: 14px 18px;
    margin-top: 16px;
    background: #A96F58;
    color: white;
    font-weight: 700;
    cursor: pointer;
  }
  .secondary {
    background: transparent;
    color: #744637;
    border: 1px solid #D9BCAF;
  }
</style>
<main>
  <h1>Interior Design App</h1>
  <p>Генератор создаст полноценный hi-fi прототип мобильного приложения для начинающих дизайнеров интерьера.</p>
  <ul>
    <li>18 экранов iPhone 390x844;</li>
    <li>каталог, подбор по критериям, специалисты и избранное;</li>
    <li>prototype links на кнопках, карточках и нижней навигации.</li>
  </ul>
  <button id="generate">Создать прототип в Figma</button>
  <button class="secondary" id="close">Закрыть</button>
</main>
<script>
  document.getElementById('generate').onclick = () => {
    parent.postMessage({ pluginMessage: { type: 'generate' } }, '*');
  };
  document.getElementById('close').onclick = () => {
    parent.postMessage({ pluginMessage: { type: 'close' } }, '*');
  };
</script>
`;

figma.showUI(ui, { width: 360, height: 470 });

figma.ui.onmessage = async (msg) => {
  if (msg.type === "close") {
    figma.closePlugin();
    return;
  }

  if (msg.type === "generate") {
    await loadFonts();
    createPrototype();
    figma.closePlugin("Готово: прототип создан и экраны связаны.");
  }
};

async function loadFonts() {
  const uniqueFonts = [FONTS.regular, FONTS.medium, FONTS.semi, FONTS.bold];
  await Promise.all(uniqueFonts.map((font) => figma.loadFontAsync(font)));
}

function createPrototype() {
  const page = figma.createPage();
  page.name = "Interior Design App - Figma prototype";
  figma.currentPage = page;

  const screens = {};
  SCREEN_DEFS.forEach(([key, name], index) => {
    const col = index % 4;
    const row = Math.floor(index / 4);
    screens[key] = createMobileFrame(name, col * (MOBILE_W + GAP_X), row * (MOBILE_H + GAP_Y));
  });

  renderCover(screens.cover, screens);
  renderHome(screens.home, screens);
  renderDesignSearch(screens.designSearch, screens);
  renderObjectChoice(screens.objectChoice, screens);
  renderRoomDesign(screens.roomDesign, screens);
  renderHousingDesign(screens.housingDesign, screens);
  renderCatalog(screens.catalog, screens);
  renderStyleFilter(screens.styleFilter, screens);
  renderClassFilter(screens.classFilter, screens);
  renderCriteriaFilter(screens.criteriaFilter, screens);
  renderProject(screens.project, screens);
  renderFavorites(screens.favorites, screens);
  renderSpecialists(screens.specialists, screens);
  renderProblemSearch(screens.problemSearch, screens);
  renderEngineers(screens.engineers, screens);
  renderDesigners(screens.designers, screens);
  renderMasterProfile(screens.masterProfile, screens);
  renderRequest(screens.request, screens);

  addFlowConnectors(screens.cover, screens);

  page.selection = [screens.home];
  figma.viewport.scrollAndZoomIntoView(Object.values(screens));
}

function createMobileFrame(name, x, y) {
  const frame = figma.createFrame();
  frame.name = name;
  frame.resize(MOBILE_W, MOBILE_H);
  frame.x = x;
  frame.y = y;
  frame.clipsContent = true;
  frame.cornerRadius = 28;
  frame.fills = [paint(COLORS.bg)];
  frame.effects = [shadow(0, 16, 36, 0.12)];
  return frame;
}

function renderCover(parent, screens) {
  fill(parent, COLORS.surface);
  text(parent, "Дизайн-проект приложения", 28, 48, 300, {
    size: 24,
    weight: "bold",
    color: COLORS.text,
    height: 64
  });
  text(parent, "Для начинающих дизайнеров интерьера", 28, 112, 300, {
    size: 15,
    color: COLORS.muted,
    height: 42
  });
  rounded(parent, 28, 176, 334, 190, 28, COLORS.surfaceSoft);
  roomMock(parent, 50, 198, 290, 146, "living");
  text(parent, "Основные пользовательские сценарии", 28, 402, 320, {
    size: 17,
    weight: "semi",
    height: 26
  });
  checklist(parent, 28, 444, [
    "Подбор дизайна по типу жилья, стилю и состоянию",
    "Каталог готовых кейсов с фильтрами",
    "Проверенные дизайнеры и инженеры",
    "Сохранение понравившихся решений в избранное"
  ]);
  const start = button(parent, "Открыть прототип", 28, 716, 334, 54, "primary");
  link(start, screens.home);
}

function renderHome(parent, screens) {
  status(parent);
  header(parent, "SenseRoom", "Подбор интерьеров для сложных задач", screens.favorites);
  rounded(parent, 20, 112, 350, 156, 28, COLORS.primarySoft);
  text(parent, "Начните с задачи", 40, 136, 180, { size: 24, weight: "bold", height: 64 });
  text(parent, "Выберите комнату, стиль и технические ограничения, а мы покажем подходящие решения.", 40, 202, 234, {
    size: 13,
    color: COLORS.primaryDark,
    height: 48
  });
  roomMock(parent, 236, 132, 110, 112, "small");
  const hero = button(parent, "Подобрать дизайн", 40, 284, 176, 44, "primary");
  link(hero, screens.designSearch);

  sectionTitle(parent, "Быстрый доступ", 20, 354);
  const designCard = featureCard(parent, 20, 390, 166, 130, "Поиск дизайна", "По объекту, стилю и состоянию", "01");
  const catalogCard = featureCard(parent, 204, 390, 166, 130, "Каталог идей", "Готовые кейсы и решения", "02");
  const specCard = featureCard(parent, 20, 538, 166, 130, "Специалисты", "Дизайнеры и инженеры", "03");
  const favCard = featureCard(parent, 204, 538, 166, 130, "Избранное", "Сохраненные проекты", "04");
  link(designCard, screens.designSearch);
  link(catalogCard, screens.catalog);
  link(specCard, screens.specialists);
  link(favCard, screens.favorites);

  addBottomNav(parent, "home", screens);
}

function renderDesignSearch(parent, screens) {
  status(parent);
  header(parent, "Поиск дизайна", "Алгоритм подбора для начинающих дизайнеров", screens.home, true);
  rounded(parent, 20, 108, 350, 96, 24, COLORS.accentSoft);
  text(parent, "Опишите объект", 40, 128, 210, { size: 21, weight: "bold", height: 32 });
  text(parent, "Чем точнее критерии, тем полезнее подборка.", 40, 164, 260, {
    size: 13,
    color: COLORS.muted,
    height: 32
  });
  sectionTitle(parent, "Что проектируем?", 20, 234);
  const room = largeChoice(parent, 20, 270, "Отдельную комнату", "Кухня, спальня, детская, санузел", "Комната");
  const flat = largeChoice(parent, 20, 388, "Жилье целиком", "Студия, квартира, дом, апартаменты", "Жилье");
  link(room, screens.roomDesign);
  link(flat, screens.housingDesign);
  sectionTitle(parent, "Нужна помощь с выбором?", 20, 536);
  const choose = button(parent, "Пройти короткий выбор объекта", 20, 572, 350, 52, "secondary");
  link(choose, screens.objectChoice);
  const catalog = button(parent, "Смотреть каталог идей", 20, 640, 350, 52, "ghost");
  link(catalog, screens.catalog);
  addBottomNav(parent, "home", screens);
}

function renderObjectChoice(parent, screens) {
  status(parent);
  header(parent, "Выбор объекта", "Уточните масштаб будущего проекта", screens.designSearch, true);
  text(parent, "Выберите вариант, который ближе к задаче клиента.", 24, 112, 330, {
    size: 15,
    color: COLORS.muted,
    height: 44
  });
  const kitchen = objectCard(parent, 20, 178, "Кухня", "мокрые зоны, хранение, вентиляция", "room");
  const studio = objectCard(parent, 20, 312, "Студия", "зонирование малого пространства", "flat");
  const oldFlat = objectCard(parent, 20, 446, "Вторичное жилье", "коммуникации и несущие стены", "flat");
  const custom = objectCard(parent, 20, 580, "Сложная комната", "ниши, низкие потолки, старые трубы", "room");
  link(kitchen, screens.roomDesign);
  link(custom, screens.roomDesign);
  link(studio, screens.housingDesign);
  link(oldFlat, screens.housingDesign);
  addBottomNav(parent, "home", screens);
}

function renderRoomDesign(parent, screens) {
  status(parent);
  header(parent, "Дизайн комнаты", "Фильтры под специфику помещения", screens.objectChoice, true);
  sectionTitle(parent, "Тип комнаты", 20, 104);
  chipGrid(parent, 20, 140, ["Кухня", "Гостиная", "Спальня", "Детская", "Санузел", "Рабочая зона"], 2);
  sectionTitle(parent, "Технические проблемы", 20, 276);
  const oldPipes = chip(parent, "старые коммуникации", 20, 312, 164, true);
  const narrow = chip(parent, "узкая площадь", 196, 312, 144, false);
  const low = chip(parent, "низкий потолок", 20, 364, 144, false);
  const many = chip(parent, "много жильцов", 176, 364, 148, true);
  link(oldPipes, screens.project);
  link(narrow, screens.criteriaFilter);
  link(low, screens.criteriaFilter);
  link(many, screens.criteriaFilter);
  sectionTitle(parent, "Рекомендуемые решения", 20, 444);
  projectListCard(parent, 20, 480, "Кухня 8 м2 с переносом хранения", "Сканди + инженерные ограничения", screens.project);
  projectListCard(parent, 20, 602, "Детская для двоих", "Зонирование, хранение, тихая зона", screens.project);
  const show = button(parent, "Показать 24 варианта", 20, 724, 350, 52, "primary");
  link(show, screens.catalog);
}

function renderHousingDesign(parent, screens) {
  status(parent);
  header(parent, "Дизайн жилья", "Подбор решения для квартиры или дома", screens.objectChoice, true);
  sectionTitle(parent, "Тип жилья", 20, 104);
  chipGrid(parent, 20, 140, ["Студия", "1-комн.", "2-комн.", "Дом", "Апартаменты", "Комната"], 3);
  sectionTitle(parent, "Состояние", 20, 254);
  chipGrid(parent, 20, 290, ["новостройка", "вторичка", "старый фонд", "без ремонта"], 2);
  sectionTitle(parent, "Фокус проекта", 20, 404);
  const zoning = wideFilter(parent, 20, 440, "Зонирование малой площади", "Для студий и семей с разным режимом дня");
  const storage = wideFilter(parent, 20, 536, "Много скрытого хранения", "Шкафы до потолка, антресоли, ниши");
  const budget = wideFilter(parent, 20, 632, "Бюджетная реализация", "Материалы и мебель из доступных линеек");
  link(zoning, screens.project);
  link(storage, screens.project);
  link(budget, screens.catalog);
  const show = button(parent, "Сформировать подборку", 20, 738, 350, 52, "primary");
  link(show, screens.catalog);
}

function renderCatalog(parent, screens) {
  status(parent);
  header(parent, "Каталог идей", "Готовые кейсы для быстрого подбора", screens.home, true);
  const style = smallFilter(parent, 20, 104, "Стиль", "Japandi");
  const klass = smallFilter(parent, 142, 104, "Класс", "Комфорт");
  const criteria = smallFilter(parent, 264, 104, "Критерии", "4");
  link(style, screens.styleFilter);
  link(klass, screens.classFilter);
  link(criteria, screens.criteriaFilter);
  projectFeedCard(parent, 20, 172, "Студия 29 м2 для пары", "Japandi, хранение, светлая палитра", screens.project);
  projectFeedCard(parent, 20, 344, "Санузел в старом фонде", "коммуникации, влагостойкие материалы", screens.project);
  projectFeedCard(parent, 20, 516, "Гостиная-кабинет", "зонирование без перегородок", screens.project);
  addBottomNav(parent, "catalog", screens);
}

function renderStyleFilter(parent, screens) {
  status(parent);
  header(parent, "Фильтр по стилям", "Выберите визуальное направление", screens.catalog, true);
  sectionTitle(parent, "Популярные стили", 20, 104);
  styleTile(parent, 20, 142, "Сканди", COLORS.primarySoft, screens.catalog);
  styleTile(parent, 204, 142, "Japandi", COLORS.accentSoft, screens.catalog);
  styleTile(parent, 20, 310, "Минимализм", "#EDE9DF", screens.catalog);
  styleTile(parent, 204, 310, "Современный", "#E6DDD8", screens.catalog);
  sectionTitle(parent, "Настроение", 20, 500);
  chipGrid(parent, 20, 536, ["теплый", "нейтральный", "контрастный", "натуральный"], 2);
  const apply = button(parent, "Применить стиль", 20, 722, 350, 52, "primary");
  link(apply, screens.catalog);
}

function renderClassFilter(parent, screens) {
  status(parent);
  header(parent, "Фильтр по классу", "Подберите уровень бюджета и материалов", screens.catalog, true);
  const eco = tariff(parent, 20, 124, "Базовый", "доступные материалы, простая мебель", "от 45 тыс. ₽");
  const comfort = tariff(parent, 20, 276, "Комфорт", "кастомное хранение и долговечные покрытия", "от 90 тыс. ₽");
  const premium = tariff(parent, 20, 428, "Премиум", "сложная столярка, авторские детали", "от 180 тыс. ₽");
  link(eco, screens.catalog);
  link(comfort, screens.catalog);
  link(premium, screens.catalog);
  const apply = button(parent, "Показать проекты класса Комфорт", 20, 724, 350, 52, "primary");
  link(apply, screens.catalog);
}

function renderCriteriaFilter(parent, screens) {
  status(parent);
  header(parent, "Фильтр по критериям", "Технические и бытовые ограничения", screens.catalog, true);
  sectionTitle(parent, "Площадь", 20, 104);
  chipGrid(parent, 20, 140, ["до 12 м2", "12-25 м2", "25-45 м2", "45+ м2"], 2);
  sectionTitle(parent, "Жильцы", 20, 254);
  chipGrid(parent, 20, 290, ["1 человек", "пара", "семья", "дети", "питомцы", "аренда"], 3);
  sectionTitle(parent, "Особенности конструкций", 20, 420);
  chipGrid(parent, 20, 456, ["несущие стены", "старые трубы", "мало света", "низкий потолок"], 2);
  const apply = button(parent, "Найти подходящие кейсы", 20, 724, 350, 52, "primary");
  link(apply, screens.project);
}

function renderProject(parent, screens) {
  status(parent);
  header(parent, "Карточка проекта", "Готовый кейс с техническими подсказками", screens.catalog, true);
  rounded(parent, 20, 94, 350, 220, 28, COLORS.surfaceSoft);
  roomMock(parent, 38, 116, 314, 170, "living");
  text(parent, "Студия 29 м2: светлое зонирование", 20, 340, 320, {
    size: 24,
    weight: "bold",
    height: 64
  });
  text(parent, "Решение для пары: спальная ниша, рабочее место у окна и система хранения до потолка.", 20, 412, 336, {
    size: 14,
    color: COLORS.muted,
    height: 54
  });
  metricRow(parent, 20, 490, [
    ["29 м2", "площадь"],
    ["комфорт", "класс"],
    ["Japandi", "стиль"]
  ]);
  sectionTitle(parent, "Почему подходит", 20, 592);
  checklist(parent, 20, 628, [
    "зонирование без капитальных перегородок",
    "сценарии света для работы и отдыха",
    "шкафы маскируют неровные стены"
  ]);
  const save = button(parent, "Сохранить в избранное", 20, 724, 164, 52, "primary");
  const expert = button(parent, "Найти профи", 196, 724, 174, 52, "secondary");
  link(save, screens.favorites);
  link(expert, screens.specialists);
}

function renderFavorites(parent, screens) {
  status(parent);
  header(parent, "Избранное", "Проекты и специалисты, которые понравились", screens.home, true);
  const tabs = segmented(parent, 20, 100, ["Проекты", "Профи"], 0);
  link(tabs[1], screens.specialists);
  projectFeedCard(parent, 20, 162, "Студия 29 м2 для пары", "сохранено сегодня, 3 критерия совпали", screens.project);
  savedMaster(parent, 20, 346, "Мария Климова", "дизайнер малых квартир", screens.masterProfile);
  rounded(parent, 20, 520, 350, 126, 24, COLORS.accentSoft);
  text(parent, "Совет", 40, 544, 280, { size: 16, weight: "semi", height: 24 });
  text(parent, "Сохраняйте 3-5 решений, чтобы сравнить планировки, материалы и стоимость реализации.", 40, 580, 286, {
    size: 14,
    color: COLORS.muted,
    height: 44
  });
  addBottomNav(parent, "favorites", screens);
}

function renderSpecialists(parent, screens) {
  status(parent);
  header(parent, "Специалисты", "Проверенные дизайнеры и инженеры", screens.home, true);
  const search = button(parent, "Поиск по проблеме", 20, 104, 350, 52, "secondary");
  link(search, screens.problemSearch);
  const engineers = proCategory(parent, 20, 184, "Инженеры", "перепланировки, коммуникации, конструктив", "12 профилей");
  const designers = proCategory(parent, 20, 324, "Дизайнеры", "малые площади, стиль, подбор мебели", "28 профилей");
  link(engineers, screens.engineers);
  link(designers, screens.designers);
  sectionTitle(parent, "Рекомендуемые", 20, 492);
  savedMaster(parent, 20, 528, "Мария Климова", "малые квартиры и студии", screens.masterProfile);
  savedMaster(parent, 20, 650, "Антон Ветров", "инженер по перепланировкам", screens.masterProfile);
  addBottomNav(parent, "specialists", screens);
}

function renderProblemSearch(parent, screens) {
  status(parent);
  header(parent, "Поиск по проблеме", "Найдите специалиста под конкретный риск", screens.specialists, true);
  sectionTitle(parent, "Что нужно решить?", 20, 104);
  const pipes = wideFilter(parent, 20, 140, "Старые коммуникации", "нужен инженер и дизайнер санузла");
  const wall = wideFilter(parent, 20, 236, "Несущие стены", "проверить возможность перепланировки");
  const small = wideFilter(parent, 20, 332, "Мало места для жильцов", "планировка и хранение");
  link(pipes, screens.engineers);
  link(wall, screens.engineers);
  link(small, screens.designers);
  sectionTitle(parent, "Подходящие профили", 20, 468);
  savedMaster(parent, 20, 504, "Антон Ветров", "конструктив и согласования", screens.masterProfile);
  savedMaster(parent, 20, 626, "Мария Климова", "зонирование малых площадей", screens.masterProfile);
}

function renderEngineers(parent, screens) {
  status(parent);
  header(parent, "Инженеры", "Проверенные эксперты по конструктиву", screens.specialists, true);
  chipGrid(parent, 20, 104, ["перепланировка", "коммуникации", "старый фонд", "согласование"], 2);
  savedMaster(parent, 20, 244, "Антон Ветров", "12 лет, согласования и несущие стены", screens.masterProfile);
  savedMaster(parent, 20, 366, "Ирина Соколова", "водоснабжение и вентиляция", screens.masterProfile);
  savedMaster(parent, 20, 488, "Павел Громов", "обследование старого фонда", screens.masterProfile);
  const help = button(parent, "Заполнить задачу для инженера", 20, 724, 350, 52, "primary");
  link(help, screens.request);
}

function renderDesigners(parent, screens) {
  status(parent);
  header(parent, "Дизайнеры", "Специализация на сложных квартирах", screens.specialists, true);
  chipGrid(parent, 20, 104, ["малые площади", "семьи", "Japandi", "бюджет"], 2);
  savedMaster(parent, 20, 244, "Мария Климова", "студии и квартиры до 45 м2", screens.masterProfile);
  savedMaster(parent, 20, 366, "Олег Нестеров", "современный стиль и хранение", screens.masterProfile);
  savedMaster(parent, 20, 488, "Вера Лисина", "детские и многофункциональные комнаты", screens.masterProfile);
  const help = button(parent, "Подобрать дизайнера", 20, 724, 350, 52, "primary");
  link(help, screens.request);
}

function renderMasterProfile(parent, screens) {
  status(parent);
  header(parent, "Профиль мастера", "Проверенный специалист", screens.specialists, true);
  rounded(parent, 20, 104, 350, 188, 28, COLORS.surface);
  avatar(parent, 42, 132, 78, "МК");
  text(parent, "Мария Климова", 138, 132, 200, { size: 22, weight: "bold", height: 34 });
  text(parent, "Дизайнер интерьера", 138, 168, 190, { size: 14, color: COLORS.muted, height: 22 });
  chip(parent, "малые площади", 138, 206, 124, true);
  chip(parent, "студии", 270, 206, 74, false);
  metricRow(parent, 32, 318, [
    ["4.9", "рейтинг"],
    ["84", "проекта"],
    ["6 лет", "опыт"]
  ]);
  sectionTitle(parent, "Кейсы специалиста", 20, 426);
  projectListCard(parent, 20, 462, "Студия с рабочим местом", "29 м2, Japandi", screens.project);
  projectListCard(parent, 20, 584, "Кухня в старом фонде", "8 м2, коммуникации", screens.project);
  const contact = button(parent, "Оставить заявку", 20, 724, 166, 52, "primary");
  const save = button(parent, "В избранное", 198, 724, 172, 52, "secondary");
  link(contact, screens.request);
  link(save, screens.favorites);
}

function renderRequest(parent, screens) {
  status(parent);
  header(parent, "Заявка", "Короткое ТЗ для специалиста", screens.masterProfile, true);
  inputBox(parent, 20, 112, "Объект", "Студия 29 м2, вторичное жилье");
  inputBox(parent, 20, 204, "Проблема", "Нужно зонирование и хранение");
  inputBox(parent, 20, 296, "Бюджет", "Комфорт, до 120 тыс. ₽ на реализацию");
  inputBox(parent, 20, 388, "Комментарий", "Старые коммуникации на кухне, мало естественного света");
  rounded(parent, 20, 530, 350, 96, 24, COLORS.accentSoft);
  text(parent, "После отправки специалист получит сохраненные проекты и критерии подбора.", 40, 558, 290, {
    size: 14,
    color: COLORS.text,
    height: 44
  });
  const send = button(parent, "Отправить заявку", 20, 724, 350, 52, "primary");
  link(send, screens.favorites);
}

function status(parent) {
  text(parent, "9:41", 24, 16, 60, { size: 13, weight: "semi", height: 18 });
  rounded(parent, 300, 18, 42, 12, 6, COLORS.text, 0.18);
  rounded(parent, 346, 18, 20, 12, 6, COLORS.text, 0.18);
}

function header(parent, title, subtitle, destination, back) {
  if (back) {
    const backBtn = rounded(parent, 20, 48, 40, 40, 14, COLORS.surface);
    text(parent, "<", 35, 56, 14, { size: 18, weight: "bold", color: COLORS.primaryDark, height: 22 });
    link(backBtn, destination);
  }
  text(parent, title, back ? 72 : 20, 46, 230, { size: 22, weight: "bold", height: 32 });
  text(parent, subtitle, back ? 72 : 20, 76, 260, { size: 12, color: COLORS.muted, height: 18 });
  const icon = rounded(parent, 330, 50, 40, 40, 14, COLORS.surface);
  text(parent, "♡", 343, 57, 18, { size: 18, color: COLORS.primary, height: 22 });
  if (destination && !back) {
    link(icon, destination);
  }
}

function sectionTitle(parent, value, x, y) {
  text(parent, value, x, y, 260, { size: 17, weight: "semi", height: 26 });
}

function featureCard(parent, x, y, w, h, title, description, number) {
  const card = rounded(parent, x, y, w, h, 24, COLORS.surface);
  card.effects = [shadow(0, 8, 24, 0.08)];
  rounded(parent, x + 14, y + 14, 42, 42, 14, COLORS.primarySoft);
  text(parent, number, x + 27, y + 25, 22, { size: 13, weight: "bold", color: COLORS.primaryDark, height: 18 });
  text(parent, title, x + 14, y + 68, w - 28, { size: 15, weight: "semi", height: 22 });
  text(parent, description, x + 14, y + 92, w - 28, { size: 11, color: COLORS.muted, height: 28 });
  return card;
}

function largeChoice(parent, x, y, title, desc, label) {
  const card = rounded(parent, x, y, 350, 94, 24, COLORS.surface);
  card.effects = [shadow(0, 8, 24, 0.07)];
  rounded(parent, x + 18, y + 18, 58, 58, 20, COLORS.primarySoft);
  text(parent, label, x + 30, y + 38, 44, { size: 10, weight: "semi", color: COLORS.primaryDark, height: 16 });
  text(parent, title, x + 94, y + 20, 210, { size: 17, weight: "semi", height: 24 });
  text(parent, desc, x + 94, y + 50, 210, { size: 12, color: COLORS.muted, height: 30 });
  text(parent, ">", x + 326, y + 34, 14, { size: 18, weight: "bold", color: COLORS.primary, height: 24 });
  return card;
}

function objectCard(parent, x, y, title, desc, type) {
  const card = rounded(parent, x, y, 350, 108, 24, COLORS.surface);
  roomMock(parent, x + 18, y + 18, 76, 72, type === "room" ? "small" : "living");
  text(parent, title, x + 112, y + 24, 190, { size: 18, weight: "semi", height: 26 });
  text(parent, desc, x + 112, y + 56, 200, { size: 12, color: COLORS.muted, height: 34 });
  text(parent, ">", x + 326, y + 42, 14, { size: 18, weight: "bold", color: COLORS.primary, height: 24 });
  return card;
}

function wideFilter(parent, x, y, title, desc) {
  const item = rounded(parent, x, y, 350, 76, 22, COLORS.surface);
  text(parent, title, x + 20, y + 16, 250, { size: 16, weight: "semi", height: 24 });
  text(parent, desc, x + 20, y + 44, 270, { size: 12, color: COLORS.muted, height: 20 });
  text(parent, ">", x + 326, y + 27, 14, { size: 18, weight: "bold", color: COLORS.primary, height: 24 });
  return item;
}

function smallFilter(parent, x, y, title, value) {
  const box = rounded(parent, x, y, 106, 50, 18, COLORS.surface);
  text(parent, title, x + 14, y + 8, 78, { size: 10, color: COLORS.muted, height: 14 });
  text(parent, value, x + 14, y + 24, 78, { size: 13, weight: "semi", color: COLORS.text, height: 18 });
  return box;
}

function styleTile(parent, x, y, title, color, destination) {
  const tile = rounded(parent, x, y, 166, 144, 26, COLORS.surface);
  rounded(parent, x + 14, y + 14, 138, 82, 20, color);
  roomMock(parent, x + 26, y + 28, 114, 52, "small");
  text(parent, title, x + 16, y + 108, 120, { size: 16, weight: "semi", height: 24 });
  link(tile, destination);
  return tile;
}

function tariff(parent, x, y, title, desc, price) {
  const card = rounded(parent, x, y, 350, 124, 26, COLORS.surface);
  text(parent, title, x + 22, y + 20, 190, { size: 20, weight: "bold", height: 28 });
  text(parent, desc, x + 22, y + 54, 228, { size: 13, color: COLORS.muted, height: 36 });
  rounded(parent, x + 230, y + 22, 96, 36, 16, COLORS.primarySoft);
  text(parent, price, x + 244, y + 32, 72, { size: 11, weight: "semi", color: COLORS.primaryDark, height: 16 });
  text(parent, ">", x + 318, y + 76, 14, { size: 18, weight: "bold", color: COLORS.primary, height: 24 });
  return card;
}

function projectListCard(parent, x, y, title, desc, destination) {
  const card = rounded(parent, x, y, 350, 98, 24, COLORS.surface);
  roomMock(parent, x + 14, y + 14, 86, 70, "small");
  text(parent, title, x + 116, y + 18, 190, { size: 16, weight: "semi", height: 24 });
  text(parent, desc, x + 116, y + 48, 194, { size: 12, color: COLORS.muted, height: 30 });
  text(parent, ">", x + 326, y + 37, 14, { size: 18, weight: "bold", color: COLORS.primary, height: 24 });
  link(card, destination);
  return card;
}

function projectFeedCard(parent, x, y, title, desc, destination) {
  const card = rounded(parent, x, y, 350, 146, 28, COLORS.surface);
  card.effects = [shadow(0, 8, 24, 0.08)];
  roomMock(parent, x + 14, y + 14, 126, 118, "living");
  text(parent, title, x + 158, y + 22, 166, { size: 17, weight: "semi", height: 48 });
  text(parent, desc, x + 158, y + 76, 166, { size: 12, color: COLORS.muted, height: 36 });
  rounded(parent, x + 158, y + 116, 72, 22, 11, COLORS.accentSoft);
  text(parent, "совпадает", x + 170, y + 120, 58, { size: 10, weight: "semi", color: COLORS.accent, height: 14 });
  text(parent, ">", x + 326, y + 60, 14, { size: 18, weight: "bold", color: COLORS.primary, height: 24 });
  link(card, destination);
  return card;
}

function savedMaster(parent, x, y, name, desc, destination) {
  const card = rounded(parent, x, y, 350, 98, 24, COLORS.surface);
  avatar(parent, x + 18, y + 18, 58, initials(name));
  text(parent, name, x + 94, y + 18, 180, { size: 17, weight: "semi", height: 24 });
  text(parent, desc, x + 94, y + 48, 198, { size: 12, color: COLORS.muted, height: 30 });
  rounded(parent, x + 278, y + 26, 48, 28, 14, COLORS.primarySoft);
  text(parent, "4.9", x + 292, y + 32, 24, { size: 12, weight: "bold", color: COLORS.primaryDark, height: 16 });
  link(card, destination);
  return card;
}

function proCategory(parent, x, y, title, desc, count) {
  const card = rounded(parent, x, y, 350, 112, 26, COLORS.surface);
  rounded(parent, x + 18, y + 18, 62, 62, 22, title === "Инженеры" ? COLORS.accentSoft : COLORS.primarySoft);
  text(parent, title === "Инженеры" ? "ИН" : "ДЗ", x + 36, y + 40, 30, {
    size: 12,
    weight: "bold",
    color: title === "Инженеры" ? COLORS.accent : COLORS.primaryDark,
    height: 16
  });
  text(parent, title, x + 100, y + 18, 190, { size: 19, weight: "bold", height: 28 });
  text(parent, desc, x + 100, y + 50, 200, { size: 12, color: COLORS.muted, height: 30 });
  text(parent, count, x + 100, y + 82, 120, { size: 11, weight: "semi", color: COLORS.primary, height: 16 });
  text(parent, ">", x + 326, y + 44, 14, { size: 18, weight: "bold", color: COLORS.primary, height: 24 });
  return card;
}

function segmented(parent, x, y, labels, activeIndex) {
  const container = rounded(parent, x, y, 350, 48, 18, COLORS.surfaceSoft);
  const items = [];
  const w = 350 / labels.length;
  labels.forEach((label, index) => {
    const item = rounded(parent, x + index * w + 4, y + 4, w - 8, 40, 15, index === activeIndex ? COLORS.surface : COLORS.surfaceSoft);
    text(parent, label, x + index * w + 28, y + 16, w - 56, {
      size: 13,
      weight: "semi",
      color: index === activeIndex ? COLORS.text : COLORS.muted,
      align: "CENTER",
      height: 18
    });
    items.push(item);
  });
  return items;
}

function inputBox(parent, x, y, label, value) {
  rounded(parent, x, y, 350, 72, 20, COLORS.surface);
  text(parent, label, x + 18, y + 12, 210, { size: 11, weight: "semi", color: COLORS.muted, height: 16 });
  text(parent, value, x + 18, y + 34, 294, { size: 14, color: COLORS.text, height: 24 });
}

function metricRow(parent, x, y, items) {
  const cellW = 106;
  items.forEach(([value, label], index) => {
    rounded(parent, x + index * (cellW + 10), y, cellW, 70, 22, COLORS.surface);
    text(parent, value, x + index * (cellW + 10), y + 16, cellW, {
      size: 18,
      weight: "bold",
      align: "CENTER",
      height: 24
    });
    text(parent, label, x + index * (cellW + 10), y + 44, cellW, {
      size: 10,
      color: COLORS.muted,
      align: "CENTER",
      height: 14
    });
  });
}

function chipGrid(parent, x, y, labels, columns) {
  const gutter = 10;
  const w = (350 - gutter * (columns - 1)) / columns;
  labels.forEach((label, index) => {
    const col = index % columns;
    const row = Math.floor(index / columns);
    chip(parent, label, x + col * (w + gutter), y + row * 48, w, index % 3 === 0);
  });
}

function chip(parent, label, x, y, w, active) {
  const item = rounded(parent, x, y, w, 36, 18, active ? COLORS.primarySoft : COLORS.surface);
  text(parent, label, x + 12, y + 10, w - 24, {
    size: 12,
    weight: active ? "semi" : "regular",
    color: active ? COLORS.primaryDark : COLORS.muted,
    height: 16,
    align: "CENTER"
  });
  return item;
}

function button(parent, label, x, y, w, h, variant) {
  let bg = COLORS.primary;
  let fg = COLORS.white;
  if (variant === "secondary") {
    bg = COLORS.surface;
    fg = COLORS.primaryDark;
  }
  if (variant === "ghost") {
    bg = COLORS.primarySoft;
    fg = COLORS.primaryDark;
  }
  const btn = rounded(parent, x, y, w, h, 18, bg);
  if (variant === "secondary") {
    btn.strokes = [paint(COLORS.line)];
    btn.strokeWeight = 1;
  }
  text(parent, label, x + 12, y + (h - 18) / 2, w - 24, {
    size: 14,
    weight: "semi",
    color: fg,
    align: "CENTER",
    height: 18
  });
  return btn;
}

function addBottomNav(parent, active, screens) {
  rounded(parent, 20, 786, 350, 48, 22, COLORS.surface);
  const items = [
    ["home", "Дом", screens.home],
    ["catalog", "Каталог", screens.catalog],
    ["favorites", "Избранное", screens.favorites],
    ["specialists", "Профи", screens.specialists]
  ];
  items.forEach(([key, label, dest], index) => {
    const x = 32 + index * 82;
    const item = rounded(parent, x, 794, 66, 32, 16, key === active ? COLORS.primarySoft : COLORS.surface, key === active ? 1 : 0);
    text(parent, label, x + 4, 803, 58, {
      size: 11,
      weight: key === active ? "semi" : "regular",
      color: key === active ? COLORS.primaryDark : COLORS.muted,
      align: "CENTER",
      height: 14
    });
    link(item, dest);
  });
}

function checklist(parent, x, y, items) {
  items.forEach((item, index) => {
    const yy = y + index * 42;
    rounded(parent, x, yy + 2, 22, 22, 11, COLORS.accentSoft);
    text(parent, "✓", x + 6, yy + 4, 12, { size: 12, weight: "bold", color: COLORS.accent, height: 16 });
    text(parent, item, x + 34, yy, 300, { size: 13, color: COLORS.text, height: 34 });
  });
}

function roomMock(parent, x, y, w, h, type) {
  const container = rounded(parent, x, y, w, h, Math.min(22, h / 4), COLORS.surface);
  rounded(parent, x + w * 0.08, y + h * 0.1, w * 0.84, h * 0.48, 18, type === "living" ? COLORS.primarySoft : COLORS.accentSoft);
  rounded(parent, x + w * 0.14, y + h * 0.6, w * 0.34, h * 0.22, 10, "#D6B1A6");
  rounded(parent, x + w * 0.54, y + h * 0.6, w * 0.32, h * 0.22, 10, "#CFA398");
  rounded(parent, x + w * 0.18, y + h * 0.18, w * 0.24, h * 0.24, 12, COLORS.white, 0.55);
  line(parent, x + w * 0.5, y + h * 0.14, x + w * 0.5, y + h * 0.88, COLORS.white, 1, 0.6);
  return container;
}

function avatar(parent, x, y, size, letters) {
  rounded(parent, x, y, size, size, size / 2, COLORS.primarySoft);
  text(parent, letters, x, y + size / 2 - 9, size, {
    size: 14,
    weight: "bold",
    color: COLORS.primaryDark,
    align: "CENTER",
    height: 18
  });
}

function addFlowConnectors(parent, screens) {
  text(parent, "Ключевые переходы", 28, 604, 260, { size: 17, weight: "semi", height: 26 });
  const flows = [
    "Дом -> Поиск дизайна -> Выбор объекта -> Комната/Жилье -> Карточка проекта -> Избранное",
    "Дом -> Каталог идей -> Фильтры -> Карточка проекта",
    "Дом -> Специалисты -> Поиск по проблеме -> Инженеры/Дизайнеры -> Профиль -> Заявка"
  ];
  flows.forEach((flow, index) => {
    text(parent, flow, 28, 642 + index * 34, 330, { size: 11, color: COLORS.muted, height: 28 });
  });
  const homeHotspot = rounded(parent, 28, 556, 150, 34, 17, COLORS.primarySoft);
  text(parent, "Старт: Дом", 54, 565, 96, { size: 12, weight: "semi", color: COLORS.primaryDark, height: 16 });
  link(homeHotspot, screens.home);
}

function link(node, destination) {
  if (!node || !destination) return;
  const reaction = [
    {
      trigger: { type: "ON_CLICK" },
      action: {
        type: "NODE",
        destinationId: destination.id,
        navigation: "NAVIGATE",
        transition: {
          type: "SMART_ANIMATE",
          easing: { type: "EASE_OUT" },
          duration: 0.25
        },
        preserveScrollPosition: false
      }
    }
  ];
  node.reactions = reaction;

  const hotspot = figma.createRectangle();
  hotspot.name = "Hotspot -> " + destination.name;
  node.parent.appendChild(hotspot);
  hotspot.x = node.x;
  hotspot.y = node.y;
  hotspot.resize(node.width, node.height);
  hotspot.cornerRadius = typeof node.cornerRadius === "number" ? node.cornerRadius : 0;
  hotspot.fills = [paint(COLORS.white, 0.01)];
  hotspot.reactions = reaction;
}

function rounded(parent, x, y, w, h, radius, color, opacity) {
  const node = figma.createRectangle();
  parent.appendChild(node);
  node.x = x;
  node.y = y;
  node.resize(w, h);
  node.cornerRadius = radius;
  node.fills = [paint(color, opacity === undefined ? 1 : opacity)];
  return node;
}

function line(parent, x1, y1, x2, y2, color, width, opacity) {
  const node = figma.createLine();
  parent.appendChild(node);
  node.x = x1;
  node.y = y1;
  node.resize(Math.max(1, x2 - x1), Math.max(1, y2 - y1));
  node.rotation = x1 === x2 ? 90 : 0;
  node.strokes = [paint(color, opacity === undefined ? 1 : opacity)];
  node.strokeWeight = width;
  return node;
}

function text(parent, value, x, y, w, opts = {}) {
  const node = figma.createText();
  parent.appendChild(node);
  node.name = "Text / " + value.slice(0, 30);
  node.x = x;
  node.y = y;
  node.resize(w, opts.height || 24);
  node.fontName = FONTS[opts.weight || "regular"];
  node.characters = value;
  node.fontSize = opts.size || 14;
  node.lineHeight = { unit: "PIXELS", value: opts.lineHeight || Math.round((opts.size || 14) * 1.35) };
  node.fills = [paint(opts.color || COLORS.text)];
  if (opts.align) {
    node.textAlignHorizontal = opts.align;
  }
  return node;
}

function fill(node, color) {
  node.fills = [paint(color)];
}

function paint(color, opacity = 1) {
  const rgb = hexToRgb(color);
  return { type: "SOLID", color: rgb, opacity };
}

function shadow(x, y, radius, alpha) {
  return {
    type: "DROP_SHADOW",
    color: { r: 0.18, g: 0.12, b: 0.08, a: alpha },
    offset: { x, y },
    radius,
    spread: 0,
    visible: true,
    blendMode: "NORMAL"
  };
}

function hexToRgb(hex) {
  const normalized = hex.replace("#", "");
  const bigint = parseInt(normalized, 16);
  return {
    r: ((bigint >> 16) & 255) / 255,
    g: ((bigint >> 8) & 255) / 255,
    b: (bigint & 255) / 255
  };
}

function initials(name) {
  return name
    .split(" ")
    .map((part) => part[0])
    .join("")
    .slice(0, 2)
    .toUpperCase();
}
