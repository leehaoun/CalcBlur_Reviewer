import sys
import os
import glob
import datetime
import matplotlib.pyplot as plt
import numpy as np
from xml.etree import ElementTree
from xml.dom import minidom
from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QTextBrowser ,QTextEdit, QDesktopWidget, QWidget, QHBoxLayout, QFrame, QFileDialog, QMessageBox, QMainWindow

class CalcData:
    sFolderPath = "D:\PixelBlur"
    sComparePath1 = ""
    sComparePath2 = ""
    nPatternCount = 8
    nChipPerLine = 4
    nLineCount = 4
    nYtick = 0.5
    nGraphHeight = 30

class xmlData:
    nBlurScore = 0
    nIndex = 0
    def __init__(self, idx, score):
        self.nBlurScore = score
        self.nIndex = idx

class MyClass:
    def __init__(self):
        # 애플리케이션 객체 생성
        app = QApplication(sys.argv)
        self.datas = CalcData()
        # 메인 윈도우 생성
        window = QMainWindow()
        window.setGeometry(100, 100, 500, 500)  # 윈도우 위치와 크기 설정
        window.setWindowTitle("CalcBlur Reviewer")

        left_widget = QWidget(window)
        right_widget = QWidget(window)
        
        window_layout = QHBoxLayout(window)
        left_layout = QHBoxLayout(left_widget)
        right_layout = QHBoxLayout(right_widget)

        left_widget.setGeometry(0, 0, window.width() // 2 , window.height())
        right_widget.setGeometry(window.width() // 2, 0, window.width() // 2, window.height())

        FolderPath_Label = QLabel("Folder Path : ", window)
        self.FolderPath_TB = QTextEdit(self.datas.sFolderPath, window)
        ChipPerLine_Label = QLabel("Chip Per Line : ", window)
        self.ChipPerLine_TB = QTextEdit(str(self.datas.nChipPerLine),window)
        LineCount_Label = QLabel("Line Count : ", window)
        yTick_Label = QLabel("yTick : ", window)
        self.Ytick_TB = QTextEdit(str(self.datas.nYtick),window);
        self.LineCount_TB = QTextEdit(str(self.datas.nLineCount),window)
        GraphHeight_Label = QLabel("Graph Height : ", window)
        self.Graph_Height_TB = QTextEdit(str(self.datas.nGraphHeight),window)
        RunButton = QPushButton("Run", window)
        RunButton2 = QPushButton("Run2", window)
        border_frame = QFrame(window)

        CompareResult_Label1 = QLabel("Compare Path1", window)
        CompareResult_Button1 = QPushButton("Search", window)
        self.CompareResult_Path1 = QTextBrowser()
        CompareResult_Label2 = QLabel("Compare Path2", window)
        CompareResult_Button2 = QPushButton("Search", window)
        self.CompareResult_Path2 = QTextBrowser()
        CompareResult_Button = QPushButton("Compare", window)

        window_layout.addWidget(left_widget)
        window_layout.addWidget(right_widget)
        window_layout.addWidget(border_frame)

        window_layout.setStretchFactor(left_widget, 1)
        window_layout.setStretchFactor(right_widget, 1)
        window_layout.setStretchFactor(border_frame, 0)

        border_frame.setFrameShape(QFrame.VLine)
        border_frame.setFrameShadow(QFrame.Sunken)
        border_frame.setStyleSheet("border: 1px solid black;")

        FolderPath_Label.setParent(left_widget)
        self.FolderPath_TB.setParent(left_widget)
        ChipPerLine_Label.setParent(left_widget)
        self.ChipPerLine_TB.setParent(left_widget)
        LineCount_Label.setParent(left_widget)
        self.LineCount_TB.setParent(left_widget)
        GraphHeight_Label.setParent(left_widget)
        self.Graph_Height_TB.setParent(left_widget)
        RunButton.setParent(left_widget)
        RunButton2.setParent(left_widget)
        yTick_Label.setParent(left_widget)
        self.Ytick_TB.setParent(left_widget)
        CompareResult_Label1.setParent(right_widget)
        CompareResult_Button1.setParent(right_widget)
        self.CompareResult_Path1.setParent(right_widget)
        CompareResult_Label2.setParent(right_widget)
        CompareResult_Button2.setParent(right_widget)
        self.CompareResult_Path2.setParent(right_widget)
        CompareResult_Button.setParent(right_widget)
        
        border_frame.setGeometry(window.width() // 2, 0, 1, window.height())
        FolderPath_Label.setGeometry(10,52,100,20)
        self.FolderPath_TB.setGeometry(110,50,130,30)
        ChipPerLine_Label.setGeometry(10,152,100,20)
        self.ChipPerLine_TB.setGeometry(110,150,50,25)
        LineCount_Label.setGeometry(10,202,100,20)
        self.LineCount_TB.setGeometry(110,200,50,25)

        yTick_Label.setGeometry(10,252,100,20)
        self.Ytick_TB.setGeometry(110,252,100,20)

        GraphHeight_Label.setGeometry(10,302,100,20)
        self.Graph_Height_TB.setGeometry(110,300,50,25)
        RunButton.setGeometry(80, 402, 100, 50)
        RunButton2.setGeometry(180, 402, 100, 50)

        CompareResult_Label1.setGeometry(10,52,100,20)
        CompareResult_Button1.setGeometry(110,50,50,25)
        self.CompareResult_Path1.setGeometry(10,100,220,50)
        CompareResult_Label2.setGeometry(10,172,100,20)
        CompareResult_Button2.setGeometry(110,170,50,25)
        self.CompareResult_Path2.setGeometry(10,220,220,50)
        CompareResult_Button.setGeometry(80,402,100,50)



        # 변수와 QLineEdit 바인딩
        self.FolderPath_TB.textChanged.connect(self.on_property_changed)
        self.ChipPerLine_TB.textChanged.connect(self.on_property_changed)
        self.Graph_Height_TB.textChanged.connect(self.on_property_changed)
        self.LineCount_TB.textChanged.connect(self.on_property_changed)
        self.Ytick_TB.textChanged.connect(self.on_property_changed)
        RunButton.clicked.connect(self.run_function)
        RunButton2.clicked.connect(self.run_function2)
        CompareResult_Button1.clicked.connect(self.select_compare_path1)
        CompareResult_Button2.clicked.connect(self.select_compare_path2)
        CompareResult_Button.clicked.connect(self.run_compare)

        # 메인 윈도우 표시
        self.center_window(window)
        window.show()

        # 애플리케이션 실행
        sys.exit(app.exec())

    def center_window(self, window):
        # 센터에 표시하기 위해 화면의 가운데 좌표를 얻음
        screen = QDesktopWidget().screenGeometry()
        x = (screen.width() - window.width()) // 2
        y = (screen.height() - window.height()) // 2
        window.move(x, y)
        
    def on_property_changed(self):
        self.datas.sFolderPath = self.FolderPath_TB.toPlainText()
        self.datas.nChipPerLine = int(self.ChipPerLine_TB.toPlainText())
        self.datas.nLineCount = int(self.LineCount_TB.toPlainText())
        self.datas.nGraphHeight = int(self.Graph_Height_TB.toPlainText())
        self.datas.nYtick = float(self.Ytick_TB.toPlainText())
    
    
    def run_function(self):
        # 실행할 함수의 코드를 여기에 작성합니다.
        sFolderPath = self.datas.sFolderPath
        folder_list = [f for f in glob.glob(sFolderPath + "**/*", recursive=False) if os.path.isdir(f)]
        folder_list.sort(key=os.path.getctime, reverse=False)

        root_folder_path = r"D:\BlurScore_Review"

        # 폴더 생성
        if not os.path.exists(root_folder_path):
            os.makedirs(root_folder_path)

        now = datetime.datetime.now()
        work_folder_path = os.path.join(root_folder_path, now.strftime("%Y-%m-%d_%H-%M-%S"))
        os.makedirs(work_folder_path)

        result_Arrays = []
        for folder in folder_list:
            xml_file = os.path.join(folder, "result.xml")
            result_Array = []
            # XML 파일이 존재하면
            if os.path.isfile(xml_file):
                try:
                    tree = ElementTree.parse(xml_file)
                    root = tree.getroot()
                    results = root.find(".//Results")
                    if results is not None:
                        for Feature in results.findall('.//Feature'):
                            Index = Feature.get('Index')
                            Blurs = Feature.findall('.//Blur')
                            if len(Blurs) < 6:
                                print("Blur Count lower than 6")
                                return
                            for blur in Blurs:
                                result_Array.append(blur.get('BlurScore'))
                    result_Arrays.append(result_Array)
                except Exception as e:
                    print(f"Error parsing XML file: {xml_file}. Error: {e}")
            # result.xml이 없으면 skip
            else:
                print(f"No result.xml file in folder: {folder}. Skipping to next folder.")
        save_path = os.path.join(work_folder_path, "result.png")
        self.save_array_graph(result_Arrays, save_path, "BlurScore")
        self.make_result_data(result_Arrays, work_folder_path)
        print("Run Finished.")


    def run_function2(self):
        # 실행할 함수의 코드를 여기에 작성합니다.
        sFolderPath = self.datas.sFolderPath
        folder_list = [f for f in glob.glob(sFolderPath + "**/*", recursive=False) if os.path.isdir(f)]
        folder_list.sort(key=os.path.getctime, reverse=False)

        root_folder_path = r"D:\BlurScore_Review"

        # 폴더 생성
        if not os.path.exists(root_folder_path):
            os.makedirs(root_folder_path)

        now = datetime.datetime.now()
        work_folder_path = os.path.join(root_folder_path, now.strftime("%Y-%m-%d_%H-%M-%S"))
        os.makedirs(work_folder_path)

        result_Arrays = []
        for folder in folder_list:
            xml_file = os.path.join(folder, "result.xml")
            result_Array = []
            # XML 파일이 존재하면
            if os.path.isfile(xml_file):
                try:
                    tree = ElementTree.parse(xml_file)
                    root = tree.getroot()
                    results = root.find(".//Results")
                    if results is not None:
                        for Feature in results.findall('.//Feature'):
                            Index = Feature.get('Index')
                            Blurs = Feature.findall('.//Blur')
                            if len(Blurs) < 6:
                                print("Blur Count lower than 6")
                                return
                            for blur in Blurs:
                                result_Array.append(blur.get('BlurScore'))
                    result_Arrays.append(result_Array)
                except Exception as e:
                    print(f"Error parsing XML file: {xml_file}. Error: {e}")
            # result.xml이 없으면 skip
            else:
                print(f"No result.xml file in folder: {folder}. Skipping to next folder.")
        save_path = os.path.join(work_folder_path, "variance_result.png")
        result_Arrays_ToVariance = self.transform_to_variance_arrays(result_Arrays)
        self.save_variance_graph(result_Arrays_ToVariance, save_path, "variance")
        print("Run Finished.")
    def transform_to_variance_arrays(self, input_arrays):
        # 문자열을 숫자로 변환한 NumPy 배열 생성
        numeric_arrays = np.array(input_arrays, dtype=float)
        
        # 열 단위로 분산 계산
        variances = np.var(numeric_arrays, axis=0)
        
        # 결과 리스트 생성
        result_Arrays_ToVariance = []
        
        # 결과 리스트에 분산 값과 각 열의 첫 번째 요소 추가
        for col_idx, variance in enumerate(variances):
            result_Arrays_ToVariance.append([variance])
            
        return result_Arrays_ToVariance

    def make_result_data(self, result_Arrays, folder_path):
        data = ElementTree.Element("data")
        count = ElementTree.SubElement(data, "count")
        count.text = str(len(result_Arrays))
        for i, line_data in enumerate(result_Arrays, start=1):
            line = ElementTree.SubElement(data, "Line", {"num" : str(i)})
            blurs = ElementTree.SubElement(line, "Blurs", {"count" : str(len(line_data))})
            for blur_Value in line_data:
                blur = ElementTree.SubElement(blurs, "Blur")
                blur.text = str(blur_Value)

        raw_string = ElementTree.tostring(data, 'utf-8')    
        parsed_string = minidom.parseString(raw_string)
        pretty_string = parsed_string.toprettyxml(indent="\t")

        # XML 데이터를 파일로 저장
        xml_file_path = os.path.join(folder_path, "data.xml")
        with open(xml_file_path, 'w') as f:
            f.write(pretty_string)

    def save_histogram(self, data, output_file):
        plt.hist(data, bins='auto')
        plt.savefig(output_file)
        plt.close()
    def save_array_graph(self, data_list, output_file, title):
        plt.figure(figsize=(12.8, 9.6))  # 그래프 크기 조정
        plt.title(title)
        for data in data_list:
            temp = np.array(data).astype(float)
            x = np.arange(len(temp))  # 인덱스를 x 축으로 사용
            y = np.array(temp)  # 값들을 y 축으로 사용
            plt.plot(x, y)  # 그래프 그리기

        plt.xlabel("SubLine")
        plt.ylabel("BlurScore")
        plt.ylim(0, self.datas.nGraphHeight)
        plt.yticks(np.arange(0, self.datas.nGraphHeight, self.datas.nYtick))  # y 축 눈금 설정
        plt.legend([f'Data {i+1}' for i in range(0, len(data_list), 1)], bbox_to_anchor=(1.01, 1.15), loc='upper left')
        plt.savefig(output_file)  # 그래프를 파일로 저장
        plt.close()  # 그래프 창 닫기
    def save_variance_graph(self, data_list, output_file, title):
        plt.figure(figsize=(12.8, 9.6))  # 그래프 크기 조정
        plt.title(title)
        for data in data_list:
            temp = np.array(data).astype(float)
            x = np.arange(len(data_list))  # 인덱스를 x 축으로 사용
            y = np.array(data_list)  # 값들을 y 축으로 사용
            plt.plot(x, y)  # 그래프 그리기

        plt.xlabel("SubLine")
        plt.ylabel("BlurScore")
        plt.ylim(0, self.datas.nGraphHeight)
        plt.yticks(np.arange(0, self.datas.nGraphHeight, self.datas.nYtick))  # y 축 눈금 설정
        plt.legend([f'Data {i+1}' for i in range(0, len(data_list), 1)], bbox_to_anchor=(1.01, 1.15), loc='upper left')
        plt.savefig(output_file)  # 그래프를 파일로 저장
        plt.close()  # 그래프 창 닫기

    def save_two_array_graph(self, data1, data2, output_file):
        x1 = np.arange(len(data1))  # 인덱스를 x 축으로 사용
        y1 = np.array(data1)  # 값들을 y 축으로 사용
        x2 = np.arange(len(data2))  # 인덱스를 x 축으로 사용
        y2 = np.array(data2)  # 값들을 y 축으로 사용
        plt.xlabel("Repeat")
        plt.ylabel("Score")
        plt.ylim(0, self.datas.nGraphHeight)
        plt.plot(x1, y1, label='Data1')  # 그래프 1 그리기
        plt.plot(x2, y2, label='Data2')  # 그래프 2 그리기
        plt.legend()  # 범례 추가
        plt.savefig(output_file)  # 그래프를 파일로 저장
        plt.close()  # 그래프 창 닫기
    def select_compare_path1(self):
        dialog = QFileDialog()
        dialog.setDirectory("D:\BlurScore_Review")
        selected_path = dialog.getExistingDirectory(None, "Select Folder")
        self.datas.sComparePath1 = selected_path
        self.CompareResult_Path1.setText(selected_path) 
    def select_compare_path2(self):
        dialog = QFileDialog()
        dialog.setDirectory("D:\BlurScore_Review")
        selected_path = dialog.getExistingDirectory(None, "Select Folder")
        self.datas.sComparePath2 = selected_path
        self.CompareResult_Path2.setText(selected_path) 
    def run_compare(self):
        try:
            first_xml_path = os.path.join(self.datas.sComparePath1, "data.xml")
            second_xml_path = os.path.join(self.datas.sComparePath2, "data.xml")
            first_Blur_Arrays = []
            second_Blur_Arrays = []
            message_box = QMessageBox()
            if not os.path.isfile(first_xml_path) or not os.path.isfile(second_xml_path):
                message_box.setWindowTitle("Warning")
                message_box.setText("data.xml 파일이 없습니다")
                message_box.exec_()
                return
            else:
                first_tree = ElementTree.parse(first_xml_path)
                first_data = first_tree.getroot()
                first_lines = first_data.findall(".//Line")
                for line in first_lines:
                    # Find the 'Blurs' element
                    blurs_element = line.find('.//Blurs')
                    # Extract the Blur values
                    blurs = []
                    for blur_element in blurs_element.findall('Blur'):
                        blur_value = float(blur_element.text)
                        blurs.append(blur_value)
                    first_Blur_Arrays.append(blurs)
                second_tree = ElementTree.parse(second_xml_path)
                second_data = second_tree.getroot()
                second_lines = second_data.findall('.//Line')
                for line in second_lines:
                    # Find the 'Blurs' element
                    blurs_element = line.find('.//Blurs')
                    # Extract the Blur values
                    blurs = []
                    for blur_element in blurs_element.findall('Blur'):
                        blur_value = float(blur_element.text)
                        blurs.append(blur_value)
                    second_Blur_Arrays.append(blurs)
                if len(first_Blur_Arrays) != len(second_Blur_Arrays):
                    message_box.setWindowTitle("Warning")
                    message_box.setText("Line 갯수가 다릅니다")
                    message_box.exec_()
                    return
        except Exception as e:
            print(f"Error: {e}")
        compare_folder_path = r"D:\BlurScore_Review\Compare"
            # 폴더 생성
        if not os.path.exists(compare_folder_path):
            os.makedirs(compare_folder_path)

        now = datetime.datetime.now()
        work_folder_path = os.path.join(compare_folder_path, now.strftime("%Y-%m-%d_%H-%M-%S"))
        os.makedirs(work_folder_path)
        tmp = 0
        for ary1, ary2 in zip(first_Blur_Arrays, second_Blur_Arrays):
            save_path = os.path.join(work_folder_path, f"plot{tmp+1}.png")
            self.save_two_array_graph(ary1,ary2,save_path)
            tmp+=1
        print("Compare Done")



# main.py 실행
if __name__ == "__main__":
    my_object = MyClass()  # 클래스의 인스턴스 생성
