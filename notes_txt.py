#начни тут создавать приложение с умными заметками
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QWidget,QHBoxLayout, QVBoxLayout,QGroupBox, QRadioButton,QPushButton, QLabel, QButtonGroup, QListWidget, QLineEdit, QTextEdit, QInputDialog)
import json

def save_note_to_file():
    with open('notes_data.json','w',encoding='utf-8') as file:
        json.dump(notes, file,sort_keys=True, ensure_ascii=False )

app = QApplication([])



notes_win = QWidget()
notes_win.setWindowTitle('Умные заметки')
notes_win.resize(900,600)

list_notes = QListWidget()
list_notes_label = QLabel('Список заметок')
btn_note_create = QPushButton('Создать заметку')
btn_note_del = QPushButton('Удалить заметку')
btn_note_save = QPushButton('Сохранить заметку')

field_tag = QLineEdit()
field_tag.setPlaceholderText('Введите тег ...')
field_text = QTextEdit()

btn_tag_create = QPushButton('Добавить к заметке')
btn_tag_del = QPushButton('Открепить от заметки')
btn_tag_find = QPushButton('Искать заметки по тегу')
list_tags = QListWidget()
list_tags_labels = QLabel('Список тегов')

layout_notes = QHBoxLayout()
col_1 = QVBoxLayout()
col_1.addWidget(field_text)

col_2 = QVBoxLayout()
col_2.addWidget(list_notes_label)
col_2.addWidget(list_notes)
row_1 = QHBoxLayout()
row_1.addWidget(btn_note_create)
row_1.addWidget(btn_note_del)

row_2 = QHBoxLayout()
row_2.addWidget(btn_note_save)
col_2.addLayout(row_1)
col_2.addLayout(row_2)

col_2.addWidget(list_tags_labels)
col_2.addWidget(list_tags)
col_2.addWidget(field_tag)

row_3 = QHBoxLayout()
row_3.addWidget(btn_tag_create)
row_3.addWidget(btn_tag_del)
row_4 = QHBoxLayout()
row_4.addWidget(btn_tag_find)

col_2.addLayout(row_3)
col_2.addLayout(row_4)

layout_notes.addLayout(col_1)
layout_notes.addLayout(col_2)
notes_win.setLayout(layout_notes)

def show_note():
    key = list_notes.selectedItems()[0].text()
    field_text.setText(notes[key]['текст'])
    list_tags.clear()
    list_tags.addItems(notes[key]['теги'])

def add_tag():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        tag = field_tag.text()

        if not tag in notes[key]['теги']:
            notes[key]['теги'].append(tag)
            list_tags.addItem(tag)
            field_tag.clear()

        with open('notes_data.json','w',encoding='utf-8') as file:
            json.dump(notes, file,sort_keys=True, ensure_ascii=False )

def del_tag():
    if list_tags.selectedItems():
        key = list_notes.selectedItems()[0].text()
        tag = list_tags.selectedItems()[0].text()
        notes[key]['теги'].remove(tag)
        list_tags.clear()

        list_tags.addItems(notes[key]['теги'])

        save_note_to_file()


    with open('notes_data.json','w',encoding='utf-8') as file:
        json.dump(notes, file,sort_keys=True, ensure_ascii=False )


def search_tag():
    tag = field_tag.text()
    if btn_tag_find.text() == 'Искать заметки по тегу' and tag:
        notes_filter = {}
        for name_note in notes:
            if tag in notes[name_note]['теги']:
                notes_filter[name_note] = notes[name_note]

        list_notes.clear()
        list_tags.clear()
        list_notes.addItems(notes_filter)

        btn_tag_find.setText('Сбросить фильтрацию по тегу')

with open('notes_data.json','r',encoding='utf-8' ) as file:  
    notes = json.load(file)





def save_note():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        notes[key]['текст'] = field_text.toPlainText()

        with open('notes_data.json','w',encoding='utf-8') as file:
            json.dump(notes, file,sort_keys=True,ensure_ascii=False )



def add_note():
    note_name, ok = QInputDialog.getText(notes_win, 'Добавить заметку','Название заметки:')
    notes[note_name] = {'текст':'','теги':[]}
    list_notes.addItem(note_name)
    list_tags.addItems(notes[note_name]['теги'])

def del_note():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        del notes[key]
        list_notes.clear
        list_tags.clear()
        field_text.clear()

        list_notes.addItems(notes)

        with open('notes_data.json','w',encoding='utf-8') as file:
            json.dump(notes, file,sort_keys=True,ensure_ascii=False )


with open('notes_data.json','r',encoding='utf-8' ) as file:  
    notes = json.load(file)

list_notes.addItems(notes)

list_notes.itemClicked.connect(show_note)
btn_note_create.clicked.connect(add_note)
btn_note_del.clicked.connect(del_note)
btn_note_save.clicked.connect(save_note)
btn_tag_create.clicked.connect(add_tag)
btn_tag_del.clicked.connect(del_tag)
btn_tag_find.clicked.connect(search_tag)

notes_win.show()
app.exec_()