import io
import shutil
import os

from PyPDF2 import PdfFileWriter, PdfFileReader

import fitz

from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfform
from reportlab.lib.colors import red, white, Color

class pdfUtil():
    
    # default pdf size : 595.27, 841.89 (a4와동일함)
    # a4 size : 210 * 297

    pdf_size = (841.89, 595.27)

    def __init__(self, gui_handler):
        self.gui_handler = gui_handler
        self.current_working_dir = os.getcwd()
        self.original_pdf_dir = os.path.join(self.current_working_dir, 'original')
        self.result_pdf_dir = os.path.join(self.current_working_dir, 'result')

        if not os.path.exists(self.original_pdf_dir):
            os.makedirs(self.original_pdf_dir)

        if not os.path.exists(self.result_pdf_dir):
            os.makedirs(self.result_pdf_dir)

    def read_pdf_file(self, file_path):
        pdf_file_object = open(file_path, 'rb')
        pdf_file = PdfFileReader(pdf_file_object)
        
        if pdf_file.isEncrypted:
            try:
                pdf_file.decrypt('')
            except:
                tmp_file_path_list = file_path.split('/')
                tmp_file_path_list[-1] = "tmp_" + tmp_file_path_list[-1]
                tmp_file_path = "/".join(tmp_file_path_list)
                cmd_command = f"qpdf --decrypt \"{file_path}\" \"{tmp_file_path}\" "
                os.system(cmd_command)
                pdf_file_object.close()
                pdf_file_object = open(tmp_file_path, 'rb')
                pdf_file = PdfFileReader(pdf_file_object)
        return pdf_file

    def write_text_to_pdf(self):
        task_list = self.gui_handler.get_input_elements()

        if not self.gui_handler.validation_check():
            self.gui_handler.not_complete_alert("조서화할 내용을 기입하지 않으셨습니다. 기입한 후 다시 시도해주세요.")
            return
        try:
            for task in task_list:
                file_name = task["file_name"]
                file_path = task["file_path"]
                input_text = task["edit_text_widget"].text()

                existing_pdf_file = self.read_pdf_file(file_path)

                output_file = PdfFileWriter()

                for page in range(existing_pdf_file.getNumPages()):
                    insert_text = input_text + str(page + 1)

                    packet = io.BytesIO()
                    # create a new PDF with Reportlab
                    can = canvas.Canvas(packet, pagesize=self.pdf_size)
                    can.setFillColorRGB(255,0,0)
                    can.setFont("Helvetica", 10)

                    offset, width = self._set_offset_and_width(insert_text)
                    can.drawString(self.pdf_size[0]*7.5/8.5-offset, self.pdf_size[1]*23/24, insert_text)
                    form = can.acroForm

                    form.textfield(name='document', 
                                    tooltip='document_number',
                                    borderStyle='inset', 
                                    forceBorder=True,
                                    x=self.pdf_size[0]*7/8-offset, 
                                    y=self.pdf_size[1]*19/20,
                                    width=width, height=20, fontSize=10, textColor=red,
                                    fillColor=Color(0,0,0, alpha=0.0),
                                    borderColor=red,
                                    borderWidth=1.3,
                                    )
                    can.save()

                    #move to the beginning of the StringIO buffer
                    packet.seek(0)
                    new_pdf = PdfFileReader(packet)
                    # read your existing PDF
                    page = existing_pdf_file.getPage(page)
                    # add the text field on 
                    page.mergePage(new_pdf.getPage(0))
                    output_file.addPage(page)
                    # finally, write "output" to a real file

                output_file_path = os.path.join(self.result_pdf_dir, "result_" + file_name)

                with open(output_file_path, 'wb') as f:
                    output_file.write(f)
                shutil.copy(file_path, os.path.join(self.original_pdf_dir, file_name))
            self.gui_handler.complete_alert()
        except:
            self.gui_handler.not_complete_alert("파일이 사용중이거나, 올바른 경로가 아닙니다.")

    def _set_offset_and_width(self, text):
        text_length = len(text)
        width = 30
        width += text_length * 5
        offset = 0 
        if width > 80:
            offset = width - 80
        # C3000-101- : 10자 이하 
        # C3000- : 16자 -> 110 (110 - 40) = 80 /16 = 5
        return (offset, width)        
