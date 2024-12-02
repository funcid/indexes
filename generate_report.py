from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER

def generate_documentation():
    # Регистрация шрифта для поддержки русского языка
    # Замените путь на актуальный путь к шрифту Arial на вашем компьютере
    pdfmetrics.registerFont(TTFont('Arial', 'C:\\Windows\\Fonts\\arial.ttf'))
    
    # Создание документа
    doc = SimpleDocTemplate(
        "travel_database_documentation.pdf",
        pagesize=A4,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=72
    )
    
    # Стили
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(
        name='CustomBody',
        fontName='Arial',
        fontSize=12,
        leading=14,
        alignment=TA_JUSTIFY
    ))
    styles.add(ParagraphStyle(
        name='CustomHeading',
        fontName='Arial',
        fontSize=16,
        leading=20,
        alignment=TA_LEFT,
        spaceAfter=30
    ))
    
    # Содержимое документа
    content = []
    
    # Заголовок
    content.append(Paragraph("Документация по системе управления путевками", styles['CustomHeading']))
    content.append(Spacer(1, 12))
    
    # Описание системы
    system_description = """
    Данная система представляет собой программное решение для управления базой данных путевок с использованием 
    типизированного файла и индексного массива. Система обеспечивает эффективное хранение и поиск информации 
    о туристических путевках.
    """
    content.append(Paragraph(system_description, styles['CustomBody']))
    content.append(Spacer(1, 12))
    
    # Структура данных
    content.append(Paragraph("Структура данных", styles['CustomHeading']))
    data_structure = """
    1. Класс TravelPackage (Путевка):
       - package_id: уникальный идентификатор путевки
       - destination: место назначения
       - hotel_name: название отеля
       - start_date: дата начала
       - duration: продолжительность в днях
       - price: стоимость
    
    2. Класс IndexRecord (Индексная запись):
       - key: ключ (номер путевки)
       - position: позиция записи в файле
    """
    content.append(Paragraph(data_structure, styles['CustomBody']))
    content.append(Spacer(1, 12))
    
    # Принцип работы
    content.append(Paragraph("Принцип работы", styles['CustomHeading']))
    working_principle = """
    1. Хранение данных:
       - Все записи о путевках хранятся в типизированном файле
       - Каждая запись сериализуется с помощью модуля pickle
       - Индексный массив хранится в оперативной памяти
    
    2. Добавление данных:
       - Новая запись добавляется в конец файла
       - В индексный массив добавляется новая запись с позицией в файле
       - Индексный массив поддерживается в отсортированном состоянии
    
    3. Поиск данных:
       - Реализовано два метода поиска:
         а) Индексный поиск (бинарный поиск по индексному массиву)
         б) Последовательный поиск (прямой поиск в файле)
    """
    content.append(Paragraph(working_principle, styles['CustomBody']))
    content.append(Spacer(1, 12))
    
    # Преимущества системы
    content.append(Paragraph("Преимущества системы", styles['CustomHeading']))
    advantages = """
    1. Эффективность поиска:
       - Бинарный поиск по индексному массиву имеет сложность O(log n)
       - Значительное превосходство в скорости над последовательным поиском
    
    2. Экономия памяти:
       - Индексный массив хранит только ключи и позиции
       - Полные данные хранятся только в файле
    
    3. Надежность:
       - Все данные сохраняются на диске
       - Индексный массив может быть легко восстановлен
    """
    content.append(Paragraph(advantages, styles['CustomBody']))
    
    # Сборка документа
    doc.build(content)

if __name__ == "__main__":
    generate_documentation() 