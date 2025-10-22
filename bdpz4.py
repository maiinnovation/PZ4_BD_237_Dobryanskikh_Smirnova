import mysql.connector
from mysql.connector import Error
import csv
import json

with open('config.json', 'r') as file:
    config = json.load(file)

db = mysql.connector.connect(**config)

if db.is_connected():
        print("ок")

else:
    print(f'не ок: {Error}')

cursor = db.cursor()

cursor.execute("DROP TABLE IF EXISTS employees")
print("таблица удалена")

cursor.execute("""
CREATE TABLE IF NOT EXISTS employees (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    email VARCHAR(255),
    age INT,
    salary DECIMAL(10,2),
    department VARCHAR(100),
    city VARCHAR(100)
)
""")
print("таблица ок")

employees_data = [
    ('Иван Иванов', 'ivan@mail.ru', 28, 50000.50, 'IT', 'Москва'),
    ('Мария Петрова', 'maria@mail.ru', 32, 65000.00, 'HR', 'СПб'),
    ('Алексей Сидоров', 'alex@mail.ru', 25, 45000.75, 'IT', 'Москва'),
    ('Ольга Козлова', 'olga@mail.ru', 29, 55000.00, 'Marketing', 'Казань'),
    ('Дмитрий Новиков', 'dmitry@mail.ru', 35, 75000.25, 'Finance', 'Москва'),
    ('Екатерина Васнецова', 'ekaterina@mail.ru', 27, 48000.00, 'HR', 'СПб'),
    ('Сергей Орлов', 'sergey@mail.ru', 31, 62000.50, 'IT', 'Новосибирск'),
    ('Анна Жукова', 'anna@mail.ru', 26, 47000.00, 'Marketing', 'Москва')
]

cursor.executemany("""
INSERT INTO employees (name, email, age, salary, department, city) 
VALUES (%s, %s, %s, %s, %s, %s)
""", employees_data)

db.commit()
print(f"добавлено {cursor.rowcount} записей")

cursor.execute("SELECT * FROM employees")
result = cursor.fetchall()
print("все сотрудники:")
for row in result:
    print(row)

cursor.execute("UPDATE employees SET name = 'Петр Петров' WHERE name LIKE 'Иван%'")
db.commit()
print(f"обновлено: {cursor.rowcount}")

cursor.execute("SELECT * FROM employees")
print("после обновления:")
for row in cursor.fetchall():
    print(row)

cursor.execute("DELETE FROM employees WHERE name = 'Петр'")
db.commit()
print(f"удалено: {cursor.rowcount}")

cursor.execute("SELECT * FROM employees")
result = cursor.fetchall()

with open('employees_export.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow([i[0] for i in cursor.description])
    writer.writerows(result)
print("данные в employees_export.csv")

with open('employees_export.csv', 'r', encoding='utf-8') as file:
    reader = csv.reader(file)
    next(reader)
    for row in reader:
        cursor.execute("INSERT INTO employees (name, email, age, salary, department, city) VALUES (%s, %s, %s, %s, %s, %s)", row[1::])
db.commit()
print("данные из CSV")

cursor.execute("DROP TABLE IF EXISTS employees")
print("таблица удалена")

cursor.close()
db.close()
print("все ок")
