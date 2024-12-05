from flask import Flask, render_template, request, redirect, url_for
import os

# Инициализация приложения Flask
app = Flask(__name__)

# Имя файла для хранения данных
DATA_FILE = 'grades.txt'

# Загрузка данных из файла при запуске приложения
try:
    with open(DATA_FILE, 'r') as file:
        data = file.read().splitlines()
except FileNotFoundError:
    data = []

# Преобразование строк данных в словарь
students = {}
for line in data:
    parts = line.split(',')
    if len(parts) >= 2:
        student_name = parts[0]
        grades = parts[1:]
        students[student_name] = dict(zip(['Математика', 'Информатика', 'Программирование', 'ИСиТ'], grades))

# Список предметов
subjects = ['Математика', 'Информатика', 'Программирование', 'ИСиТ']

@app.route('/')
def index():
    """Отображение главной страницы"""
    return render_template('index.html', students=students, subjects=subjects)

@app.route('/add_mark', methods=['POST'])
def add_mark():
    """Обработка добавления новой оценки"""
    student_name = request.form['student_name']
    subject = request.form['subject']
    mark = request.form['mark']
    
    if student_name not in students:
        students[student_name] = {subj: '' for subj in subjects}
    
    students[student_name][subject] = mark
    
    # Сохраняем изменения в файл
    lines = []
    for student, grades in students.items():
        grade_values = [str(grades[subj]) for subj in subjects]
        lines.append(f"{student},{','.join(grade_values)}")
    
    with open(DATA_FILE, 'w') as file:
        file.write('\n'.join(lines))
    
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)