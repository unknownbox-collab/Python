import sys, sqlite3, os
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import *

mainScreen = uic.loadUiType("ui/main.ui")[0]
settingName = 'default'

class MainClass(QMainWindow, mainScreen):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon("image/icon.png"))
        self.toSplitGrade.clicked.connect(self.openSplitGradeClass)
        self.toGradeCalculator.clicked.connect(self.openCalculatorClass)

    def openSplitGradeClass(self):
        SplitGradeClass(self)
    
    def openCalculatorClass(self):
        CalculatorClass(self)

class SplitGradeClass(QDialog):
    def __init__(self,parent):
        super(SplitGradeClass,self).__init__(parent)
        uic.loadUi("ui/splitGrade.ui", self)
        self.setWindowIcon(QIcon("image/icon.png"))
        self.ok.clicked.connect(self.displaySplitResult)
        self.numInput.returnPressed.connect(self.displaySplitResult)
        self.show()
    
    def displaySplitResult(self):
        students = int(self.numInput.text())
        grade = [
            students*0.04,
            students*0.11,
            students*0.23,
            students*0.4,
            students*0.6,
            students*0.77,
            students*0.89,
            students*0.96, 
            students
        ]
        grade = list(map(round,grade))
        out = ""
        for i in range(9):
            if (i == 0):
                out += f"1등급 : {str(grade[0])}명\n"
            else:
                out += f"{str(i+1)}등급 : {str(grade[i]-grade[i-1])}명\n"
        self.displayer.setText(out)

class CalculatorClass(QDialog):
    global settingName
    def __init__(self,parent):        
        super(CalculatorClass,self).__init__(parent)
        uic.loadUi("ui/calculator.ui", self)
        self.setWindowIcon(QIcon("image/icon.png"))
        
        #sqlite
        setting = sqlite3.connect(f'settings/{settingName}.db')
        remoter = setting.cursor()
        self.subject = {}
        for row in remoter.execute('SELECT * FROM stocks'):
            self.subject[row[0]] = row[1]
        self.subjectList = list(self.subject.keys())

        #pyqt
        self.displaySubject.setRowCount(len(self.subjectList))
        for i in range(len(self.subjectList)):
            self.displaySubject.setItem(i,0,QTableWidgetItem(f'{self.subjectList[i]}({self.subject[self.subjectList[i]]})'))
            spinBox = QSpinBox(self)
            spinBox.setMinimum(1)
            spinBox.setMaximum(9)
            self.displaySubject.setCellWidget(i,1,spinBox)
        self.ok.clicked.connect(self.calculate)
        self.settingSubject.clicked.connect(self.openSettingSubject)
        self.loadSetting.clicked.connect(self.openLoadSetting)
        self.show()
    
    def openSettingSubject(self):
        SettingSubjectClass(self)
    
    def openLoadSetting(self):
        LoadSettingClass(self)

    def calculate(self):
        adder = [0,0]
        for i in range(len(self.subjectList)):
            adder[0] += int(self.subject[self.subjectList[i]]) * self.displaySubject.cellWidget(i,1).value()
            adder[1] += int(self.subject[self.subjectList[i]])
        self.displayResult.setText(str(adder[0]/adder[1]))

class SettingSubjectClass(QDialog):
    def __init__(self,parent):
        super(SettingSubjectClass,self).__init__(parent)
        uic.loadUi("ui/settingSubject.ui", self)
        for i in range(len(self.subjectList)):
            self.displaySubject.setItem(i,0,QTableWidgetItem(f'{self.subjectList[i]}({self.subject[self.subjectList[i]]})'))
            spinBox = QSpinBox(self)
            spinBox.setMinimum(1)
            spinBox.setMaximum(9)
            self.displaySubject.setCellWidget(i,1,spinBox)
        self.setWindowIcon(QIcon("image/icon.png"))
        self.show()

class LoadSettingClass(QDialog):
    def __init__(self,parent):
        super(LoadSettingClass,self).__init__(parent)
        uic.loadUi("ui/loadSubject.ui", self)
        self.setWindowIcon(QIcon("image/icon.png"))
        self.show()

if __name__ == "__main__":
    app = QApplication(sys.argv) 

    myWindow = MainClass() 

    myWindow.show()

    app.exec_()