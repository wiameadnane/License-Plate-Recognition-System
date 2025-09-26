from PyQt6.QtWidgets import QPushButton, QVBoxLayout, QWidget, QLabel, QProgressBar
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from Function import Plate_detection

from PyQt6.QtGui import QPixmap, QPalette, QBrush

from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtCore import pyqtSlot

from third_window import ThirdScreen

class DetectionThread(QThread):
    progress_updated = pyqtSignal(int)
    detection_complete = pyqtSignal(dict)

    def __init__(self, video_path):
        super().__init__()
        self.video_path = video_path

    def run(self):
        try:
            # Call the detection function with progress callback
            results = Plate_detection(self.video_path, self.progress_updated.emit)
            self.detection_complete.emit(results)

            # After the processing is done, make sure to emit 100%
            self.progress_updated.emit(100)

        except Exception as e:
            print(f"Error in detection thread: {e}")
            self.detection_complete.emit({})


class SecondScreen(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()

        self.stacked_widget = stacked_widget
        self.video_path = None

        self.setAutoFillBackground(True)
        palette = self.palette()
        background = QPixmap("backgrounds/background2.png")
        palette.setBrush(QPalette.ColorRole.Window, QBrush(background))
        self.setPalette(palette)

        # Layout and widgets
        layout = QVBoxLayout()
        print("Loading... Please wait.")

        self.label = QLabel("")
        layout.addWidget(self.label)

        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        layout.addWidget(self.progress_bar)

        self.progress_bar.setStyleSheet("""
                    QProgressBar {
                        border: 2px solid #aaa;
                        border-radius: 5px;
                        background-color: #000000;
                        text-align: center;
                    }
                    QProgressBar::chunk {
                        background-color: #007bff; /* Blue color */
                        width: 20px; /* Optional: Controls chunk size for striped effect */
                    }
                """)

        self.setLayout(layout)
        self.detection_thread = None

    def go_to_main_screen(self):
        self.stacked_widget.setCurrentIndex(0)

    def go_to_third_screen(self, results, video_path):
        print("Navigating to the third screen...")
        print(f"Results: {results}")
        self.stacked_widget.setCurrentIndex(2)
        third_screen = self.stacked_widget.widget(2)  # Use widget(index) instead of currentWidget()
        if isinstance(third_screen, ThirdScreen):
            third_screen.get_result_and_video_path(results, video_path)
        else:
            print("Error: Third screen not found or incorrectly initialized.")

    def display_file_info(self, video_path):
        # Start the detection process
        self.start_detection(video_path)

    def start_detection(self, video_path):
        from Function import Plate_detection  # Import here to avoid circular dependency issues
        # Start the detection thread
        self.video_path = video_path
        self.detection_thread = DetectionThread(video_path)
        self.detection_thread.progress_updated.connect(self.update_progress)
        self.detection_thread.detection_complete.connect(self.detection_finished)
        print("it has finished")
        self.detection_thread.start()

    def update_progress(self, value):
        # Update progress bar value
        self.progress_bar.setValue(value)


    def detection_finished(self, results):
        print("YESYES IT IS")
        # Pass both results and video_path to the next screen
        self.update_ui_and_navigate(results, self.video_path)

    @pyqtSlot(dict)
    def update_ui_and_navigate(self, results, video_path):
        self.label.setText("Detection Complete!")
        print("ABOUT TO GO TO THIRD SCREEN")
        self.go_to_third_screen(results, video_path)


