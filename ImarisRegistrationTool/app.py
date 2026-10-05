from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QPushButton,
    QFileDialog,
    QLabel,
    QComboBox,
    QMessageBox,
    QVBoxLayout,
    QHBoxLayout,
    QProgressBar
    )
from PySide6.QtCore import QThread, Signal
from ims_utils import load_ims
from registration import PARAMETERS_FILES, run_elastix
from metrics import evaluate_alignment

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


class RegistrationThread(QThread):

    registration_finished = Signal(object, object)

    def __init__(self, fix_vol, mov_vol, pars,out_path):
        super().__init__()

        self.fix_vol= fix_vol
        self.mov_vol= mov_vol
        self.pars= pars
        self.out_path= out_path

    def run(self):
        ali_vol, out_time_path= run_elastix(self.fix_vol,self.mov_vol,self.pars,self.out_path)
        self.registration_finished.emit(ali_vol,out_time_path)
            

        
        


def main():

    output_path= None

    def choose_output_dir():
        nonlocal output_path

        selected_path = QFileDialog.getExistingDirectory(
            window,
            "Choose output folder to save registration",
            "")

        if selected_path:
            output_path = selected_path
            file_output_label.setText(output_path)


    def run_registration():
        if fixed.volume is None or moving.volume is None:
            QMessageBox.warning(window,
                "Image not loaded",
                "\nPlease load both fixed and moving images."
                )
            return

        if output_path is None:
            QMessageBox.warning(window,
                                "Output directory not selected",
                                "\nPlease select an output folder.")
            return

        transform_boxes=[transform_box_1,transform_box_2,transform_box_3]

        parameters= []

        for tran_box in transform_boxes:
            transform= tran_box.currentText()

            if transform != "None":
                parameters.append(PARAMETERS_FILES[transform])

        progress_bar.show()

        registration_thread = RegistrationThread(fixed.volume,
                                            moving.volume,
                                            parameters,
                                            output_path)
        registration_thread.registration_finished.connect(registration_finished)
        

    def registration_finished(aligned_volume, output_path_time):
        metrics= evaluate_alignment(fixed.volume, moving.volume, aligned_volume)
        
        progress_bar.hide()
        
        message = (
            "Registration completed successfully!\n\n"
            "Alignment Metrics:\n"
            f"MAE:  {metrics['mae_before']:.2f}  →  {metrics['mae_after']:.2f}\n"
            f"MSE:  {metrics['mse_before']:.2f}  →  {metrics['mse_after']:.2f}\n"
            f"NCC:  {metrics['ncc_before']:.3f}  →  {metrics['ncc_after']:.3f}\n\n"
            f"Results saved to:\n{output_path_time}"
            )
        
        QMessageBox.information(
            window,
            "Registration complete",
            message
            )



    app = QApplication([])

    window = QWidget()
    window.setWindowTitle("Image Registration Tool")
    window.resize(1200, 900)

    main_layout= QVBoxLayout()

    images_layout= QHBoxLayout()

    fixed= ImagePanel("IMAGE 1 - FIXED")
    moving= ImagePanel("IMAGE 2 - MOVING")

    images_layout.addWidget(fixed)
    images_layout.addWidget(moving)

    main_layout.addLayout(images_layout)

    transform_label_1=QLabel("Transform Type - Step 1:")
    transform_box_1= QComboBox()
    transform_box_1.addItems(["Translation","Rigid","Affine"])

    main_layout.addWidget(transform_label_1)
    main_layout.addWidget(transform_box_1)

    transform_label_2=QLabel("Transform Type - Step 2:")
    transform_box_2= QComboBox()
    transform_box_2.addItems(["None","Translation","Rigid","Affine"])
    
    main_layout.addWidget(transform_label_2)
    main_layout.addWidget(transform_box_2)

    transform_label_3=QLabel("Transform Type - Step 3:")
    transform_box_3= QComboBox()
    transform_box_3.addItems(["None","Translation","Rigid","Affine"])
    
    main_layout.addWidget(transform_label_3)
    main_layout.addWidget(transform_box_3)

    output_path_label=QLabel("Output folder")
    main_layout.addWidget(output_path_label)

    browse_output_button = QPushButton("Browse")
    main_layout.addWidget(browse_output_button)
    
    file_output_label = QLabel("No directory selected")
    main_layout.addWidget(file_output_label)
    
    browse_output_button.clicked.connect(choose_output_dir)

    reg_bottom=QPushButton("Run Registration")
    main_layout.addWidget(reg_bottom)
    reg_bottom.clicked.connect(run_registration)

    progress_bar = QProgressBar()
    progress_bar.setRange(0, 0)
    progress_bar.hide()
    main_layout.addWidget(progress_bar)



    window.setLayout(main_layout)

    window.show()

    app.exec()

main()