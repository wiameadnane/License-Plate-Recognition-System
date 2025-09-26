import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QStackedWidget
from main_window import MainScreen
from second_window import SecondScreen
from third_window import ThirdScreen
from fourth_window import FourthScreen


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Multi-Screen App")
        self.setGeometry(310, 70, 800, 586)

        # Create the QStackedWidget
        self.stacked_widget = QStackedWidget()

        # Create the screens
        self.main_screen = MainScreen(self.stacked_widget)
        self.second_screen = SecondScreen(self.stacked_widget)
        self.third_screen = ThirdScreen(self.stacked_widget)
        self.fourth_screen = FourthScreen(self.stacked_widget)

        # Add screens to the QStackedWidget
        self.stacked_widget.addWidget(self.main_screen)
        self.stacked_widget.addWidget(self.second_screen)
        self.stacked_widget.addWidget(self.third_screen)
        self.stacked_widget.addWidget(self.fourth_screen)

        # Set the QStackedWidget as the central widget
        self.setCentralWidget(self.stacked_widget)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    main_window = MainWindow()
    main_window.show()

    sys.exit(app.exec())

