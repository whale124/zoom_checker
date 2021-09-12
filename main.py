import sys, os, os.path
#from typing import Set

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import uic


# UI파일 연결
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    # base_path : py code directory
    return os.path.join(base_path,"resource/",relative_path)


form = resource_path('checker.ui')
form_class = uic.loadUiType(form)[0]

# Zoom 채팅 파일 이름
zoom_path = os.path.expanduser('~') + "/Documents/Zoom/"
zoom_chat_file_name = "/meeting_saved_chat.txt"
list_dir_path = os.getcwd()+"/list/"

# list 폴더 내 파일 이름
list_name = []

# 화면을 띄우는데 사용되는 Class 선언
class WindowClass(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # 프로그램 버전 표시
        self.lb_version.setText("1.0.6")

        # list 폴더가 없을 경우 생성
        # Error 방지
        if(os.path.isdir(list_dir_path)) != 1:
            os.makedirs(list_dir_path)

        # data.txt 파일 불러오기
        self.data_file_load()

        # 줌 채팅 목록 불러오기
        self.LoadChat_item()

        # font load
        font_var = QFont("Noto Sans KR")
        self.te.setCurrentFont(font_var)

        # 버튼에 기능을 연결하는 코드
        self.bt_check.clicked.connect(self.buttonF_check)
        self.bt_delete.clicked.connect(self.buttonF_delete)
        self.bt_exit.clicked.connect(self.buttonF_exit)

        # "./list"에서 명단 목록 불러오기
        self.LoadList_RB.clicked.connect(self.LoadList_item)  # 파일에서 명단 목록
        #self.MakeList_RB.clicked.connect(self.RadioButtonF_2)  # 명단 목록 생성

        # 채팅 파일 다시 불러오기
        self.ReLoadChat.clicked.connect(self.chat_reload)

        # 채팅 목록 선택이 변했을때
        self.LoadChat_ComboBox.currentIndexChanged.connect(self.LoadChat_ComboBox_load)

        self.LoadList_show_button.clicked.connect(self.LoadList_show)
        #self.LoadList_CB.currentIndexChanged.connect(self.LoadList_show)


		# 첫 화면
        #print(os.listdir("./resource/"))
        if os.path.isfile("./resource/welcome.txt") == 1:
            try:
                file = open("./resource/welcome.txt", 'r', encoding='utf-8')
                self.Information_label.setText(file.read())
                file.close()

            except ValueError:
                # 오류 발생시 표시
                self.te.setPlainText('Error!\nCheck your "data.txt" file')

    # 체크 버튼 클릭
    def buttonF_check(self):
        # 입력한 값을 잘게 나눔
        input_data = (self.te.toPlainText()).split()

        self.te.clear()
        self.Absent_count_lb.clear()

        A = []  # 출석 학생
        B = []  # 전체 학생
        # C=[]     미출석 학생

        # 파일에서 목록 불러오기
        if self.LoadList_RB.isChecked():
            if self.LoadList_CB.currentText() != "":
                filename = "%s%s.txt" % (list_dir_path , self.LoadList_CB.currentText())
                #print(filename)

                file = open(filename, 'r', encoding='utf-8')
                data = file.read().split()

                for num in data:
                # "#"으로 시작하는 문자는 포함하지 않음
                    if num[0:1] != "#" :
                        B.append(num)

                file.close()

            else:
                self.te.append("Error!")

        # 목록 새로 만들기
        elif self.MakeList_RB.isChecked():
            data_grade = self.MakeList_grade_spinBox.value()
            data_class = self.MakeList_class_spinBox.value()
            data_last = self.MakeList_amount_spinBox.value()

            # data_cut = '%d%02d' % (data_grade,data_class)
            data_zero = '%d%02d00' % (data_grade, data_class)

            # 명단 저장하기가 켜져 있으면
            if self.MakeList_save_CheckB.isChecked():
                filename = "%s%d-%d.txt" % (list_dir_path , data_grade , data_class)
                file = open(filename,'w',encoding='utf-8')

                # 명단 생성
                for num in range(1, data_last + 1):
                    num_st: int = int(data_zero) + num
                    B.append(str(num_st))

                    # 명단 저장
                    file.write(str(num_st)+"\n")
                file.close()

            else:
                # 명단 생성
                for num in range(1, data_last + 1):
                    num_st: int = int(data_zero) + num
                    B.append(str(num_st))


        else:
            self.te.append("Error!")

        # 자신의 학번
        A.append(self.le_usr_num.text())

        # 입력한 값에서 학번만 추출
        for num in input_data:
            A.append(num[0:5])

        # C=B-A
        set_C = set(B) - set(A)
        C = list(set_C)

        # 자료 올림차순 정리
        C.sort()

        self.Absent_count_lb.setText(str(len(C)) + " 명")
        # print(str(len(complement_list))+"명\n")
        for num in C:
            # 번호만 보기 활성화시
            if self.cb_num.checkState() == 2:
                num = num[3:5]
            # print(d)
            self.te.append(num)

    # 채팅 파일 목록 불러오기
    def LoadChat_item(self):
        list_name.clear()
        list_name.append("")

        self.LoadChat_ComboBox.clear()
        self.LoadChat_ComboBox.addItem("INPUT")

        # Zoom 디렉터리 검사
        if os.path.isdir(zoom_path):
            file_list = os.listdir(zoom_path)
            file_list.sort()

            for num in file_list:
                # 채팅 파일 이름에서 년도와 코드를 제외하고 로딩
                self.LoadChat_ComboBox.addItem(num[5:-11])
                list_name.append(num)
                #self.LoadChat_ComboBox.addItem(num)

    # 채팅 파일 읽어오기
    def LoadChat_ComboBox_load(self):
        if self.LoadChat_ComboBox.currentText() != "INPUT":

            # 삭제된 텍스트를 리스트로 복구.
            file_path = zoom_path + list_name[self.LoadChat_ComboBox.currentIndex()] + zoom_chat_file_name

			# 복구 후 테이블에 입력
            if os.path.isfile(file_path):
                file = open(file_path, 'r', encoding='utf-8')
                self.te.setPlainText(file.read())
                file.close()

    # 채팅 목록 다시 불러오기
    def chat_reload(self):
        # 현재 선택된 파일 이름 백업
        back_txt_path = self.LoadChat_ComboBox.currentText()
        back_list_path = self.LoadList_CB.currentText()

        # data 파일 및 채팅 목록 재 로딩
        self.data_file_load()
        self.LoadChat_item()

        # 백업한 항목이 있다면 불러오기
        if(self.LoadChat_ComboBox.findText(back_txt_path)):
            self.LoadChat_ComboBox.setCurrentText(back_txt_path)
            #print(self.LoadChat_ComboBox.currentText())
        if(self.LoadList_CB.findText(back_list_path)):
            self.LoadList_CB.setCurrentText(back_list_path)

        # 채팅 파일 읽어오기
        self.LoadChat_ComboBox_load()

    # 데이터 로드
    def data_file_load(self):
        # 파일 유무를 확인 후 연다
        if os.path.isfile("data.txt") == 1:
            try:
                file = open("data.txt", 'r', encoding='utf-8')
                data_read = file.read().split()

                # 학년, 반, 번호, 본인 학번
                self.MakeList_grade_spinBox.setValue(int(data_read[0]))
                self.MakeList_class_spinBox.setValue(int(data_read[1]))
                self.MakeList_amount_spinBox.setValue(int(data_read[2]))
                self.le_usr_num.setText(data_read[3])

                # 번호만 표시/명단 저장
                self.cb_num.setChecked(int(data_read[4]))
                self.MakeList_save_CheckB.setChecked(int(data_read[6]))

                # 명단 불러오기 토글
                if int(data_read[5]):
                    self.LoadList_RB.toggle()
                    self.LoadList_item()
                else:
                    self.MakeList_RB.toggle()

                file.close()

            except ValueError:
                # 오류 발생시 표시
                self.te.setPlainText('Error!\nCheck your "data.txt" file')

    # 명단 불러오기
    def LoadList_item(self):
        # 기존 항목 백업
        back_list_path = self.LoadList_CB.currentText()
        #print(back_list_path)

        self.LoadList_CB.clear()
        #self.cb_num.setChecked(False)

        file_list = os.listdir(list_dir_path)
        file_list.sort()

        for num in file_list:
            if num[-3:] == "txt":
                self.LoadList_CB.addItem(num[:-4])

        if(self.LoadList_CB.findText(back_list_path)):
            self.LoadList_CB.setCurrentText(back_list_path)

	# 선택된 명단을 보여주는 함수
    def LoadList_show(self):
        # 보기 항목이 선택되어 있으면
        #if self.LoadList_show_cb.isChecked():

        # 명단이 선택되어 있어야함
        if self.LoadList_CB.currentText() != "":
            filename = "%s%s.txt" % (list_dir_path, self.LoadList_CB.currentText())
            # print(filename)

            file = open(filename, 'r', encoding='utf-8')
            data = file.read()

            self.List_TextEdit.clear()

            self.List_TextEdit.append(data)

            file.close()

        else:
            self.te.append("Error!")

    #def RadioButtonF_2(self):
    #    self.cb_num.setChecked(True)

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

