from PyQt5 import QtCore, QtGui, QtWidgets
import sqlite3


class Ui_User(object):

    # create private variable and get/set functions
    _UserID = 0
    _Access_areas = []

    def get_private_name(self):
        return Ui_User._UserID

    def get_private_areas(self):
        return Ui_User._Access_areas

    def show_private(self):
        self.User_name_Label.setText(Ui_User._UserID)

    #Get user private variables
    def set_private(self, val):
        Ui_User._UserID = val
        conn = sqlite3.connect("sqlite/application_database.db")
        cur = conn.cursor()
        with conn:
            cur.execute("SELECT ID_Xwrwn_Prosvasis FROM users_info WHERE Username=:usern", {'usern': val})
            result = cur.fetchone()
        Area_IDs = str(result[0]).split(',')
        for id in Area_IDs:
            Ui_User._Access_areas.append(id)


    #Show areas IDs on selected label func
    def show_areas(self):
        conn = sqlite3.connect("sqlite/application_database.db")
        cur = conn.cursor()
        username = self.get_private_name()
        areas_list = self.get_private_areas()
        area_names_list = []
        with conn:
            cur.execute("SELECT ID_Xwrwn_Prosvasis FROM users_info WHERE Username=:usern", {'usern': username})
            result = cur.fetchone()
        Local_Area_IDs = str(result[0]).split(',')
        for id in Local_Area_IDs:
            with conn:
                cur.execute("SELECT onoma_xwrou FROM xwroi_idrymatos WHERE ID_xwrou=:idx", {'idx': id})
                result2 = cur.fetchone()
                if result2 :
                    area_names_list.append(result2[0])
        if 'None' not in areas_list:
            text_string = ''
            for i in range(0,len(areas_list)):
                text_string +='ID :{}, Area : {}\n'.format(areas_list[i],area_names_list[i])
            self.access_ids_string_label.setText(text_string)
        else:
            self.access_ids_string_label.setText('No area rights')

    #Load equipment func
    def load_equipment_data(self):
        conn = sqlite3.connect("sqlite/application_database.db")
        cur = conn.cursor()
        areas_list = self.get_private_areas()
        with conn:
            self.equipment_table.setRowCount(0)
            for area in areas_list:
                result = cur.execute('SELECT * FROM yliko_xwrwn WHERE ID_Xwrou=:idx',{'idx':area})
                for row_number, row_data in enumerate(result):
                    self.equipment_table.insertRow(row_number)
                    for col_number, data in enumerate(row_data):
                        self.equipment_table.setItem(row_number, col_number, QtWidgets.QTableWidgetItem(str(data)))

        self.search_xwrou_input.setText('')
        self.search_ylikou_input.setText('')
        self.search_daneismou_input.setText('')
        self.search_keywords_input.setText('')
        self.search_katigoria_input.setText('')

    # Search for equipment/material function

    def search_for_equipment(self):
        areas_ids = self.get_private_areas()
        id_xwrou = self.search_xwrou_input.text()
        typos_ylikou = self.search_ylikou_input.text()
        katastasti_daneismou = self.search_daneismou_input.text()
        lekseis_kleidia = self.search_keywords_input.text()
        katigoria = self.search_katigoria_input.text()
        sql_where = ''
        katastasti_daneismou_choices = ['Available', 'Borrowed']

        if not (id_xwrou or typos_ylikou or katastasti_daneismou or lekseis_kleidia or katigoria):
            self.warning('Failure', 'Please provide at least one search parameter.')
        elif id_xwrou and (id_xwrou not in areas_ids):
            self.warning('Failure','You dont have the right access for that area\nor area doesnt exist.')
        elif katastasti_daneismou and katastasti_daneismou not in katastasti_daneismou_choices:
            self.warning('Failure', 'Loan status can either be Available or Borrowed.')
            self.load_equipment_data()
        else:
            if id_xwrou and (typos_ylikou or katastasti_daneismou or katigoria):
                sql_where += 'ID_Xwrou=:idx AND '
            elif id_xwrou:
                sql_where += 'ID_Xwrou=:idx'
            if typos_ylikou and (katastasti_daneismou or katigoria):
                sql_where += 'typos=:typ AND '
            elif typos_ylikou:
                sql_where += 'typos=:typ'
            if katastasti_daneismou and katigoria:
                sql_where += 'katastasi_daneismou=:katd AND '
            elif katastasti_daneismou:
                sql_where += 'katastasi_daneismou=:katd'
            if katigoria:
                sql_where += 'katigoria=:katg'

            if not lekseis_kleidia:
                # Dynamic Creation of SQL Query
                sql = 'SELECT * FROM yliko_xwrwn WHERE '
                sql += sql_where
                conn = sqlite3.connect("sqlite/application_database.db")
                cur = conn.cursor()
                with conn:
                    result = cur.execute(sql, {'idx': id_xwrou, 'typ': typos_ylikou, 'katd': katastasti_daneismou,
                                               'katg': katigoria})
                    self.equipment_table.setRowCount(0)
                    for row_number, row_data in enumerate(result):
                        self.equipment_table.insertRow(row_number)
                        for col_number, data in enumerate(row_data):
                            self.equipment_table.setItem(row_number, col_number, QtWidgets.QTableWidgetItem(str(data)))
                    if (self.equipment_table.rowCount()) > 0:
                        self.messagebox('Success', ' One or more items matching the description found!')
                        self.search_xwrou_input.setText('')
                        self.search_ylikou_input.setText('')
                        self.search_daneismou_input.setText('')
                        self.search_keywords_input.setText('')
                        self.search_katigoria_input.setText('')
                    else:
                        self.warning('No results', ' No items matching the description found!')
                        self.load_equipment_data()
            elif lekseis_kleidia and not (id_xwrou or typos_ylikou or katastasti_daneismou or katigoria):
                target_keywords = lekseis_kleidia.split(',')
                matching_items = []
                conn = sqlite3.connect("sqlite/application_database.db")
                cur = conn.cursor()

                with conn:
                    for id in areas_ids:
                        cur.execute("SELECT ID_ylikou,lekseis_kleidia FROM yliko_xwrwn WHERE ID_Xwrou={}".format(id))
                        keywords_per_id = cur.fetchall()

                        for item in keywords_per_id:
                            item_keywords = str(item[1]).split(',')
                            for word in item_keywords:
                                if word in target_keywords:
                                    matching_items.append(item[0])
                for item in matching_items:
                    if matching_items.count(item)>1:
                        matching_items.remove(item)
                items_count = len(matching_items)
                self.equipment_table.setRowCount(items_count)
                if items_count > 0:
                    for i in range(0, items_count):
                        for id in areas_ids:
                            cur.execute('SELECT * FROM yliko_xwrwn WHERE ID_ylikou={} AND ID_Xwrou={}'.format(matching_items[i]
                                                                                                              ,id))
                            match = cur.fetchone()
                            if match != None:
                                for x in range(0, len(match)):
                                    self.equipment_table.setItem(i, x, QtWidgets.QTableWidgetItem(str(match[x])))

                    self.messagebox('Success', ' One or more items matching the description found!')
                    self.search_xwrou_input.setText('')
                    self.search_ylikou_input.setText('')
                    self.search_daneismou_input.setText('')
                    self.search_keywords_input.setText('')
                    self.search_katigoria_input.setText('')
                else:
                    self.warning('Failure', ' No items matching the description found!')
                    self.load_equipment_data()

            elif lekseis_kleidia and (id_xwrou or typos_ylikou or katastasti_daneismou or katigoria):
                first_matching_items_ids = []
                second_matching_items_ids = []
                final_matching_items_ids = []
                target_keywords = lekseis_kleidia.split(',')

                # Dynamic Creation of SQL Query
                sql = 'SELECT * FROM yliko_xwrwn WHERE '
                sql += sql_where
                conn = sqlite3.connect("sqlite/application_database.db")
                cur = conn.cursor()
                with conn:
                    cur.execute(sql, {'idx': id_xwrou, 'typ': typos_ylikou, 'katd': katastasti_daneismou,
                                      'katg': katigoria})
                    first_matches = cur.fetchall()

                    for item in first_matches:
                        id = item[0]
                        first_matching_items_ids.append(id)

                    for id in areas_ids:
                        cur.execute("SELECT ID_ylikou,lekseis_kleidia FROM yliko_xwrwn WHERE ID_Xwrou={}".format(id))
                        keywords_per_id = cur.fetchall()

                        for item in keywords_per_id:
                            item_keywords = str(item[1]).split(',')
                            for word in item_keywords:
                                if word in target_keywords:
                                    second_matching_items_ids.append(item[0])

                    for item in first_matching_items_ids:
                        if item in second_matching_items_ids:
                            final_matching_items_ids.append(item)

                    items_count = len(final_matching_items_ids)
                    self.equipment_table.setRowCount(items_count)

                    if items_count > 0:
                        for i in range(0, items_count):
                            for id in areas_ids:
                                cur.execute('SELECT * FROM yliko_xwrwn WHERE ID_ylikou={} AND ID_Xwrou={}'.format(
                                   final_matching_items_ids[i], id))
                                match = cur.fetchone()
                                if match != None:
                                    for x in range(0, len(match)):
                                        self.equipment_table.setItem(i, x, QtWidgets.QTableWidgetItem(str(match[x])))

                        self.messagebox('Success', ' One or more items matching the description found!')
                        self.search_xwrou_input.setText('')
                        self.search_ylikou_input.setText('')
                        self.search_daneismou_input.setText('')
                        self.search_keywords_input.setText('')
                        self.search_katigoria_input.setText('')
                    else:
                        self.warning('Failure', ' No items matching the description found!')
                        self.load_equipment_data()

    # Create Success Messagebox

    def messagebox(self, title, message):
        mess = QtWidgets.QMessageBox()

        mess.setWindowTitle(title)
        mess.setText(message)
        mess.setStandardButtons(QtWidgets.QMessageBox.Ok)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("media/success.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        mess.setWindowIcon(icon)
        self.search_xwrou_input.setText('')
        self.search_ylikou_input.setText('')
        self.search_daneismou_input.setText('')
        self.search_keywords_input.setText('')
        self.search_katigoria_input.setText('')
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
        self.search_xwrou_input.setText('')
        self.search_ylikou_input.setText('')
        self.search_daneismou_input.setText('')
        self.search_keywords_input.setText('')
        self.search_katigoria_input.setText('')
        mess.exec_()

    def setupUi(self, User):
        User.setObjectName("User")
        User.resize(1120, 734)
        User.setMinimumSize(QtCore.QSize(1120, 734))
        User.setMaximumSize(QtCore.QSize(1120, 734))
        font = QtGui.QFont()
        font.setFamily("Myriad Pro Light")
        User.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("media/user.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        User.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(User)
        self.centralwidget.setObjectName("centralwidget")
        self.logged_in_as_label = QtWidgets.QLabel(self.centralwidget)
        self.logged_in_as_label.setGeometry(QtCore.QRect(650, 620, 121, 21))
        font = QtGui.QFont()
        font.setFamily("Myriad Pro Light")
        font.setPointSize(10)
        font.setBold(True)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(75)
        font.setStrikeOut(False)
        font.setKerning(False)
        self.logged_in_as_label.setFont(font)
        self.logged_in_as_label.setObjectName("logged_in_as_label")
        self.User_name_Label = QtWidgets.QLabel(self.centralwidget)
        self.User_name_Label.setGeometry(QtCore.QRect(800, 620, 251, 21))
        font = QtGui.QFont()
        font.setFamily("Myriad Pro Light")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.User_name_Label.setFont(font)
        self.User_name_Label.setText("")
        self.User_name_Label.setScaledContents(False)
        self.User_name_Label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.User_name_Label.setWordWrap(False)
        self.User_name_Label.setObjectName("User_name_Label")
        self.equipment_table = QtWidgets.QTableWidget(self.centralwidget)
        self.equipment_table.setEnabled(True)
        self.equipment_table.setGeometry(QtCore.QRect(0, 270, 1111, 301))
        self.equipment_table.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setFamily("Myriad Pro Light")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        font.setStrikeOut(False)
        font.setKerning(True)
        self.equipment_table.setFont(font)
        self.equipment_table.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.equipment_table.setTabletTracking(False)
        self.equipment_table.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.equipment_table.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.equipment_table.setAutoFillBackground(False)
        self.equipment_table.setFrameShape(QtWidgets.QFrame.Box)
        self.equipment_table.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.equipment_table.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.equipment_table.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.equipment_table.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.equipment_table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.equipment_table.setDefaultDropAction(QtCore.Qt.IgnoreAction)
        self.equipment_table.setAlternatingRowColors(False)
        self.equipment_table.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.equipment_table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.equipment_table.setShowGrid(True)
        self.equipment_table.setGridStyle(QtCore.Qt.DashLine)
        self.equipment_table.setWordWrap(False)
        self.equipment_table.setRowCount(10)
        self.equipment_table.setColumnCount(19)
        self.equipment_table.setObjectName("equipment_table")
        item = QtWidgets.QTableWidgetItem()
        self.equipment_table.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.equipment_table.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.equipment_table.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.equipment_table.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.equipment_table.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.equipment_table.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.equipment_table.setHorizontalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        self.equipment_table.setHorizontalHeaderItem(7, item)
        item = QtWidgets.QTableWidgetItem()
        self.equipment_table.setHorizontalHeaderItem(8, item)
        item = QtWidgets.QTableWidgetItem()
        self.equipment_table.setHorizontalHeaderItem(9, item)
        item = QtWidgets.QTableWidgetItem()
        self.equipment_table.setHorizontalHeaderItem(10, item)
        item = QtWidgets.QTableWidgetItem()
        self.equipment_table.setHorizontalHeaderItem(11, item)
        item = QtWidgets.QTableWidgetItem()
        self.equipment_table.setHorizontalHeaderItem(12, item)
        item = QtWidgets.QTableWidgetItem()
        self.equipment_table.setHorizontalHeaderItem(13, item)
        item = QtWidgets.QTableWidgetItem()
        self.equipment_table.setHorizontalHeaderItem(14, item)
        item = QtWidgets.QTableWidgetItem()
        self.equipment_table.setHorizontalHeaderItem(15, item)
        item = QtWidgets.QTableWidgetItem()
        self.equipment_table.setHorizontalHeaderItem(16, item)
        item = QtWidgets.QTableWidgetItem()
        self.equipment_table.setHorizontalHeaderItem(17, item)
        item = QtWidgets.QTableWidgetItem()
        self.equipment_table.setHorizontalHeaderItem(18, item)
        item = QtWidgets.QTableWidgetItem()
        self.equipment_table.setItem(0, 0, item)
        self.equipment_table.horizontalHeader().setCascadingSectionResizes(False)
        self.equipment_table.horizontalHeader().setMinimumSectionSize(39)
        self.equipment_table.verticalHeader().setStretchLastSection(False)
        self.search_label = QtWidgets.QLabel(self.centralwidget)
        self.search_label.setGeometry(QtCore.QRect(10, 10, 211, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setUnderline(False)
        font.setWeight(75)
        self.search_label.setFont(font)
        self.search_label.setObjectName("search_label")
        self.line_2 = QtWidgets.QFrame(self.centralwidget)
        self.line_2.setGeometry(QtCore.QRect(0, 30, 300, 16))
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.label_search_xwrou = QtWidgets.QLabel(self.centralwidget)
        self.label_search_xwrou.setGeometry(QtCore.QRect(10, 50, 91, 21))
        font = QtGui.QFont()
        font.setFamily("Myriad Pro Light")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.label_search_xwrou.setFont(font)
        self.label_search_xwrou.setObjectName("label_search_xwrou")
        self.label_search_yliko = QtWidgets.QLabel(self.centralwidget)
        self.label_search_yliko.setGeometry(QtCore.QRect(10, 80, 151, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_search_yliko.setFont(font)
        self.label_search_yliko.setObjectName("label_search_yliko")
        self.label_search_daneismos = QtWidgets.QLabel(self.centralwidget)
        self.label_search_daneismos.setGeometry(QtCore.QRect(10, 110, 241, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_search_daneismos.setFont(font)
        self.label_search_daneismos.setObjectName("label_search_daneismos")
        self.label_search_keywords = QtWidgets.QLabel(self.centralwidget)
        self.label_search_keywords.setGeometry(QtCore.QRect(10, 140, 301, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_search_keywords.setFont(font)
        self.label_search_keywords.setObjectName("label_search_keywords")
        self.label_search_katigoria_ylikou = QtWidgets.QLabel(self.centralwidget)
        self.label_search_katigoria_ylikou.setGeometry(QtCore.QRect(10, 170, 171, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_search_katigoria_ylikou.setFont(font)
        self.label_search_katigoria_ylikou.setObjectName("label_search_katigoria_ylikou")
        self.search_xwrou_input = QtWidgets.QLineEdit(self.centralwidget)
        self.search_xwrou_input.setGeometry(QtCore.QRect(370, 50, 113, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(8)
        font.setBold(False)
        font.setWeight(50)
        self.search_xwrou_input.setFont(font)
        self.search_xwrou_input.setText("")
        self.search_xwrou_input.setObjectName("search_xwrou_input")
        self.search_ylikou_input = QtWidgets.QLineEdit(self.centralwidget)
        self.search_ylikou_input.setGeometry(QtCore.QRect(370, 80, 113, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(8)
        font.setBold(False)
        font.setWeight(50)
        self.search_ylikou_input.setFont(font)
        self.search_ylikou_input.setText("")
        self.search_ylikou_input.setObjectName("search_ylikou_input")
        self.search_daneismou_input = QtWidgets.QLineEdit(self.centralwidget)
        self.search_daneismou_input.setGeometry(QtCore.QRect(370, 110, 113, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(8)
        font.setBold(False)
        font.setWeight(50)
        self.search_daneismou_input.setFont(font)
        self.search_daneismou_input.setObjectName("search_daneismou_input")
        self.search_keywords_input = QtWidgets.QLineEdit(self.centralwidget)
        self.search_keywords_input.setGeometry(QtCore.QRect(370, 140, 113, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(8)
        font.setBold(False)
        font.setWeight(50)
        self.search_keywords_input.setFont(font)
        self.search_keywords_input.setText("")
        self.search_keywords_input.setObjectName("search_keywords_input")
        self.search_katigoria_input = QtWidgets.QLineEdit(self.centralwidget)
        self.search_katigoria_input.setGeometry(QtCore.QRect(370, 170, 113, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(8)
        font.setBold(False)
        font.setWeight(50)
        self.search_katigoria_input.setFont(font)
        self.search_katigoria_input.setObjectName("search_katigoria_input")
        self.equipment_search_button = QtWidgets.QPushButton(self.centralwidget)
        self.equipment_search_button.setGeometry(QtCore.QRect(10, 210, 181, 31))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.equipment_search_button.setFont(font)
        self.equipment_search_button.setObjectName("equipment_search_button")
        self.equip_search_info_label = QtWidgets.QLabel(self.centralwidget)
        self.equip_search_info_label.setGeometry(QtCore.QRect(540, 70, 531, 16))
        font = QtGui.QFont()
        font.setFamily("Myriad Pro Light")
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.equip_search_info_label.setFont(font)
        self.equip_search_info_label.setObjectName("equip_search_info_label")
        self.equipment_search_button_2 = QtWidgets.QPushButton(self.centralwidget)
        self.equipment_search_button_2.setGeometry(QtCore.QRect(270, 210, 181, 31))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.equipment_search_button_2.setFont(font)
        self.equipment_search_button_2.setObjectName("equipment_search_button_2")
        self.search_access_ids_label = QtWidgets.QLabel(self.centralwidget)
        self.search_access_ids_label.setGeometry(QtCore.QRect(30, 620, 281, 21))
        font = QtGui.QFont()
        font.setFamily("Myriad Pro Light")
        font.setPointSize(10)
        font.setBold(True)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(75)
        font.setStrikeOut(False)
        font.setKerning(False)
        self.search_access_ids_label.setFont(font)
        self.search_access_ids_label.setObjectName("search_access_ids_label")
        self.access_ids_string_label = QtWidgets.QLabel(self.centralwidget)
        self.access_ids_string_label.setGeometry(QtCore.QRect(320, 560, 141,141))
        font = QtGui.QFont()
        font.setFamily("Myriad Pro Light")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.access_ids_string_label.setFont(font)
        self.access_ids_string_label.setText("")
        self.access_ids_string_label.setScaledContents(False)
        self.access_ids_string_label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.access_ids_string_label.setWordWrap(False)
        self.access_ids_string_label.setObjectName("access_ids_string_label")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(540, 160, 520, 51))
        font = QtGui.QFont()
        font.setFamily("Myriad Pro Light")
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setGeometry(QtCore.QRect(512, 120, 734, 3))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.line_3 = QtWidgets.QFrame(self.centralwidget)
        self.line_3.setGeometry(QtCore.QRect(503, 0, 20, 271))
        self.line_3.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        User.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(User)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1120, 20))
        self.menubar.setObjectName("menubar")
        User.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(User)
        self.statusbar.setObjectName("statusbar")
        User.setStatusBar(self.statusbar)

        self.retranslateUi(User)
        QtCore.QMetaObject.connectSlotsByName(User)

    def retranslateUi(self, User):
        _translate = QtCore.QCoreApplication.translate
        User.setWindowTitle(_translate("User", "User Access"))
        self.logged_in_as_label.setText(_translate("User", "Logged in as:"))
        item = self.equipment_table.horizontalHeaderItem(0)
        item.setText(_translate("Admin", "ID Υλικού"))
        item = self.equipment_table.horizontalHeaderItem(1)
        item.setText(_translate("Admin", "ID Χώρου Υλικού"))
        item = self.equipment_table.horizontalHeaderItem(2)
        item.setText(_translate("Admin", "Χαρακτηριστικά/Χρήση Υλικού"))
        item = self.equipment_table.horizontalHeaderItem(3)
        item.setText(_translate("Admin", "Τύπος Υλικού"))
        item = self.equipment_table.horizontalHeaderItem(4)
        item.setText(_translate("Admin", "Ποσότητα"))
        item = self.equipment_table.horizontalHeaderItem(5)
        item.setText(_translate("Admin", "Κατάσταση Υλικού"))
        item = self.equipment_table.horizontalHeaderItem(6)
        item.setText(_translate("Admin", "Εταιρία "))
        item = self.equipment_table.horizontalHeaderItem(7)
        item.setText(_translate("Admin", "Μοντέλο"))
        item = self.equipment_table.horizontalHeaderItem(8)
        item.setText(_translate("Admin", "Ακριβής Ονομασία"))
        item = self.equipment_table.horizontalHeaderItem(9)
        item.setText(_translate("Admin", "Χρόνος Κτήσης"))
        item = self.equipment_table.horizontalHeaderItem(10)
        item.setText(_translate("Admin", "Σειριακός Αριθμός"))
        item = self.equipment_table.horizontalHeaderItem(11)
        item.setText(_translate("Admin", "Σκοπός Χρήσης"))
        item = self.equipment_table.horizontalHeaderItem(12)
        item.setText(_translate("Admin", "Βάρος"))
        item = self.equipment_table.horizontalHeaderItem(13)
        item.setText(_translate("Admin", "Διαθεσιμότητα"))
        item = self.equipment_table.horizontalHeaderItem(14)
        item.setText(_translate("Admin", "Δ.Μετακίνησης"))
        item = self.equipment_table.horizontalHeaderItem(15)
        item.setText(_translate("Admin", "Κατάσταση Δανεισμού"))
        item = self.equipment_table.horizontalHeaderItem(16)
        item.setText(_translate("Admin", "Κατηγορία"))
        item = self.equipment_table.horizontalHeaderItem(17)
        # Set Columns Width
        self.equipment_table.setColumnWidth(0, 180)
        self.equipment_table.setColumnWidth(1, 180)
        self.equipment_table.setColumnWidth(2, 250)
        self.equipment_table.setColumnWidth(3, 180)
        self.equipment_table.setColumnWidth(4, 180)
        self.equipment_table.setColumnWidth(5, 180)
        self.equipment_table.setColumnWidth(6, 180)
        self.equipment_table.setColumnWidth(7, 180)
        self.equipment_table.setColumnWidth(8, 180)
        self.equipment_table.setColumnWidth(9, 180)
        self.equipment_table.setColumnWidth(10, 180)
        self.equipment_table.setColumnWidth(11, 180)
        self.equipment_table.setColumnWidth(12, 180)
        self.equipment_table.setColumnWidth(13, 180)
        self.equipment_table.setColumnWidth(14, 180)
        self.equipment_table.setColumnWidth(15, 180)
        self.equipment_table.setColumnWidth(16, 180)
        self.equipment_table.setColumnWidth(17, 180)
        self.equipment_table.setColumnWidth(18, 180)
        item.setText(_translate("Admin", "Υποκατηγορία"))
        item = self.equipment_table.horizontalHeaderItem(18)
        item.setText(_translate("Admin", "Λέξεις Κλειδιά"))
        __sortingEnabled = self.equipment_table.isSortingEnabled()
        self.equipment_table.setSortingEnabled(False)
        self.equipment_table.setSortingEnabled(__sortingEnabled)
        self.equipment_table.setSortingEnabled(False)
        self.equipment_table.setSortingEnabled(__sortingEnabled)
        self.search_label.setText(_translate("User", "Αναζήτηση Υλικών"))
        self.label_search_xwrou.setText(_translate("User", "Χώρος :"))
        self.label_search_yliko.setText(_translate("User", "Τύπος Υλικού :"))
        self.label_search_daneismos.setText(_translate("User", "Κατάσταση Δανεισμού :"))
        self.label_search_keywords.setText(_translate("User", "Λέξεις Κλειδιά(χωρίστε με κόμμα) :"))
        self.label_search_katigoria_ylikou.setText(_translate("User", "Κατηγορία Υλικού :"))
        self.equipment_search_button.setText(_translate("User", "Αναζήτηση Υλικού"))
        self.equipment_search_button.clicked.connect(self.search_for_equipment)
        self.equipment_search_button_2.clicked.connect(self.load_equipment_data)
        self.equip_search_info_label.setText(_translate("User", "Για αναζήτηση εισάγετε κάποια πληροφορία στα δίπλα πλαίσια."))
        self.equipment_search_button_2.setText(_translate("User", "Επαναφόρτωση"))
        self.search_access_ids_label.setText(_translate("User", "Χώροι Πρόσβασης:"))
        self.label.setText(_translate("User", "Ως απλός χρήστης έχετε πρόσβαση μόνο σε λειτουργία αναζήτησης,\nσύμφωνα "
"με τα δικαιώματα χώρων που σας έχουν δωθεί."))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    User = QtWidgets.QMainWindow()
    ui = Ui_User()
    ui.setupUi(User)
    User.show()
    sys.exit(app.exec_())
