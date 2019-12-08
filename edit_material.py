from PyQt5 import QtCore, QtGui, QtWidgets
import sqlite3

class Ui_edit_material(object):

    _Material_ID = None

    def setprivates(self, item):
        Ui_edit_material._Material_ID = item

    def returnmatid(self):
        return self._Material_ID

    # Create Success Messagebox

    def messagebox(self, title, message):
        mess = QtWidgets.QMessageBox()
        mess.setWindowTitle(title)
        mess.setText(message)
        mess.setStandardButtons(QtWidgets.QMessageBox.Ok)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("media/success.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        mess.setWindowIcon(icon)
        mess.exec_()

    # Create Warning Messagebox

    def warning(self, title, message):
        mess = QtWidgets.QMessageBox()
        mess.setWindowTitle(title)
        mess.setText(message)
        mess.setStandardButtons(QtWidgets.QMessageBox.Ok)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("media/failure.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        mess.setWindowIcon(icon)
        mess.exec_()

    #Add clear fields function

    def clear_function(self):
        self.lineEdit_material.setText('')
        self.lineEdit_3_material.setText('')
        self.lineEdit_4_material.setText('')
        self.lineEdit_5_material.setText('')
        self.lineEdit_6_material.setText('')
        self.lineEdit_7_material.setText('')
        self.lineEdit_8_material.setText('')
        self.lineEdit_2_material.setText('')


    #Update material function

    def update_material(self):

        xaraktiristika = self.lineEdit_material.text()
        posotita = self.lineEdit_2_material.text()
        katastasi = self.lineEdit_3_material.text()
        etairia = self.lineEdit_4_material.text()
        montelo = self.lineEdit_5_material.text()
        lekseis_kleidia = self.lineEdit_6_material.text()
        katigoria = self.lineEdit_7_material.text()
        ypokatigoria = self.lineEdit_8_material.text()
        material_id = self.returnmatid()

        if (xaraktiristika and posotita and katastasi and etairia and montelo and lekseis_kleidia):

            if ypokatigoria and not katigoria:
                ypokatigoria = None
            if not katigoria:
                katigoria = None
            if not ypokatigoria:
                ypokatigoria = None

            conn = sqlite3.connect("sqlite/application_database.db")
            cur = conn.cursor()
            with conn:
                result = cur.execute("""UPDATE yliko_xwrwn SET perigrafi_xrisis='{}',posotita='{}',katastasi='{}',
                                        etairia='{}',montelo='{}',lekseis_kleidia='{}',katigoria='{}',ypokatigoria='{}'
                                        WHERE  ID_ylikou='{}'""".format(xaraktiristika,posotita,katastasi,etairia,
                                                                        montelo,lekseis_kleidia,katigoria,ypokatigoria,
                                                                        material_id))
                self.clear_function()
                self.messagebox('Success', 'Material with ID={} successfully updated!'.format(self._Material_ID))

        else:
            self.warning('Failure', 'Empty fields,please insert all required information.')

    def load_item_data(self):

        ID_Ylikou = self.returnmatid()

        conn = sqlite3.connect("sqlite/application_database.db")
        cur = conn.cursor()

        with conn:
            cur.execute("SELECT perigrafi_xrisis FROM yliko_xwrwn WHERE ID_ylikou='{}'".format(ID_Ylikou))
            result = cur.fetchone()
            result = result[0]
            self.lineEdit_material.setText(result)

            cur.execute("SELECT posotita FROM yliko_xwrwn WHERE ID_ylikou='{}'".format(ID_Ylikou))
            result = cur.fetchone()
            result = result[0]
            self.lineEdit_2_material.setText(result)

            cur.execute("SELECT katastasi FROM yliko_xwrwn WHERE ID_ylikou='{}'".format(ID_Ylikou))
            result = cur.fetchone()
            result = result[0]
            self.lineEdit_3_material.setText(result)

            cur.execute("SELECT etairia FROM yliko_xwrwn WHERE ID_ylikou='{}'".format(ID_Ylikou))
            result = cur.fetchone()
            result = result[0]
            self.lineEdit_4_material.setText(result)

            cur.execute("SELECT montelo FROM yliko_xwrwn WHERE ID_ylikou='{}'".format(ID_Ylikou))
            result = cur.fetchone()
            result = result[0]
            self.lineEdit_5_material.setText(result)

            cur.execute("SELECT lekseis_kleidia FROM yliko_xwrwn WHERE ID_ylikou='{}'".format(ID_Ylikou))
            result = cur.fetchone()
            result = result[0]
            self.lineEdit_6_material.setText(result)

            cur.execute("SELECT katigoria FROM yliko_xwrwn WHERE ID_ylikou='{}'".format(ID_Ylikou))
            result = cur.fetchone()
            result = result[0]
            self.lineEdit_7_material.setText(result)

            cur.execute("SELECT ypokatigoria FROM yliko_xwrwn WHERE ID_ylikou='{}'".format(ID_Ylikou))
            result = cur.fetchone()
            result = result[0]
            self.lineEdit_8_material.setText(result)


    def setupUi(self, edit_material):
        edit_material.setObjectName("edit_material")
        edit_material.resize(650, 680)
        edit_material.setMinimumSize(QtCore.QSize(650, 680))
        edit_material.setMaximumSize(QtCore.QSize(650, 680))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("media/gear.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        edit_material.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(edit_material)
        self.centralwidget.setObjectName("centralwidget")
        self.update_material_button = QtWidgets.QPushButton(self.centralwidget)
        self.update_material_button.setGeometry(QtCore.QRect(120, 535, 150, 31))
        font = QtGui.QFont()
        font.setFamily("Sitka")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.update_material_button.setFont(font)
        self.update_material_button.setObjectName("update_material_button")
        self.update_material_button.clicked.connect(self.update_material)
        self.clear_material_fields = QtWidgets.QPushButton(self.centralwidget)
        self.clear_material_fields.setGeometry(QtCore.QRect(400, 535, 150, 31))
        font = QtGui.QFont()
        font.setFamily("Sitka")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.clear_material_fields.setFont(font)
        self.clear_material_fields.setObjectName("clear_material_fields")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.clear_material_fields.clicked.connect(self.clear_function)
        self.label.setGeometry(QtCore.QRect(40, 10, 361, 16))
        font = QtGui.QFont()
        font.setFamily("Lucida Calligraphy")
        font.setPointSize(8)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.lineEdit_material = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_material.setGeometry(QtCore.QRect(400, 120, 180, 20))
        self.lineEdit_material.setObjectName("lineEdit_material")
        self.lineEdit_2_material = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_2_material.setGeometry(QtCore.QRect(400, 170, 180, 20))
        self.lineEdit_2_material.setObjectName("lineEdit_2_material")
        self.lineEdit_3_material = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_3_material.setGeometry(QtCore.QRect(400, 220, 180, 20))
        self.lineEdit_3_material.setObjectName("lineEdit_3_material")
        self.lineEdit_4_material = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_4_material.setGeometry(QtCore.QRect(400, 270, 180, 20))
        self.lineEdit_4_material.setObjectName("lineEdit_4_material")
        self.lineEdit_5_material = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_5_material.setGeometry(QtCore.QRect(400, 320, 180, 20))
        self.lineEdit_5_material.setObjectName("lineEdit_5_material")
        self.label_material_xaraktiristika = QtWidgets.QLabel(self.centralwidget)
        self.label_material_xaraktiristika.setGeometry(QtCore.QRect(40, 120, 350, 21))
        font = QtGui.QFont()
        font.setFamily("Sitka Text")
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.label_material_xaraktiristika.setFont(font)
        self.label_material_xaraktiristika.setObjectName("label_material_xaraktiristika")
        self.label_material_xaraktiristika_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_material_xaraktiristika_2.setGeometry(QtCore.QRect(40, 170, 350, 21))
        font = QtGui.QFont()
        font.setFamily("Sitka Text")
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.label_material_xaraktiristika_2.setFont(font)
        self.label_material_xaraktiristika_2.setObjectName("label_material_xaraktiristika_2")
        self.label_material_xaraktiristika_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_material_xaraktiristika_3.setGeometry(QtCore.QRect(40, 220, 350, 21))
        font = QtGui.QFont()
        font.setFamily("Sitka Text")
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.label_material_xaraktiristika_3.setFont(font)
        self.label_material_xaraktiristika_3.setObjectName("label_material_xaraktiristika_3")
        self.label_material_xaraktiristika_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_material_xaraktiristika_4.setGeometry(QtCore.QRect(40, 270, 350, 21))
        font = QtGui.QFont()
        font.setFamily("Sitka Text")
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.label_material_xaraktiristika_4.setFont(font)
        self.label_material_xaraktiristika_4.setObjectName("label_material_xaraktiristika_4")
        self.label_material_xaraktiristika_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_material_xaraktiristika_5.setGeometry(QtCore.QRect(40, 320, 350, 21))
        font = QtGui.QFont()
        font.setFamily("Sitka Text")
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.label_material_xaraktiristika_5.setFont(font)
        self.label_material_xaraktiristika_5.setObjectName("label_material_xaraktiristika_5")
        self.label_material_xaraktiristika_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_material_xaraktiristika_6.setGeometry(QtCore.QRect(40, 370, 350, 21))
        font = QtGui.QFont()
        font.setFamily("Sitka Text")
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.label_material_xaraktiristika_6.setFont(font)
        self.label_material_xaraktiristika_6.setObjectName("label_material_xaraktiristika_6")
        self.lineEdit_6_material = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_6_material.setGeometry(QtCore.QRect(400, 370, 180, 20))
        self.lineEdit_6_material.setObjectName("lineEdit_6_material")
        self.label_material_xaraktiristika_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_material_xaraktiristika_7.setGeometry(QtCore.QRect(40, 420, 350, 21))
        font = QtGui.QFont()
        font.setFamily("Sitka Text")
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.label_material_xaraktiristika_7.setFont(font)
        self.label_material_xaraktiristika_7.setObjectName("label_material_xaraktiristika_7")
        self.label_material_xaraktiristika_8 = QtWidgets.QLabel(self.centralwidget)
        self.label_material_xaraktiristika_8.setGeometry(QtCore.QRect(40, 470, 350, 21))
        font = QtGui.QFont()
        font.setFamily("Sitka Text")
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.label_material_xaraktiristika_8.setFont(font)
        self.label_material_xaraktiristika_8.setObjectName("label_material_xaraktiristika_8")
        self.lineEdit_7_material = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_7_material.setGeometry(QtCore.QRect(400, 420, 180, 20))
        self.lineEdit_7_material.setObjectName("lineEdit_7_material")
        self.lineEdit_8_material = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_8_material.setGeometry(QtCore.QRect(400, 470, 180, 20))
        self.lineEdit_8_material.setObjectName("lineEdit_8_material")
        edit_material.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(edit_material)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 650, 21))
        self.menubar.setObjectName("menubar")
        edit_material.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(edit_material)
        self.statusbar.setObjectName("statusbar")
        edit_material.setStatusBar(self.statusbar)

        self.retranslateUi(edit_material)
        QtCore.QMetaObject.connectSlotsByName(edit_material)

    def retranslateUi(self, edit_material):
        _translate = QtCore.QCoreApplication.translate
        edit_material.setWindowTitle(_translate("edit_material", "Επεξεργασία Υλικού"))
        self.update_material_button.setText(_translate("edit_material", "Επεξεργασία Υλικού"))
        self.clear_material_fields.setText(_translate("edit_material", "Καθαρισμός "))
        self.label.setText(_translate("edit_material", "Συμπληρώστε τα στοίχεια για επεξεργασία υλικού."))
        self.label_material_xaraktiristika.setText(_translate("edit_material", "Βασικά Χαρακτηριστικά :"))
        self.label_material_xaraktiristika_2.setText(_translate("edit_material", "Ποσότητα Ομοίων Αντικειμένων :"))
        self.label_material_xaraktiristika_3.setText(_translate("edit_material", "Κατάσταση :"))
        self.label_material_xaraktiristika_4.setText(_translate("edit_material", "Εταιρία :"))
        self.label_material_xaraktiristika_5.setText(_translate("edit_material", "Μοντέλο :"))
        self.label_material_xaraktiristika_6.setText(_translate("edit_material", "Λέξεις Κλειδιά(Χωρίστε με κόμμα):"))
        self.label_material_xaraktiristika_7.setText(_translate("edit_material", "Κατηγορία:"))
        self.label_material_xaraktiristika_8.setText(_translate("edit_material", "Υποκατηγορία:"))




if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    edit_material = QtWidgets.QMainWindow()
    ui = Ui_edit_material()
    ui.setupUi(edit_material)
    edit_material.show()
    sys.exit(app.exec_())
