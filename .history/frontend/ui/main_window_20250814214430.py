from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, 
                               QTableWidget, QTableWidgetItem, QPushButton, 
                               QLabel, QMessageBox, QHeaderView)
from PySide6.QtCore import Qt
from controllers.api_client import APIClient

class MainWindow(QWidget):
    def __init__(self, api_client: APIClient):
        super().__init__()
        self.api_client = api_client
        self.setWindowTitle("Password Manager - My Passwords")
        self.setGeometry(100, 100, 800, 600)
        self.init_ui()
        self.load_passwords()
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Header
        header = QLabel("My Password Vault")
        header.setAlignment(Qt.AlignCenter)
        header.setStyleSheet("font-size: 20px; font-weight: bold; margin: 10px;")
        
        # Table for passwords
        self.password_table = QTableWidget()
        self.password_table.setColumnCount(4)
        self.password_table.setHorizontalHeaderLabels(['Site Name', 'Username', 'URL', 'Notes'])
        
        # Make table fill the space
        header_view = self.password_table.horizontalHeader()
        header_view.setSectionResizeMode(0, QHeaderView.Stretch)
        header_view.setSectionResizeMode(1, QHeaderView.Stretch)
        header_view.setSectionResizeMode(2, QHeaderView.Stretch)
        header_view.setSectionResizeMode(3, QHeaderView.Stretch)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        self.add_btn = QPushButton("Add Password")
        self.edit_btn = QPushButton("Edit Selected")
        self.delete_btn = QPushButton("Delete Selected")
        self.refresh_btn = QPushButton("Refresh")
        self.logout_btn = QPushButton("Logout")
        
        self.add_btn.clicked.connect(self.add_password)
        self.edit_btn.clicked.connect(self.edit_password)
        self.delete_btn.clicked.connect(self.delete_password)
        self.refresh_btn.clicked.connect(self.load_passwords)
        self.logout_btn.clicked.connect(self.logout)
        
        button_layout.addWidget(self.add_btn)
        button_layout.addWidget(self.edit_btn)
        button_layout.addWidget(self.delete_btn)
        button_layout.addWidget(self.refresh_btn)
        button_layout.addStretch()
        button_layout.addWidget(self.logout_btn)
        
        layout.addWidget(header)
        layout.addWidget(self.password_table)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
    
    def load_passwords(self):
        """Load passwords from API"""
        result = self.api_client.get_passwords()
        
        if 'error' in result:
            QMessageBox.critical(self, "Error", f"Failed to load passwords: {result['error']}")
            return
        
        # Clear table
        self.password_table.setRowCount(0)
        
        # Populate table
        passwords = result if isinstance(result, list) else []
        self.password_table.setRowCount(len(passwords))
        
        for row, password in enumerate(passwords):
            self.password_table.setItem(row, 0, QTableWidgetItem(password.get('site_name', '')))
            self.password_table.setItem(row, 1, QTableWidgetItem(password.get('username', '')))
            self.password_table.setItem(row, 2, QTableWidgetItem(password.get('site_url', '')))
            self.password_table.setItem(row, 3, QTableWidgetItem(password.get('notes', '')))
            
            # Store password ID in first column for later use
            item = self.password_table.item(row, 0)
            if item:
                item.setData(Qt.UserRole, password.get('id'))
    
    def add_password(self):
        QMessageBox.information(self, "Info", "Add password dialog coming soon!")
    
    def edit_password(self):
        current_row = self.password_table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Warning", "Please select a password to edit")
            return
        
        QMessageBox.information(self, "Info", "Edit password dialog coming soon!")
    
    def delete_password(self):
        current_row = self.password_table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Warning", "Please select a password to delete")
            return
        
        # Get password ID
        item = self.password_table.item(current_row, 0)
        if not item:
            return
        
        password_id = item.data(Qt.UserRole)
        site_name = item.text()
        
        # Confirm deletion
        reply = QMessageBox.question(self, "Confirm Delete", 
                                   f"Are you sure you want to delete the password for '{site_name}'?",
                                   QMessageBox.Yes | QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            result = self.api_client.delete_password(password_id)
            
            if 'error' in result:
                QMessageBox.critical(self, "Error", f"Failed to delete password: {result['error']}")
            else:
                QMessageBox.information(self, "Success", "Password deleted successfully!")
                self.load_passwords()  # Refresh the list
    
    def logout(self):
        self.api_client.logout()
        self.close()
        
        # Show login window again (we'll implement this properly later)
        QMessageBox.information(self, "Info", "Logged out successfully! Please restart the application to login again.")