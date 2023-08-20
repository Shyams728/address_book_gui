import sys
import mysql.connector as sql
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QGridLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QTextEdit,
    QListWidget,
    QDateEdit,
    QComboBox,
    QTableWidget,
    QTableWidgetItem,
    QDialog,
    QVBoxLayout,
    QMessageBox,
)
from PyQt5.QtGui import QPalette, QIcon
from PyQt5.QtCore import Qt
import datetime
import re
import pandas as pd


class Database:
    def __init__(self):
        self.mysql_connect = sql.connect(
            host="localhost", user="root", password="shy@123", database="addressbook"
        )

    def insert_data(self, data):
        query = (
            "INSERT INTO contacts (name, gender, work, cell, home, email, birthday, address, city, state, pincode, note) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        )
        with self.mysql_connect.cursor() as cursor:
            cursor.execute(query, data)
            self.mysql_connect.commit()

        return cursor.lastrowid

    def delete_data(self, name):
        query = f"DELETE FROM contacts WHERE name='{name}'"

        with self.mysql_connect.cursor() as cursor:
            cursor.execute(query)
            self.mysql_connect.commit()

        return cursor.lastrowid

    def update_data(self, data):
        query = (
            "UPDATE contacts SET name=%s, gender=%s, work=%s, cell=%s, home=%s, email=%s, birthday=%s, address=%s, "
            "city=%s, state=%s, pincode=%s, note=%s WHERE contact_id=%s"
        )
        with self.mysql_connect.cursor() as cursor:
            cursor.execute(query, data)
            self.mysql_connect.commit()

        return cursor.rowcount

    def search_data(self, name):
        query = "SELECT contact_id, name, gender, work, cell, home, email, birthday, address, city, state, pincode FROM contacts WHERE name LIKE %s"
        data = ("%" + name + "%",)

        with self.mysql_connect.cursor() as cursor:
            cursor.execute(query, data)
            results = cursor.fetchall()

        return results


class ShowDataDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Show Contacts Data")
        self.setWindowIcon(QIcon("database.png"))
        self.setGeometry(100, 100, 800, 400)
        self.initUI()

    def initUI(self):
        self.tableWidget = QTableWidget()
        self.loadData()

        layout = QVBoxLayout()
        layout.addWidget(self.tableWidget)
        self.setLayout(layout)

    def loadData(self):
        database = Database()
        query = "SELECT * FROM contacts"
        df = pd.read_sql(query, database.mysql_connect)

        self.tableWidget.setRowCount(len(df))
        self.tableWidget.setColumnCount(len(df.columns))
        self.tableWidget.setHorizontalHeaderLabels(df.columns)

        for row_idx, row in df.iterrows():
            for col_idx, value in enumerate(row):
                item = QTableWidgetItem(str(value))
                self.tableWidget.setItem(row_idx, col_idx, item)

    # Apply the "Fusion" style for a modern look
    QApplication.setStyle("Fusion")

    # Create a palette for customization
    palette = QPalette()

    # Customize colors
    palette.setColor(QPalette.Window, Qt.white)
    palette.setColor(QPalette.WindowText, Qt.black)
    palette.setColor(QPalette.Button, Qt.lightGray)
    palette.setColor(QPalette.ButtonText, Qt.black)
    palette.setColor(QPalette.Highlight, Qt.blue)
    palette.setColor(QPalette.HighlightedText, Qt.white)

    # Set the palette for the application
    QApplication.setPalette(palette)


class AddressBookGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, 600, 400)
        self.setWindowTitle("Address Book")
        self.setWindowIcon(QIcon("address_book.png"))

        state_names = ["---- Select State / UT ----"] + sorted(
            [
                "Dadra and Nagar Haveli and Daman and Diu",
                "West Bengal",
                "Arunachal Pradesh",
                "Puducherry",
                "Kerala",
                "Uttar Pradesh",
                "Mizoram",
                "Meghalaya",
                "Goa",
                "Bihar",
                "Tripura",
                "Nagaland",
                "Delhi",
                "Chandigarh",
                "Tamil Nadu",
                "Jharkhand",
                "Sikkim",
                "Maharashtra",
                "Uttarakhand",
                "Ladakh",
                "Rajasthan",
                "Madhya Pradesh",
                "Manipur",
                "Andaman and Nicobar Islands",
                "Assam",
                "Punjab",
                "Odisha",
                "Telangana",
                "Jammu and Kashmir",
                "Himachal Pradesh",
                "Karnataka",
                "Andhra Pradesh",
                "Haryana",
                "Lakshadweep",
                "Gujarat",
                "Chhattisgarh",
            ]
        )

        self.nameLabel = QLabel("Name:")
        self.nameLineEdit = QLineEdit()

        self.genderLabel = QLabel("Gender:")
        self.genderComboBox = QComboBox()
        self.genderComboBox.addItems(["♂ Male", "♀ Female", "⚧ Other"])

        self.workLabel = QLabel("Profession:")
        self.workLineEdit = QLineEdit()

        self.cellLabel = QLabel("Cell:")
        self.cellLineEdit = QLineEdit()
        self.cellLineEdit.textChanged.connect(self.on_cell_changed)

        self.homeLabel = QLabel("Home:")
        self.homeLineEdit = QLineEdit()

        self.emailLabel = QLabel("Email:")
        self.emailLineEdit = QLineEdit()
        self.emailLineEdit.textChanged.connect(self.on_email_changed)

        self.birthdayLabel = QLabel("Birthday:")
        self.birthdayLineEdit = QDateEdit()
        self.birthdayLineEdit.setCalendarPopup(True)

        self.addressLabel = QLabel("Address:")
        self.addressLineEdit = QLineEdit()

        self.cityLabel = QLabel("City:")
        self.cityLineEdit = QLineEdit()

        self.stateLabel = QLabel("State:")
        self.stateComboBox = QComboBox()
        self.stateComboBox.addItems(state_names)
        self.stateComboBox.currentTextChanged.connect(self.on_state_changed)

        self.pincodeLabel = QLabel("Pincode:")
        self.pincodeLineEdit = QLineEdit()
        self.pincodeLineEdit.textChanged.connect(self.on_pincode_changed)

        self.noteLabel = QLabel("Note:")
        self.noteTextEdit = QTextEdit()

        self.addButton = QPushButton("Add Contact")
        self.addButton.clicked.connect(self.addContact)

        self.updateButton = QPushButton("Update Contact")
        self.updateButton.clicked.connect(self.updateContact)

        self.deleteButton = QPushButton("Delete Contact")
        self.deleteButton.clicked.connect(self.deleteContact)

        self.searchButton = QPushButton("Search Contact")
        self.searchButton.clicked.connect(self.searchContact)

        self.showDataButton = QPushButton("Show Data")
        self.showDataButton.clicked.connect(self.showDataDialog)

        self.layout = QGridLayout()

        self.layout.addWidget(self.nameLabel, 0, 0)
        self.layout.addWidget(self.nameLineEdit, 0, 1, 1, 3)
        self.layout.addWidget(self.genderLabel, 1, 0)
        self.layout.addWidget(self.genderComboBox, 1, 1)
        self.layout.addWidget(self.birthdayLabel, 1, 2)
        self.layout.addWidget(self.birthdayLineEdit, 1, 3)
        self.layout.addWidget(self.workLabel, 2, 0)
        self.layout.addWidget(self.workLineEdit, 2, 1)
        self.layout.addWidget(self.cellLabel, 2, 2)
        self.layout.addWidget(self.cellLineEdit, 2, 3)
        self.layout.addWidget(self.homeLabel, 3, 0)
        self.layout.addWidget(self.homeLineEdit, 3, 1)
        self.layout.addWidget(self.emailLabel, 3, 2)
        self.layout.addWidget(self.emailLineEdit, 3, 3)
        self.layout.addWidget(self.addressLabel, 5, 0)
        self.layout.addWidget(self.addressLineEdit, 5, 1, 1, 3)
        self.layout.addWidget(self.cityLabel, 6, 0)
        self.layout.addWidget(self.cityLineEdit, 6, 1)
        self.layout.addWidget(self.stateLabel, 6, 2)
        self.layout.addWidget(self.stateComboBox, 6, 3)
        self.layout.addWidget(self.pincodeLabel, 7, 0)
        self.layout.addWidget(self.pincodeLineEdit, 7, 1)
        self.layout.addWidget(self.noteLabel, 8, 0)
        self.layout.addWidget(self.noteTextEdit, 8, 1, 1, 3)
        self.layout.addWidget(self.addButton, 9, 0)
        self.layout.addWidget(self.updateButton, 9, 1)
        self.layout.addWidget(self.deleteButton, 9, 2)
        self.layout.addWidget(self.searchButton, 9, 3)
        self.layout.addWidget(self.showDataButton, 10, 0, 1, 4)

        self.setLayout(self.layout)

        """'***********************using Regex Validating data formats*************************************"""

    def check_email_format(self, email):
        regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)*$"
        return re.match(regex, email)

    def on_email_changed(self, email):
        valid = self.check_email_format(email)
        if not valid:
            self.emailLabel.setStyleSheet("color: red")
            self.emailLabel.setText("Invalid email address")
        else:
            self.emailLabel.setStyleSheet("color: black")
            self.emailLabel.setText("Valid email address")

    def check_indian_cell_format(self, cell):
        cell = cell.replace(" ", "")
        regex = r"^(?:\+91|0)?[6789]\d{9}$"
        return re.match(regex, cell) is not None

    def on_cell_changed(self, cell):
        valid = self.check_indian_cell_format(cell)
        if not valid:
            self.cellLabel.setStyleSheet("color: red")
            self.cellLabel.setText("Invalid Indian cell number")
        else:
            self.cellLabel.setStyleSheet("color: black")
            self.cellLabel.setText("Cell Number")

    def check_pincode_format(self, pincode):
        # Remove spaces from the input
        pincode = pincode.replace(" ", "")

        # Check if pincode is 6 digits
        if pincode.isdigit() and len(pincode) == 6:
            return True
        return False

    def on_pincode_changed(self, pincode):
        valid = self.check_pincode_format(pincode)
        if not valid:
            self.pincodeLabel.setStyleSheet("color: red")
            self.pincodeLabel.setText("Invalid pincode (6 digits required)")
        else:
            self.pincodeLabel.setStyleSheet("color: black")
            self.pincodeLabel.setText("Valid pincode")

    def on_state_changed(self, state):
        if state == "---- Select State / UT ----":
            self.stateLabel.setStyleSheet("color: red")
            self.stateLabel.setText("select the state")
        else:
            self.stateLabel.setStyleSheet("color: black")
            self.stateLabel.setText("State")

        """**************************************************************"""

    # method to show the ShowDataDialog
    def showDataDialog(self):
        show_data_dialog = ShowDataDialog()
        show_data_dialog.exec_()

    def addContact(self):
        name = self.nameLineEdit.text().strip().title()
        gender_qt = self.genderComboBox.currentText()
        # to remove special charecter
        gender = re.sub(r"[^\w\s]", "", gender_qt)
        work = self.workLineEdit.text()
        cell = self.cellLineEdit.text()
        home = self.homeLineEdit.text()
        email = self.emailLineEdit.text()
        birthday_qdate = self.birthdayLineEdit.date()
        birthday = datetime.date(
            birthday_qdate.year(), birthday_qdate.month(), birthday_qdate.day()
        )
        address = self.addressLineEdit.text()
        city = self.cityLineEdit.text()
        state = self.stateComboBox.currentText()
        pincode = self.pincodeLineEdit.text()
        note = self.noteTextEdit.toPlainText()

        data = (
            name,
            gender,
            work,
            cell,
            home,
            email,
            birthday,
            address,
            city,
            state,
            pincode,
            note,
        )
        contact_id = Database().insert_data(data)

        if contact_id > 0:
            self.listWidget.addItem(f"{name} ({contact_id})")
            self.nameLineEdit.clear()
            self.genderComboBox.setCurrentIndex(0)
            self.cellLineEdit.clear()
            self.homeLineEdit.clear()
            self.emailLineEdit.clear()
            self.birthdayLineEdit.setDate(datetime.date.today())
            self.addressLineEdit.clear()
            self.cityLineEdit.clear()
            self.stateComboBox.setCurrentIndex(0)
            self.pincodeLineEdit.clear()
            self.noteTextEdit.clear()

            QMessageBox.information(
                self, "Success", f"Contact {name} added successfully!"
            )
        else:
            QMessageBox.warning(self, "Error", "Failed to add contact!")

    def searchContact(self):
        name = self.nameLineEdit.text()

        results = Database().search_data(name)

        if len(results) == 0:
            QMessageBox.information(
                self, "Error", f"No contact found with name {name}!"
            )
        else:
            contact = results[0]  # Get the first tuple from results
            message_box = QMessageBox()
            message_box.setWindowTitle("Contact Details")
            message_box.setInformativeText(
                f"ID: {contact[0]}\nName: {contact[1]}\nGender: {contact[2]}\nProfession: {contact[3]}\nCell: {contact[4]}\nHome: {contact[5]}\nEmail: {contact[6]}\nBirthday: {contact[7]}\nAddress: {contact[8]}\nCity: {contact[9]}\nState: {contact[10]}\nPincode: {contact[11]}"
            )
            message_box.exec_()

    def updateContact(self):
        name_qt = self.nameLineEdit.text()
        name = name_qt.strip().title()

        if name:
            database = Database()
            results = database.search_data(name)

            if len(results) == 0:
                QMessageBox.information(
                    self, "Error", f"No contact found with name {name}!"
                )
            else:
                contact = results[0]  #first search result will be used for updating the data
                contact_id = contact[0]  # Extract the contact ID from the tuple
                gender_qt = self.genderComboBox.currentText()
                gender = re.sub(r"[^\w\s]", "", gender_qt) # to remove special  gender icon charecter
                work = self.workLineEdit.text()
                cell = self.cellLineEdit.text()
                home = self.homeLineEdit.text()
                email = self.emailLineEdit.text()
                birthday_qdate = self.birthdayLineEdit.date()
                birthday = datetime.date(
                    birthday_qdate.year(), birthday_qdate.month(), birthday_qdate.day()
                )
                address = self.addressLineEdit.text()
                city = self.cityLineEdit.text()
                state = self.stateComboBox.currentText()
                pincode = self.pincodeLineEdit.text()
                note = self.noteTextEdit.toPlainText()

                data = (
                    name,
                    gender,
                    work,
                    cell,
                    home,
                    email,
                    birthday,
                    address,
                    city,
                    state,
                    pincode,
                    note,
                    contact_id,
                )
                updated_rows = database.update_data(data)

                if updated_rows > 0:
                    QMessageBox.information(
                        self, "Success", f"Contact {name} updated successfully!"
                    )
                else:
                    QMessageBox.warning(self, "Error", "Failed to update contact!")

    def deleteContact(self):
        contact_name = self.nameLineEdit.text()
        if not contact_name:
            return

        confirmation = QMessageBox.question(
            self,
            "Confirm Deletion",
            f"Do you want to delete the contact '{contact_name}'?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )

        if confirmation == QMessageBox.Yes:
            Database().delete_data(contact_name)

            QMessageBox.information(
                self,
                "Contact Deleted",
                f"The contact '{contact_name}' has been deleted.",
                QMessageBox.Ok,
            )

    def showData(self):
        data = self.data
        dialog = ShowDataDialog(data)
        dialog.exec_()

    def show(self):
        super().show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AddressBookGUI()
    window.show()
    sys.exit(app.exec_())
