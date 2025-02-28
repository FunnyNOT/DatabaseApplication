from PyQt5 import QtCore, QtGui, QtWidgets
import sqlite3


class Ui_add_equipment(object):
    _AreaID = None
    _Equip_Type = None

    def setprivates(self,area,type):
        Ui_add_equipment._AreaID=area
        Ui_add_equipment._Equip_Type=type

    def returnarea(self):
        return self._AreaID

    def returntype(self):
        return self._Equip_Type

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

    #Create Clear fields Function

    def clear_function(self):
        self.lineEdit_equipment.setText('')
        self.lineEdit_equipment_2.setText('')
        self.lineEdit_equipment_3.setText('')
        self.lineEdit_equipment_4.setText('')
        self.lineEdit_equipment_5.setText('')
        self.lineEdit_equipment_6.setText('')
        self.lineEdit_equipment_7.setText('')
        self.lineEdit_equipment_8.setText('')
        self.lineEdit_equipment_9.setText('')
        self.lineEdit_equipment_10.setText('')
        self.lineEdit_equipment_11.setText('')
        self.lineEdit_equipment_12.setText('')
        self.lineEdit_equipment_13.setText('')
        self.lineEdit_equipment_14.setText('')

    #Insert Equipment function

    def insert_equipment(self):
        Id_xwrou = self.returnarea()
        type = self.returntype()
        onomasia = self.lineEdit_equipment.text()
        montelo = self.lineEdit_equipment_2.text()
        xaraktiristika = self.lineEdit_equipment_3.text()
        xronos_ktisis = self.lineEdit_equipment_4.text()
        serialno = self.lineEdit_equipment_5.text()
        use_reason = self.lineEdit_equipment_6.text()
        posotita = self.lineEdit_equipment_7.text()
        katastasi = self.lineEdit_equipment_8.text()
        varos = self.lineEdit_equipment_9.text()
        diathesimotita = self.lineEdit_equipment_10.text()
        lekseis_kleidia = self.lineEdit_equipment_11.text()
        katigoria = self.lineEdit_equipment_12.text()
        ypokatigoria = self.lineEdit_equipment_13.text()
        dinatotita_metak = self.lineEdit_equipment_14.text()


        if (onomasia and montelo and xaraktiristika and xronos_ktisis and serialno and use_reason and posotita
            and katastasi and varos and diathesimotita and lekseis_kleidia and dinatotita_metak and Id_xwrou and type):

            if not katigoria:
                katigoria = None
            if not ypokatigoria:
                ypokatigoria = None
            if ypokatigoria and not katigoria:
                ypokatigoria = None

            conn = sqlite3.connect("sqlite/application_database.db")
            cur = conn.cursor()
            with conn:
                result = cur.execute("""INSERT INTO yliko_xwrwn('ID_Xwrou','perigrafi_xrisis','posotita','katastasi',
                                                    'onomasia_organou','montelo','lekseis_kleidia','katigoria','ypokatigoria' ,'typos'
                                                    ,'xronos_ktisis','seiriakos_arithmos','varos','diathesimotita','dinatotita_metakinisis'
                                                    ,'skopos_xrisis') 
                                                    VALUES('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')
                                                    """.format(Id_xwrou, xaraktiristika, posotita, katastasi,onomasia,
                                                               montelo, lekseis_kleidia, katigoria, ypokatigoria,type,
                                                               xronos_ktisis,serialno,varos,diathesimotita,dinatotita_metak
                                                               ,use_reason))

                self.clear_function()
                self.messagebox('Success', 'Equipment successfully added to area with ID={}'.format(self._AreaID))

        else:
            self.warning('Failure', 'Empty fields,please insert all required information.')




    def setupUi(self, add_equipment):
        add_equipment.setObjectName("add_equipment")
        add_equipment.resize(650, 680)
        add_equipment.setMinimumSize(QtCore.QSize(650, 680))
        add_equipment.setMaximumSize(QtCore.QSize(650, 680))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("media/gear.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        add_equipment.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(add_equipment)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(40, 10, 361, 16))
        font = QtGui.QFont()
        font.setFamily("Lucida Calligraphy")
        font.setPointSize(8)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_equipment_ = QtWidgets.QLabel(self.centralwidget)
        self.label_equipment_.setGeometry(QtCore.QRect(40, 50, 350, 21))
        font = QtGui.QFont()
        font.setFamily("Sitka Text")
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.label_equipment_.setFont(font)
        self.label_equipment_.setObjectName("label_equipment_")
        self.label_equipment_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_equipment_2.setGeometry(QtCore.QRect(40, 80, 350, 21))
        font = QtGui.QFont()
        font.setFamily("Sitka Text")
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.label_equipment_2.setFont(font)
        self.label_equipment_2.setObjectName("label_equipment_2")
        self.label_equipment_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_equipment_3.setGeometry(QtCore.QRect(40, 110, 350, 21))
        font = QtGui.QFont()
        font.setFamily("Sitka Text")
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.label_equipment_3.setFont(font)
        self.label_equipment_3.setObjectName("label_equipment_3")
        self.label_equipment_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_equipment_4.setGeometry(QtCore.QRect(40, 140, 350, 21))
        font = QtGui.QFont()
        font.setFamily("Sitka Text")
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.label_equipment_4.setFont(font)
        self.label_equipment_4.setObjectName("label_equipment_4")
        self.label_equipment_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_equipment_5.setGeometry(QtCore.QRect(40, 170, 350, 21))
        font = QtGui.QFont()
        font.setFamily("Sitka Text")
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.label_equipment_5.setFont(font)
        self.label_equipment_5.setObjectName("label_equipment_5")
        self.label_equipment_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_equipment_6.setGeometry(QtCore.QRect(40, 200, 350, 21))
        font = QtGui.QFont()
        font.setFamily("Sitka Text")
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.label_equipment_6.setFont(font)
        self.label_equipment_6.setObjectName("label_equipment_6")
        self.label_equipment_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_equipment_7.setGeometry(QtCore.QRect(40, 230, 350, 21))
        font = QtGui.QFont()
        font.setFamily("Sitka Text")
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.label_equipment_7.setFont(font)
        self.label_equipment_7.setObjectName("label_equipment_7")
        self.label_equipment_8 = QtWidgets.QLabel(self.centralwidget)
        self.label_equipment_8.setGeometry(QtCore.QRect(40, 260, 350, 21))
        font = QtGui.QFont()
        font.setFamily("Sitka Text")
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.label_equipment_8.setFont(font)
        self.label_equipment_8.setObjectName("label_equipment_8")
        self.label_equipment_9 = QtWidgets.QLabel(self.centralwidget)
        self.label_equipment_9.setGeometry(QtCore.QRect(40, 290, 350, 21))
        font = QtGui.QFont()
        font.setFamily("Sitka Text")
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.label_equipment_9.setFont(font)
        self.label_equipment_9.setObjectName("label_equipment_9")
        self.label_equipment_10 = QtWidgets.QLabel(self.centralwidget)
        self.label_equipment_10.setGeometry(QtCore.QRect(40, 320, 350, 21))
        font = QtGui.QFont()
        font.setFamily("Sitka Text")
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.label_equipment_10.setFont(font)
        self.label_equipment_10.setObjectName("label_equipment_10")
        self.label_equipment_11 = QtWidgets.QLabel(self.centralwidget)
        self.label_equipment_11.setGeometry(QtCore.QRect(40, 350, 350, 21))
        font = QtGui.QFont()
        font.setFamily("Sitka Text")
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.label_equipment_11.setFont(font)
        self.label_equipment_11.setObjectName("label_equipment_11")
        self.label_equipment_12 = QtWidgets.QLabel(self.centralwidget)
        self.label_equipment_12.setGeometry(QtCore.QRect(40, 380, 350, 21))
        font = QtGui.QFont()
        font.setFamily("Sitka Text")
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.label_equipment_12.setFont(font)
        self.label_equipment_12.setObjectName("label_equipment_12")
        self.label_equipment_13 = QtWidgets.QLabel(self.centralwidget)
        self.label_equipment_13.setGeometry(QtCore.QRect(40, 410, 350, 21))
        font = QtGui.QFont()
        font.setFamily("Sitka Text")
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.label_equipment_13.setFont(font)
        self.label_equipment_13.setObjectName("label_equipment_13")
        self.label_equipment_14 = QtWidgets.QLabel(self.centralwidget)
        self.label_equipment_14.setGeometry(QtCore.QRect(40, 440, 350, 21))
        font = QtGui.QFont()
        font.setFamily("Sitka Text")
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.label_equipment_14.setFont(font)
        self.label_equipment_14.setObjectName("label_equipment_14")
        self.insert_equipment_button = QtWidgets.QPushButton(self.centralwidget)
        self.insert_equipment_button.setGeometry(QtCore.QRect(100, 535, 180, 31))
        #Link insert equipment button to function
        self.insert_equipment_button.clicked.connect(self.insert_equipment)
        font = QtGui.QFont()
        font.setFamily("Sitka")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.insert_equipment_button.setFont(font)
        self.insert_equipment_button.setObjectName("insert_equipment_button")
        self.clear_equipment_fields = QtWidgets.QPushButton(self.centralwidget)
        self.clear_equipment_fields.setGeometry(QtCore.QRect(400, 535, 180, 31))
        font = QtGui.QFont()
        font.setFamily("Sitka")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.clear_equipment_fields.setFont(font)
        self.clear_equipment_fields.setObjectName("clear_equipment_fields")
        # Link clear button to function
        self.clear_equipment_fields.clicked.connect(self.clear_function)
        self.lineEdit_equipment = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_equipment.setGeometry(QtCore.QRect(400, 50, 180, 20))
        self.lineEdit_equipment.setObjectName("lineEdit_equipment")
        self.lineEdit_equipment_2 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_equipment_2.setGeometry(QtCore.QRect(400, 80, 180, 20))
        self.lineEdit_equipment_2.setObjectName("lineEdit_equipment_2")
        self.lineEdit_equipment_3 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_equipment_3.setGeometry(QtCore.QRect(400, 110, 180, 20))
        self.lineEdit_equipment_3.setObjectName("lineEdit_equipment_3")
        self.lineEdit_equipment_4 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_equipment_4.setGeometry(QtCore.QRect(400, 140, 180, 20))
        self.lineEdit_equipment_4.setObjectName("lineEdit_equipment_4")
        self.lineEdit_equipment_5 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_equipment_5.setGeometry(QtCore.QRect(400, 170, 180, 20))
        self.lineEdit_equipment_5.setObjectName("lineEdit_equipment_5")
        self.lineEdit_equipment_6 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_equipment_6.setGeometry(QtCore.QRect(400, 200, 180, 20))
        self.lineEdit_equipment_6.setObjectName("lineEdit_equipment_6")
        self.lineEdit_equipment_7 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_equipment_7.setGeometry(QtCore.QRect(400, 230, 180, 20))
        self.lineEdit_equipment_7.setObjectName("lineEdit_equipment_7")
        self.lineEdit_equipment_8 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_equipment_8.setGeometry(QtCore.QRect(400, 260, 180, 20))
        self.lineEdit_equipment_8.setObjectName("lineEdit_equipment_8")
        self.lineEdit_equipment_9 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_equipment_9.setGeometry(QtCore.QRect(400, 290, 180, 20))
        self.lineEdit_equipment_9.setObjectName("lineEdit_equipment_9")
        self.lineEdit_equipment_10 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_equipment_10.setGeometry(QtCore.QRect(400, 320, 180, 20))
        self.lineEdit_equipment_10.setObjectName("lineEdit_equipment_10")
        self.lineEdit_equipment_11 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_equipment_11.setGeometry(QtCore.QRect(400, 350, 180, 20))
        self.lineEdit_equipment_11.setObjectName("lineEdit_equipment_11")
        self.lineEdit_equipment_12 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_equipment_12.setGeometry(QtCore.QRect(400, 380, 180, 20))
        self.lineEdit_equipment_12.setObjectName("lineEdit_equipment_12")
        self.lineEdit_equipment_13 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_equipment_13.setGeometry(QtCore.QRect(400, 410, 180, 20))
        self.lineEdit_equipment_13.setObjectName("lineEdit_equipment_13")
        self.lineEdit_equipment_14 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_equipment_14.setGeometry(QtCore.QRect(400, 440, 180, 20))
        self.lineEdit_equipment_14.setObjectName("lineEdit_equipment_14")
        add_equipment.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(add_equipment)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 650, 21))
        self.menubar.setObjectName("menubar")
        add_equipment.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(add_equipment)
        self.statusbar.setObjectName("statusbar")
        add_equipment.setStatusBar(self.statusbar)

        self.retranslateUi(add_equipment)
        QtCore.QMetaObject.connectSlotsByName(add_equipment)

    def retranslateUi(self, add_equipment):
        _translate = QtCore.QCoreApplication.translate
        add_equipment.setWindowTitle(_translate("add_equipment", "Προσθήκη Εργαστηριακού Εξοπλισμού"))
        self.label.setText(_translate("add_equipment", "Συμπληρώστε τα στοίχεια για εισαγωγή εξοπλισμού."))
        self.label_equipment_.setText(_translate("add_equipment", "Ακριβής Ονομασία:"))
        self.label_equipment_2.setText(_translate("add_equipment", "Μοντέλο:"))
        self.label_equipment_3.setText(_translate("add_equipment", "Βασικά Χαρακτηριστικά :"))
        self.label_equipment_4.setText(_translate("add_equipment", "Χρόνος Κτήσης:"))
        self.label_equipment_5.setText(_translate("add_equipment", "Σειριακός Αριθμός:"))
        self.label_equipment_6.setText(_translate("add_equipment", "Σκοπός Χρήσης:"))
        self.label_equipment_7.setText(_translate("add_equipment", "Ποσότητα:"))
        self.label_equipment_8.setText(_translate("add_equipment", "Κατάσταση:"))
        self.label_equipment_9.setText(_translate("add_equipment", "Βάρος:"))
        self.label_equipment_10.setText(_translate("add_equipment", "Διαθεσιμότητα:"))
        self.label_equipment_11.setText(_translate("add_equipment", "Λέξεις Κλεδιά(Χωρίστε με κόμμα):"))
        self.label_equipment_12.setText(_translate("add_equipment", "Κατηγορία:"))
        self.label_equipment_13.setText(_translate("add_equipment", "Υποκατηγορία:"))
        self.label_equipment_14.setText(_translate("add_equipment", "Δυνατότητα Μετακίνησης:"))
        self.insert_equipment_button.setText(_translate("add_equipment", "Προσθήκη Εξοπλισμού"))
        self.clear_equipment_fields.setText(_translate("add_equipment", "Καθαρισμός "))




if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    add_equipment = QtWidgets.QMainWindow()
    ui = Ui_add_equipment()
    ui.setupUi(add_equipment)
    add_equipment.show()
    sys.exit(app.exec_())
