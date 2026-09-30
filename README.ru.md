<p align="right">
  <a href="README.md">English</a> | <b>Русский</b>
</p>

> [!TIP]
> ### ⚡ Выгодная подписка на Antigravity, Claude и AI-сервисы
> Купить надежную и недорогую подписку можно в **[Taynik](https://t.me/taynikstore_bot?start=ref2001577066__15)**:
> - 🛡️ **Гарантия стабильности** — подписки не слетают, работают полный оплаченный срок.
> - ⭐ **Множество реальных отзывов** от разработчиков и пользователей.
> - 🚀 **Моментальная выдача** и лучшие цены на рынке.
> 
> 👉 **[Перейти в бота Taynik](https://t.me/taynikstore_bot?start=ref2001577066__15)**

<p align="center">
  <img src="docs/media/banner.png" alt="universal-modder" width="100%">
</p>

<p align="center">
  <b>Навыки, инструменты и fal MCP, позволяющие ИИ-агентам (Antigravity, Claude Code, Codex, Cursor) модифицировать практически любую ПК-игру из вашей библиотеки.</b><br>
  Находит игру, определяет движок и способ модификации, изучает реальный декомпилированный код, собирает мод,<br>
  генерирует спрайты, 3D-модели и звук через <a href="https://fal.ai">fal</a>, тестирует мод в запущенной игре и монтирует видеоролик.
</p>

<p align="center">
  <a href="#установка"><img alt="Antigravity ready" src="https://img.shields.io/badge/Antigravity-ready-4285F4?labelColor=0A0D12"></a>
  <a href="#установка"><img alt="Claude Code plugin" src="https://img.shields.io/badge/Claude%20Code-plugin-B6FF3B?labelColor=0A0D12"></a>
  <a href="https://fal.ai"><img alt="assets by fal" src="https://img.shields.io/badge/assets-fal-B6FF3B?labelColor=0A0D12"></a>
  <a href="LICENSE"><img alt="MIT" src="https://img.shields.io/badge/license-MIT-B6FF3B?labelColor=0A0D12"></a>
</p>

<p align="center">
  <img src="docs/media/teaser.gif" alt="Тактический ядерный удар в Terraria и роботакси в Age of Empires II, созданные с universal-modder" width="560">
</p>

> **О форке:** Этот форк (`makasinok/universal-modder-antigravity`) расширяет оригинальный проект ([`rehan-remade/universal-modder`](https://github.com/rehan-remade/universal-modder)):
> - **Нативная поддержка Antigravity**: каталог `.agents/skills/` для всех 9 навыков, файл правил `GEMINI.md`, конфигурация fal MCP в `mcp_config.json` и хуки запуска.
> - **Полная поддержка Linux, Steam Deck и Proton**: нативная автоматизация игр (`um win` через `xdotool`, `import`, `ffmpeg`), сканирование Flatpak Steam, поиск сохранений в префиксах Proton (`compatdata/<appid>/pfx`), а также обнаружение игр из Heroic Games Launcher и Lutris.
> - **Диагностика окружения (`um doctor`)**: проверка ОС, дисплейного сервера (X11/Wayland), системных утилит (`uv`, `ffmpeg`, `blender`), аппаратных видеокодеров GPU (`nvenc`, `vaapi`), префиксов Proton и декомпиляторов (`ilspycmd`, `ghidra`, `dotnet`).

## Установка

**Для Antigravity (Antigravity IDE / CLI)**:
Откройте репозиторий как воркспейс или клонируйте:
```bash
git clone https://github.com/makasinok/universal-modder-antigravity && cd universal-modder-antigravity
```
Antigravity автоматически подключит 9 навыков из `.agents/skills/`, применит правила безопасности из `GEMINI.md` и подключится к fal MCP через `mcp_config.json`.

**Как плагин для Claude Code**:
```
/plugin marketplace add rehan-remade/universal-modder
/plugin install universal-modder@universal-modder
```

**Или клонируйте и запустите Claude / Codex / Cursor**:
```bash
git clone https://github.com/makasinok/universal-modder-antigravity && cd universal-modder-antigravity && claude
```

Затем укажите [ключ fal API](https://fal.ai/dashboard/keys) для генерации ассетов. Он используется как встроенным MCP-сервером fal, так и утилитой `um fal`:
```bash
export FAL_KEY=...
```
Также потребуется Python 3.10+ и ffmpeg. Рекомендуется менеджер `uv` (CLI автоматически настраивает окружение через него). Для рендера 3D в спрайты необходим Blender. Управление играми поддерживается на **Linux** (нативно, Flatpak Steam или Proton), **Windows** и **WSL**.
Запустите `um doctor` в любой момент для полной диагностики вашего окружения.

## Примеры запросов
> Сделай мод для Terraria: добавь ракетницу с самонаведением и тактический ядерный удар, оставляющий кратер в мире. Нарисуй спрайты через fal.

> Создай новую цивилизацию для Age of Empires II с уникальным юнитом, отрендеренным из 3D-модели.

> У меня есть Skyrim SE. Что потребуется, чтобы добавить в него режим строительства блоков как в Minecraft?

> На каком движке сделана игра `C:\Games\Foo` (или `/path/to/game`) и как её обычно модифицируют?

Агент начинает с навыка **mod-any-game** и проходит полный цикл: разведка (recon), выбор пути моддинга, создание изолированной среды (бэкап сохранений), чтение реального кода игры, создание первого рабочего прототипа, генерация ассетов, тестирование в реальной игре, запись геймплея и сборка релиза.

## Что внутри

**Навыки (`skills/`)**

| Навык | Что делает |
|---|---|
| `mod-any-game` | Полный цикл моддинга, жесткие правила безопасности и **12 справочников по движкам**: Unity, Unreal, .NET/XNA (Terraria, Stardew, Celeste), Godot, Source 1/2, Bethesda, Minecraft, AoE2/Genie, RE Engine/FromSoft/GTA/Cyberpunk/BG3, нативный C++, инди-движки (GameMaker, RPG Maker, Ren'Py, Paradox, Doom, HTML5, LÖVE, Java), ретро-декомпиляции |
| `game-recon` | Определение движка и версии, управляемый код или нативный, античит, загрузчики модов, папки сохранений, популярные методы моддинга → формирование `MODDING_PLAN.md` |
| `reverse-engineering` | Декомпиляция через ILSpy / Cpp2IL / Vineflower / Ghidra и IDA через MCP / Cheat Engine / Frida / RenderDoc; реверс бинарных форматов с проверкой round-trip |
| `fal-assets` | Спрайты с прозрачным фоном, консистентные варианты, пиксель-арт, бесшовные текстуры, PBR-карты, 3D из картинок, авто-риггинг, звуковые эффекты, музыка, озвучка, катсцены |
| `asset-pipeline` | Преобразование арта под спецификации движка: обрезка краев, nearest-neighbor скейлинг, палитры, спрайт-листы, маски командных цветов, 3D в спрайты с 8/16 ракурсами |
| `game-automation` | Запуск, безопасные GPU-скриншоты, симуляция кликов и клавиш, запуск в окне, закрытие окон отчетов о крашах, внутриигровые JSON-мосты для ИИ |
| `showcase-video` | Запись игрового окна с захватом звука самой игры, выбор лучших моментов по контактным листам, монтаж стильного видео по EDL-таймлайну с титрами и музыкой |
| `mashup-mods` | Мэшапы и кросс-игровой контент: перенос механик, passthrough-моды, запуск декомпилированных игр как библиотек, чистые реимплементации |
| `publish-mod` | Линтер перед релизом, упаковка под платформы, указание авторства и генераций, публикация |

**CLI-инструмент `um` (`bin/um`, Python). У каждой команды есть подробный `--help`.**

| Команда | Назначение |
|---|---|
| `um doctor` | Диагностика системы: ОС, дисплейный сервер, установленные утилиты, Steam/Proton, видеокодеры GPU |
| `um scan` | Поиск игр в Steam (нативный и Flatpak), Epic, Xbox, Heroic, Lutris, префиксов Proton; анализ движка, детекция .NET/C++, античитов, установленных лоадеров и сохранений |
| `um fal` | Генерация через fal: `sprite`, `image`, `edit`, `rmbg`, `pixelate`, `upscale`, `texture`, `pbr`, `model3d`, `rig`, `sfx`, `music`, `voice`, `video`, `run`, `search`, `schema`, `price` |
| `um sprite` | Обработка спрайтов: `cutout`, `fit`, `pixelate`, `palette`, `sheet`, `slice`, `frames`, `team-mask`, `seamless`, `preview` |
| `um render3d` | GLB → спрайты с углами камеры игры (`aoe2`, `iso8`, `trueiso`, `topdown`, `side`, `turntable`) через Blender |
| `um win` | Кроссплатформенная автоматизация (Windows, WSL и Linux): `shot`, `record`, `drive` (xdotool / WinDrive), `ps`, `kill`, `launch`, `reg` |
| `um video` | Монтаж видео: `contact` (контактные листы), `compile` (EDL-монтаж с титрами и музыкой), `mux`, `beats`, `first-frame` |
| `um backup` | Снимки, сравнение и восстановление папок сохранений (пути Windows и Linux/Proton) |
| `um publish check` | Проверка репозитория мода перед публикацией: блокирует случайную утечку файлов игры, декомпилированного кода и API-ключей |

Также в комплекте: **сервер fal MCP** (`.mcp.json`), хук SessionStart для добавления `um` в PATH, а также PowerShell-инструменты в `tools/win/` для захвата аудио и ввода в Windows.

<p align="center"><img src="docs/media/pipeline.png" alt="3D-пайплайн: от концепта fal к 3D и 16 ракурсам AoE2. 2D-пайплайн: арт fal к обрезке и спрайту 64x26 для Terraria в игре." width="100%"></p>

## Примеры созданных модов
- **[examples/terraria-tmodloader](examples/terraria-tmodloader)**: *Fal Arsenal* для tModLoader. Самонаводящаяся ракетница, тактический ядерный удар (кратер + гриб взрыва), цепная молниевая винтовка, гравитационная пушка, орбитальный удар, 3 новых врага и двухфазный босс Drone Mothership. Все спрайты созданы через fal.
- **[examples/aoe2-de-civ](examples/aoe2-de-civ)**: *San Franciscans* для Age of Empires II DE.
  - Новая цивилизация с уникальным юнитом «Роботакси» и дронами доставки, отрендеренными из 3D-моделей fal под ракурсом камеры AoE2.
  - Чудо света: Пирамида Трансамерика.
  - Реверс-инжиниринг формата `.sld` и собственный генератор спрайтов.

Оба мода начинались с однострочных промптов. Выводы и практический опыт зафиксированы в справочниках навыков ([`skills/mod-any-game/references/case-studies.md`](skills/mod-any-game/references/case-studies.md)).

## Правила безопасности
- **Только одиночные офлайн-игры, которыми вы владеете.** Агент категорически отказывается внедряться в онлайн-игры с античитом, создавать мультиплеерные читы или обходить античит, DRM и проверки владения игрой.
- **Никаких файлов игры и декомпилированного кода в релизе.** Моды публикуются в виде исходного кода, ваших собственных ассетов, патчей или конвертеров.
- **Обязательный бэкап перед изменением сохранений** и завершение процессов строго по конкретному PID.
- **Запрос подтверждения у пользователя** перед симуляцией ввода мыши/клавиатуры, установкой загрузчиков модов в директории игр или публикацией.

Подробное обоснование: [`skills/mod-any-game/references/safety.md`](skills/mod-any-game/references/safety.md).

## Авторы и благодарности
- Разработано на основе реальных сессий моддинга Terraria и Age of Empires II с Claude Code.
- Ассеты: [fal](https://fal.ai) (GPT Image 2, Nano Banana 2, FLUX, Trellis 2, ElevenLabs...).
- Благодарность сообществам: tModLoader, genieutils-py, AoE2ScenarioParser, BepInEx, Harmony, UE4SS, REFramework, SKSE, Fabric, ILSpy, Ghidra и другим разработчикам инструментария для модов.
- Адаптация и развитие для **Antigravity** (Google DeepMind) и платформы Linux/Proton: `@makasinok`.

Лицензия: MIT. Шрифты: Space Grotesk и JetBrains Mono (SIL OFL).
