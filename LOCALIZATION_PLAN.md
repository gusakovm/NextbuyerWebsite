# План локализации внешних Tilda ресурсов

## Цель
Скачать все внешние файлы с Tilda CDN и заменить ссылки на локальные пути в index.html, чтобы сайт работал независимо от подписки Tilda.

## Найденные внешние ресурсы

**Ресурсы для локализации:**
- 23+ JavaScript файлов с `static.tildacdn.net` и `neo.tildacdn.com`
- 9+ CSS файлов с `static.tildacdn.net`
- 30+ изображений с `thb.tildacdn.net` (67 ссылок)
- 2 проектных файла с cache-buster: `tilda-blocks-page47866911.min.css?t=1753432672` и `.js`
- Favicon файлы

**Ресурсы которые оставляем внешними:**
- Google Fonts (fonts.googleapis.com)
- Google Analytics/Tag Manager (www.googletagmanager.com)

## Критические файлы

- [docs/index.html](docs/index.html) - основной HTML файл (1.2MB, НЕЛЬЗЯ открывать напрямую!)
- [docs/custom.css?t=1753432672.css](docs/custom.css?t=1753432672.css) - кастомные стили
- [docs/custom.css?t=1753432577.css](docs/custom.css?t=1753432577.css) - старая версия кастомных стилей

## Структура папок

Создадим следующую структуру в `docs/`:

```
docs/
├── assets/
│   ├── js/
│   │   ├── tilda-framework/    # Все Tilda JS файлы
│   │   └── project/            # Проектный JS с cache-buster
│   ├── css/
│   │   ├── tilda-framework/    # Все Tilda CSS файлы
│   │   └── project/            # Проектный CSS с cache-buster
│   └── images/
│       ├── tilda-cdn/          # Изображения с thb.tildacdn.net
│       └── favicons/           # Favicon файлы
├── custom.css                  # Объединенный custom.css
└── index.html
```

## Этапы реализации

### Этап 1: Создание структуры папок
```bash
mkdir -p docs/assets/{js/{tilda-framework,project},css/{tilda-framework,project},images/{tilda-cdn,favicons}}
```

### Этап 2: Извлечение списка уникальных URL

Используя grep, извлечём все уникальные URL для скачивания:

**JavaScript файлы:**
- Извлечь все URL с `static.tildacdn.net/js/` и `neo.tildacdn.com/js/`
- Извлечь проектный JS с query параметром

**CSS файлы:**
- Извлечь все URL с `static.tildacdn.net/css/`
- Извлечь проектный CSS с query параметром

**Изображения:**
- Извлечь все уникальные Tilda ID изображений из URL `thb.tildacdn.net`
- Извлечь favicon URL из `static.tildacdn.net`

### Этап 3: Скачивание файлов

Создать bash скрипт для скачивания всех файлов:

1. Скачать все JS файлы в `docs/assets/js/tilda-framework/`
2. Скачать проектный JS (без query параметра) в `docs/assets/js/project/`
3. Скачать все CSS файлы в `docs/assets/css/tilda-framework/`
4. Скачать проектный CSS в `docs/assets/css/project/`
5. Скачать изображения:
   - Для каждого уникального Tilda ID скачать изображение из `thb.tildacdn.net`
   - Обрабатывать resize параметры: `/-/resize/20x/` и похожие
   - Сохранять с именем формата: `tild[ID]-[filename].png`
6. Скачать favicon файлы в `docs/assets/images/favicons/`

### Этап 4: Замена URL в index.html

Использовать sed для замены URL БЕЗ открытия файла:

**Tilda JavaScript:**
```bash
sed -i '' 's|https://static\.tildacdn\.net/js/|./assets/js/tilda-framework/|g' docs/index.html
sed -i '' 's|https://neo\.tildacdn\.com/js/|./assets/js/tilda-framework/|g' docs/index.html
```

**Tilda CSS:**
```bash
sed -i '' 's|https://static\.tildacdn\.net/css/|./assets/css/tilda-framework/|g' docs/index.html
```

**Проектные файлы с cache-buster:**
```bash
sed -i '' 's|https://static\.tildacdn\.net/ws/project8746385/\([^"]*\)\.css\?t=[0-9]*|./assets/css/project/\1.css|g' docs/index.html
sed -i '' 's|https://static\.tildacdn\.net/ws/project8746385/\([^"]*\)\.js\?t=[0-9]*|./assets/js/project/\1.js|g' docs/index.html
```

