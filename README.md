# Kingdom Tetris — Pyxel project

Готовый каркас проекта под macOS Apple Silicon (M1/M2/M3/M4) и актуальный Pyxel.

## 1. Установка с нуля, если Homebrew отсутствует

### Шаг 1 — Command Line Tools

Открой Terminal:

```bash
xcode-select --install
```

Заверши установку системного окна.

### Шаг 2 — Homebrew

Официальная команда Homebrew:

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

На Apple Silicon Homebrew обычно устанавливается в `/opt/homebrew`.

После установки Homebrew сам покажет 1–2 команды для добавления `brew` в PATH. Выполни именно то, что он напечатает.

Типичный вариант для Apple Silicon:

```bash
echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
eval "$(/opt/homebrew/bin/brew shellenv)"
```

Проверка:

```bash
brew --version
```

### Шаг 3 — Python + pipx

```bash
brew install python
brew install pipx
pipx ensurepath
```

Закрой и снова открой Terminal.

Проверь:

```bash
python3 --version
pipx --version
```

Pyxel 2.9.x требует Python 3.11+.

### Шаг 4 — Pyxel

```bash
pipx install pyxel
```

Если уже установлен:

```bash
pipx upgrade pyxel
```

Проверка:

```bash
pyxel --version
```

### Шаг 5 — дополнительные инструменты для ресурсов

```bash
brew install ffmpeg
```

FFmpeg нужен только для подготовки/конвертации аудио и видео. Самой игре он не требуется.

## 2. Запуск

Перейди в папку проекта:

```bash
cd kingdom_tetris
```

Запусти:

```bash
python3 main.py
```

## 3. Управление

- ← / → — движение
- ↓ — мягкое ускоренное падение
- Z / X / ↑ — вращение
- Space — hard drop
- Shift + Q — +10 линий (чит для теста)
- Стрелки ↑ / ↓ — меню
- Enter / Space — выбор пункта меню
- ESC / Enter — назад из рекордов
- Любая из игровых клавиш — пропуск кат-сцены

## 4. Ресурсы

Проект запускается даже без `.pyxres`: в этом случае используются цветные заглушки.

Когда готовая графика и звук будут перенесены в Pyxel Editor, положи файлы:

- `resources/main_game.pyxres`
- `resources/phase2.pyxres`

Код автоматически обнаружит их.

Редактор:

```bash
pyxel edit resources/main_game.pyxres
```

и:

```bash
pyxel edit resources/phase2.pyxres
```

## 5. Спрайты фигур

В `image bank 0` ожидаются 16×16 спрайты:

- I: `(u=0, v=0)`
- O: `(u=16, v=0)`
- T: `(u=32, v=0)`
- S: `(u=48, v=0)`
- Z: `(u=64, v=0)`
- J: `(u=80, v=0)`
- L: `(u=96, v=0)`

Такая же раскладка используется в `phase2.pyxres`, но изображения там должны быть обновлёнными.

## 6. Рекорды

Файл `records.json` создаётся автоматически.
Хранятся 5 лучших результатов.
