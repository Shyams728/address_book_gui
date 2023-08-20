---

# Address Book GUI using PyQt5 and MySQL

This Python script utilizes the PyQt5 library to create a straightforward graphical user interface (GUI) for managing an address book. The GUI enables users to perform tasks such as adding, updating, deleting, and searching for contacts within the address book. Additionally, the application integrates with a MySQL database to store contact information.

## Code Breakdown

### 1. Import Statements

- `import sys`: Imports the `sys` module, granting access to interpreter-related variables and functions.
- `import mysql.connector as sql`: Imports the MySQL Connector library for interacting with MySQL databases.
- `from PyQt5.QtWidgets import ...`: Imports various classes from `PyQt5.QtWidgets`, providing UI components for desktop application development.

### 2. Class Definition - AddressBookGUI

- Inherits from `QWidget`, the base class for all PyQt UI objects.
- `__init__`: Constructor initializing the GUI by calling the `initUI` method.
- `initUI`: Sets up the entire GUI layout using a grid structure, creating labels, text fields, buttons, and other UI components.
- UI components are categorized into sections (e.g., Name, Work, Cell) with corresponding labels and input fields.
- Buttons like "Add Contact," "Update Contact," "Delete Contact," and "Search Contact" are established and linked to relevant functions.

### 3. Class Definition - Database

- Defines methods for interacting with the MySQL database:
  - `__init__`: Initializes a connection to the MySQL database.
  - `insert_data`: Inserts contact data into the database.
  - `delete_data`: Deletes contact data from the database.
  - `update_data`: Updates contact data in the database.
  - `search_data`: Searches for contact data in the database.
  - `show_data`: Shows all the contacts data in the database.

### 4. Class Definition - ShowDataDialog

- Inherits from `QDialog`, creating a dialog window to display contact data in a table format.
- `__init__`: Constructor initializing the dialog window by calling the `initUI` method.
- `initUI`: Sets up the table widget and loads data from the database.

### 5. Event Handling Functions

- Functions (`addContact`, `updateContact`, `deleteContact`, `searchContact`) manage adding, updating, deleting, and searching contacts in the MySQL database.

### 6. Main Execution Block

- The code within the `if __name__ == '__main__':` block executes when the script is directly run (not imported).
- An `QApplication` instance `app` is created, managing the GUI application.
- An `AddressBookGUI` instance `window` is established.
- The `show` method is invoked on `window` to display the GUI.
- The `sys.exit(app.exec_())` line enters the main event loop, sustaining the GUI until the user closes the application.

## Summary

This code generates an address book application featuring a user-friendly interface for adding, updating, deleting, and searching contacts. The GUI elements are structured using a grid layout, while contact data is stored in a MySQL database. The PyQt5 library empowers developers to craft the graphical interface and manage user interactions effectively.

# Address Book Application

The Address Book Application is a graphical user interface (GUI) program built using PyQt5 and MySQL. It allows users to manage their contacts by adding, updating, deleting, and searching for contact information.

## Features

- Add new contacts with details such as name, gender, profession, contact numbers, email, birthday, address, city, state, pincode, and notes.
- Update existing contacts with updated information.
- Delete contacts from the address book.
- Search for contacts based on their names and view their details.
- Display a table view of all contacts for easy visualization.
- Apply a modern "Fusion" style for a sleek user interface.

## Requirements

- Python 3.11.x
- PyQt5
- MySQL Connector (Python package)
- MySQL server
- MySQL Workbench

## Installation

1. Clone or download the repository to your local machine.
2. Install the required Python packages using the following command:
   ```bash
   pip install pyqt5 mysql-connector-python
   ```
3. Set up a MySQL server and create a database named `addressbook`.
4. Modify the database connection details in the code (`Database` class) to match your MySQL server configuration.

## Usage

1. Run the program using the following command:
   ```bash
   python address_book.py
   ```
2. The GUI window of the Address Book Application will appear.
3. Use the various buttons and fields to perform actions such as adding, updating, and deleting contacts.
4. You can also search for contacts and view their details.
5. To display a table view of all contacts, click the "Show Data" button.

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or create a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

This program was created as a sample application using PyQt5 and MySQL for enhancing skill set under the guidence of GUVI EdTech.

---

