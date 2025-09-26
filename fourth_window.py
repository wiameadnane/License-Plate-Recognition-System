from PyQt6.QtWidgets import QVBoxLayout, QWidget, QPushButton
from PyQt6.QtCore import QUrl
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtMultimediaWidgets import QVideoWidget
import os


class FourthScreen(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.video_path = None
        # Layout for the fourth screen
        layout = QVBoxLayout()

        # Create a QVideoWidget to display the video
        self.video_widget = QVideoWidget(self)
        layout.addWidget(self.video_widget)

        # Create play button
        play_button = QPushButton("Play Video", self)
        play_button.clicked.connect(self.play_video)
        layout.addWidget(play_button)

        play_button.setStyleSheet("""
                            QPushButton {
                                background-color: #ffffff;   /* Black background */
                                color: #44a2e2;              /* Blue text */
                                border: 2px solid #44a2e2;   /* Blue border */
                                font-size: 14px;          /* Optional: Adjust text size */
                                border-radius: 5px;       /* Optional: Rounded corners */
                                padding: 5px;             /* Optional: Add padding */
                            }
                            QPushButton:hover {
                                background-color: #000000; /* Slightly lighter black on hover */
                                color: #44a2e2;          /* Light blue text on hover */
                                border-color: #44a2e2;   /* Light blue border on hover */
                            }
                            QPushButton:pressed {
                                background-color: #222222; /* Darker black on press */
                                color: darkblue;           /* Dark blue text on press */
                                border-color: darkblue;    /* Dark blue border on press */
                            }
                            """)

        # Create back button
        back_button = QPushButton("Back to Third Screen", self)
        back_button.clicked.connect(self.go_to_third_screen)
        layout.addWidget(back_button)

        back_button.setStyleSheet("""
                                    QPushButton {
                                        background-color: #ffffff;   /* Black background */
                                        color: #44a2e2;              /* Blue text */
                                        border: 2px solid #44a2e2;   /* Blue border */
                                        font-size: 14px;          /* Optional: Adjust text size */
                                        border-radius: 5px;       /* Optional: Rounded corners */
                                        padding: 5px;             /* Optional: Add padding */
                                    }
                                    QPushButton:hover {
                                        background-color: #000000; /* Slightly lighter black on hover */
                                        color: #44a2e2;          /* Light blue text on hover */
                                        border-color: #44a2e2;   /* Light blue border on hover */
                                    }
                                    QPushButton:pressed {
                                        background-color: #222222; /* Darker black on press */
                                        color: darkblue;           /* Dark blue text on press */
                                        border-color: darkblue;    /* Dark blue border on press */
                                    }
                                    """)

        # Set the layout
        self.setLayout(layout)

        # Initialize QMediaPlayer
        self.media_player = QMediaPlayer(self)
        self.media_player.setVideoOutput(self.video_widget)

        # Add audio output
        self.audio_output = QAudioOutput()
        self.media_player.setAudioOutput(self.audio_output)

    def play_video(self):
        if hasattr(self, 'video_path'):
            if not os.path.exists(self.video_path):
                print(f"Error: Video file does not exist at {self.video_path}")
                return

            # Set the media and play
            self.media_player.setSource(QUrl.fromLocalFile(self.video_path))
            self.media_player.play()
        else:
            print("Error: Video path is not set.")

    def go_to_third_screen(self):
        self.stacked_widget.setCurrentIndex(2)

    def set_video_path(self, video_path):
        # Ensure the input video path exists
        if not os.path.exists(video_path):
            print(f"Error: Input video file does not exist at {video_path}")
            return

        # Derive the processed video path
        base_name = os.path.basename(video_path)  # Extract file name, e.g., 'car_video.mp4'
        file_name_without_extension = os.path.splitext(base_name)[0]   # Remove extension, e.g., 'car_video'
        processed_video_path = f'./{file_name_without_extension}_out.mp4'  # Add '_out' suffix

        # Check if the processed video file exists
        if not os.path.exists(processed_video_path):
            print(f"Error: Processed video file does not exist at {processed_video_path}")
            return

        # Set the valid processed video path
        self.video_path = processed_video_path
        print(f"Video path set to: {self.video_path}")