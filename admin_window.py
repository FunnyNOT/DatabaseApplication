from PyQt5 import QtCore, QtGui, QtWidgets
import re
import sqlite3
from add_material import Ui_add_material
from add_equipment import Ui_add_equipment
from edit_material import Ui_edit_material
from edit_equipment import Ui_edit_equipment
from loan_equip import Ui_loan_window

class Ui_Admin(object):

    # create private variable and get/set functions
    _UserID = 0

    def get_private(self):
        return Ui_Admin._UserID

    def print_private(self):
        self.User_name_Label.setText(Ui_Admin._UserID)

    def set_private(self, val):
        Ui_Admin._UserID = val

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

    # Load users_info table from SQlite Database into the UI TableWidget
    def load_users_Data(self):
        conn = sqlite3.connect("sqlite/application_database.db")
        query = 'SELECT * FROM users_info'
        result = conn.execute(query)

        self.user_table.setRowCount(0)

        for row_number, row_data in enumerate(result):
            self.user_table.insertRow(row_number)
            for col_number, data in enumerate(row_data):
                self.user_table.setItem(row_number, col_number, QtWidgets.QTableWidgetItem(str(data)))
        conn.close()

    # Load xwroi_idrymatos table from SQlite Database into the Ui TableWidget
    def load_areas_Data(self):
        conn = sqlite3.connect("sqlite/application_database.db")
        query = 'SELECT * FROM xwroi_idrymatos'
        with conn:
            result = conn.execute(query)

        self.areas_table.setRowCount(0)

        for row_number, row_data in enumerate(result):
            self.areas_table.insertRow(row_number)
            for col_number, data in enumerate(row_data):
                self.areas_table.setItem(row_number, col_number, QtWidgets.QTableWidgetItem(str(data)))

    def load_supervisor_Data(self):
        conn = sqlite3.connect("sqlite/application_database.db")
        query = """SELECT ID,First_Name,Last_Name,Email FROM users_info WHERE ID_Xwrwn_Prosvasis IS NOT NULL 
                   AND Access_Level>=1"""
        with conn:
            result = conn.execute(query)

        self.area_supervisor_table.setRowCount(0)

        for row_number, row_data in enumerate(result):
            self.area_supervisor_table.insertRow(row_number)
            for col_number, data in enumerate(row_data):
                self.area_supervisor_table.setItem(row_number, col_number, QtWidgets.QTableWidgetItem(str(data)))


    # User Search button onclick Function to locate specific user
    def search_for_user(self):
        required_fields = 2
        fields_counter = 0
        user_fname = self.usersearch_onoma_input.text()
        user_lname = self.usersearch_epitheto_input.text()
        user_phone = self.usersearch_tilefono_input.text()
        user_email = self.usersearch_email_input.text()
        user_access_areas = self.usersearch_id_xwrwn_input.text()
        sql_where = ''

        if (user_fname):
            fields_counter += 1
            sql_where = 'First_Name=:fname '
        if (user_lname and user_fname):
            fields_counter += 1
            sql_where += 'AND Last_Name=:lname '
        elif (user_lname):
            fields_counter += 1
            sql_where += 'Last_Name=:lname '
        if (user_phone and (user_fname or user_lname)):
            fields_counter += 1
            sql_where += 'AND Phone_Number=:phone '
        elif (user_phone):
            fields_counter += 1
            sql_where += 'Phone_Number=:phone '
        if (user_email and (user_fname or user_lname or user_phone)):
            fields_counter += 1
            sql_where += 'AND Email=:mail '
        elif (user_email):
            fields_counter += 1
            sql_where += 'Email=:mail '
        if (user_access_areas and (user_fname or user_lname or user_phone or user_email)):
            fields_counter += 1
            sql_where += 'AND ID_Xwrwn_Prosvasis=:IDXwrwn'

        # Dynamic Creation of SQL Query
        sql = 'SELECT * FROM users_info WHERE '
        sql += sql_where
        if fields_counter >= required_fields:
            conn = sqlite3.connect("sqlite/application_database.db")
            cur = conn.cursor()

            with conn:
                result = cur.execute(sql,
                                     {'fname': user_fname, 'lname': user_lname, 'phone': user_phone, 'mail': user_email,
                                      'IDXwrwn': user_access_areas})
                self.user_table.setRowCount(0)
                for row_number, row_data in enumerate(result):
                    self.user_table.insertRow(row_number)
                    for col_number, data in enumerate(row_data):
                        self.user_table.setItem(row_number, col_number, QtWidgets.QTableWidgetItem(str(data)))
                if (self.user_table.rowCount()) > 0:
                    self.messagebox('Success', ' One or more users matching the description found!')
                else:
                    self.warning('No results', ' No users matching the description found!')

        else:
            self.warning("Failed to Search", "Please provide more information: Insufficient input data.")
            self.usersearch_onoma_input.setText('')
            self.usersearch_epitheto_input.setText('')
            self.usersearch_tilefono_input.setText('')
            self.usersearch_email_input.setText('')
            self.usersearch_id_xwrwn_input.setText('')

    # Reset tablewidget after Search/Load Full Database users_info table data
    def clear_Search_user(self):
        conn = sqlite3.connect("sqlite/application_database.db")
        query = 'SELECT * FROM users_info'
        result = conn.execute(query)

        self.user_table.setRowCount(0)

        for row_number, row_data in enumerate(result):
            self.user_table.insertRow(row_number)
            for col_number, data in enumerate(row_data):
                self.user_table.setItem(row_number, col_number, QtWidgets.QTableWidgetItem(str(data)))
        self.usersearch_onoma_input.setText('')
        self.usersearch_epitheto_input.setText('')
        self.usersearch_tilefono_input.setText('')
        self.usersearch_email_input.setText('')
        self.usersearch_id_xwrwn_input.setText('')
        self.rights_management_userid_input.setText('')
        self.rights_management_access_level_input.setText('')
        self.rights_management_id_xwrwn_input.setText('')
        conn.close()

    # Set User Privileges/Set User Areas of Access
    def set_user_privileges(self):
        UserID = self.rights_management_userid_input.text()
        Desired_Access_Level = self.rights_management_access_level_input.text()
        Access_Areas_IDs = self.rights_management_id_xwrwn_input.text()
        sql_tables = ''
        Error_Check = 0
        access_level_choices = [0,1,2]
        if (not UserID):
            self.warning('Failure', 'No user selected: Please insert User ID.')
        if (Desired_Access_Level == '' and Access_Areas_IDs == ''):
            self.warning('Failure', 'No privileges selected: Please provide any privileges.')

        if (Access_Areas_IDs):
            Areas_ID_List = str(Access_Areas_IDs).split(',')
            conn = sqlite3.connect("sqlite/application_database.db")
            cur = conn.cursor()
            with conn:
                for item in Areas_ID_List:
                    result_3 = cur.execute("SELECT * FROM xwroi_idrymatos WHERE ID_xwrou=:idarea", {'idarea': item})
                    if cur.fetchone() is None:
                        Error_Check += 1
                        print(Error_Check)

                if Error_Check > 0:
                    self.warning("Failure", "Included ID of non-existent area.")
                    self.rights_management_userid_input.setText('')
                    self.rights_management_access_level_input.setText('')
                    self.rights_management_id_xwrwn_input.setText('')

        if (UserID and (Desired_Access_Level or Access_Areas_IDs) and Error_Check == 0):
            conn = sqlite3.connect("sqlite/application_database.db")
            cur = conn.cursor()
            with conn:
                result_2 = cur.execute('SELECT * from users_info WHERE ID=:userid', {'userid': UserID})
                if (len(cur.fetchall()) <= 0):
                    self.warning('Failure', 'No user with selected ID.')
                    self.rights_management_userid_input.setText('')
                    self.rights_management_access_level_input.setText('')
                    self.rights_management_id_xwrwn_input.setText('')
                else:
                    if Desired_Access_Level and (int(Desired_Access_Level) in access_level_choices):
                        if (Desired_Access_Level) and (not Access_Areas_IDs) :
                            sql_tables = 'Access_Level=:access'
                        elif Desired_Access_Level and Access_Areas_IDs :
                            sql_tables += 'Access_Level=:access, ID_Xwrwn_Prosvasis=:areas'
                        elif (Access_Areas_IDs) and (not Desired_Access_Level):
                            sql_tables += 'ID_Xwrwn_Prosvasis=:areas'

                        # Dynamic creation of SQL Query
                        sql = 'UPDATE users_info SET '
                        sql += sql_tables
                        sql_part2 = ' WHERE ID=:userid '
                        sql += sql_part2
                        if (UserID) and (Desired_Access_Level or Access_Areas_IDs):
                            conn = sqlite3.connect("sqlite/application_database.db")
                            cur = conn.cursor()
                            with conn:
                                result_1 = cur.execute(sql, {'userid': UserID, 'access': Desired_Access_Level,
                                                             'areas': Access_Areas_IDs})
                            self.clear_Search_user()
                            self.messagebox('Success', 'Privileges of user with ID={} updated!'.format(UserID))
                    elif not Desired_Access_Level:
                        if (Desired_Access_Level) and (not Access_Areas_IDs):
                            sql_tables = 'Access_Level=:access'
                        elif Desired_Access_Level and Access_Areas_IDs:
                            sql_tables += 'Access_Level=:access, ID_Xwrwn_Prosvasis=:areas'
                        elif (Access_Areas_IDs) and (not Desired_Access_Level):
                            sql_tables += 'ID_Xwrwn_Prosvasis=:areas'

                            # Dynamic creation of SQL Query
                        sql = 'UPDATE users_info SET '
                        sql += sql_tables
                        sql_part2 = ' WHERE ID=:userid '
                        sql += sql_part2
                        if (UserID) and (Desired_Access_Level or Access_Areas_IDs):
                            conn = sqlite3.connect("sqlite/application_database.db")
                            cur = conn.cursor()
                            with conn:
                                result_1 = cur.execute(sql, {'userid': UserID, 'access': Desired_Access_Level,
                                                             'areas': Access_Areas_IDs})
                            self.clear_Search_user()
                            self.messagebox('Success', 'Privileges of user with ID={} updated!'.format(UserID))

                    else:
                        self.warning('Failure','Invalid access level choice.\n'
                                               'Access level must be 0(User),1(Supervisor) or 2(Admin).')
                        self.clear_Search_user()
        self.load_supervisor_Data()


    # Reset tablewidget after Search/Load Full Database xwroi_idrymatos table data
    def clear_area_data(self):
        conn = sqlite3.connect("sqlite/application_database.db")
        query = 'SELECT * FROM xwroi_idrymatos'
        result = conn.execute(query)

        self.areas_table.setRowCount(0)

        for row_number, row_data in enumerate(result):
            self.areas_table.insertRow(row_number)
            for col_number, data in enumerate(row_data):
                self.areas_table.setItem(row_number, col_number, QtWidgets.QTableWidgetItem(str(data)))
        self.areas_management_area_name_input.setText('')
        self.areas_management_area_use_input.setText('')
        conn.close()

    # Reset tablewidget after Search for Area Supervisor
    def clear_supervisor_data(self):
        self.area_supervisor_table.setRowCount(8)
        for rows in range(0, 8):
            for col in range(0, 4):
                self.area_supervisor_table.setItem(rows, col, QtWidgets.QTableWidgetItem(''))
        self.area_supervisor_id_input.setText('')
        self.load_supervisor_Data()

    # Delete Rights Function for specific user base on User Id
    def delete_rights(self):
        UserID = self.rights_management_userid_input.text()
        Desired_Access_Level = self.rights_management_access_level_input.text()
        Access_Areas_IDs = self.rights_management_id_xwrwn_input.text()

        if (Desired_Access_Level or Access_Areas_IDs):
            self.warning('Cancelled', 'Please Insert only User ID to revoke rights.')
            self.rights_management_userid_input.setText('')
            self.rights_management_access_level_input.setText('')
            self.rights_management_id_xwrwn_input.setText('')
        elif (not UserID):
            self.warning('Failure', 'No user selected: Please insert User ID.')
        elif (UserID):
            conn = sqlite3.connect("sqlite/application_database.db")
            cur = conn.cursor()
            with conn:
                result_3 = cur.execute('SELECT * from users_info WHERE ID=:userid', {'userid': UserID})
            if (len(cur.fetchall()) <= 0):
                self.warning('Failure', 'No user with selected ID.')
                self.rights_management_userid_input.setText('')
                self.rights_management_access_level_input.setText('')
                self.rights_management_id_xwrwn_input.setText('')
            else:
                with conn:
                    result_4 = cur.execute(
                        'UPDATE users_info SET Access_Level=:access, ID_Xwrwn_Prosvasis=null WHERE ID=:userid',
                        {'userid': UserID, 'access': 0})
                self.messagebox('Success', 'User rights for user with ID={} revoked!'.format(UserID))
                self.clear_Search_user()
        self.load_supervisor_Data()

    # Delete Area from SQlite Database function for specific user based on Area ID
    def delete_area(self):
        Area_ID = self.area_delete_id_input.text()

        if (not Area_ID):
            self.warning('Failure', 'Please provide Area ID to delete area.')
        else:
            conn = sqlite3.connect("sqlite/application_database.db")
            cur = conn.cursor()
            with conn:
                result = cur.execute('SELECT * from xwroi_idrymatos WHERE ID_Xwrou=:areaid', {'areaid': Area_ID})
            if (len(cur.fetchall()) <= 0):
                self.warning('Failure', 'No area with selected ID.')
                self.area_delete_id_input.setText('')
            else:
                with conn:
                    result_2 = cur.execute('DELETE FROM xwroi_idrymatos WHERE ID_Xwrou={}'.format(Area_ID))
                    self.messagebox('Success', 'Area with ID={} deleted successfully!'.format(Area_ID))
                self.clear_area_data()
                self.area_delete_id_input.setText('')
                self.correct_Access_Areas_IDs(Area_ID)

    # Reassign corrected areas id after deleting area to all users
    def correct_Access_Areas_IDs(self, AreaID):
        conn = sqlite3.connect("sqlite/application_database.db")
        cur = conn.cursor()
        Areas_List = []
        fixed_string = ''
        with conn:
            result = cur.execute("SELECT ID,ID_Xwrwn_Prosvasis FROM users_info")
            supervisors = cur.fetchall()
            for item in supervisors:
                Areas_IDs = str(item[1]).split(',')
                for id in Areas_IDs:
                    if id != AreaID:
                        Areas_List.append(id)

                    Areas_Tuple = tuple(Areas_List)
                    fixed_string = ','.join(Areas_Tuple)
                    Complete_Tuple = (item[0], fixed_string)
                Areas_List.clear()
                del Areas_Tuple
                if fixed_string == '':
                    Complete_Tuple = (item[0], None)
                result_1 = cur.execute("UPDATE users_info SET ID_Xwrwn_Prosvasis=:areasid WHERE ID=:id",
                                       {'areasid': str(Complete_Tuple[1]), 'id': Complete_Tuple[0]})
        self.clear_Search_user()

    # Insert Area to xwroi_idrymatos SQlite Database table function
    def insert_area(self):

        Area_Name = self.areas_management_area_name_input.text()
        Area_Use = self.areas_management_area_use_input.text()

        if (not (Area_Name and Area_Use)):
            self.warning('Failure', 'Please provide information to insert area.')
            self.areas_management_area_name_input.setText('')
            self.areas_management_area_use_input.setText('')
        if (Area_Use and Area_Name):
            conn = sqlite3.connect("sqlite/application_database.db")
            cur = conn.cursor()
            with conn:
                result = cur.execute(
                    "INSERT INTO xwroi_idrymatos('xrisi_xwrou','onoma_xwrou') VALUES('{}','{}')".format(Area_Use,
                                                                                                        Area_Name))
            self.messagebox('Success', 'Area successfully added to Database!')
            self.areas_management_area_name_input.setText('')
            self.areas_management_area_use_input.setText('')
            self.clear_area_data()

    # Search for Area Function
    def search_for_area(self):
        Area_Name = self.areas_management_area_name_input.text()
        Area_Use = self.areas_management_area_use_input.text()
        sql_where = ''

        if (not (Area_Name or Area_Use)):
            self.warning('Failure', 'Please provide information to search for area.')
            self.areas_management_area_name_input.setText('')
            self.areas_management_area_use_input.setText('')

        else:
            if (Area_Name and (not Area_Use)):
                sql_where = 'onoma_xwrou=:areaname'
            elif (Area_Name and Area_Use):
                sql_where = 'onoma_xwrou=:areaname AND xrisi_xwrou=:areause'
            elif (Area_Use and (not Area_Name)):
                sql_where = 'xrisi_xwrou=:areause'

            sql = 'SELECT * FROM xwroi_idrymatos WHERE '
            sql += sql_where
            conn = sqlite3.connect("sqlite/application_database.db")
            cur = conn.cursor()

            with conn:
                result = cur.execute(sql, {'areaname': Area_Name, 'areause': Area_Use})
                self.areas_table.setRowCount(0)
                for row_number, row_data in enumerate(result):
                    self.areas_table.insertRow(row_number)
                    for col_number, data in enumerate(row_data):
                        self.areas_table.setItem(row_number, col_number, QtWidgets.QTableWidgetItem(str(data)))
                if (self.areas_table.rowCount()) > 0:
                    self.messagebox('Success', ' One or more areas matching the description found!')
                    self.areas_management_area_name_input.setText('')
                    self.areas_management_area_use_input.setText('')
                else:
                    self.warning('No results', ' No areas matching the description found!')
                    self.clear_area_data()

    # Search for area supervisor function
    def search_for_supervisor(self):
        Area_ID = self.area_supervisor_id_input.text()
        Area_Supervisors = []
        Supervisors_Info = []
        if (not Area_ID):
            self.warning('Failure', 'Please provide area ID to search for supervisors.')

        else:
            conn = sqlite3.connect("sqlite/application_database.db")
            cur = conn.cursor()

            with conn:
                result = cur.execute("SELECT ID,ID_Xwrwn_Prosvasis FROM users_info")

                supervisors = cur.fetchall()

            for item in supervisors:
                Areas_IDs = str(item[1]).split(',')
                for id in Areas_IDs:
                    if id == Area_ID:
                        Area_Supervisors.append(item[0])

            with conn:
                self.area_supervisor_table.setRowCount(0)
                for id in Area_Supervisors:
                    result_1 = cur.execute("SELECT ID,First_Name,Last_Name,EMAIL FROM users_info WHERE ID=:ids",
                                           {'ids': str(id)})
                    Supervisors_Info.append(cur.fetchone())

                length_error_handler = len(Supervisors_Info) - 1
                if length_error_handler == 0:
                    length_error_handler = 1
                for item in Supervisors_Info:
                    for i in range(0, length_error_handler):
                        self.area_supervisor_table.insertRow(i)
                        for col_number in range(0, 4):
                            self.area_supervisor_table.setItem(i, col_number,
                                                               QtWidgets.QTableWidgetItem(str(item[col_number])))

                if (len(Supervisors_Info) > 0):
                    self.messagebox('Success', ' One or more supervisors found for specified area!')
                    self.area_supervisor_id_input.setText('')
                else:
                    self.warning('No results', ' No supervisors matching the area ID found!')
                    self.area_supervisor_id_input.setText('')

    def check_equip_input(self):
        area = self.search_xwrou_input.text()
        equip_type = self.search_ylikou_input.text()
        equip_types = ['Material', 'Equipment']
        invalid = [self.search_daneismou_input.text(), self.search_keywords_input.text(), self.search_katigoria_input.text()]
        filled_spaces = 0

        for empty in invalid:
            if empty != '':
                filled_spaces += 1


        if filled_spaces>0:
            self.warning('Failure','Please provide only Area ID and equipment type.')
            self.load_equipment_data()

        elif not(area and equip_type):
            self.warning('Failure', 'Please provide Area ID and equipment type.')

        elif (equip_type not in equip_types):
            self.warning('Failure','Invalid equip type.'
                                   '\nType can either be Material or Equipment.')
            self.load_equipment_data()

        elif (equip_type == 'Material'):
            conn = sqlite3.connect("sqlite/application_database.db")
            cur = conn.cursor()

            with conn:
                result = cur.execute("SELECT * FROM xwroi_idrymatos WHERE ID_xwrou=:idarea",
                                     {'idarea':area})
            if (len(cur.fetchall())) <=0:
                self.warning('Failure','No area with selected ID.')
                self.load_equipment_data()
            else:
                self.window = QtWidgets.QMainWindow()
                self.ui = Ui_add_material()
                self.ui.setupUi(self.window)
                self.window.show()
                self.ui.setprivates(area,equip_type)

        elif (equip_type == 'Equipment'):
            conn = sqlite3.connect("sqlite/application_database.db")
            cur = conn.cursor()

            with conn:
                result = cur.execute("SELECT * FROM xwroi_idrymatos WHERE ID_xwrou=:idarea",
                                     {'idarea': area})
            if (len(cur.fetchall())) <= 0:
                self.warning('Failure', 'No area with selected ID.')
                self.load_equipment_data()
            else:
                self.window = QtWidgets.QMainWindow()
                self.ui = Ui_add_equipment()
                self.ui.setupUi(self.window)
                self.window.show()
                self.ui.setprivates(area, equip_type)

    def load_equipment_data(self):
        conn = sqlite3.connect("sqlite/application_database.db")
        query = 'SELECT * FROM yliko_xwrwn'
        result = conn.execute(query)

        self.equipment_table.setRowCount(0)

        for row_number, row_data in enumerate(result):
            self.equipment_table.insertRow(row_number)
            for col_number, data in enumerate(row_data):
                self.equipment_table.setItem(row_number, col_number, QtWidgets.QTableWidgetItem(str(data)))

        self.search_xwrou_input.setText('')
        self.search_ylikou_input.setText('')
        self.search_daneismou_input.setText('')
        self.search_keywords_input.setText('')
        self.search_katigoria_input.setText('')
        self.id_ylikou_management_input.setText('')

        conn.close()

    #Delete Equipment/Material from DB func
    def delete_equipment(self):

        id_ylikou = self.id_ylikou_management_input.text()

        if not id_ylikou:
            self.warning('Failure','Please provide Equipment/Material ID to proceed.')

        elif id_ylikou:

            conn = sqlite3.connect("sqlite/application_database.db")
            cur = conn.cursor()

            with conn:
                result = cur.execute("SELECT * FROM yliko_xwrwn WHERE ID_ylikou=:idyl",
                                     {'idyl': id_ylikou})
            if (len(cur.fetchall())) <= 0:
                self.warning('Failure', 'No item with selected ID.')
                self.id_ylikou_management_input.setText('')

            else:
                with conn:
                    result = cur.execute("DELETE FROM yliko_xwrwn WHERE ID_ylikou=:idyl2",{'idyl2': id_ylikou})
                    self.messagebox('Success','Item with ID={} deleted successfully!'.format(id_ylikou))

                self.id_ylikou_management_input.setText('')
                self.load_equipment_data()

    #Check item id and connect to edit windows(Material/Equipment)

    def checkedit(self):

        id_ylikou = self.id_ylikou_management_input.text()

        if not id_ylikou:
            self.warning('Failure', 'Please provide Equipment/Material ID to proceed.')

        elif id_ylikou:

            conn = sqlite3.connect("sqlite/application_database.db")
            cur = conn.cursor()

            with conn:
                result = cur.execute("SELECT * FROM yliko_xwrwn WHERE ID_ylikou=:idyl",
                                     {'idyl': id_ylikou})
            if (len(cur.fetchall())) <= 0:
                self.warning('Failure', 'No item with selected ID.')
                self.id_ylikou_management_input.setText('')
            else:

                with conn:
                    result = cur.execute("SELECT typos FROM yliko_xwrwn WHERE ID_ylikou=:idyl2",{'idyl2': id_ylikou})

                Typos_Ylikou = cur.fetchone()
                Typos_Ylikou = Typos_Ylikou[0]

                if Typos_Ylikou == 'Material':
                    self.window = QtWidgets.QMainWindow()
                    self.ui = Ui_edit_material()
                    self.ui.setupUi(self.window)
                    self.window.show()
                    self.ui.setprivates(id_ylikou)
                    self.ui.load_item_data()

                if Typos_Ylikou == 'Equipment':
                    self.window = QtWidgets.QMainWindow()
                    self.ui = Ui_edit_equipment()
                    self.ui.setupUi(self.window)
                    self.window.show()
                    self.ui.setprivates(id_ylikou)
                    self.ui.load_item_data()

    # Search for equipment/material function

    def search_for_equipment(self):
        id_xwrou = self.search_xwrou_input.text()
        typos_ylikou = self.search_ylikou_input.text()
        katastasti_daneismou = self.search_daneismou_input.text()
        lekseis_kleidia = self.search_keywords_input.text()
        katigoria = self.search_katigoria_input.text()
        sql_where = ''
        katastasti_daneismou_choices = ['Available', 'Borrowed']



        if not(id_xwrou or typos_ylikou or katastasti_daneismou or lekseis_kleidia or katigoria):
            self.warning('Failure', 'Please provide at least one search parameter.')
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
                     result = cur.execute(sql,{'idx':id_xwrou,'typ':typos_ylikou,'katd':katastasti_daneismou,
                                               'katg':katigoria})
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
            elif lekseis_kleidia and not(id_xwrou or typos_ylikou or katastasti_daneismou or katigoria):
                target_keywords = lekseis_kleidia.split(',')
                matching_items = []
                conn = sqlite3.connect("sqlite/application_database.db")
                cur = conn.cursor()

                with conn:
                    cur.execute("SELECT ID_ylikou,lekseis_kleidia FROM yliko_xwrwn")
                    keywords_per_id = cur.fetchall()

                for item in keywords_per_id:
                    item_keywords = str(item[1]).split(',')
                    for word in item_keywords:
                        if word in target_keywords:
                            matching_items.append(item[0])
                items_count = len(matching_items)
                self.equipment_table.setRowCount(items_count)
                if items_count > 0:
                    for i in range(0,items_count):
                        cur.execute('SELECT * FROM yliko_xwrwn WHERE ID_ylikou={}'.format(matching_items[i]))
                        match = cur.fetchone()
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

                    cur.execute("SELECT ID_ylikou,lekseis_kleidia FROM yliko_xwrwn")
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
                            cur.execute('SELECT * FROM yliko_xwrwn WHERE ID_ylikou={}'.format(final_matching_items_ids[i]))
                            match = cur.fetchone()
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

    def lend_equip(self):

        id_ylikou = self.id_ylikou_management_input.text()

        if not id_ylikou:
            self.warning('Failure','Please provide equipment ID.')
        else:
            conn = sqlite3.connect("sqlite/application_database.db")
            cur = conn.cursor()

            with conn:
                cur.execute('SELECT * FROM yliko_xwrwn WHERE ID_ylikou={}'.format(id_ylikou))

            if len(cur.fetchall()) > 0:

                self.window = QtWidgets.QMainWindow()
                self.ui = Ui_loan_window()
                self.ui.setupUi(self.window)
                self.window.show()
                self.ui.setprivates(id_ylikou)

            else:
                self.warning('Failure', 'No item with ID={} .'.format(id_ylikou))
                self.id_ylikou_management_input.setText('')


    def setupUi(self, Admin):
        Admin.setObjectName("Admin")
        Admin.resize(1120, 734)
        Admin.setMinimumSize(QtCore.QSize(1120, 734))
        Admin.setMaximumSize(QtCore.QSize(1120, 734))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Admin.sizePolicy().hasHeightForWidth())
        Admin.setSizePolicy(sizePolicy)
        Admin.setBaseSize(QtCore.QSize(797, 647))
        font = QtGui.QFont()
        font.setPointSize(10)
        Admin.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("media/admin.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Admin.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(Admin)
        self.centralwidget.setObjectName("centralwidget")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(0, 0, 1111, 611))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Myriad Pro Light")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.tabWidget.setFont(font)
        self.tabWidget.setMouseTracking(False)
        self.tabWidget.setDocumentMode(False)
        self.tabWidget.setTabsClosable(False)
        self.tabWidget.setTabBarAutoHide(False)
        self.tabWidget.setObjectName("tabWidget")
        self.users = QtWidgets.QWidget()
        self.users.setObjectName("users")
        self.user_table = QtWidgets.QTableWidget(self.users)
        self.user_table.setGeometry(QtCore.QRect(0, 270, 1111, 301))
        font = QtGui.QFont()
        font.setFamily("Myriad Pro Light")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.user_table.setFont(font)
        self.user_table.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.user_table.setFrameShape(QtWidgets.QFrame.Box)
        self.user_table.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.user_table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.user_table.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.user_table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.user_table.setGridStyle(QtCore.Qt.DashLine)
        self.user_table.setRowCount(10)
        self.user_table.setObjectName("user_table")
        self.user_table.setColumnCount(9)
        item = QtWidgets.QTableWidgetItem()
        self.user_table.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.user_table.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.user_table.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.user_table.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.user_table.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.user_table.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.user_table.setHorizontalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        self.user_table.setHorizontalHeaderItem(7, item)
        item = QtWidgets.QTableWidgetItem()
        self.user_table.setHorizontalHeaderItem(8, item)
        # set column width
        self.user_table.setColumnWidth(0, 180)
        self.user_table.setColumnWidth(1, 180)
        self.user_table.setColumnWidth(2, 180)
        self.user_table.setColumnWidth(3, 180)
        self.user_table.setColumnWidth(4, 180)
        self.user_table.setColumnWidth(5, 180)
        self.user_table.setColumnWidth(6, 180)
        self.user_table.setColumnWidth(7, 180)
        self.user_table.setColumnWidth(8, 180)
        self.search_label_2 = QtWidgets.QLabel(self.users)
        self.search_label_2.setGeometry(QtCore.QRect(10, 6, 211, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setUnderline(False)
        font.setWeight(75)
        self.search_label_2.setFont(font)
        self.search_label_2.setObjectName("search_label_2")
        self.line_4 = QtWidgets.QFrame(self.users)
        self.line_4.setGeometry(QtCore.QRect(0, 20, 300, 20))
        self.line_4.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_4.setObjectName("line_4")
        self.label_usersearch_onoma = QtWidgets.QLabel(self.users)
        self.label_usersearch_onoma.setGeometry(QtCore.QRect(10, 40, 121, 21))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.label_usersearch_onoma.setFont(font)
        self.label_usersearch_onoma.setObjectName("label_usersearch_onoma")
        self.label_usersearch_epitheto = QtWidgets.QLabel(self.users)
        self.label_usersearch_epitheto.setGeometry(QtCore.QRect(10, 70, 241, 21))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.label_usersearch_epitheto.setFont(font)
        self.label_usersearch_epitheto.setObjectName("label_usersearch_epitheto")
        self.label_usersearch_tilefono = QtWidgets.QLabel(self.users)
        self.label_usersearch_tilefono.setGeometry(QtCore.QRect(10, 100, 271, 21))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.label_usersearch_tilefono.setFont(font)
        self.label_usersearch_tilefono.setObjectName("label_usersearch_tilefono")
        self.label_usersearch_email = QtWidgets.QLabel(self.users)
        self.label_usersearch_email.setGeometry(QtCore.QRect(10, 130, 241, 21))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.label_usersearch_email.setFont(font)
        self.label_usersearch_email.setObjectName("label_usersearch_email")
        self.label_usersearch_id_xwrwn = QtWidgets.QLabel(self.users)
        self.label_usersearch_id_xwrwn.setGeometry(QtCore.QRect(10, 156, 461, 20))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.label_usersearch_id_xwrwn.setFont(font)
        self.label_usersearch_id_xwrwn.setObjectName("label_usersearch_id_xwrwn")
        self.usersearch_onoma_input = QtWidgets.QLineEdit(self.users)
        self.usersearch_onoma_input.setGeometry(QtCore.QRect(370, 40, 113, 20))
        self.usersearch_onoma_input.setObjectName("usersearch_onoma_input")
        self.usersearch_epitheto_input = QtWidgets.QLineEdit(self.users)
        self.usersearch_epitheto_input.setGeometry(QtCore.QRect(370, 70, 113, 20))
        self.usersearch_epitheto_input.setObjectName("usersearch_epitheto_input")
        self.usersearch_tilefono_input = QtWidgets.QLineEdit(self.users)
        self.usersearch_tilefono_input.setGeometry(QtCore.QRect(370, 100, 113, 20))
        self.usersearch_tilefono_input.setObjectName("usersearch_tilefono_input")
        self.usersearch_email_input = QtWidgets.QLineEdit(self.users)
        self.usersearch_email_input.setGeometry(QtCore.QRect(370, 130, 113, 21))
        self.usersearch_email_input.setObjectName("usersearch_email_input")
        self.usersearch_id_xwrwn_input = QtWidgets.QLineEdit(self.users)
        self.usersearch_id_xwrwn_input.setGeometry(QtCore.QRect(370, 180, 113, 20))
        self.usersearch_id_xwrwn_input.setObjectName("usersearch_id_xwrwn_input")
        self.line_5 = QtWidgets.QFrame(self.users)
        self.line_5.setGeometry(QtCore.QRect(520, 0, 20, 271))
        self.line_5.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_5.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_5.setObjectName("line_5")
        self.user_rights_management_label = QtWidgets.QLabel(self.users)
        self.user_rights_management_label.setGeometry(QtCore.QRect(540, 6, 291, 20))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.user_rights_management_label.setFont(font)
        self.user_rights_management_label.setObjectName("user_rights_management_label")
        self.line_6 = QtWidgets.QFrame(self.users)
        self.line_6.setGeometry(QtCore.QRect(530, 20, 300, 20))
        self.line_6.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_6.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_6.setObjectName("line_6")
        self.rights_management_userid_label = QtWidgets.QLabel(self.users)
        self.rights_management_userid_label.setGeometry(QtCore.QRect(540, 40, 121, 21))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.rights_management_userid_label.setFont(font)
        self.rights_management_userid_label.setObjectName("rights_management_userid_label")
        self.rights_management_access_level_label = QtWidgets.QLabel(self.users)
        self.rights_management_access_level_label.setGeometry(QtCore.QRect(540, 70, 251, 21))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.rights_management_access_level_label.setFont(font)
        self.rights_management_access_level_label.setObjectName("rights_management_access_level_label")
        self.rights_management_id_xwrwn_label = QtWidgets.QLabel(self.users)
        self.rights_management_id_xwrwn_label.setGeometry(QtCore.QRect(540, 100, 491, 21))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.rights_management_id_xwrwn_label.setFont(font)
        self.rights_management_id_xwrwn_label.setObjectName("rights_management_id_xwrwn_label")
        self.rights_management_userid_input = QtWidgets.QLineEdit(self.users)
        self.rights_management_userid_input.setGeometry(QtCore.QRect(920, 40, 113, 20))
        self.rights_management_userid_input.setObjectName("rights_management_userid_input")
        self.rights_management_access_level_input = QtWidgets.QLineEdit(self.users)
        self.rights_management_access_level_input.setGeometry(QtCore.QRect(920, 70, 113, 21))
        self.rights_management_access_level_input.setObjectName("rights_management_access_level_input")
        self.rights_management_id_xwrwn_input = QtWidgets.QLineEdit(self.users)
        self.rights_management_id_xwrwn_input.setGeometry(QtCore.QRect(920, 130, 113, 20))
        self.rights_management_id_xwrwn_input.setText("")
        self.rights_management_id_xwrwn_input.setObjectName("rights_management_id_xwrwn_input")
        self.rights_management_button = QtWidgets.QPushButton(self.users)
        self.rights_management_button.setGeometry(QtCore.QRect(540, 205, 231, 31))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.rights_management_button.setFont(font)
        self.rights_management_button.setObjectName("rights_management_button")
        self.user_search_info_label = QtWidgets.QLabel(self.users)
        self.user_search_info_label.setGeometry(QtCore.QRect(10, 240, 491, 21))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.user_search_info_label.setFont(font)
        self.user_search_info_label.setObjectName("user_search_info_label")
        self.user_management_info_label = QtWidgets.QLabel(self.users)
        self.user_management_info_label.setGeometry(QtCore.QRect(540, 240, 511, 21))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.user_management_info_label.setFont(font)
        self.user_management_info_label.setObjectName("user_management_info_label")
        self.user_search_button = QtWidgets.QPushButton(self.users)
        self.user_search_button.setGeometry(QtCore.QRect(20, 205, 191, 31))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.user_search_button.setFont(font)
        self.user_search_button.setObjectName("user_search_button")
        self.clear_search_button = QtWidgets.QPushButton(self.users)
        self.clear_search_button.setGeometry(QtCore.QRect(300, 205, 191, 31))
        self.clear_search_button.setObjectName("clear_search_button")
        self.pushButton_2 = QtWidgets.QPushButton(self.users)
        self.pushButton_2.setGeometry(QtCore.QRect(800, 205, 231, 31))
        self.pushButton_2.setObjectName("pushButton_2")
        self.tabWidget.addTab(self.users, "")
        self.areas = QtWidgets.QWidget()
        self.areas.setObjectName("areas")
        self.areas_table = QtWidgets.QTableWidget(self.areas)
        self.areas_table.setGeometry(QtCore.QRect(0, 270, 571, 301))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.areas_table.sizePolicy().hasHeightForWidth())
        self.areas_table.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Myriad Pro Light")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.areas_table.setFont(font)
        self.areas_table.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.areas_table.setFrameShape(QtWidgets.QFrame.Box)
        self.areas_table.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.areas_table.setAutoScroll(False)
        self.areas_table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.areas_table.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.areas_table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.areas_table.setShowGrid(True)
        self.areas_table.setGridStyle(QtCore.Qt.DashLine)
        self.areas_table.setWordWrap(True)
        self.areas_table.setRowCount(10)
        self.areas_table.setObjectName("areas_table")
        self.areas_table.setColumnCount(3)
        item = QtWidgets.QTableWidgetItem()
        self.areas_table.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.areas_table.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.areas_table.setHorizontalHeaderItem(2, item)
        # item = QtWidgets.QTableWidgetItem()
        # self.areas_table.setHorizontalHeaderItem(3, item)
        # self.areas_table.setColumnWidth(3, 150)
        self.areas_management_label = QtWidgets.QLabel(self.areas)
        self.areas_management_label.setGeometry(QtCore.QRect(10, 10, 171, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setUnderline(False)
        font.setWeight(75)
        self.areas_management_label.setFont(font)
        self.areas_management_label.setObjectName("areas_management_label")
        self.line_7 = QtWidgets.QFrame(self.areas)
        self.line_7.setGeometry(QtCore.QRect(0, 30, 300, 16))
        self.line_7.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_7.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_7.setObjectName("line_7")
        self.areas_management_area_name_label = QtWidgets.QLabel(self.areas)
        self.areas_management_area_name_label.setGeometry(QtCore.QRect(10, 50, 151, 16))
        self.areas_management_area_name_label.setObjectName("areas_management_area_name_label")
        self.areas_management_useofarea_label = QtWidgets.QLabel(self.areas)
        self.areas_management_useofarea_label.setGeometry(QtCore.QRect(10, 80, 121, 21))
        self.areas_management_useofarea_label.setObjectName("areas_management_useofarea_label")
        self.label_3 = QtWidgets.QLabel(self.areas)
        self.label_3.setGeometry(QtCore.QRect(10, 100, 47, 13))
        self.label_3.setText("")
        self.label_3.setObjectName("label_3")
        self.areas_management_area_name_input = QtWidgets.QLineEdit(self.areas)
        self.areas_management_area_name_input.setGeometry(QtCore.QRect(180, 50, 113, 20))
        self.areas_management_area_name_input.setObjectName("areas_management_area_name_input")
        self.areas_management_area_use_input = QtWidgets.QLineEdit(self.areas)
        self.areas_management_area_use_input.setGeometry(QtCore.QRect(180, 80, 113, 20))
        self.areas_management_area_use_input.setObjectName("areas_management_area_use_input")
        self.areas_search_button = QtWidgets.QPushButton(self.areas)
        self.areas_search_button.setGeometry(QtCore.QRect(60, 120, 181, 31))
        self.areas_search_button.setObjectName("areas_search_button")
        self.areas_insert_button = QtWidgets.QPushButton(self.areas)
        self.areas_insert_button.setGeometry(QtCore.QRect(60, 160, 181, 31))
        self.areas_insert_button.setObjectName("areas_insert_button")
        self.area_delete_label = QtWidgets.QLabel(self.areas)
        self.area_delete_label.setGeometry(QtCore.QRect(340, 10, 321, 20))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.area_delete_label.setFont(font)
        self.area_delete_label.setObjectName("area_delete_label")
        self.line_8 = QtWidgets.QFrame(self.areas)
        self.line_8.setGeometry(QtCore.QRect(320, 0, 20, 271))
        self.line_8.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_8.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_8.setObjectName("line_8")
        self.line_9 = QtWidgets.QFrame(self.areas)
        self.line_9.setGeometry(QtCore.QRect(330, 30, 300, 16))
        self.line_9.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_9.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_9.setObjectName("line_9")
        self.area_delete_id_label = QtWidgets.QLabel(self.areas)
        self.area_delete_id_label.setGeometry(QtCore.QRect(360, 80, 91, 20))
        self.area_delete_id_label.setObjectName("area_delete_id_label")
        self.area_delete_id_input = QtWidgets.QLineEdit(self.areas)
        self.area_delete_id_input.setGeometry(QtCore.QRect(500, 80, 113, 20))
        self.area_delete_id_input.setObjectName("area_delete_id_input")
        self.area_delete_button = QtWidgets.QPushButton(self.areas)
        self.area_delete_button.setGeometry(QtCore.QRect(400, 140, 181, 31))
        self.area_delete_button.setObjectName("area_delete_button")
        self.line_10 = QtWidgets.QFrame(self.areas)
        self.line_10.setGeometry(QtCore.QRect(650, 0, 20, 271))
        self.line_10.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_10.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_10.setObjectName("line_10")
        self.line_11 = QtWidgets.QFrame(self.areas)
        self.line_11.setGeometry(QtCore.QRect(660, 30, 300, 16))
        self.line_11.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_11.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_11.setObjectName("line_11")
        self.area_supervisor_search_label = QtWidgets.QLabel(self.areas)
        self.area_supervisor_search_label.setGeometry(QtCore.QRect(670, 10, 321, 20))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.area_supervisor_search_label.setFont(font)
        self.area_supervisor_search_label.setObjectName("area_supervisor_search_label")
        self.area_supervisor_id_search_label = QtWidgets.QLabel(self.areas)
        self.area_supervisor_id_search_label.setGeometry(QtCore.QRect(700, 80, 111, 21))
        self.area_supervisor_id_search_label.setObjectName("area_supervisor_id_search_label")
        self.area_supervisor_id_input = QtWidgets.QLineEdit(self.areas)
        self.area_supervisor_id_input.setGeometry(QtCore.QRect(940, 80, 113, 21))
        self.area_supervisor_id_input.setObjectName("area_supervisor_id_input")
        self.area_supervisor_search_button = QtWidgets.QPushButton(self.areas)
        self.area_supervisor_search_button.setGeometry(QtCore.QRect(770, 140, 181, 31))
        self.area_supervisor_search_button.setObjectName("area_supervisor_search_button")
        self.area_supervisor_table = QtWidgets.QTableWidget(self.areas)
        self.area_supervisor_table.setGeometry(QtCore.QRect(570, 270, 541, 301))
        font = QtGui.QFont()
        font.setFamily("Myriad Pro Light")
        font.setPointSize(10)
        self.area_supervisor_table.setFont(font)
        self.area_supervisor_table.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.area_supervisor_table.setFrameShape(QtWidgets.QFrame.Box)
        self.area_supervisor_table.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.area_supervisor_table.setAutoScroll(False)
        self.area_supervisor_table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.area_supervisor_table.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.area_supervisor_table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.area_supervisor_table.setGridStyle(QtCore.Qt.DashLine)
        self.area_supervisor_table.setRowCount(10)
        self.area_supervisor_table.setObjectName("area_supervisor_table")
        self.area_supervisor_table.setColumnCount(4)
        item = QtWidgets.QTableWidgetItem()
        self.area_supervisor_table.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.area_supervisor_table.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.area_supervisor_table.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.area_supervisor_table.setHorizontalHeaderItem(3, item)
        # set column width
        self.area_supervisor_table.setColumnWidth(0, 120)
        self.area_supervisor_table.setColumnWidth(1, 120)
        self.area_supervisor_table.setColumnWidth(2, 120)
        self.area_supervisor_table.setColumnWidth(3, 160)
        # set column width
        self.areas_table.setColumnWidth(0, 150)
        self.areas_table.setColumnWidth(1, 150)
        self.areas_table.setColumnWidth(2, 150)
        self.areas_table.setColumnWidth(3, 150)
        self.areas_clearsearch_button = QtWidgets.QPushButton(self.areas)
        self.areas_clearsearch_button.setGeometry(QtCore.QRect(60, 200, 181, 31))
        self.areas_clearsearch_button.setObjectName("areas_clearsearch_button")
        self.supervisor_clearsearch_button = QtWidgets.QPushButton(self.areas)
        self.supervisor_clearsearch_button.setGeometry(QtCore.QRect(770, 180, 181, 31))
        self.supervisor_clearsearch_button.setObjectName("supervisor_clearsearch_button")
        self.label = QtWidgets.QLabel(self.areas)
        self.label.setGeometry(QtCore.QRect(10, 240, 301, 21))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.areas)
        self.label_2.setGeometry(QtCore.QRect(340, 240, 301, 21))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label_4 = QtWidgets.QLabel(self.areas)
        self.label_4.setGeometry(QtCore.QRect(670, 240, 391, 21))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.tabWidget.addTab(self.areas, "")
        self.equipment = QtWidgets.QWidget()
        self.equipment.setObjectName("equipment")
        self.equipment_table = QtWidgets.QTableWidget(self.equipment)
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
        self.search_label = QtWidgets.QLabel(self.equipment)
        self.search_label.setGeometry(QtCore.QRect(10, 10, 211, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setUnderline(False)
        font.setWeight(75)
        self.search_label.setFont(font)
        self.search_label.setObjectName("search_label")
        self.equip_search_info_label = QtWidgets.QLabel(self.equipment)
        self.equip_search_info_label.setGeometry(QtCore.QRect(5, 240, 521, 16))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.equip_search_info_label.setFont(font)
        self.equip_search_info_label.setObjectName("equip_search_info_label")
        self.line = QtWidgets.QFrame(self.equipment)
        self.line.setGeometry(QtCore.QRect(530, 0, 20, 271))
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.line_2 = QtWidgets.QFrame(self.equipment)
        self.line_2.setGeometry(QtCore.QRect(0, 30, 300, 16))
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.label_search_xwrou = QtWidgets.QLabel(self.equipment)
        self.label_search_xwrou.setGeometry(QtCore.QRect(10, 50, 290, 21))
        font = QtGui.QFont()
        font.setFamily("Myriad Pro Light")
        font.setBold(False)
        font.setWeight(50)
        self.label_search_xwrou.setFont(font)
        self.label_search_xwrou.setObjectName("label_search_xwrou")
        self.label_search_yliko = QtWidgets.QLabel(self.equipment)
        self.label_search_yliko.setGeometry(QtCore.QRect(10, 80, 330, 21))
        self.label_search_yliko.setObjectName("label_search_yliko")
        self.label_search_daneismos = QtWidgets.QLabel(self.equipment)
        self.label_search_daneismos.setGeometry(QtCore.QRect(10, 110, 241, 21))
        self.label_search_daneismos.setObjectName("label_search_daneismos")
        self.label_search_keywords = QtWidgets.QLabel(self.equipment)
        self.label_search_keywords.setGeometry(QtCore.QRect(10, 140, 301, 21))
        self.label_search_keywords.setObjectName("label_search_keywords")
        self.label_search_katigoria_ylikou = QtWidgets.QLabel(self.equipment)
        self.label_search_katigoria_ylikou.setGeometry(QtCore.QRect(10, 170, 171, 21))
        self.label_search_katigoria_ylikou.setObjectName("label_search_katigoria_ylikou")
        self.search_xwrou_input = QtWidgets.QLineEdit(self.equipment)
        self.search_xwrou_input.setGeometry(QtCore.QRect(370, 50, 113, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(8)
        font.setBold(False)
        font.setWeight(50)
        self.search_xwrou_input.setFont(font)
        self.search_xwrou_input.setText("")
        self.search_xwrou_input.setObjectName("search_xwrou_input")
        self.search_ylikou_input = QtWidgets.QLineEdit(self.equipment)
        self.search_ylikou_input.setGeometry(QtCore.QRect(370, 80, 113, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(8)
        font.setBold(False)
        font.setWeight(50)
        self.search_ylikou_input.setFont(font)
        self.search_ylikou_input.setText("")
        self.search_ylikou_input.setObjectName("search_ylikou_input")
        self.search_daneismou_input = QtWidgets.QLineEdit(self.equipment)
        self.search_daneismou_input.setGeometry(QtCore.QRect(370, 110, 113, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(8)
        font.setBold(False)
        font.setWeight(50)
        self.search_daneismou_input.setFont(font)
        self.search_daneismou_input.setObjectName("search_daneismou_input")
        self.search_keywords_input = QtWidgets.QLineEdit(self.equipment)
        self.search_keywords_input.setGeometry(QtCore.QRect(370, 140, 113, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(8)
        font.setBold(False)
        font.setWeight(50)
        self.search_keywords_input.setFont(font)
        self.search_keywords_input.setText("")
        self.search_keywords_input.setObjectName("search_keywords_input")
        self.search_katigoria_input = QtWidgets.QLineEdit(self.equipment)
        self.search_katigoria_input.setGeometry(QtCore.QRect(370, 170, 113, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(8)
        font.setBold(False)
        font.setWeight(50)
        self.search_katigoria_input.setFont(font)
        self.search_katigoria_input.setObjectName("search_katigoria_input")
        self.equipment_search_button = QtWidgets.QPushButton(self.equipment)
        self.equipment_search_button.setGeometry(QtCore.QRect(10, 200, 181, 31))
        self.equipment_search_button.setObjectName("equipment_search_button")
        self.equipment_refresh_button = QtWidgets.QPushButton(self.equipment)
        self.equipment_refresh_button.setGeometry(QtCore.QRect(600, 180, 220, 31))
        self.equipment_refresh_button.setObjectName("equipment_refresh_button")
        self.equipment_refresh_button.clicked.connect(self.load_equipment_data)
        self.equipment_refresh_button.setText('Επαναφόρτωση Δεδομένων')
        self.equipment_management_label = QtWidgets.QLabel(self.equipment)
        self.equipment_management_label.setGeometry(QtCore.QRect(550, 10, 211, 20))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.equipment_management_label.setFont(font)
        self.equipment_management_label.setObjectName("equipment_management_label")
        self.line_3 = QtWidgets.QFrame(self.equipment)
        self.line_3.setGeometry(QtCore.QRect(540, 30, 300, 16))
        self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.equipment_management_info_label = QtWidgets.QLabel(self.equipment)
        self.equipment_management_info_label.setGeometry(QtCore.QRect(550, 240, 531, 16))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.equipment_management_info_label.setFont(font)
        self.equipment_management_info_label.setObjectName("equipment_management_info_label")
        self.delete_button_ylikou = QtWidgets.QPushButton(self.equipment)
        self.delete_button_ylikou.setGeometry(QtCore.QRect(600, 130, 220, 31))
        self.delete_button_ylikou.setObjectName("delete_button_ylikou")
        self.id_ylikou_management_label = QtWidgets.QLabel(self.equipment)
        self.id_ylikou_management_label.setGeometry(QtCore.QRect(580, 80, 91, 16))
        self.id_ylikou_management_label.setObjectName("id_ylikou_management_label")
        self.id_ylikou_management_input = QtWidgets.QLineEdit(self.equipment)
        self.id_ylikou_management_input.setGeometry(QtCore.QRect(820, 80, 113, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(8)
        font.setBold(False)
        font.setWeight(50)
        self.id_ylikou_management_input.setFont(font)
        self.id_ylikou_management_input.setObjectName("id_ylikou_management_input")
        self.edit_button_ylikou = QtWidgets.QPushButton(self.equipment)
        self.edit_button_ylikou.setGeometry(QtCore.QRect(850, 130, 220, 31))
        self.edit_button_ylikou.setObjectName("edit_button_ylikou")
        #Create equipment lend button
        self.lend_button_ylikou = QtWidgets.QPushButton(self.equipment)
        self.lend_button_ylikou.setGeometry(QtCore.QRect(850, 180, 220, 31))
        self.lend_button_ylikou.setObjectName("lend_button_ylikou")
        self.lend_button_ylikou.setText('Δανεισμός Υλικού')
        self.lend_button_ylikou.clicked.connect(self.lend_equip)
        #Link edit button to func
        self.edit_button_ylikou.clicked.connect(self.checkedit)
        self.pushButton = QtWidgets.QPushButton(self.equipment)
        self.pushButton.setGeometry(QtCore.QRect(290, 200, 181, 31))
        self.pushButton.setObjectName("pushButton")
        self.tabWidget.addTab(self.equipment, "")
        self.logged_in_as_label = QtWidgets.QLabel(self.centralwidget)
        self.logged_in_as_label.setGeometry(QtCore.QRect(650, 620, 121, 21))
        font = QtGui.QFont()
        font.setFamily("Myriad Pro")
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
        self.User_name_Label.setGeometry(QtCore.QRect(800, 620, 81, 21))
        font = QtGui.QFont()
        font.setFamily("Palatino Linotype")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.User_name_Label.setFont(font)
        self.User_name_Label.setScaledContents(False)
        self.User_name_Label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.User_name_Label.setWordWrap(False)
        self.User_name_Label.setObjectName("User_name_Label")
        Admin.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(Admin)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1120, 26))
        self.menubar.setObjectName("menubar")
        Admin.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(Admin)
        self.statusbar.setObjectName("statusbar")
        Admin.setStatusBar(self.statusbar)

        self.retranslateUi(Admin)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Admin)

    def retranslateUi(self, Admin):
        _translate = QtCore.QCoreApplication.translate
        Admin.setWindowTitle(_translate("Admin", "Admin Access "))
        item = self.user_table.horizontalHeaderItem(0)
        item.setText(_translate("Admin", "ID Χρήστη"))
        item = self.user_table.horizontalHeaderItem(1)
        item.setText(_translate("Admin", "Username"))
        item = self.user_table.horizontalHeaderItem(2)
        item.setText(_translate("Admin", "Password"))
        item = self.user_table.horizontalHeaderItem(3)
        item.setText(_translate("Admin", "Email"))
        item = self.user_table.horizontalHeaderItem(4)
        item.setText(_translate("Admin", "Αριθμός Τηλεφώνου"))
        item = self.user_table.horizontalHeaderItem(5)
        item.setText(_translate("Admin", "Όνομα"))
        item = self.user_table.horizontalHeaderItem(6)
        item.setText(_translate("Admin", "Επίθετο"))
        item = self.user_table.horizontalHeaderItem(7)
        item.setText(_translate("Admin", "Επίπεδο Πρόσβασης"))
        item = self.user_table.horizontalHeaderItem(8)
        item.setText(_translate("Admin", "ID Χώρων Πρόσβασης"))
        self.search_label_2.setText(_translate("Admin", "Αναζήτηση Χρήστη"))
        self.label_usersearch_onoma.setText(_translate("Admin", "Όνομα Χρήστη :"))
        self.label_usersearch_epitheto.setText(_translate("Admin", "Επίθετο Χρήστη :"))
        self.label_usersearch_tilefono.setText(_translate("Admin", "Τηλέφωνο Χρήστη :"))
        self.label_usersearch_email.setText(_translate("Admin", "Email Χρήστη :"))
        self.label_usersearch_id_xwrwn.setText(_translate("Admin", "ID Χώρων Πρόσβασης Χρήστη(χωρίστε με κόμμα) :"))
        self.user_rights_management_label.setText(_translate("Admin", "Ορισμός Δικαιωμάτων Χρηστών"))
        self.rights_management_userid_label.setText(_translate("Admin", "ID Χρήστη :"))
        self.rights_management_access_level_label.setText(_translate("Admin", "Επιθυμητό Επίπεδο Πρόσβασης :"))
        self.rights_management_id_xwrwn_label.setText(_translate("Admin", "ID Χώρων Πρόσβασης Χρήστη(χωρίστε με κόμμα) :"))
        self.rights_management_button.setText(_translate("Admin", "Ορισμός Δικαιωμάτων"))
        # Call set privileges function on click
        self.rights_management_button.clicked.connect(self.set_user_privileges)
        self.user_search_info_label.setText(_translate("Admin", "Για αναζήτηση εισάγετε 2 τουλάχιστον στοιχεία χρήστη."))
        self.user_management_info_label.setText(_translate("Admin", "Εισάγετε τα απαραίτητα στοιχεία για ορισμό δικαιωμάτων."))
        self.user_search_button.setText(_translate("Admin", "Αναζήτηση Χρηστη"))
        self.clear_search_button.setText(_translate("Admin", "Καθαρισμός"))
        # Connect user search function on button and clear search on clear button
        self.user_search_button.clicked.connect(self.search_for_user)
        self.clear_search_button.clicked.connect(self.clear_Search_user)
        self.pushButton_2.setText(_translate("Admin", "Αφαίρεση Δικαιωμάτων"))
        # Call delete_rights function on click
        self.pushButton_2.clicked.connect(self.delete_rights)
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.users), _translate("Admin", "Διαχείριση Χρηστών"))
        item = self.areas_table.horizontalHeaderItem(0)
        item.setText(_translate("Admin", "ID Χώρου"))
        item = self.areas_table.horizontalHeaderItem(1)
        item.setText(_translate("Admin", "Χρήση Χώρου"))
        item = self.areas_table.horizontalHeaderItem(2)
        item.setText(_translate("Admin", "Ονομασία Χώρου"))
        # set column width
        self.areas_table.setColumnWidth(0, 150)
        self.areas_table.setColumnWidth(1, 200)
        self.areas_table.setColumnWidth(2, 205)
        # item = self.areas_table.horizontalHeaderItem(3)
        # item.setText(_translate("Admin", "ID Επόπτη"))
        self.areas_management_label.setText(_translate("Admin", "Διαχείριση Χώρων"))
        self.areas_management_area_name_label.setText(_translate("Admin", "Ονομασία Χώρου:"))
        self.areas_management_useofarea_label.setText(_translate("Admin", "Χρήση Χώρου :"))
        self.areas_search_button.setText(_translate("Admin", "Αναζήτηση Χώρου"))
        # Link area search button to function
        self.areas_search_button.clicked.connect(self.search_for_area)
        self.areas_insert_button.setText(_translate("Admin", "Προσθήκη Χώρου"))
        # Link area insert button to function
        self.areas_insert_button.clicked.connect(self.insert_area)
        self.area_delete_label.setText(_translate("Admin", "Διαγραφή Χώρου"))
        self.area_delete_id_label.setText(_translate("Admin", "ID Χώρου :"))
        self.area_delete_button.setText(_translate("Admin", "Διαγραφή Χώρου"))
        # Link area delete button to function
        self.area_delete_button.clicked.connect(self.delete_area)
        self.area_supervisor_search_label.setText(_translate("Admin", "Αναζήτηση Επόπτη Χώρου"))
        self.area_supervisor_id_search_label.setText(_translate("Admin", "ID Χώρου :"))
        self.area_supervisor_search_button.setText(_translate("Admin", "Αναζήτηση Επόπτη"))
        #Link area supervisor search function to button
        self.area_supervisor_search_button.clicked.connect(self.search_for_supervisor)
        item = self.area_supervisor_table.horizontalHeaderItem(0)
        item.setText(_translate("Admin", "ID Επόπτη"))
        item = self.area_supervisor_table.horizontalHeaderItem(1)
        item.setText(_translate("Admin", "Όνομα"))
        item = self.area_supervisor_table.horizontalHeaderItem(2)
        item.setText(_translate("Admin", "Επίθετο"))
        item = self.area_supervisor_table.horizontalHeaderItem(3)
        item.setText(_translate("Admin", "Email"))
        self.areas_clearsearch_button.setText(_translate("Admin", "Καθαρισμός"))
        self.supervisor_clearsearch_button.setText(_translate("Admin", "Καθαρισμός"))
        self.label.setText(_translate("Admin", "Εισάγετε στοιχεία για διαχείριση χώρου."))
        self.label_2.setText(_translate("Admin", "Εισάγετε ID χώρου για διαγραφή."))
        self.label_4.setText(_translate("Admin", "Εισάγετε ID χώρου για αναζήτηση επόπτη."))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.areas), _translate("Admin", "Διαχείριση Χώρων"))
        self.equipment_table.setSortingEnabled(False)
        # Connect Clear Areas Search to Function/Set Button text
        self.areas_clearsearch_button.clicked.connect(self.clear_area_data)
        # Connect Clear Supervisor Area Search to Function/Set Button text
        self.supervisor_clearsearch_button.clicked.connect(self.clear_supervisor_data)
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
        #Set Columns Width
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
        self.search_label.setText(_translate("Admin", "Αναζήτηση Υλικών"))
        self.equip_search_info_label.setText(_translate("Admin", "Πραγματοποιήστε αναζήτηση,ή προσθέστε υλικό."))
        self.label_search_xwrou.setText(_translate("Admin", "ID Χώρου(Απαραίτητο για Προσθήκη):"))
        self.label_search_yliko.setText(_translate("Admin", "Τύπος Υλικού(Απαραίτητο για Προσθήκη):"))
        self.label_search_daneismos.setText(_translate("Admin", "Κατάσταση Δανεισμού :"))
        self.label_search_keywords.setText(_translate("Admin", "Λέξεις Κλειδιά(χωρίστε με κόμμα) :"))
        self.label_search_katigoria_ylikou.setText(_translate("Admin", "Κατηγορία Υλικού :"))
        self.equipment_search_button.setText(_translate("Admin", "Αναζήτηση Υλικού"))
        #Link search equip/material button to function
        self.equipment_search_button.clicked.connect(self.search_for_equipment)
        self.equipment_management_label.setText(_translate("Admin", "Διαχείριση Υλικών"))
        self.equipment_management_info_label.setText(_translate("Admin", "Εισάγετε ID υλικού για διαγραφή ή επεξεργασία. "))
        self.delete_button_ylikou.setText(_translate("Admin", "Διαγραφή Υλικού"))
        #Link del button to func
        self.delete_button_ylikou.clicked.connect(self.delete_equipment)
        self.id_ylikou_management_label.setText(_translate("Admin", "ID Υλικού :"))
        self.edit_button_ylikou.setText(_translate("Admin", "Επεξεργασία Υλικού"))
        self.pushButton.setText(_translate("Admin", "Προσθήκη Υλικού"))
        #Link Add equipment/material button to checktype function
        self.pushButton.clicked.connect(self.check_equip_input)
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.equipment), _translate("Admin", "Διαχείριση Υλικού Χώρων"))
        self.logged_in_as_label.setText(_translate("Admin", "Logged in as:"))
        self.User_name_Label.setText(_translate("Admin", "Admin"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Admin = QtWidgets.QMainWindow()
    ui = Ui_Admin()
    ui.setupUi(Admin)
    ui.load_users_Data()
    ui.load_areas_Data()
    ui.load_equipment_data()
    ui.load_supervisor_Data()
    ui.tabWidget.setCurrentIndex(0)
    Admin.show()
    sys.exit(app.exec_())

