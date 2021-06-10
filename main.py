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
list_dir_path = os.getcwd()+"/list/"

# list 폴더 내 파일 이름
list_name=[]

# 화면을 띄우는데 사용되는 Class 선언
class WindowClass(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # list 폴더가 없을 경우 생성
        # Error 방지
        if(os.path.isdir(list_dir_path)) != 1:
            os.makedirs(list_dir_path)

        # data.txt 파일 불러오기
        self.data_file_load()

        # 줌 채팅 목록 불러오기
        self.chat_list_load()

        # font load
        fontVar = QFont("Noto Sans KR")
        self.te.setCurrentFont(fontVar)

        # 버튼에 기능을 연결하는 코드
        self.bt_check.clicked.connect(self.buttonF_check)
        self.bt_delete.clicked.connect(self.buttonF_delete)
        self.bt_exit.clicked.connect(self.buttonF_exit)

        self.RB_1.clicked.connect(self.RadioButtonF_1)  # 파일에서 명단 목록
        #self.RB_2.clicked.connect(self.RadioButtonF_2)  # 명단 목록 생성

        # 채팅 파일 다시 불러오기
        self.bt_chat_reload.clicked.connect(self.chat_list_reload)

        # 채팅 목록 선택이 변했을때
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
        if self.RB_1.isChecked():
            if self.CB_1.currentText() != "":
                filename = "%s%s.txt" % (list_dir_path , self.CB_1.currentText())
                #print(filename)

                file = open(filename, 'r', encoding='utf-8')
                data = file.read().split()

                for num in data:
                    B.append(num)

                file.close()

            else:
                self.te.append("Error!")

        # 목록 새로 만들기
        elif self.RB_2.isChecked():
            data_grade = self.sb_grade.value()
            data_class = self.sb_class.value()
            data_last = self.sb_last.value()

            # data_cut = '%d%02d' % (data_grade,data_class)
            data_zero = '%d%02d00' % (data_grade, data_class)

            # 명단 저장하기가 켜져 있으면
            if self.cb_save_list.isChecked():
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

        self.lb_not.setText(str(len(C)) + "명")
        # print(str(len(complement_list))+"명\n")
        for num in C:
            #번호만 보기 활성화시
            if self.cb_num.checkState() == 2:
                num = num[3:5]
            # print(d)
            self.te.append(num)

    # 채팅 파일 목록 불어오기
    def chat_list_load(self):
        list_name.clear()
        list_name.append("")

        self.chat_txt.clear()
        self.chat_txt.addItem("INPUT")

        # Zoom 디렉터리 검사
        if os.path.isdir(zoom_path):
            file_list = os.listdir(zoom_path)
            file_list.sort()

            for num in file_list:
                # 채팅 파일 이름에서 년도와 코드를 제외하고 로딩
                self.chat_txt.addItem(num[5:-11])
                list_name.append(num)
                #self.chat_txt.addItem(num)

    # 채팅 파일 읽어오기
    def chat_txt_load(self):
        if self.chat_txt.currentText() != "INPUT":

            # 삭제된 텍스트를 리스트로 복구.
            file_path = zoom_path + list_name[self.chat_txt.currentIndex()] + zoom_chat_file_name

            if os.path.isfile(file_path):
                file = open(file_path, 'r', encoding='utf-8')
                self.te.setPlainText(file.read())
                file.close()

    # 채팅 목록 다시 불러오기
    def chat_list_reload(self):
        # 현재 선택된 파일 이름 백업
        back_txt_path = self.chat_txt.currentText()
        back_list_path = self.CB_1.currentText()

        # data 파일 및 채팅 목록 재 로딩
        self.data_file_load()
        self.chat_list_load()

        # 백업한 항목이 있다면 불러오기
        if(self.chat_txt.findText(back_txt_path)):
            self.chat_txt.setCurrentText(back_txt_path)
            #print(self.chat_txt.currentText())
        if(self.CB_1.findText(back_list_path)):
            self.CB_1.setCurrentText(back_list_path)

        # 채팅 파일 읽어오기
        self.chat_txt_load()

    # 데이터 로드
    def data_file_load(self):
        # 파일 유무를 확인 후 연다
        if os.path.isfile("data.txt") == 1:
            file = open("data.txt", 'r', encoding='utf-8')
            data_read = file.read().split()

            # 학년, 반, 번호, 본인 학번
            self.sb_grade.setValue(int(data_read[0]))
            self.sb_class.setValue(int(data_read[1]))
            self.sb_last.setValue(int(data_read[2]))
            self.le_usr_num.setText(data_read[3])

            # 번호만 표시/명단 저장
            self.cb_num.setChecked(int(data_read[4]))
            self.cb_save_list.setChecked(int(data_read[6]))

            # 명단 불러오기 토글
            if int(data_read[5]):
                self.RB_1.toggle()
                self.RadioButtonF_1()
            else:
                self.RB_2.toggle()

            file.close()

    # 학번 데이터 불러오기
    def RadioButtonF_1(self):
        # 기존 항목 백업
        back_list_path = self.CB_1.currentText()
        #print(back_list_path)

        self.CB_1.clear()
        #self.cb_num.setChecked(False)

        file_list = os.listdir(list_dir_path)
        file_list.sort()

        for num in file_list:
            if num[-3:] == "txt":
                self.CB_1.addItem(num[:-4])

        if(self.CB_1.findText(back_list_path)):
            self.CB_1.setCurrentText(back_list_path)

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

# ('checker.ui','.'),('./resource/view-refresh.svg','./resource/'),('./resource/icon.png','./resource/')
# pyinstaller -F main.spec
