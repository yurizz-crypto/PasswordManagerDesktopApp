from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, 
                               QTableWidget, QTableWidgetItem, QPushButton, 
                               QLabel, QMessageBox, QHeaderView, QLineEdit,
                               QSplitter, QFrame)
from PySide6.QtCore import Qt
from controllers.api_client import APIClient
from ui.add_password_dialog import AddPasswordDialog
from ui.edit_password_dialog import EditPasswordDialog

class MainWindow(QWidget):
    def __init__(self, api_client: APIClient):
        super().__init__()
        self.api_client = api_client
        self.setWindowTitle("Password Manager - My Passwords")
        self.setGeometry(100, 100, 1000, 700)
        self.password_data = []  # Store full password data
        self.init_ui()
        self.load_passwords()
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Header with user info and search
        header_frame = QFrame()
        header_frame.setStyleSheet("QFrame { background-color: #f0f0f0; border-radius: 5px; padding: 10px; }")
        header_layout = QHBoxLayout()
        
        title = QLabel("🔐 My Password Vault")
        title.setStyleSheet("font-size: 20px; font-weight: bold; color: #2c3e50;")
        
        # Search box
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search passwords by site name or username...")
        self.search_input.setFixedWidth(300)
        self.search_input.textChanged.connect(self.filter_passwords)
        
        header_layout.addWidget(title)
        header_layout.addStretch()
        header_layout.addWidget(QLabel("Search:"))
        header_layout.addWidget(self.search_input)
        
        header_frame.setLayout(header_layout)
        
        # Table for passwords
        self.password_table = QTableWidget()
        self.password_table.setColumnCount(5)
        self.password_table.setHorizontalHeaderLabels(['Site Name', 'Username', 'URL', 'Notes', 'Last Updated'])
        
        # Make table look better
        self.password_table.setAlternatingRowColors(True)
        self.password_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.password_table.setSelectionMode(QTableWidget.SingleSelection)
        
        # Set column widths
        header_view = self.password_table.horizontalHeader()
        header_view.setSectionResizeMode(0, QHeaderView.ResizeToContents)  # Site Name
        header_view.setSectionResizeMode(1, QHeaderView.ResizeToContents)  # Username
        header_view.setSectionResizeMode(2, QHeaderView.Stretch)           # URL
        header_view.setSectionResizeMode(3, QHeaderView.Stretch)           # Notes
        header_view.setSectionResizeMode(4, QHeaderView.ResizeToContents)  # Last Updated
        
        # Double-click to edit
        self.password_table.doubleClicked.connect(self.edit_password)
        
        # Buttons section
        button_frame = QFrame()
        button_frame.setStyleSheet("QFrame { background-color: #f8f9fa; border-radius: 5px; padding: 10px; }")
        button_layout = QHBoxLayout()
        
        # Main action buttons
        self.add_btn = QPushButton("➕ Add Password")
        self.edit_btn = QPushButton("✏️ Edit Selected")
        self.delete_btn = QPushButton("🗑️ Delete Selected")
        self.view_btn = QPushButton("👁️ View Password")
        
        # Utility buttons
        self.refresh_btn = QPushButton("🔄 Refresh")
        self.export_btn = QPushButton("📤 Export")
        
        # Logout button
        self.logout_btn = QPushButton("🚪 Logout")
        
        # Style buttons
        self.add_btn.setStyleSheet("QPushButton { background-color: #28a745; color: white; font-weight: bold; padding: 8px 16px; border-radius: 4px; }")
        self.edit_btn.setStyleSheet("QPushButton { background-color: #007bff; color: white; font-weight: bold; padding: 8px 16px; border-radius: 4px; }")
        self.delete_btn.setStyleSheet("QPushButton { background-color: #dc3545; color: white; font-weight: bold; padding: 8px 16px; border-radius: 4px; }")
        self.view_btn.setStyleSheet("QPushButton { background-color: #17a2b8; color: white; font-weight: bold; padding: 8px 16px; border-radius: 4px; }")
        self.logout_btn.setStyleSheet("QPushButton { background-color: #6c757d; color: white; font-weight: bold; padding: 8px 16px; border-radius: 4px; }")
        
        # Connect buttons
        self.add_btn.clicked.connect(self.add_password)
        self.edit_btn.clicked.connect(self.edit_password)
        self.delete_btn.clicked.connect(self.delete_password)
        self.view_btn.clicked.connect(self.view_password)
        self.refresh_btn.clicked.connect(self.load_passwords)
        self.export_btn.clicked.connect(self.export_passwords)
        self.logout_btn.clicked.connect(self.logout)
        
        button_layout.addWidget(self.add_btn)
        button_layout.addWidget(self.edit_btn)
        button_layout.addWidget(self.delete_btn)
        button_layout.addWidget(self.view_btn)
        button_layout.addWidget(QLabel("|"))  # Separator
        button_layout.addWidget(self.refresh_btn)
        button_layout.addWidget(self.export_btn)
        button_layout.addStretch()
        button_layout.addWidget(self.logout_btn)
        
        button_frame.setLayout(button_layout)
        
        # Status bar
        self.status_label = QLabel("Ready")
        self.status_label.setStyleSheet("color: #666; font-size: 12px; padding: 5px;")
        
        layout.addWidget(header_frame)
        layout.addWidget(self.password_table)
        layout.addWidget(button_frame)
        layout.addWidget(self.status_label)
        
        self.setLayout(layout)
    
    def load_passwords(self):
        """Load passwords from API"""
        self.status_label.setText("Loading passwords...")
        result = self.api_client.get_passwords()
        
        if 'error' in result:
            QMessageBox.critical(self, "Error", f"Failed to load passwords: {result['error']}")
            self.status_label.setText("Error loading passwords")
            return
        
        # Store full password data
        self.password_data = result if isinstance(result, list) else []
        self.populate_table(self.password_data)
        
        # Update status
        count = len(self.password_data)
        self.status_label.setText(f"Loaded {count} password{'s' if count != 1 else ''}")
    
    def populate_table(self, passwords):
        """Populate table with password data"""
        # Clear table
        self.password_table.setRowCount(0)
        
        # Populate table
        self.password_table.setRowCount(len(passwords))
        
        for row, password in enumerate(passwords):
            self.password_table.setItem(row, 0, QTableWidgetItem(password.get('site_name', '')))
            self.password_table.setItem(row, 1, QTableWidgetItem(password.get('username', '')))
            self.password_table.setItem(row, 2, QTableWidgetItem(password.get('site_url', '')))
            self.password_table.setItem(row, 3, QTableWidgetItem(password.get('notes', '')))
            
            # Format date
            updated_at = password.get('updated_at', '')
            if updated_at:
                # Simple date formatting (you can improve this)
                date_part = updated_at.split('T')[0] if 'T' in updated_at else updated_at
                self.password_table.setItem(row, 4, QTableWidgetItem(date_part))
            else:
                self.password_table.setItem(row, 4, QTableWidgetItem(''))
            
            # Store full password data in first column for later use
            item = self.password_table.item(row, 0)
            if item:
                item.setData(Qt.UserRole, password)
    
    def filter_passwords(self):
        """Filter passwords based on search input"""
        search_text = self.search_input.text().lower()
        
        if not search_text:
            # Show all passwords
            self.populate_table(self.password_data)
            return
        
        # Filter passwords
        filtered_passwords = []
        for password in self.password_data:
            site_name = password.get('site_name', '').lower()
            username = password.get('username', '').lower()
            site_url = password.get('site_url', '').lower()
            
            if (search_text in site_name or 
                search_text in username or 
                search_text in site_url):
                filtered_passwords.append(password)
        
        self.populate_table(filtered_passwords)
        
        # Update status
        total = len(self.password_data)
        filtered = len(filtered_passwords)
        self.status_label.setText(f"Showing {filtered} of {total} password{'s' if total != 1 else ''}")
    
    def get_selected_password(self):
        """Get the currently selected password data"""
        current_row = self.password_table.currentRow()
        if current_row < 0:
            return None
        
        item = self.password_table.item(current_row, 0)
        if not item:
            return None
        
        return item.data(Qt.UserRole)
    
    def add_password(self):
        """Show add password dialog"""
        dialog = AddPasswordDialog(self.api_client)
        dialog.password_added.connect(self.load_passwords)
        dialog.exec()
    
    def edit_password(self):
        """Show edit password dialog"""
        password_data = self.get_selected_password()
        if not password_data:
            QMessageBox.warning(self, "Warning", "Please select a password to edit")
            return
        
        dialog = EditPasswordDialog(self.api_client, password_data)
        dialog.password_updated.connect(self.load_passwords)
        dialog.exec()
    
    def view_password(self):
        """Show password in a popup"""
        password_data = self.get_selected_password()
        if not password_data:
            QMessageBox.warning(self, "Warning", "Please select a password to view")
            return
        
        # Get the decrypted password
        result = self.api_client._make_request('GET', f'/passwords/{password_data["id"]}/')
        
        if 'error' in result:
            QMessageBox.critical(self, "Error", f"Failed to retrieve password: {result['error']}")
            return
        
        decrypted_password = result.get('decrypted_password', 'Error decrypting')
        site_name = password_data.get('site_name', 'Unknown')
        
        # Show password in message box
        msg = QMessageBox()
        msg.setWindowTitle(f"Password for {site_name}")
        msg.setText(f"Site: {site_name}\nUsername: {password_data.get('username', '')}\nPassword: {decrypted_password}")
        msg.setStandardButtons(QMessageBox.Ok)
        
        # Make it easier to copy
        msg.setTextInteractionFlags(Qt.TextSelectableByMouse)
        msg.exec()
    
    def delete_password(self):
        """Delete selected password"""
        password_data = self.get_selected_password()
        if not password_data:
            QMessageBox.warning(self, "Warning", "Please select a password to delete")
            return
        
        site_name = password_data.get('site_name', 'Unknown')
        
        # Confirm deletion
        reply = QMessageBox.question(self, "Confirm Delete", 
                                   f"Are you sure you want to delete the password for '{site_name}'?\n\nThis action cannot be undone.",
                                   QMessageBox.Yes | QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            result = self.api_client.delete_password(password_data['id'])
            
            if 'error' in result:
                QMessageBox.critical(self, "Error", f"Failed to delete password: {result['error']}")
            else:
                QMessageBox.information(self, "Success", "Password deleted successfully!")
                self.load_passwords()  # Refresh the list
    
    def export_passwords(self):
        """Export passwords (placeholder)"""
        QMessageBox.information(self, "Export", "Export functionality coming in next update!")
    
    def logout(self):
        """Logout and close application"""
        reply = QMessageBox.question(self, "Logout", 
                                   "Are you sure you want to logout?",
                                   QMessageBox.Yes | QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            self.api_client.logout()
            self.close()
            
            # You could show the login window again here
            QMessageBox.information(self, "Logged Out", "You have been logged out successfully!")