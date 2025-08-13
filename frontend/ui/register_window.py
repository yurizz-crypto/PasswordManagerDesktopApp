from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, 
                               QLineEdit, QPushButton, QLabel, 
                               QMessageBox, QFormLayout)
from PySide6.QtCore import Qt, Signal
from controllers.api_client import APIClient

class RegisterWindow(QWidget):
    registration_successful = Signal()
    
    def __init__(self):
        super().__init__()
        self.api_client = APIClient()
        self.setWindowTitle("Password Manager - Register")
        self.setFixedSize(450, 400)
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Title
        title = QLabel("Create New Account")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 24px; font-weight: bold; margin: 20px;")
        
        # Form
        form_layout = QFormLayout()
        
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Choose a username")
        
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Enter your email")
        
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Create a password")
        self.password_input.setEchoMode(QLineEdit.Password)
        
        self.confirm_password_input = QLineEdit()
        self.confirm_password_input.setPlaceholderText("Confirm your password")
        self.confirm_password_input.setEchoMode(QLineEdit.Password)
        
        form_layout.addRow("Username:", self.username_input)
        form_layout.addRow("Email:", self.email_input)
        form_layout.addRow("Password:", self.password_input)
        form_layout.addRow("Confirm Password:", self.confirm_password_input)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        self.register_btn = QPushButton("Register")
        self.cancel_btn = QPushButton("Cancel")
        
        self.register_btn.clicked.connect(self.register)
        self.cancel_btn.clicked.connect(self.close)
        
        button_layout.addWidget(self.register_btn)
        button_layout.addWidget(self.cancel_btn)
        
        layout.addWidget(title)
        layout.addLayout(form_layout)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
    
    def register(self):
        # Get input values
        username = self.username_input.text().strip()
        email = self.email_input.text().strip()
        password = self.password_input.text()
        confirm_password = self.confirm_password_input.text()
        
        # Validate inputs
        if not username or not email or not password or not confirm_password:
            QMessageBox.warning(self, "Error", "Please fill all fields")
            return
        
        if password != confirm_password:
            QMessageBox.warning(self, "Error", "Passwords do not match")
            return
        
        if len(password) < 8:
            QMessageBox.warning(self, "Error", "Password must be at least 8 characters long")
            return
        
        # Try to register
        result = self.api_client.register(email, username, password)
        
        if 'error' in result:
            QMessageBox.critical(self, "Registration Failed", str(result['error']))
        else:
            QMessageBox.information(self, "Success", "Account created successfully! You can now login.")
            self.registration_successful.emit()
            self.close()