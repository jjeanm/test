from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QListWidget, QLineEdit, QTextEdit, QInputDialog, QHBoxLayout, QVBoxLayout, QFormLayout

# Membuat aplikasi
app = QApplication([])
notes = []  # Daftar catatan

# Mengatur parameter window aplikasi
notes_win = QWidget()
notes_win.setWindowTitle('Smart Notes')  # Judul window
notes_win.resize(900, 600)  # Ukuran window

# Widget di dalam window aplikasi
list_notes = QListWidget()  
list_notes_label = QLabel('List of notes')  

button_note_create = QPushButton('Create note')  
button_note_del = QPushButton('Delete note')  
button_note_save = QPushButton('Save note') 

# Input untuk tag dan teks catatan
field_tag = QLineEdit('')
field_tag.setPlaceholderText('Enter tag...')  
field_text = QTextEdit()

# Tombol untuk mengelola tag
button_tag_add = QPushButton('Add to note')  
button_tag_del = QPushButton('Unpin from note')  
button_tag_search = QPushButton('Search notes by tag')  
list_tags = QListWidget()  
list_tags_label = QLabel('List of tags')  

# Pengaturan tata letak widget menggunakan layout
layout_notes = QHBoxLayout()

# Kolom 1: Area teks catatan
col_1 = QVBoxLayout()
col_1.addWidget(field_text)

# Kolom 2: Daftar catatan dan pengelolaan tag
col_2 = QVBoxLayout()
col_2.addWidget(list_notes_label)
col_2.addWidget(list_notes)

# Baris 1: Tombol buat dan hapus catatan
row_1 = QHBoxLayout()
row_1.addWidget(button_note_create)
row_1.addWidget(button_note_del)

# Baris 2: Tombol simpan catatan
row_2 = QHBoxLayout()
row_2.addWidget(button_note_save)

# Menambahkan baris-baris ke dalam kolom 2
col_2.addLayout(row_1)
col_2.addLayout(row_2)

# Menambahkan daftar tag dan input tag ke kolom 2
col_2.addWidget(list_tags_label)
col_2.addWidget(list_tags)
col_2.addWidget(field_tag)

# Baris 3: Tombol untuk menambah dan menghapus tag
row_3 = QHBoxLayout()
row_3.addWidget(button_tag_add)
row_3.addWidget(button_tag_del)

# Baris 4: Tombol untuk mencari catatan berdasarkan tag
row_4 = QHBoxLayout()
row_4.addWidget(button_tag_search)

# Menambahkan baris 3 dan 4 ke kolom 2
col_2.addLayout(row_3)
col_2.addLayout(row_4)

# Menggabungkan kolom 1 dan kolom 2 ke dalam layout utama
layout_notes.addLayout(col_1, stretch=2)
layout_notes.addLayout(col_2, stretch=1)

# Menetapkan layout ke window aplikasi
notes_win.setLayout(layout_notes)

# Fungsionalitas Aplikasi
def show_note():
    # Menampilkan catatan yang dipilih dari daftar
    key = list_notes.selectedItems()[0].text()
    print(key)
    for note in notes:
        if note[0] == key:
            field_text.setText(note[1])
            list_tags.clear()
            list_tags.addItems(note[2])

def add_note():
    # Menambahkan catatan baru
    note_name, ok = QInputDialog.getText(notes_win, "Add note", "Note name: ")
    if ok and note_name != "":
        note = [note_name, '', []]  # [Nama catatan, Isi catatan, Daftar tag]
        notes.append(note)
        list_notes.addItem(note[0])
        list_tags.addItems(note[2])
        print(notes)
        with open(str(len(notes)-1)+".txt", "w") as file:
            file.write(note[0] + '\n')

def save_note():
    # Menyimpan catatan yang dipilih
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        index = 0
        for note in notes:
            if note[0] == key:
                note[1] = field_text.toPlainText()  # Menyimpan isi teks catatan
                with open(str(index)+".txt", "w") as file:
                    file.write(note[0] + '\n')  # Menyimpan nama catatan
                    file.write(note[1] + '\n')  # Menyimpan isi catatan
                    for tag in note[2]:
                        file.write(tag + ' ')  # Menyimpan tag catatan
                    file.write('\n')
            index += 1
        print(notes)
    else:
        print("Note to save is not selected!")  # Jika tidak ada catatan yang dipilih

# Penanganan event
list_notes.itemClicked.connect(show_note)  # Menampilkan catatan saat dipilih
button_note_create.clicked.connect(add_note)  # Menambah catatan saat tombol ditekan
button_note_save.clicked.connect(save_note)  # Menyimpan catatan saat tombol ditekan

# Memulai aplikasi
notes_win.show()

# Inisialisasi catatan dari file
name = 0
note = []
while True:
    filename = str(name) + ".txt"
    try:
        with open(filename, "r", encoding='utf-8') as file:
            for line in file:
                line = line.replace('\n', '')
                note.append(line)
        tags = note[2].split(' ')  # Memisahkan tag yang tersimpan
        note[2] = tags

        notes.append(note)
        note = []
        name += 1
    except IOError:
        break

# Menampilkan semua catatan yang sudah dimuat
print(notes)
for note in notes:
    list_notes.addItem(note[0])

# Menjalankan aplikasi
app.exec_()
