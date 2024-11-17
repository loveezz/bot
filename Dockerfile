FROM python:3.11

WORKDIR /app

# Копируем файл зависимостей
COPY requirements.txt requirements.txt

# Обновляем setuptools и pip
RUN pip install --upgrade setuptools pip

# Устанавливаем зависимости
RUN pip install -r requirements.txt

# Копируем остальные файлы
COPY . .

# Указываем команду запуска
CMD ["python", "app/main.py"]
