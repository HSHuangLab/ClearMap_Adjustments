from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QPushButton,
    QFileDialog,
    QLabel,
    QComboBox)
from ims_utils import load_ims


def main():

    file_path = ""


    app = QApplication([])

    window = QWidget()
    window.setWindowTitle("Image Registration Tool")
    window.resize(700, 500)

    file_label = QLabel("No file selected", window)
    file_label.move(20, 60)
    file_label.resize(650, 30)

    def choose_file():
        
        nonlocal file_path

        file_path, selected_filter = QFileDialog.getOpenFileName(
            window,
            "Choose an Imaris file",
            "",
            "Imaris files (*.ims)"
        )

        if file_path:
            file_label.setText(file_path)

    def load_selected_image():
        if not file_path:
            return

        resolution = int(resolution_box.currentText())
        channel = int(channel_box.currentText())

        volume = load_ims(file_path, resolution, channel)

        print("Loaded volume:", volume.shape)

    browse_button = QPushButton("Browse", window)
    browse_button.move(20, 20)
    browse_button.clicked.connect(choose_file)

    resolution_label = QLabel("Resolution Level:", window)
    resolution_label.move(20, 100)

    resolution_box = QComboBox(window)
    resolution_box.addItems(["0", "1", "2", "3", "4", "5", "6"])
    resolution_box.setCurrentText("4")
    resolution_box.move(140, 95)

    channel_label = QLabel("Channel:", window)
    channel_label.move(20, 140)

    channel_box = QComboBox(window)
    channel_box.addItems(["0"])
    channel_box.move(140, 135)

    load_button = QPushButton("Load Image", window)
    load_button.move(20, 180)
    load_button.clicked.connect(load_selected_image)


    window.show()

    app.exec()

main()