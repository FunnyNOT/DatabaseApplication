from PyQt5 import QtCore, QtGui, QtWidgets
import sqlite3

class Ui_loan_window(object):
    _ID_ylikou = 0


    def setprivates(self,id):
        self._ID_ylikou = id

    def return_priv(self):
        return self._ID_ylikou

    def cancel_loan(self):
        id_ylikou = self.return_priv()
        load_cancel = 'Available'

        conn = sqlite3.connect("sqlite/application_database.db")
        cur = conn.cursor()

        with conn:
            cur.execute("DELETE FROM daneismos WHERE ID_ylikou='{}'".format(id_ylikou))
            print(2)
            cur.execute("UPDATE yliko_xwrwn SET katastasi_daneismou='{}' WHERE ID_ylikou='{}'".format(load_cancel,id_ylikou))
            self.messagebox('Success','Item is now available for loan.')


    def loan_eq(self):
        id_ylikou = self.return_priv()
        borrow_str = 'Borrowed'


        conn = sqlite3.connect("sqlite/application_database.db")
        cur = conn.cursor()

        with conn:
            cur.execute("SELECT katastasi_daneismou FROM yliko_xwrwn WHERE ID_Ylikou={}".format(id_ylikou))
            status = cur.fetchone()
            status = status[0]

        if status == 'Available':
            onoma_xristi = str(self.lineEdit_onoma.text())
            epitheto_xristi = str(self.lineEdit_epitheto.text())

            conn = sqlite3.connect("sqlite/application_database.db")
            cur = conn.cursor()

            with conn:
                cur.execute("SELECT * FROM users_info WHERE First_Name='{}' AND Last_Name='{}'".format(onoma_xristi,epitheto_xristi))
            if len(cur.fetchall()) > 0:
                with conn:
                    cur.execute("""INSERT INTO daneismos('ID_ylikou','onoma_xristi','epitheto_xristi') 
                                                       VALUES ('{}','{}','{}')""".format(id_ylikou, onoma_xristi, epitheto_xristi))
                    cur.execute("UPDATE yliko_xwrwn SET katastasi_daneismou='{}' WHERE ID_ylikou='{}'".format(borrow_str,id_ylikou))
                    self.messagebox('Success','Item succesfully loaned.')
                    self.lineEdit_epitheto.setText('')
                    self.lineEdit_onoma.setText('')
            else:
                self.warning('Failure','Failed to loan item.')
                self.lineEdit_epitheto.setText('')
                self.lineEdit_onoma.setText('')

        else:
            with conn:
                cur.execute("SELECT onoma_xristi,epitheto_xristi FROM daneismos WHERE ID_ylikou={}".format(id_ylikou))
                result = cur.fetchone()
            self.warning('Failure', 'Item already borrowed , cancel current loan first.\n'
                                    'Loaned to User: {} {}'.format(result[0],result[1]))
            self.lineEdit_epitheto.setText('')
            self.lineEdit_onoma.setText('')


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

    def setupUi(self, loan_window):
        loan_window.setObjectName("loan_window")
        loan_window.resize(698, 472)
        loan_window.setMinimumSize(QtCore.QSize(698, 472))
        loan_window.setMaximumSize(QtCore.QSize(698, 472))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("media/gear.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        loan_window.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(loan_window)
        self.centralwidget.setObjectName("centralwidget")
        self.loan_button = QtWidgets.QPushButton(self.centralwidget)
        self.loan_button.setGeometry(QtCore.QRect(100, 310, 151, 31))
        font = QtGui.QFont()
        font.setFamily("Sitka Display")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.loan_button.setFont(font)
        self.loan_button.setObjectName("loan_button")
        self.loan_button.clicked.connect(self.loan_eq)
        self.cancel_loan_button = QtWidgets.QPushButton(self.centralwidget)
        self.cancel_loan_button.setGeometry(QtCore.QRect(400, 310, 170, 31))
        self.cancel_loan_button.clicked.connect(self.cancel_loan)
        font = QtGui.QFont()
        font.setFamily("Sitka Display")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.cancel_loan_button.setFont(font)
        self.cancel_loan_button.setObjectName("cancel_loan_button")
        self.name_label = QtWidgets.QLabel(self.centralwidget)
        self.name_label.setGeometry(QtCore.QRect(120, 110, 151, 31))
        font = QtGui.QFont()
        font.setFamily("Sitka")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.name_label.setFont(font)
        self.name_label.setObjectName("name_label")
        self.lineEdit_onoma = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_onoma.setGeometry(QtCore.QRect(300, 110, 161, 20))
        self.lineEdit_onoma.setObjectName("lineEdit_onoma")
        self.lineEdit_epitheto = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_epitheto.setGeometry(QtCore.QRect(300, 190, 161, 20))
        self.lineEdit_epitheto.setObjectName("lineEdit_epitheto")
        self.last_name_label = QtWidgets.QLabel(self.centralwidget)
        self.last_name_label.setGeometry(QtCore.QRect(120, 190, 151, 21))
        font = QtGui.QFont()
        font.setFamily("Sitka")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.last_name_label.setFont(font)
        self.last_name_label.setObjectName("last_name_label")
        self.loan_label = QtWidgets.QLabel(self.centralwidget)
        self.loan_label.setGeometry(QtCore.QRect(10, 20, 570, 25))
        font = QtGui.QFont()
        font.setFamily("Sitka Heading")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.loan_label.setFont(font)
        self.loan_label.setObjectName("loan_label")
        loan_window.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(loan_window)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 698, 21))
        self.menubar.setObjectName("menubar")
        loan_window.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(loan_window)
        self.statusbar.setObjectName("statusbar")
        loan_window.setStatusBar(self.statusbar)

        self.retranslateUi(loan_window)
        QtCore.QMetaObject.connectSlotsByName(loan_window)

    def retranslateUi(self, loan_window):
        _translate = QtCore.QCoreApplication.translate
        loan_window.setWindowTitle(_translate("loan_window", "Δανεισμός Εξοπλισμού"))
        self.loan_button.setText(_translate("loan_window", "Δανεισμός Υλικού"))
        self.cancel_loan_button.setText(_translate("loan_window", "Ακύρωση Δανεισμού"))
        self.name_label.setText(_translate("loan_window", "Όνομα χρήστη :"))
        self.last_name_label.setText(_translate("loan_window", "Επίθετο  :"))
        self.loan_label.setText(_translate("loan_window", "Εισάγετε στοιχεία για δανεισμό υλικού ή τερματίστε δανεισμό υλικού."))




if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    loan_window = QtWidgets.QMainWindow()
    ui = Ui_loan_window()
    ui.setupUi(loan_window)
    loan_window.show()
    sys.exit(app.exec_())
