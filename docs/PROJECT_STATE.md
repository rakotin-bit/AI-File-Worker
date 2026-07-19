v0.3.5.1

Работает:
✓ OpenRouter
✓ Model Registry
✓ Router
✓ SQLite Stats

Следующий шаг:
v0.3.6 Performance scoring
---

# Текущий этап разработки

## Версия

v0.3.6 — Model Performance Tracking (в разработке)

## Текущее состояние AI Router

Работает:

- OpenRouter интеграция
- Model Registry
- TTL Cache моделей
- Model Router
- ModelPriorityManager
- ModelStats
- SQLite хранение статистики моделей
- Exploration Mode

## Текущая проблема

Модели имеют разное время ответа.

Наблюдение:

- tencent/hy3:free — высокая стабильность, но большее время ответа
- nvidia/nemotron-nano-12b-v2-vl:free — быстрее
- nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free — быстрее

## Следующий шаг

Добавить измерение производительности моделей:

- время ответа;
- среднее время обработки;
- использование скорости в Model Router.

Цель:

Router должен выбирать не только самую успешную модель, но оптимальную по балансу:

качество + стабильность + скорость.

v0.3.6.1

Работает:

✓ OpenRouter
✓ Model Registry
✓ TTL Cache моделей
✓ Model Router
✓ ModelPriorityManager
✓ ModelStats
✓ SQLite хранение статистики моделей
✓ Exploration Mode
✓ Model latency tracking


---

# Текущий этап разработки

## Версия

v0.3.6.1 — Model Performance Tracking

## Текущее состояние AI Router

Работает:

- OpenRouter интеграция;
- получение списка моделей через Model Registry;
- TTL Cache моделей;
- автоматический выбор модели через Router;
- fallback между моделями;
- накопление статистики моделей;
- измерение времени ответа моделей.

## Проверено

Последний тест:

Модель:

tencent/hy3:free


Результат:

- Success: 7
- Failures: 0
- Average response time: 5.56s
- Последний latency: 5.46s


## Текущее ограничение

ModelPriorityManager сейчас отвечает за:

- ранжирование моделей;
- обновление статистики.

Для дальнейшего развития Router необходимо разделить:

- выбор модели;
- сбор и анализ производительности.

## Следующий шаг

v0.3.7 — Performance Layer Separation

Цель:

Подготовить архитектуру к v0.4 Intelligent Model Router.

Добавить:

- отдельный слой Performance Tracking;
- независимое управление статистикой;
- подготовку к расширенному scoring:

качество

+

стабильность

+

скорость

+

стоимость