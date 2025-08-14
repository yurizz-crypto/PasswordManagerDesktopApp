from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, 
                               QLineEdit, QPushButton, QLabel, 
                               QTextEdit, QFormLayout, QMessageBox,
                               QCheckBox)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QPixmap, QIcon
import random
import string

class AddPasswordDialog(QDialog):
    password_added = Signal()
    
    def __init__(self, api_client):
        super().__init__()
        self.api_client = api_client
        self.setWindowTitle("Add New Password")
        self.setFixedSize(500, 400)
        self.setModal(True)
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Title
        title = QLabel("Add New Password Entry")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 18px; font-weight: bold; margin: 10px;")
        
        # Form
        form_layout = QFormLayout()
        
        # Site Name (Required)
        self.site_name_input = QLineEdit()
        self.site_name_input.setPlaceholderText("e.g., Google, Facebook, GitHub")
        
        # Site URL (Optional)
        self.site_url_input = QLineEdit()
        self.site_url_input.setPlaceholderText("e.g., https://www.google.com")
        
        # Username (Required)
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Your username or email")
        
        # Password (Required)
        password_layout = QHBoxLayout()
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter your password")
        self.password_input.setEchoMode(QLineEdit.Password)
        
        # Show/Hide password button
        self.show_password_btn = QPushButton("Show")
        self.show_password_btn.setFixedWidth(60)
        self.show_password_btn.clicked.connect(self.toggle_password_visibility)
        
        # Generate password button
        self.generate_btn = QPushButton("Generate")
        self.generate_btn.setFixedWidth(70)
        self.generate_btn.clicked.connect(self.generate_password)
        
        password_layout.addWidget(self.password_input)
        password_layout.addWidget(self.show_password_btn)
        password_layout.addWidget(self.generate_btn)
        # Notes (Optional)
        self.notes_input = QTextEdit()
        self.notes_input.setPlaceholderText("Optional notes about this account...")
        self.notes_input.setMaximumHeight(80)
        
        form_layout.addRow("Site Name *:", self.site_name_input)
        form_layout.addRow("Site URL:", self.site_url_input)
        form_layout.addRow("Username *:", self.username_input)
        form_layout.addRow("Password *:", password_layout)
        form_layout.addRow("Notes:", self.notes_input)
        
        # Required fields note
        required_note = QLabel("* Required fields")
        required_note.setStyleSheet("color: #666; font-size: 12px;")
        
        # Buttons
        button_layout = QHBoxLayout()
        
        self.save_btn = QPushButton("Save Password")
        self.cancel_btn = QPushButton("Cancel")
        
        self.save_btn.clicked.connect(self.save_password)
        self.cancel_btn.clicked.connect(self.reject)
        
        # Make save button more prominent
        self.save_btn.setStyleSheet("QPushButton { background-color: #4CAF50; color: white; font-weight: bold; }")
        
        button_layout.addWidget(self.cancel_btn)
        button_layout.addWidget(self.save_btn)
        
        layout.addWidget(title)
        layout.addLayout(form_layout)
        layout.addWidget(required_note)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
        
        # Set focus to first field
        self.site_name_input.setFocus()
    
    def toggle_password_visibility(self):
        """Toggle password visibility"""
        if self.password_input.echoMode() == QLineEdit.Password:
            self.password_input.setEchoMode(QLineEdit.Normal)
            self.show_password_btn.setText("Hide")
        else:
            self.password_input.setEchoMode(QLineEdit.Password)
            self.show_password_btn.setText("Show")
    
    def generate_password(self):
        """Generate a secure random password"""
        length = 16
        characters = string.ascii_letters + string.digits + "!@#$%^&*"
        
        # Ensure password has at least one of each type
        password = [
            random.choice(string.ascii_lowercase),
            random.choice(string.ascii_uppercase),
            random.choice(string.digits),
            random.choice("!@#$%^&*")
        ]
        
        # Fill the rest randomly
        for _ in range(length - 4):
            password.append(random.choice(characters))
        
        # Shuffle the password
        random.shuffle(password)
        generated_password = ''.join(password)
        
        self.password_input.setText(generated_password)
        
        # Temporarily show the generated password
        if self.password_input.echoMode() == QLineEdit.Password:
            self.password_input.setEchoMode(QLineEdit.Normal)
            self.show_password_btn.setText("Hide")
    
    def save_password(self):
        """Save the password entry"""
        # Get form data
        site_name = self.site_name_input.text().strip()
        site_url = self.site_url_input.text().strip()
        username = self.username_input.text().strip()
        password = self.password_input.text()
        notes = self.notes_input.toPlainText().strip()
        
        # Validate required fields
        if not site_name:
            QMessageBox.warning(self, "Error", "Site name is required")
            self.site_name_input.setFocus()
            return
        
        if not username:
            QMessageBox.warning(self, "Error", "Username is required")
            self.username_input.setFocus()
            return
        
        if not password:
            QMessageBox.warning(self, "Error", "Password is required")
            self.password_input.setFocus()
            return
        
        # Try to save
        result = self.api_client.create_password(
            site_name=site_name,
            site_url=site_url,
            username=username,
            password=password,
            notes=notes
        )
        
        if 'error' in result:
            QMessageBox.critical(self, "Error", f"Failed to save password: {result['error']}")
        else:
            QMessageBox.information(self, "Success", "Password saved successfully!")
            self.password_added.emit()
            self.accept()