**Изображения:**
```bash
# Изображения с resize параметрами
sed -i '' 's|https://thb\.tildacdn\.net/\(tild[a-f0-9-]*\)/-/resize/[^/]*/\([^"'\'']*\)|./assets/images/tilda-cdn/\1-\2|g' docs/index.html

# Favicon и OG изображения
sed -i '' 's|https://static\.tildacdn\.net/tild[a-f0-9-]*/\([^"'\'']*\)|./assets/images/favicons/\1|g' docs/index.html
```

**Custom CSS:**
```bash
# Убрать URL-encoded query параметры
sed -i '' 's|custom\.css%3Ft=[0-9]*\.css|custom.css|g' docs/index.html
```

**Удалить DNS prefetch для Tilda:**
```bash
sed -i '' '/dns-prefetch.*tildacdn/d' docs/index.html
```

### Этап 5: Обновление форм

В index.html есть две формы с классом `t-form__inputsbox`. Нужно:

1. Найти все формы через grep
2. Обновить action URL формы на `https://api.cdoc.cc/nextbuyer-step1`
3. Убрать редирект после отправки
4. Возможно, отключить Tilda-специфичные обработчики форм

### Этап 6: Объединение custom.css

Оба файла `custom.css?t=*.css` идентичны (3.5K). Нужно:

1. Удалить файлы с query параметрами в имени
2. Создать один файл `docs/custom.css` с содержимым

### Этап 7: Проверка результата

**Автоматическая проверка:**
```bash
# Проверить что не осталось ссылок на Tilda CDN (кроме ws.tildacdn.com для форм)
grep -c 'static\.tildacdn\|neo\.tildacdn\|thb\.tildacdn' docs/index.html

# Проверить что все локальные файлы существуют
grep -o '\./assets/[^"'\'']*' docs/index.html | sort -u | while read file; do
  [ -f "docs/$file" ] && echo "✓ $file" || echo "✗ MISSING: $file"
done

# Подсчитать количество скачанных файлов
find docs/assets -type f | wc -l
```

**Ручная проверка:**
1. Открыть `docs/index.html` в браузере (file://)
2. Проверить консоль на 404 ошибки
3. Проверить что стили применяются корректно
4. Проверить что изображения загружаются
5. Проверить работу интерактивных элементов (popup, video, анимации)
6. Протестировать отправку форм

### Этап 8: Git commit

После успешной проверки:
```bash
git add docs/assets/
git add docs/index.html
git add docs/custom.css
git rm "docs/custom.css?t=1753432577.css"
git rm "docs/custom.css?t=1753432672.css"

git commit -m "Localize Tilda CDN resources

- Download 23+ JS files from static.tildacdn.net and neo.tildacdn.com
- Download 9+ CSS files from static.tildacdn.net
- Download 30+ images from thb.tildacdn.net
- Replace all CDN URLs with local paths
- Keep Google Fonts and Analytics external
- Update form action to api.cdoc.cc
- Consolidate custom.css files

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"
```

## Важные замечания

1. **index.html нельзя читать напрямую** - файл слишком большой (1.2MB), используем только grep/sed
2. **Google Fonts и Analytics оставляем внешними** - они должны работать через CDN
3. **Формы нужно переделать** - вместо Tilda API отправлять на `https://api.cdoc.cc/nextbuyer-step1`
4. **Cache-buster параметры** - убираем из URL при скачивании, файлы сохраняем без `?t=timestamp`
5. **Изображения с resize** - скачиваем оригиналы, размер контролируем через CSS
6. **Backup** - перед заменой URL создать backup: `cp docs/index.html docs/index.html.backup`
7. **WebSocket для форм** - возможно понадобится оставить `ws.tildacdn.com` если формы используют WebSocket

## Ожидаемый результат

После выполнения плана:
- Все Tilda CDN ресурсы будут локальными
- Сайт будет работать даже если подписка Tilda истечет
- Google Fonts и Analytics продолжат работать через внешний CDN
- Формы будут отправляться на собственный API endpoint
- Размер репозитория увеличится на ~5-10MB (JS, CSS, изображения)
- Количество HTTP запросов к внешним доменам сократится с ~180 до ~4 (Google Fonts и Analytics)
