from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QPushButton,
    QFileDialog,
    QLabel,
    QComboBox,
    QMessageBox,
    QVBoxLayout,
    QHBoxLayout)
from ims_utils import load_ims

class ImagePanel(QWidget):
    def __init__(self, title):
        super().__init__()

        self.file_path = ""
        self.volume= None
        self.metadata= None

        self.layout= QVBoxLayout()
        self.setLayout(self.layout)

        self.title_label= QLabel(title)
        self.layout.addWidget(self.title_label)

        self.browse_button = QPushButton("Browse")
        self.layout.addWidget(self.browse_button)

        self.file_label = QLabel("No file selected")
        self.layout.addWidget(self.file_label)

        self.browse_button.clicked.connect(self.choose_file)
        self.resolution_label = QLabel("Resolution Level:")
        self.layout.addWidget(self.resolution_label)
        self.resolution_box = QComboBox()
        self.resolution_box.addItems(["0", "1", "2", "3", "4", "5", "6"])
        self.resolution_box.setCurrentText("4")
        self.layout.addWidget(self.resolution_box)
    
        self.channel_label = QLabel("Channel:")
        self.layout.addWidget(self.channel_label)
        self.channel_box = QComboBox()
        self.channel_box.addItems(["0"])
        self.layout.addWidget(self.channel_box)
     
        self.load_button = QPushButton("Load Image")
        self.layout.addWidget(self.load_button)
        self.load_button.clicked.connect(self.load_selected_image)

        self.info_label = QLabel("No image loaded")
        self.layout.addWidget(self.info_label)

    def choose_file(self):
        file_path, selected_filter = QFileDialog.getOpenFileName(
            self,
            "Choose an Imaris file",
            "",
            "Imaris files (*.ims)"
        )

        if file_path:
            self.file_path = file_path
            self.file_label.setText(file_path)

    def load_selected_image(self):
        if not self.file_path:
            return
    
        self.resolution = int(self.resolution_box.currentText())
        self.channel = int(self.channel_box.currentText())
    
        try:
            self.volume, self.metadata = load_ims(self.file_path,
                                                   self.resolution,
                                                   self.channel)
            self.physical_size = self.metadata["physical_size_um"]
            self.physical_size_mm = (
            self.physical_size[0] / 1000,
            self.physical_size[1] / 1000,
            self.physical_size[2] / 1000
            )
    
            self.info_label.setText(
                "Loaded volume: " + str(self.volume.shape)+ " voxels"+
                "\nVolume size: " + str(round(self.physical_size_mm[0], 2))+ " × "
                + str(round(self.physical_size_mm[1], 2))
                + " × "
                + str(round(self.physical_size_mm[2], 2))
                + " mm"
                )
    
        except ValueError as error:
            QMessageBox.warning(self,
                "Image too large",
                str(error) + "\nPlease select a lower resolution level."
            )
        


def main():

    app = QApplication([])

    window = QWidget()
    window.setWindowTitle("Image Registration Tool")
    window.resize(900, 650)

    main_layout= QVBoxLayout()

    images_layout= QHBoxLayout()

    fixed= ImagePanel("IMAGE 1 - FIXED")
    moving= ImagePanel("IMAGE 2 - MOVING")

    images_layout.addWidget(fixed)
    images_layout.addWidget(moving)

    main_layout.addLayout(images_layout)

    transform_label=QLabel("Transform Type:")
    transform_box= QComboBox()
    transform_box.addItems(["Translation","Rigid","Affine"])

    main_layout.addWidget(transform_label)
    main_layout.addWidget(transform_box)

    reg_bottom=QPushButton("Run Registration")
    main_layout.addWidget(reg_bottom)

    window.setLayout(main_layout)

    window.show()

    app.exec()

main()