from PyQt6.QtWidgets import QPushButton, QVBoxLayout, QWidget, QLabel, QProgressBar, QMessageBox

import os
import pandas as pd
from Function import interpolate_csv, process_video
from fourth_window import FourthScreen

from PyQt6.QtGui import QPixmap, QPalette, QBrush

class ThirdScreen(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()

        self.stacked_widget = stacked_widget  # Ensure the reference is saved here
        self.result = None
        self.video_path = None

        self.setAutoFillBackground(True)
        palette = self.palette()
        background = QPixmap("backgrounds/background3.png")
        palette.setBrush(QPalette.ColorRole.Window, QBrush(background))
        self.setPalette(palette)

        # Layout and widgets for the main screen
        layout = QVBoxLayout()
        self.label = QLabel("")
        layout.addWidget(self.label)

        button1 = QPushButton("Save Plates File")
        button1.clicked.connect(self.save_results_as_csv)
        layout.addWidget(button1)

        # Set the style for the button
        button1.setStyleSheet("""
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

        button2 = QPushButton("Visualize the Plates Video")
        button2.clicked.connect(self.visualize_video)
        layout.addWidget(button2)
        self.setLayout(layout)

        button2.setStyleSheet("""
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

        main_button = QPushButton("Back to Main Screen")
        main_button.clicked.connect(self.go_to_main_screen)
        layout.addWidget(main_button)

        main_button.setStyleSheet("""
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

    def go_to_main_screen(self):
        self.stacked_widget.setCurrentIndex(0)

    def get_result_and_video_path(self, results, video_path):
        self.results = results
        self.video_path = video_path


    def visualize_video(self):
        self.label.setText(f"visualisation of video")
        base_name = os.path.basename(self.video_path)  # Output: 'car_video.mp4'
        file_name_without_extension = os.path.splitext(base_name)[0]  # Output: 'car_video'
        input_file = f"{file_name_without_extension}_results.csv"  # Output: 'car_video_results.csv'
        print(input_file)
        interpolate_csv(input_file)
        base_name, ext = os.path.splitext(input_file)
        # Construct the interpolated CSV file name
        interpolated_file = f"{base_name}_interpolated{ext}"

        # Process the video using the interpolated CSV
        process_video(interpolated_file, self.video_path)

        self.go_to_fourthscreen()

    def save_results_as_csv(self):
        if self.results:
            print("Saving results as CSV...")

            # Initialize a list to store all extracted results
            extracted_data = []

            # Flatten the nested structure and extract required fields
            for frame_nmr, car_info in self.results.items():
                print(f"Processing frame number: {frame_nmr}")  # Debug print
                for car_id, details in car_info.items():
                    # Extract values safely with .get() to avoid key errors
                    plate_text = details.get('license_plate', {}).get('text', None)
                    plate_text_score = details.get('license_plate', {}).get('text_score', None)

                    # Validate car_id
                    if isinstance(car_id, (int, float)):
                        car_id = car_id
                    else:
                        print(f"Error: Invalid car_id detected. Skipping this entry.")  # Error handling

                    # Append the extracted data to the list
                    extracted_data.append({
                        'car_id': car_id,
                        'license_number': plate_text,
                        'license_number_score': plate_text_score
                    })

            # Convert extracted data to DataFrame
            if extracted_data:
                data = pd.DataFrame(extracted_data)

                # Keep only the row with the maximum 'license_number_score' per car_id
                data['license_number_score'] = pd.to_numeric(data['license_number_score'], errors='coerce')
                data_filtered = data.loc[data.groupby('car_id')['license_number_score'].idxmax()]

                print(f"Extracted data: {data_filtered.head()}")  # Debug print to check if data was collected properly

                # Define the output file name based on the input video name
                base_name = os.path.basename(self.video_path)  # Extracts 'car_video.mp4'
                file_name_without_extension = os.path.splitext(base_name)[0]  # Extracts 'car_video'
                output_file_name = f"{file_name_without_extension}_plates.csv"  # Creates 'car_video_plates.csv'

                # Save the filtered data as a CSV file
                data_filtered.to_csv(output_file_name, index=False,
                                     columns=['car_id', 'license_number', 'license_number_score'])
                print(f"Results saved successfully as '{output_file_name}'")
            else:
                print("No data extracted. Please check the structure of your results.")
        else:
            print("No results available to save.")

    def go_to_fourthscreen(self):
        # Set the video path and switch to the fourth screen
        fourth_screen = self.stacked_widget.widget(3)  # Get the fourth screen
        if isinstance(fourth_screen, FourthScreen):
            fourth_screen.set_video_path(self.video_path)  # Pass the video path
            self.stacked_widget.setCurrentIndex(3)  # Navigate to the fourth screen
        else:
            # Show a message box in case of an error
            QMessageBox.critical(self, "Error", "Fourth screen not found or incorrectly initialized.")

