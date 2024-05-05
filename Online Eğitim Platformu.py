import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget, QLineEdit, QMessageBox, QListWidget, QListWidgetItem, QDialog, QDialogButtonBox
from PyQt6.QtCore import Qt


class AnaPencere(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Online Eğitim Platformu")
        self.setGeometry(200, 200, 400, 300)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.label = QLabel("Dersler")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setStyleSheet("font-size: 18px; font-weight: bold;")
        self.layout.addWidget(self.label)

        self.dersler = ["Bilgisayar Ağları", "Yapay Zeka", "Veri Yapıları", "Mobil Programlama", "Web Geliştirme"]
        self.butonlar = []

        for ders in self.dersler:
            buton = QPushButton(ders)
            buton.setStyleSheet("QPushButton { padding: 10px; font-size: 16px; } QPushButton:hover { background-color: #f0f0f0; }")
            buton.clicked.connect(lambda checked, ders=ders: self.kayit_ol(ders))
            self.butonlar.append(buton)
            self.layout.addWidget(buton)

        self.kayitlar = []

        self.kayitlar_pencere = None

        self.menu_bar = self.menuBar()
        self.kayitlar_menu = self.menu_bar.addMenu("Kayıtlar")
        self.goster_kayitlar_action = self.kayitlar_menu.addAction("Kayıtları Göster")
        self.goster_kayitlar_action.triggered.connect(self.goster_kayitlar)

    def goster_kayitlar(self):
        if not self.kayitlar_pencere:
            self.kayitlar_pencere = KayitlarPencere(self.kayitlar)
        self.kayitlar_pencere.update_kayitlar(self.kayitlar)  # Kayıtları güncellemek için yeni bir metot kullan
        self.kayitlar_pencere.show()

    def kayit_ol(self, ders):
        if len(self.kayitlar) >= 5:
            QMessageBox.warning(self, "Kontenjan Dolu", "Üzgünüz, bu dersin kontenjanı dolmuştur.")
            return

        dialog = KayitDialog(self)
        if dialog.exec():
            isim = dialog.isim.text()
            soyisim = dialog.soyisim.text()
            tel = dialog.tel.text()
            email = dialog.email.text()

            self.kayitlar.append({"Ders": ders, "İsim": isim, "Soyisim": soyisim, "Tel": tel, "Email": email})
            self.goster_kayitlar()  # Kayıt işlemi tamamlandığında kayıtları göstermek için fonksiyonu çağır

class KayitDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Kayıt Formu")
        self.setFixedSize(300, 200)

        layout = QVBoxLayout(self)

        self.isim = QLineEdit(self)
        self.isim.setPlaceholderText("İsim")
        layout.addWidget(self.isim)

        self.soyisim = QLineEdit(self)
        self.soyisim.setPlaceholderText("Soyisim")
        layout.addWidget(self.soyisim)

        self.tel = QLineEdit(self)
        self.tel.setPlaceholderText("Telefon")
        layout.addWidget(self.tel)

        self.email = QLineEdit(self)
        self.email.setPlaceholderText("Email")
        layout.addWidget(self.email)

        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel, parent=self)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

class KayitlarPencere(QMainWindow):
    def __init__(self, kayitlar):
        super().__init__()

        self.setWindowTitle("Kayıtlar")
        self.setGeometry(200, 200, 400, 300)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.label = QLabel("Kayıtlar")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setStyleSheet("font-size: 18px; font-weight: bold;")
        self.layout.addWidget(self.label)

        self.list_widget = QListWidget()
        self.layout.addWidget(self.list_widget)

        self.update_kayitlar(kayitlar)

        # itemClicked sinyalini show_details metoduna bağla
        self.list_widget.itemClicked.connect(self.show_details)

    def update_kayitlar(self, kayitlar):
        self.list_widget.clear()
        for kayit in kayitlar:
            item = QListWidgetItem(f"{kayit['İsim']} {kayit['Soyisim']} - {kayit['Ders']}")
            item.setData(Qt.ItemDataRole.UserRole, kayit)  # Özel veriyi item'a ekle
            self.list_widget.addItem(item)

    def show_details(self, item):
        # Item'dan özel veriyi al
        kayit = item.data(Qt.ItemDataRole.UserRole)
        QMessageBox.information(self, "Kayıt Detayları", f"İsim: {kayit['İsim']}\nSoyisim: {kayit['Soyisim']}\nTelefon: {kayit['Tel']}\nEmail: {kayit['Email']}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    pencere = AnaPencere()
    pencere.show()
    sys.exit(app.exec())
