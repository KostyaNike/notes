from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QListWidget, QHBoxLayout,\
    QVBoxLayout, QLineEdit, QTextEdit, QInputDialog # Імпортування віджетів для того щоб код працював.
import json # Імпортування 'json'

app = QApplication([])# створення додатку


# '''Замітки в json'''
# notes = {
#     "Ласкаво просимо!": {
#         "текст": "Це найкращий додаток для заміток у світі!",
#         "теги": ["добро", "інструкція"]
#     }
# }
# with open("notes_data.json", "w") as file: # записуємо замітки в json
#     json.dump(notes, file)


window = QWidget()# створення вікна додатку
window.resize(900, 600)# розмір вікна
window.setWindowTitle("Notes")# заголовок вікна
'''ІНТЕРФЕЙС ПРОГРАМИ'''
text_field = QTextEdit()# велике поля для вводу

list_notes = QListWidget()# список заміток
list_notes_label = QLabel("Список заміток")
# кнопки для дій з замітками
btn_create_note = QPushButton("Створити замітку")
btn_del_note = QPushButton("Видалити замітку")
btn_save_note = QPushButton("Зберегти замітку")

list_tags = QListWidget()# список тегів
list_tags_label = QLabel("Список тегів")
# кнопки для дій з тегами
btn_add_tag = QPushButton("Додати до замітки")
btn_del_tag = QPushButton("Відкріпити від замітки")
btn_search_note = QPushButton("Шукати замітки по тегу")

input_tag = QLineEdit()# поле для вводу тегу
input_tag.setPlaceholderText("Введіть тег.......")

col1 = QVBoxLayout()
col1.addWidget(text_field)

col2 = QVBoxLayout()
col2.addWidget(list_notes_label)
col2.addWidget(list_notes)

row1 = QHBoxLayout()
row1.addWidget(btn_create_note)
row1.addWidget(btn_del_note)

row2 = QHBoxLayout()
row2.addWidget(btn_save_note)

col2.addLayout(row1)
col2.addLayout(row2)
col2.addWidget(list_tags_label)
col2.addWidget(list_tags)
col2.addWidget(input_tag)

row3 = QHBoxLayout()
row3.addWidget(btn_add_tag)
row3.addWidget(btn_del_tag)

row4 = QHBoxLayout()
row4.addWidget(btn_search_note)

col2.addLayout(row3)
col2.addLayout(row4)

layout_notes = QHBoxLayout()
layout_notes.addLayout(col1, stretch=5)
layout_notes.addLayout(col2, stretch=4)

window.setLayout(layout_notes)
'''ФУНКЦІОНАЛ ПРОГРАМИ'''

'''РОБОТА З ТЕКСТОМ ЗАМІТКИ'''
def show_note():
    key = list_notes.selectedItems()[0].text()
    text_field.clear()
    text_field.setText(notes[key]['текст'])
    list_tags.clear()
    list_tags.addItems(notes[key]['теги'])

# Функція для додавання нової замітки.
def add_note():
    note_name, ok = QInputDialog.getText(window, 'Додати замітку', 'Назва замітки:')
    if note_name and ok != '':
        notes[note_name] = {'текст': '', 'теги': []}
        list_notes.addItem(note_name)
        list_tags.addItems(notes[note_name]['теги'])

# Функція для видалення замітки.
def del_note():
    if list_notes.selectedItems()[0].text():
        key = list_notes.selectedItems()[0].text()
        del notes[key]
        text_field.clear()
        list_notes.clear()
        list_tags.clear()
        list_notes.addItems(notes)
        with open('notes_data.json', 'w') as file:
            json.dump(notes, file, sort_keys=True)

# Функція для збереження замітки.
def save_note():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        notes[key]['текст'] = text_field.toPlainText()
        with open('notes_data.json', 'w') as file:
            json.dump(notes, file, sort_keys=True)

def del_tag(): # Функція видалення тегу
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        tag = list_tags.selectedItems()[0].text()
        notes[key]['теги'].remove(tag)
        list_tags.clear()
        list_tags.addItems(notes[key]['теги'])
        with open('notes_data.json', 'w') as file:
            json.dump(notes, file, sort_keys=True)

def add_tag(): # Функція додавання тегу
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        if input_tag.text():
            tag = input_tag.text()
            if not tag in notes[key]['теги']:
                notes[key]['теги'].append(tag)
                list_tags.addItem(tag)
                input_tag.clear()
                with open('notes_data.json', 'w') as file:
                    json.dump(notes, file, sort_keys=True)



def search_note(): # Функція пошуку тегу
    if input_tag.text() and btn_search_note.text() == 'Шукати замітки по тегу':
        tag = input_tag.text()
        notes_filtered = {}
        for note in notes:
            if tag in notes[note]['теги']:
                notes_filtered[note] = notes[note]
        btn_search_note.setText('Cкинути пошук')
        list_notes.clear()
        list_tags.clear()
        list_notes.addItems(notes_filtered)
    elif input_tag.text() and btn_search_note.text() == 'Cкинути пошук':
        input_tag.clear()
        list_tags.clear()
        list_notes.clear()
        list_notes.addItems(notes)
        btn_search_note.setText('Шукати замітки по тегу')


btn_del_tag.clicked.connect(del_tag) # Здібність кнопки видалення тегу працювати.
btn_add_tag.clicked.connect(add_tag) # Здібність кнопки додавання тегу працювати.
btn_search_note.clicked.connect(search_note) # Здібність кнопки пошуку тегу працювати.

btn_del_note.clicked.connect(del_note) # Здібність кнопки видалення замітки працювати.
btn_save_note.clicked.connect(save_note) # Здібність кнопки збереження замітки працювати.
btn_create_note.clicked.connect(add_note) # Здібність кнопки створення замітки працювати.

list_notes.itemClicked.connect(show_note)

with open('notes_data.json', 'r') as file:
    notes = json.load(file)
list_notes.addItems(notes)
    
window.show() # Команда для відображення вікна.

app.exec_()


