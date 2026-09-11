"""UI Module - User interface for Task Tracker"""

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QTableWidget, QTableWidgetItem,
    QComboBox, QMessageBox
)
from PyQt6.QtCore import Qt
from src.database import TaskDatabase


class TaskTrackerUI(QMainWindow):
    """Main window for Task Tracker."""
    
    def __init__(self):
        """Initialize UI and database."""
        super().__init__()
        self.db = TaskDatabase()
        self.selected_id = None
        self.init_ui()
        self.load_tasks()
    
    def init_ui(self):
        """Set up UI elements."""
        self.setWindowTitle("Project Task Progress Tracker")
        self.setGeometry(100, 100, 700, 500)
        
        widget = QWidget()
        self.setCentralWidget(widget)
        layout = QVBoxLayout(widget)
        
        # Title
        title = QLabel("Task Progress Tracker")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 18px; font-weight: bold; padding: 10px;")
        layout.addWidget(title)
        
        # Inputs
        name_layout = QHBoxLayout()
        name_layout.addWidget(QLabel("Task Name:"))
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter task name...")
        name_layout.addWidget(self.name_input)
        layout.addLayout(name_layout)
        
        status_layout = QHBoxLayout()
        status_layout.addWidget(QLabel("Task Status:"))
        self.status_input = QComboBox()
        self.status_input.addItems(["Pending", "In Progress", "Completed"])
        status_layout.addWidget(self.status_input)
        layout.addLayout(status_layout)
        
        # Buttons
        btn_layout = QHBoxLayout()
        self.add_btn = self.create_button("Add", "#4CAF50", self.add_task)
        self.update_btn = self.create_button("Update", "#2196F3", self.update_task)
        self.delete_btn = self.create_button("Delete", "#f44336", self.delete_task)
        self.clear_btn = self.create_button("Clear", "#FF9800", self.clear_selection)
        
        self.update_btn.setEnabled(False)
        self.delete_btn.setEnabled(False)
        
        for btn in [self.add_btn, self.update_btn, self.delete_btn, self.clear_btn]:
            btn_layout.addWidget(btn)
        layout.addLayout(btn_layout)
        
        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["ID", "Task Name", "Status"])
        self.table.setColumnWidth(0, 50)
        self.table.setColumnWidth(1, 400)
        self.table.setColumnWidth(2, 150)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.cellClicked.connect(self.select_task)
        layout.addWidget(self.table)
        
        self.statusBar().showMessage("Ready")
    
    def create_button(self, text: str, color: str, callback) -> QPushButton:
        """Create styled button."""
        btn = QPushButton(text)
        btn.setStyleSheet(f"background-color: {color}; color: white; padding: 8px; font-weight: bold;")
        btn.clicked.connect(callback)
        return btn
    
    def load_tasks(self):
        """Load and display tasks."""
        tasks = self.db.get_all_tasks()
        self.table.setRowCount(len(tasks))
        
        for row, task in enumerate(tasks):
            self.table.setItem(row, 0, self.create_item(str(task["id"]), True))
            self.table.setItem(row, 1, self.create_item(task["name"]))
            self.table.setItem(row, 2, self.create_status_item(task["status"]))
        
        self.statusBar().showMessage(f"Loaded {len(tasks)} task(s)")
    
    def create_item(self, text: str, center: bool = False) -> QTableWidgetItem:
        """Create table item."""
        item = QTableWidgetItem(text)
        if center:
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        return item
    
    def create_status_item(self, status: str) -> QTableWidgetItem:
        """Create status item with color."""
        item = QTableWidgetItem(status)
        item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        colors = {"Completed": Qt.GlobalColor.green, "In Progress": Qt.GlobalColor.yellow}
        item.setBackground(colors.get(status, Qt.GlobalColor.lightGray))
        return item
    
    def add_task(self):
        """Add new task."""
        name = self.name_input.text().strip()
        if not name:
            QMessageBox.warning(self, "Input Error", "Please enter a task name!")
            return
        
        if self.db.add_task(name, self.status_input.currentText()):
            self.load_tasks()
            self.clear_inputs()
            self.statusBar().showMessage(f"Task '{name}' added!")
        else:
            QMessageBox.critical(self, "Error", "Failed to add task!")
    
    def select_task(self, row, column):
        """Select task from table."""
        self.selected_id = int(self.table.item(row, 0).text())
        task = self.db.get_task_by_id(self.selected_id)
        
        if task:
            self.name_input.setText(task["name"])
            self.status_input.setCurrentText(task["status"])
            self.update_btn.setEnabled(True)
            self.delete_btn.setEnabled(True)
            self.statusBar().showMessage(f"Selected: {task['name']}")
    
    def update_task(self):
        """Update existing task."""
        if not self.selected_id:
            QMessageBox.warning(self, "No Selection", "Please select a task!")
            return
        
        name = self.name_input.text().strip()
        if not name:
            QMessageBox.warning(self, "Input Error", "Task name cannot be empty!")
            return
        
        if self.db.update_task(self.selected_id, name, self.status_input.currentText()):
            self.load_tasks()
            self.clear_selection()
            self.statusBar().showMessage("Task updated!")
        else:
            QMessageBox.critical(self, "Error", "Failed to update!")
    
    def delete_task(self):
        """Delete task."""
        if not self.selected_id:
            QMessageBox.warning(self, "No Selection", "Please select a task!")
            return
        
        task = self.db.get_task_by_id(self.selected_id)
        if not task:
            return
        
        reply = QMessageBox.question(self, "Confirm", f"Delete '{task['name']}'?",
                                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        
        if reply == QMessageBox.StandardButton.Yes and self.db.delete_task(self.selected_id):
            self.load_tasks()
            self.clear_selection()
            self.statusBar().showMessage(f"Task deleted!")
    
    def clear_selection(self):
        """Clear selection."""
        self.selected_id = None
        self.clear_inputs()
        self.table.clearSelection()
        self.update_btn.setEnabled(False)
        self.delete_btn.setEnabled(False)
        self.statusBar().showMessage("Selection cleared")
    
    def clear_inputs(self):
        """Clear input fields."""
        self.name_input.clear()
        self.status_input.setCurrentIndex(0)
    
    def closeEvent(self, event):
        """Clean up on close."""
        self.db.close()
        event.accept()
