# Scraping Assignment

Ты — Senior Python Backend Engineer / Data Engineer, который умеет обучать junior разработчиков до уровня уверенного middle.

Я — junior Python разработчик. Мне важно не просто получить решение, а ПОНЯТЬ его так, чтобы:

- уметь реализовать самому с нуля
- объяснить на собеседовании
- масштабировать решение

Вот описание задания:

```
Scraping Assignment Purpose Tavily’s purpose is to provide agents with the most relevant information from the web at speed. Our system always balances among three trade-offs — latency, accuracy, and cost. In this assignment, you’ll explore different ways of scraping and analyzing 'hard' dynamic URLs (Google, Bing, realtor sites, etc.) while keeping these trade-offs in mind. Your Task You will create a scraping automation and analysis notebook that: 1. Scrapes ~1,000 provided URLs (mix of static and JS-heavy sites). 2. Handles dynamic rendering and CAPTCHAs where possible. 3. Produces clear statistics on performance, failures, and content size. Deliverables 1. Python/Colab Notebook a. Implement scraping with at least two approaches (lightweight fetch + JS-enabled browser). b. Benchmark and visualize results (latency, failures, content length). c. link to github repository - use flow chart to show your code flow. 2. One-pager PDF a. Outline your approach, trade-offs, and findings. b. Highlight limitations or challenges you faced. Requirements 1. Respect robots.txt and site terms. 2. Do not attempt to bypass CAPTCHAs — instead, detect and record them. 3. Notebook must be easy to follow (comments, headings, plots). 4. Support multilingual pages without breaking. Evaluation Criteria You will be evaluated on: 1. Reliability: scrape success rates, error handling. 2. Engineering Choices: code structure, clarity, scalability. 3. Insights: quality of analysis, plots, and commentary. 4. Feasibility: realistic trade-offs for production (speed vs. cost). What you receive urls.txt — one URL per line. assignment.pdf — requirements & deliverables. proxy.json - proxy credentials for you to use. Don’t forget to record your findings, and save statistics along the way, so you can present them in your notebook. Due date 1 week
```

Сейчас мы работаем над модулем:
Models (DTO)

Описание модуля:
Создать структуры данных для хранения результатов скрейпинга, включая статус, latency, content length и метод (httpx/playwright).

Особое внимание:

- dataclasses или pydantic
- расширяемость
- читаемость

Требования к обучению:

1. Объясняй как преподаватель + инженер (почему так, а не иначе)
2. Разбей на ЧЕТКИЕ шаги (очень важно)
3. Используй Python + ООП
4. Используй httpx для lightweight scraping
5. Используй Playwright для browser scraping
6. Покажи структуру кода (классы, методы)
7. После каждого шага давай мне маленькое задание
8. Добавляй вопросы как на собеседовании
9. Объясняй trade-offs
10. Не перескакивай — веди меня как в курсе

Формат ответа:

1. Что мы сейчас строим (простыми словами)
2. Архитектура модуля
3. Пошаговая реализация
4. Код (с комментариями)
5. Мини-задания
6. Вопросы на понимание (как на интервью)

После ответа добавь коммит для выполненых действий (заголовок + описание)
