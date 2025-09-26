import sys
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtWidgets import QPushButton, QLabel, QVBoxLayout, QWidget
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Main Window")

        # Button to open second window
        self.button = QPushButton("Go to Second Window")
        self.button.clicked.connect(self.open_second_window)

        # Set layout
        layout = QVBoxLayout()
        layout.addWidget(QLabel("This is the main window"))
        layout.addWidget(self.button)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def open_second_window(self):
        self.second_window = SecondWindow()  # Create an instance of the second window
        self.second_window.show()  # Show the second window





# Entry point of the application
app = QApplication(sys.argv)

main_window = MainWindow()
main_window.show()

sys.exit(app.exec())