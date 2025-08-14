from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, 
                               QLineEdit, QPushButton, QLabel, 
                               QTextEdit, QFormLayout, QMessageBox,
                               QCheckBox)
from PySide6.QtCore import Qt, Signal
import random
import string

class EditPasswordDialog(QDialog):
    password_updated = Signal()
    
    def __init__(self, api_client, password_data):
        super().__init__()
        self.api_client = api_client
        self.password_id = password_data.get('id')
        self.password_data = password_data
        self.setWindowTitle("Edit Password")
        self.setFixedSize(500, 450)
        self.setModal(True)
        self.init_ui()
        self.load_data()
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Title
        title = QLabel("Edit Password Entry")
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
        
        # Password section
        password_layout = QVBoxLayout()
        
        # Current password display
        current_password_layout = QHBoxLayout()
        self.current_password_input = QLineEdit()
        self.current_password_input.setPlaceholderText("Loading current password...")
        self.current_password_input.setEchoMode(QLineEdit.Password)
        self.current_password_input.setReadOnly(True)
        
        self.show_current_btn = QPushButton("Show")
        self.show_current_btn.setFixedWidth(60)
        self.show_current_btn.clicked.connect(self.toggle_current_password_visibility)
        
        current_password_layout.addWidget(QLabel("Current:"))
        current_password_layout.addWidget(self.current_password_input)
        current_password_layout.addWidget(self.show_current_btn)
        
        # New password input
        new_password_layout = QHBoxLayout()
        self.new_password_input = QLineEdit()
        self.new_password_input.setPlaceholderText("Leave empty to keep current password")
        self.new_password_input.setEchoMode(QLineEdit.Password)
        
        self.show_new_btn = QPushButton("Show")
        self.show_new_btn.setFixedWidth(60)
        self.show_new_btn.clicked.connect(self.toggle_new_password_visibility)
        
        self.generate_btn = QPushButton("Generate")
        self.generate_btn.setFixedWidth(70)
        self.generate_btn.clicked.connect(self.generate_password)
        
        new_password_layout.addWidget(QLabel("New:"))
        new_password_layout.addWidget(self.new_password_input)
        new_password_layout.addWidget(self.show_new_btn)
        new_password_layout.addWidget(self.generate_btn)
        
        password_layout.addLayout(current_password_layout)
        password_layout.addLayout(new_password_layout)
        
        # Notes (Optional)
        self.notes_input = QTextEdit()
        self.notes_input.setPlaceholderText("Optional notes about this account...")
        self.notes_input.setMaximumHeight(80)
        
        form_layout.addRow("Site Name *:", self.site_name_input)
        form_layout.addRow("Site URL:", self.site_url_input)
        form_layout.addRow("Username *:", self.username_input)
        form_layout.addRow("Password:", password_layout)
        form_layout.addRow("Notes:", self.notes_input)
        
        # Required fields note
        required_note = QLabel("* Required fields")
        required_note.setStyleSheet("color: #666; font-size: 12px;")
        
        # Buttons
        button_layout = QHBoxLayout()
        
        self.update_btn = QPushButton("Update Password")
        self.cancel_btn = QPushButton("Cancel")
        
        self.update_btn.clicked.connect(self.update_password)
        self.cancel_btn.clicked.connect(self.reject)
        
        # Make update button more prominent
        self.update_btn.setStyleSheet("QPushButton { background-color: #2196F3; color: white; font-weight: bold; }")
        
        button_layout.addWidget(self.cancel_btn)
        button_layout.addWidget(self.update_btn)
        
        layout.addWidget(title)
        layout.addLayout(form_layout)
        layout.addWidget(required_note)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
    
    def load_data(self):
        """Load existing password data"""
        # Get the full password details including decrypted password
        result = self.api_client._make_request('GET', f'/passwords/{self.password_id}/')
        
        if 'error' not in result:
            self.site_name_input.setText(result.get('site_name', ''))
            self.site_url_input.setText(result.get('site_url', ''))
            self.username_input.setText(result.get('username', ''))
            self.notes_input.setPlainText(result.get('notes', ''))
            
            # Set current password
            decrypted_password = result.get('decrypted_password', '')
            self.current_password_input.setText(decrypted_password)
            self.current_password_input.setPlaceholderText("")
        else:
            QMessageBox.critical(self, "Error", f"Failed to load password details: {result['error']}")
    
    def toggle_current_password_visibility(self):
        """Toggle current password visibility"""
        if self.current_password_input.echoMode() == QLineEdit.Password:
            self.current_password_input.setEchoMode(QLineEdit.Normal)
            self.show_current_btn.setText("Hide")
        else:
            self.current_password_input.setEchoMode(QLineEdit.Password)
            self.show_current_btn.setText("Show")
    
    def toggle_new_password_visibility(self):
        """Toggle new password visibility"""
        if self.new_password_input.echoMode() == QLineEdit.Password:
            self.new_password_input.setEchoMode(QLineEdit.Normal)
            self.show_new_btn.setText("Hide")
        else:
            self.new_password_input.setEchoMode(QLineEdit.Password)
            self.show_new_btn.setText("Show")
    
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
        
        self.new_password_input.setText(generated_password)
        
        # Temporarily show the generated password
        if self.new_password_input.echoMode() == QLineEdit.Password:
            self.new_password_input.setEchoMode(QLineEdit.Normal)
            self.show_new_btn.setText("Hide")
    
    def update_password(self):
        """Update the password entry"""
        # Get form data
        site_name = self.site_name_input.text().strip()
        site_url = self.site_url_input.text().strip()
        username = self.username_input.text().strip()
        new_password = self.new_password_input.text()
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
        
        # Prepare update data
        update_data = {
            'site_name': site_name,
            'site_url': site_url,
            'username': username,
            'notes': notes
        }
        
        # Only include new password if provided
        if new_password.strip():
            update_data['password'] = new_password
        
        # Try to update
        result = self.api_client.update_password(self.password_id, **update_data)
        
        if 'error' in result:
            QMessageBox.critical(self, "Error", f"Failed to update password: {result['error']}")
        else:
            QMessageBox.information(self, "Success", "Password updated successfully!")
            self.password_updated.emit()
            self.accept()