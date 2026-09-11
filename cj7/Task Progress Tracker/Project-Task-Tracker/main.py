"""
Main Entry Point - Starts the Task Tracker application
"""

import sys
from PyQt6.QtWidgets import QApplication
from src.ui import TaskTrackerUI


def main():
    """Start the application."""
    app = QApplication(sys.argv)
    app.setApplicationName("Task Progress Tracker")
    window = TaskTrackerUI()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
