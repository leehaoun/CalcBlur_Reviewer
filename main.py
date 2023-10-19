import sys
import os
import glob
import datetime
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.cm as cm
import tkinter as tk
import csv
from tkinter import filedialog
from datetime import datetime as dt  # Rename the datetime module
from xml.etree import ElementTree
from xml.dom import minidom
from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QTextBrowser ,QTextEdit, QDesktopWidget, QWidget, QHBoxLayout, QFrame, QFileDialog, QMessageBox, QMainWindow
from collections import defaultdict
from multiprocessing import Pool

class CalcData:
    sFolderPath = "D:\PixelBlur"
    sCSVPath = ""
    sComparePath1 = ""
    sComparePath2 = ""
    nPatternCount = 12
    nIndexCount = 10
    nYtick = 0.5
    nGraphHeight = 10

class xmlData:
    nBlurScore = 0
    nIndex = 0
    def __init__(self, idx, score):
        self.nBlurScore = score
        self.nIndex = idx

def process_csv_data(i, csv_data):
    sTitle = csv_data[i][1]
    MemX = float(csv_data[i][7])
    MemY = float(csv_data[i][8])
    Width = float(csv_data[i][9])
    Height = float(csv_data[i][10])
    if Width >= Height:
        size = Width
    else:
        size = Height
    # Return the updated Title_List and grouped_data
    return sTitle, (MemX, MemY), size

def process_data(grouped_data, GT_List, title):
    if len(grouped_data[title]) > 0:
        matchCnt, list_idx = Calc_Percentage(GT_List, grouped_data[title], 30)
        GTLen = len(GT_List)
        return matchCnt / GTLen * 100, list_idx
    return 0

def Calc_Percentage(GT_List, Target_List, range):
    nCount = 0
    idx_list = []
    for idx, ((x, y) , size) in enumerate(GT_List):
        for (x2, y2), size2 in Target_List:
            if Check_Range(x,x2,range) and Check_Range(y,y2,range) and Check_Range(size,size2, 1): 
                nCount += 1
                idx_list.append(idx)
                break
    return nCount, idx_list


