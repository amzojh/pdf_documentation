import os
import fnmatch
import sys

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QDesktopWidget, QHBoxLayout, QVBoxLayout, QLineEdit, QLabel, QDialog, QFileDialog, QMessageBox
from PyQt5.QtCore import QCoreApplication

from .pdf_util import pdfUtil

class GUIWidget(QWidget):

    def __init__(self):
        super().__init__()
        self.pdf_util_class = pdfUtil(self)
        self.input_layout_elements = []
        self.initUI()

    def _file_validation_check(self, file_list):
        for file_path in file_list:
            file_name = os.path.basename(file_path)
            if not fnmatch.fnmatch(file_name, "*.pdf"):
                return False

        return True

    def _clear_all_widget(self): 
        if len(self.input_layout_elements) == 0:
            return
    
        for element in self.input_layout_elements:
            self.vertical_box.removeWidget(element["current_process_info"])
            self.vertical_box.removeWidget(element["edit_text_widget"])
            element["current_process_info"].deleteLater()
            element["edit_text_widget"].deleteLater()
            element["current_process_info"] = None
            element["edit_text_widget"] = None

    def change_header(self, label, text):
        label.setText(text)
        label.adjustSize()

    def push_button_to_search(self):
        fname = QFileDialog.getOpenFileNames(self)

        if not self._file_validation_check(fname[0]):
            self.not_complete_alert("pdf파일만 선택해주십시오.")
            return

        if len(fname[0]) > 10:
            QMessageBox.about(self, "조회서 조서화프로그램", "한번에 10개 이하로 수행해주십시오")            
        
        elif len(fname[0]) != 0:
            self.file_list = fname[0]
            self._clear_all_widget()
            self.make_input_screen(len(self.file_list))
            self.adjustSize()


    def validation_check(self):
        for i in range(len(self.input_layout_elements)):
            if len(self.input_layout_elements[i]["edit_text_widget"].text()) == 0:
                return False
        return True
    
    def complete_alert(self):
        QMessageBox.about(self, "조회서 조서화프로그램", "작업이 완료되었습니다.")

    def not_complete_alert(self, text):
        QMessageBox.about(self, "조회서 조서화프로그램", text)

    def make_input_screen(self, index):    
        self.input_layout_elements = []

        for i in range(index):
            input_dict = {}
            input_dict["file_name"] = os.path.basename(self.file_list[i])  # 현재 task 정보를 보여줌.
            input_dict["file_path"] = self.file_list[i]
            input_dict["current_process_info"] = QLabel('')
            input_dict["edit_text_widget"] = QLineEdit()


            self.vertical_box.addWidget(input_dict["current_process_info"])
            self.vertical_box.addWidget(input_dict["edit_text_widget"])

            self.change_header(input_dict["current_process_info"], input_dict["file_name"])

            self.input_layout_elements.append(input_dict)

    def get_input_elements(self):
        if self.input_layout_elements is None or len(self.input_layout_elements) == 0:
            self.input_layout_elements = []            
        return self.input_layout_elements

    def initUI(self):

        self.file_btn = QPushButton("파일찾기")
        self.file_btn.clicked.connect(self.push_button_to_search)

        cancle_btn = QPushButton("취소", self) # 부모 위젯은 MyApp 임
        ok_btn = QPushButton("생성", self)

        self.info_label = QLabel('', self)
        self.head_label = QLabel('', self)

        cancle_btn.clicked.connect(QCoreApplication.instance().quit)
        ok_btn.clicked.connect(self.pdf_util_class.write_text_to_pdf)
        
        self.vertical_box = QVBoxLayout()

        horizontal_box_btn = QHBoxLayout()

        horizontal_box_btn.addStretch(0.5)
        horizontal_box_btn.addWidget(ok_btn)
        horizontal_box_btn.addStretch(0.1)
        horizontal_box_btn.addWidget(cancle_btn)
        horizontal_box_btn.addStretch(0.5)
        
        self.vertical_box.addWidget(self.file_btn)
        self.vertical_box.addLayout(horizontal_box_btn)

        self.setLayout(self.vertical_box)
        self.setWindowTitle('조회서 문서화 프로그램')
        self.resize(400,150)
        self.center()
        self.show() # 화면에 띄우기

    def center(self):
        
        qr = self.frameGeometry() # 현재 위치를 가져옴
        cp = QDesktopWidget().availableGeometry().center() # 사용하는 화면 모니터 위치 파악
        qr.moveCenter(cp) # 가운데로 이동
        self.move(qr.topLeft())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui_class = GUIWidget()
    sys.exit(app.exec_())
