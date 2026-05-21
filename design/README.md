# SenseRoom design assets

Готовые SVG-макеты находятся в каталоге:

`design/svg-screens/`

Основные файлы:

- 18 отдельных экранов `00_...svg` - `17_...svg`;
- `_all_screens_board.svg` - все экраны на одном полотне;
- `svg-screens/README.md` - инструкция по импорту в Figma и карта переходов;
- `generate_svg_screens.py` - генератор SVG-файлов для повторной сборки.

Для обновления SVG:

```bash
python3 design/generate_svg_screens.py
```
