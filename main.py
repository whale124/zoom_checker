import sys, os, os.path
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import uic


# UI파일 연결
# 단, UI파일은 Python 코드 파일과 같은 디렉터리에 위치야한다.
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


form = resource_path('checker.ui')
form_class = uic.loadUiType(form)[0]

# Zoom 채팅 파일 이름
zoom_path = os.path.expanduser('~') + "/Documents/Zoom/"
zoom_chat_file_name = "/meeting_saved_chat.txt"


# 화면을 띄우는데 사용되는 Class 선언
class WindowClass(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # data.txt 파일 불러오기
        self.data_load()

        # 줌 채팅 목록 불러오기
        self.chat_txt_select()

        # font load
        fontVar = QFont("Noto Sans KR")
        self.te.setCurrentFont(fontVar)

        # 버튼에 기능을 연결하는 코드
        self.bt_check.clicked.connect(self.buttonF_check)
        self.bt_delete.clicked.connect(self.buttonF_delete)
        self.bt_exit.clicked.connect(self.buttonF_exit)

        self.RB_1.clicked.connect(self.RadioButtonF_1)  # 파일에서 명단 목록
        self.RB_2.clicked.connect(self.RadioButtonF_2)  # 명단 목록 생성

        # 채팅 파일 다시 불러오기
        self.bt_chat_reload.clicked.connect(self.chat_txt_load)

        # combo box changed
        self.chat_txt.currentIndexChanged.connect(self.chat_txt_load)

    # 체크 버튼 클릭
    def buttonF_check(self):
        # 입력한 값을 잘게 나눔
        input_data = (self.te.toPlainText()).split()

        self.te.clear()
        self.lb_not.clear()

        A = []  # 출석 학생
        B = []  # 전체 학생
        # C=[]     미출석 학생

        # 파일에서 목록 불러오기
        if self.RB_1.isChecked() == 1:
            if self.CB_1.currentText() != "":
                filename = self.CB_1.currentText()
                file = open(filename, 'r', encoding='utf-8')
                data = file.read().split()

                for num in data:
                    B.append(num)

                file.close()

            else:
                self.te.append("Error!\nMake sure you have selected the correct item"
                               "\n\n\n\n-------\n\nOnline Checker\n"
                               "\nbuilt on 2021.06.04\n"
                               "\nversion\nPython 3.8\nPyqt 5.15.4\n"
                               "\nFonts - Noto Sans KR\n"
                               "https://fonts.google.com/specimen/Noto+Sans+KR#standard-styles"
                               "\n\nDeveloped by Lee for Sim\n"
                               "\nBug report: hyeonje1147@naver.com")

        # 목록 새로 만들기
        elif self.RB_2.isChecked() == 1:
            data_grade = self.sb_grade.value()
            data_class = self.sb_class.value()
            data_last = self.sb_last.value()

            # data_cut = '%d%02d' % (data_grade,data_class)
            data_zero = '%d%02d00' % (data_grade, data_class)

            for num in range(1, data_last + 1):
                num_st: int = int(data_zero) + num
                B.append(str(num_st))
        else:
            self.te.append("Error!")

        # 자신의 학번
        A.append(self.le_usr_num.text())

        for num in input_data:
            A.append(num[0:5])

        set_C = set(B) - set(A)
        C = list(set_C)

        # 자료 올림차순 정리
        C.sort()

        self.lb_not.setText(str(len(C)) + "명")
        # print(str(len(complement_list))+"명\n")
        for num in C:
            if self.cb_num.checkState() == 2:
                num = num[3:5]
            # print(d)
            self.te.append(num)

    # 채팅 파일 선택
    def chat_txt_select(self):
        self.chat_txt.clear()
        self.chat_txt.addItem("INPUT")

        # Zoom 디렉터리 검사
        if os.path.isdir(zoom_path):
            file_list = os.listdir(zoom_path)

            for num in file_list:
                self.chat_txt.addItem(num[5:-11])

    # 채팅 파일 읽어오기
    def chat_txt_load(self):
        if self.chat_txt.currentText() == "INPUT":
            print("NONE")
        else:
            file_path = zoom_path + self.chat_txt.currentText() + zoom_chat_file_name
            if os.path.isfile(file_path):
                file = open(file_path, 'r', encoding='utf-8')
                self.te.setPlainText(file.read())
                file.close()

    # 데이터 로드
    def data_load(self):

        if os.path.isfile("data.txt") == 1:
            file = open("data.txt", 'r', encoding='utf-8')
            data_read = file.read().split()

            self.sb_grade.setValue(int(data_read[0]))
            self.sb_class.setValue(int(data_read[1]))
            self.sb_last.setValue(int(data_read[2]))
            self.le_usr_num.setText(data_read[3])
            self.cb_num.setChecked(int(data_read[4]))

            file.close()

    # 학번 데이터 불러오기
    def RadioButtonF_1(self):
        self.CB_1.clear()
        self.cb_num.setChecked(False)

        file_list = os.listdir()

        for num in file_list:
            if num[-3:] == "txt":
                if num[0:2] == "F_":
                    self.CB_1.addItem(num)
                    # print(self.CB_1.currentText())

    def RadioButtonF_2(self):
        self.cb_num.setChecked(True)

    # 입력 테이블 지우는 함수
    def buttonF_delete(self):
        self.te.clear()

    # 프로그램 종료
    def buttonF_exit(self):
        sys.exit(app.exec_())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    app.exec_()

# ('checker.ui','.'),('view-refresh.svg','.'),('icon.png','.')
# pyinstaller --onefile --windowed main.spec