def Check_Range(source, target, range):
    if target >= source - range and target <= source + range:
        return True 
    else: return False

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
        IndexCount_Label = QLabel("Index Count : ", window)
        self.IndexCount_TB = QTextEdit(str(self.datas.nIndexCount),window)
        PatternCount_Label = QLabel("Pattern Count : ", window)
        self.PatternCount_TB = QTextEdit(str(self.datas.nPatternCount),window)
        yTick_Label = QLabel("yTick : ", window)
        self.Ytick_TB = QTextEdit(str(self.datas.nYtick),window)
        GraphHeight_Label = QLabel("Graph Height : ", window)
        self.Graph_Height_TB = QTextEdit(str(self.datas.nGraphHeight),window)
        RunButton = QPushButton("Run", window)
        RunButton2 = QPushButton("Run2", window)
        border_frame = QFrame(window)

        CSV_Path_Label = QLabel("CSV Path", window)
        CSV_Search_Button = QPushButton("Search", window)
        self.CSV_Path = QTextBrowser()
        CSV_Review_Button = QPushButton("CSV Review", window)

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
        IndexCount_Label.setParent(left_widget)
        self.IndexCount_TB.setParent(left_widget)
        PatternCount_Label.setParent(left_widget)
        self.PatternCount_TB.setParent(left_widget)
        GraphHeight_Label.setParent(left_widget)
        self.Graph_Height_TB.setParent(left_widget)
        RunButton.setParent(left_widget)
        RunButton2.setParent(left_widget)
        yTick_Label.setParent(left_widget)
        self.Ytick_TB.setParent(left_widget)
        CSV_Path_Label.setParent(right_widget)
        CSV_Search_Button.setParent(right_widget)
        self.CSV_Path.setParent(right_widget)
        CSV_Review_Button.setParent(right_widget)
        
        border_frame.setGeometry(window.width() // 2, 0, 1, window.height())
        FolderPath_Label.setGeometry(10,52,100,20)
        self.FolderPath_TB.setGeometry(110,50,130,30)
        IndexCount_Label.setGeometry(10,152,100,20)
        self.IndexCount_TB.setGeometry(110,150,50,25)
        PatternCount_Label.setGeometry(10,202,100,20)
        self.PatternCount_TB.setGeometry(110,200,50,25)

        yTick_Label.setGeometry(10,252,100,20)
        self.Ytick_TB.setGeometry(110,252,100,20)

        GraphHeight_Label.setGeometry(10,302,100,20)
        self.Graph_Height_TB.setGeometry(110,300,50,25)
        RunButton.setGeometry(80, 402, 100, 50)
        RunButton2.setGeometry(180, 402, 100, 50)

        CSV_Path_Label.setGeometry(10,52,100,20)
        CSV_Search_Button.setGeometry(110,50,50,25)
        self.CSV_Path.setGeometry(10,100,220,50)
        CSV_Review_Button.setGeometry(80,402,100,50)



        # 변수와 QLineEdit 바인딩
        self.FolderPath_TB.textChanged.connect(self.on_property_changed)
        self.IndexCount_TB.textChanged.connect(self.on_property_changed)
        self.Graph_Height_TB.textChanged.connect(self.on_property_changed)
        self.PatternCount_TB.textChanged.connect(self.on_property_changed)
        self.Ytick_TB.textChanged.connect(self.on_property_changed)
        RunButton.clicked.connect(self.run_function)
        RunButton2.clicked.connect(self.run_function2)
        CSV_Search_Button.clicked.connect(self.CSV_Search)
        CSV_Review_Button.clicked.connect(self.CSV_Review)
        # CompareResult_Button1.clicked.connect(self.select_compare_path1)
        # CompareResult_Button2.clicked.connect(self.select_compare_path2)
        # CompareResult_Button.clicked.connect(self.run_compare)

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
        self.datas.nIndexCount = int(self.IndexCount_TB.toPlainText())
        self.datas.nPatternCount = int(self.PatternCount_TB.toPlainText())
        self.datas.nGraphHeight = int(self.Graph_Height_TB.toPlainText())
        self.datas.nYtick = float(self.Ytick_TB.toPlainText())
        
    def get_csv_file_path(self):
        root = tk.Tk()
        root.withdraw()  # 메인 창을 숨기고 파일 대화 상자만 표시
        
        file_path = filedialog.askopenfilename(
            title="CSV 파일 선택",
            filetypes=[("CSV 파일", "*.csv")],
        )
        
        if file_path:
            return file_path
        else:
            return None
        
    def read_csv_file(self, file_path):
        data = []
        try:
            with open(file_path, newline='', encoding='utf-8') as csvfile:
                csvreader = csv.reader(csvfile)
                for row in csvreader:
                    data.append(row)
            return data
        except FileNotFoundError:
            print(f"파일을 찾을 수 없습니다: {file_path}")
            return None
        except Exception as e:
            print(f"파일을 읽어오는 중 오류 발생: {str(e)}")
            return None

    def CSV_Search(self):
        self.datas.sCSVPath = self.get_csv_file_path()
        self.CSV_Path.clear()
        self.CSV_Path.append(self.datas.sCSVPath)

    def CSV_Review(self):
        num_cores = os.cpu_count()
        sCSVPath = self.datas.sCSVPath
        if sCSVPath == "":
            print("csv Path를 입력하세요")
            return
        else:
            csv_data = self.read_csv_file(self.datas.sCSVPath)
            grouped_data = defaultdict(list)
            Title_List = []

            pool = Pool(num_cores)
            # Use the Pool to process the first loop in parallel
            #results = pool.starmap(process_csv_data, [(i, csv_data) for i in range(1, len(csv_data))])
            results = pool.starmap(process_csv_data, [(i, csv_data) for i in range(1, 10000)])
            # Unpack the results to get the updated Title_List and grouped_data
            # Close the pool of processes
            pool.close()
            pool.join()
            for title, pos, size in results:
                grouped_data[title].append((pos, size))
                if title not in Title_List:
                    Title_List.append(title)
        
            #firstTitle = Title_List[len(Title_List) - 1]
            firstTitle = Title_List[0]
            GT_List = grouped_data[firstTitle]

            error_List = []
            for idx, ((x, y) , size) in enumerate(GT_List):
                for idx2, ((x2, y2) , size2) in enumerate(GT_List):
                    if(abs(x-x2) < 10 and abs(y-y2) < 10 and idx != idx2):
                        error_List.append((idx,idx2))
            return
            # Percentage_List = []
            # List_idx = []

            # pool = Pool(num_cores)
           
            # # Use the Pool to process the second loop in parallel
            # # Percentage_List = pool.starmap(process_data, [(grouped_data, GT_List, Title_List[i]) for i in range(0 , len(Title_List) - 1)])
            # results = pool.starmap(process_data, [(grouped_data, GT_List, Title_List[i]) for i in range(2 , 3)])
            # for Percentages, lists in results:          
            #     Percentage_List = [p for p in Percentages if p > 50]
            #     List_idx = lists
            # # Create a new Pool object for the second loop
            # # Close the pool of processes
            # pool.close()
            # pool.join()
                        
            # root_folder_path = r"D:\BlurScore_Review"
            # now = datetime.datetime.now()
            # work_folder_path = os.path.join(root_folder_path, now.strftime("%Y-%m-%d_%H-%M-%S"))
            # os.makedirs(work_folder_path)
            # save_path = os.path.join(work_folder_path, "result.png")
            # # 리스트의 합계 계산
            # total = sum(Percentage_List)

            # # 리스트의 요소 개수 계산
            # count = len(Percentage_List)

            # # 평균 계산
            # average = total / count

            # # 평균 출력
            # print("반복 횟수:", count)
            # print("반복성 평균:", average)

            # self.save_array_graph(Percentage_List, save_path, "Percentages", True)
            return

    def run_function(self):
        # 실행할 함수의 코드를 여기에 작성합니다.
        sFolderPath = self.datas.sFolderPath
        def extract_datetime(folder_name):
            try:
                year = int(folder_name[:4])
                month = int(folder_name[4:5])
                day = int(folder_name[5:7])
                hour = int(folder_name[7:9])
                minute = int(folder_name[9:11])
                second = int(folder_name[11:13])
                return dt(year, month, day, hour, minute, second)  # Use the renamed datetime module
            except ValueError:
                # Handle incorrect folder name format gracefully
                return dt.min
    
        folder_list = [f for f in glob.glob(sFolderPath + "**/*", recursive=False) if os.path.isdir(f)]
        # folder_list.sort(key=os.path.getctime, reverse=False)
        folder_list.sort(key=lambda folder: extract_datetime(os.path.basename(folder)))
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
            result_Array = [[] for _ in range(self.datas.nPatternCount)]
            if os.path.isfile(xml_file):
                try:
                    tree = ElementTree.parse(xml_file)
                    root = tree.getroot()
                    results = root.find(".//Results")
                    if results is not None:
                        for Feature in results.findall('.//Feature'):
                            Index = Feature.get('Index')
                            Blurs = Feature.findall('.//Blur')
                            if len(Blurs) < self.datas.nPatternCount:
                                print("Blur Count lower than 12")
                                return
                            for blur in Blurs:
                                subIndex = blur.get('SubIndex')
                                result_Array[int(subIndex) - 1].append(blur.get('BlurScore'))
                    flattened_Array = []
                    for inner_Array in result_Array:
                        flattened_Array.extend(inner_Array)
                    result_Arrays.append(flattened_Array)
                except Exception as e:
                    print(f"Error parsing XML file: {xml_file}. Error: {e}")
            # result.xml이 없으면 skip
            else:
                print(f"No result.xml file in folder: {folder}. Skipping to next folder.")
        save_path = os.path.join(work_folder_path, "result.png")

        converted_arrays = []
        for arr in result_Arrays:
            converted_arr = [float(element) for element in arr]
            converted_arrays.append(converted_arr)
        # converted_arrays = [np.array(sublist) for sublist in converted_arrays]
        # 배열들을 NumPy 배열로 변환
        data = np.array(converted_arrays)
        # 각 열(요소별)의 평균과 표준편차 계산
        means = np.nanmean(data, axis=0)
        stddevs = np.nanstd(data, axis=0)

        # sigma3_values = []
        # for i in range(len(means)):
        #     lower_bound = means[i] - 3 * stddevs[i]
        #     upper_bound = means[i] + 3 * stddevs[i]
        #     sigma3_values.append((lower_bound + upper_bound) / 2)

        chipNum = int(len(result_Arrays[0]) / self.datas.nPatternCount)
        self.make_result_data(result_Arrays, stddevs ,work_folder_path)
        self.save_array_graph(result_Arrays, save_path, "BlurScore")
        # sigma3_values의 평균을 계산하여 출력
        sigma3_mean = sum(stddevs) / len(stddevs)
        print("Sigma3 Values의 평균:", sigma3_mean)
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


    def make_result_data(self, result_Arrays, sigma_Arrays , folder_path):
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

    # def save_array_graph(self, data_list, output_file, title, chipNum):
    #     fig, ax = plt.subplots(figsize=(12.8, 9.6))
    #     ax.set_title(title)
        
    #     color_map = cm.get_cmap('tab20b', len(data_list)//2)
    #     color_map_c = cm.get_cmap('tab20c', len(data_list)//2)
        
    #     for idx, data in enumerate(data_list):
    #         temp = np.array(data).astype(float)
    #         x = np.arange(len(temp))
    #         y = np.array(temp)
            
    #         if idx % 2 == 0:
    #             color = color_map(idx // 2)
    #         else:
    #             color = color_map_c((idx - 1) // 2)
            
    #         ax.plot(x, y, label=f'Data {idx+1}', color=color)
    #         ax.text(x[-1] + 0.5, y[-1], str(idx+1), fontsize=8, ha='center', va='bottom')

    #     ax.set_xlabel("SubLine")
    #     ax.set_ylabel("BlurScore")
    #     ax.set_ylim(0, self.datas.nGraphHeight)
    #     ax.set_xlim(0,len(data_list[0]))
    #     pattern = []
    #     for i in range(1, self.datas.nPatternCount + 1):
    #        pattern.extend([str(i)] * self.datas.nIndexCount)
    #     ax.set_xticks(np.arange(0, len(data), 1), pattern)
    #     ax.set_yticks(np.arange(0, self.datas.nGraphHeight, self.datas.nYtick))
    #     ax.legend(bbox_to_anchor=(1.01, 1.15), loc='upper left')
        
    #     # Add a secondary x-axis (ax2)
    #     ax2 = ax.twiny()  # Use twiny() instead of twinx() to create a new x-axis
        
    #     def ax2_to_x(x):
    #         return x / self.datas.nPatternCount  # Convert back to original scale
        
    #     x_positions = np.arange(-1, len(data_list[0]), self.datas.nPatternCount - 1)
    #     ax2.set_xlim(ax.get_xlim())
    #     ax2.set_xticks(x_positions)
    #     ax2.set_xticklabels([f'{int(ax2_to_x(x)):g}' for x in x_positions])
    #     ax2.set_xlabel("구분선")
    #     for x_position in x_positions:
    #         ax2.axvline(x=x_position, color='gray', linestyle='--', alpha=0.5)
    
    #     plt.savefig(output_file)
    #     plt.close()

    def save_array_graph(self, data_list, output_file, title, isCSVReview = False):
        fig, ax = plt.subplots(figsize=(12.8, 9.6))
        ax.set_title(title)
        
        color_map = cm.get_cmap('tab20b', len(data_list)//2)
        color_map_c = cm.get_cmap('tab20c', len(data_list)//2)
        
        if isCSVReview:
            ax.plot(data_list)
        else:
            for idx, data in enumerate(data_list):
                temp = np.array(data).astype(float)
                x = np.arange(len(temp))
                y = np.array(temp)
                if idx % 2 == 0:
                    color = color_map(idx // 2)
                else:
                    color = color_map_c((idx - 1) // 2)
                ax.plot(x, y, label=f'Data {idx+1}', color=color)
                ax.text(x[-1] + 0.5, y[-1], str(idx+1), fontsize=8, ha='center', va='bottom')
            
        ax.set_ylim(0, self.datas.nGraphHeight)
        if isCSVReview :
            ax.set_xlabel("Repeat")
            ax.set_ylabel("Percentage")
            xlim = len(data_list)
            xtick = 1
            ax.set_xticks(np.arange(0, xlim, 1))
            ax.set_yticks(np.arange(0, 101, 5))
            ax.legend(bbox_to_anchor=(1.01, 1.15), loc='upper left')
        else:
            ax.set_xlabel("SubLine")
            ax.set_ylabel("BlurScore")
            xlim = len(data_list[0])
            xtick = len(data)
            ax.set_xlim(0,xlim)
            pattern = []
            for i in range(1, self.datas.nPatternCount + 1):
                pattern.extend([str(i)] * self.datas.nIndexCount)
            ax.set_xticks(np.arange(0, data, 1), pattern)
            ax.set_yticks(np.arange(0, self.datas.nGraphHeight, self.datas.nYtick))
            ax.legend(bbox_to_anchor=(1.01, 1.15), loc='upper left')
            x_positions = np.arange(-1, xlim, self.datas.nPatternCount - 2)
            for x_position in x_positions:
                if (x_position + 1) % (self.datas.nPatternCount - 2) == 0:
                    ax.axvline(x=x_position, color='gray', linestyle=':', alpha=0.5)

        plt.savefig(output_file)
        plt.close()


# main.py 실행
if __name__ == "__main__":
    my_object = MyClass()  # 클래스의 인스턴스 생성
