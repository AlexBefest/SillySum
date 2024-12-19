import json
from openai import OpenAI

# Замените на ваши значения
YOUR_SITE_URL = "your_site_url"
YOUR_APP_NAME = "your_app_name"

# Инициализация клиента OpenAI
client = OpenAI(
    base_url="http://192.168.31.31:5001/v1",
    api_key="$OPENROUTER_API_KEY"
)

# Открытие файла .jsonl и чтение сообщений
messages = []
with open('2024-12-18 @17h 52m 21s 629ms.jsonl', 'r', encoding='utf-8') as file:
    for line in file:
        try:
            msg = json.loads(line)
            if 'mes' in msg:
                role = 'user' if msg['is_user'] else 'assistant'
                content = msg['mes']
                messages.append({"role": role, "content": content})
        except json.JSONDecodeError:
            print("Ошибка при чтении строки JSON:", line)
            continue

# Разбиение сообщений на чанки по 20 сообщений
chunk_size = 25
chunks = [messages[i:i + chunk_size] for i in range(0, len(messages), chunk_size)]

# Список для сохранения суммаризаций
summaries = []

# Отправка каждого чанка на API и сохранение суммаризаций
for chunk in chunks:
    # Добавление сообщения для ИИшки о суммаризации
    chunk.append({"role": "user", "content": "Проведи суммаризацию этих сообщений в вымышленной ролевой игре и верни подробный пересказ событий на английском языке. Не цитируй героев, просто перескажи от третьего лица."})
    
    # Отправка чанка на API
    completion = client.chat.completions.create(
        extra_headers={
            "HTTP-Referer": YOUR_SITE_URL,
            "X-Title": YOUR_APP_NAME,
        },
        model="qwen/qwen-2.5-coder-32b-instruct",
        messages=chunk
    )
    
    # Сохранение суммаризации
    summary = completion.choices[0].message.content
    summaries.append(summary)
    
    # Вывод чанка и ответа ИИшки
    for msg in chunk:
        print(f"{msg['role']}: {msg['content']}")
    print("Суммаризация ИИшки:")
    print(summary)
    print("\n" + "="*80 + "\n")

# Сохранение суммаризаций в JSON файл
with open('summaries.json', 'w', encoding='utf-8') as summary_file:
    json.dump(summaries, summary_file, ensure_ascii=False, indent=4)

print("Суммаризации сохранены в файл summaries.json")