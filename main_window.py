from PyQt6.QtWidgets import QPushButton, QVBoxLayout, QWidget, QFileDialog, QSpacerItem, QSizePolicy
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QPalette, QBrush
import os


class MainScreen(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()

        self.stacked_widget = stacked_widget  # Reference to the stacked widget

        # Set the background image
        self.setAutoFillBackground(True)
        palette = self.palette()
        background = QPixmap("backgrounds/Upload your video.png")
        palette.setBrush(QPalette.ColorRole.Window, QBrush(background))
        self.setPalette(palette)

        # Layout and widgets for the main screen
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Align all elements to the center

        # Set margins of the layout (control the space around the edges)
        layout.setContentsMargins(0, 0, 0, 0)

        # Add a spacer item to position the button
        spacer_top = QSpacerItem(50, 675, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        layout.addItem(spacer_top)

        upload_button = QPushButton("")

        upload_button.setStyleSheet("""
                    QPushButton {
                        background-color: transparent;
                        border: none;
                        color: white;  /* Couleur du texte */
                        font-size: 16px;  /* Taille du texte */
                    }
                    QPushButton:hover {
                        background-color: rgba(255, 255, 255, 50);  /* Effet sur hover */
                    }
                """)

        # Set fixed size for the button (Width = 200, Height = 50)
        upload_button.setFixedSize(150, 50)

        layout.addWidget(upload_button)

        # Add a spacer below to ensure the button stays centered
        spacer_bottom = QSpacerItem(50, 250, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        layout.addItem(spacer_bottom)

        # Connect the button to the file dialog
        upload_button.clicked.connect(self.open_file_dialog)

        self.setLayout(layout)

        # Set window size and position (if necessary)
        self.setGeometry(100, 100, 600, 800)

    def open_file_dialog(self):
        try:
            # Open a file dialog to select video files
            file_path, _ = QFileDialog.getOpenFileName(
                self,
                "Select Video File",
                "",
                "Video Files (*.mp4 *.avi *.mkv *.mov *.flv);;All Files (*)",
            )

            # Check if a file was selected and update the label
            if file_path:
                if self.is_video_file(file_path):
                    print(f"Selected file path: {file_path}")
                    self.go_to_second_screen(file_path)
                else:
                    print("Invalid file type. Please select a video file.")

        except Exception as e:
            print(f"Error: {e}")

    @staticmethod
    def is_video_file(file_path):
        # Check the file extension for common video formats
        video_extensions = [".mp4", ".avi", ".mkv", ".mov", ".flv"]
        return any(file_path.lower().endswith(ext) for ext in video_extensions)

    def go_to_second_screen(self, file_path):
        # Switch to the second screen and start detection
        self.stacked_widget.setCurrentIndex(1)
        second_screen = self.stacked_widget.currentWidget()
        second_screen.start_detection(file_path)