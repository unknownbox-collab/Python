import sys, sqlite3, os
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5 import QtCore
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
    def __init__(self,parent):
        super(CalculatorClass,self).__init__(parent)
        uic.loadUi("ui/calculator.ui", self)
        self.setWindowIcon(QIcon("image/icon.png"))
        self.loadDB()

        self.ok.clicked.connect(self.calculate)
        self.settingSubject.clicked.connect(self.openSettingSubject)
        self.loadSetting.clicked.connect(self.openLoadSetting)
        self.show()
    
    def loadDB(self):
        setting = sqlite3.connect(f'settings/{settingName}.db')
        remoter = setting.cursor()
        self.subject = {}
        for row in remoter.execute(f'SELECT * FROM "{settingName}"'):
            self.subject[row[0]] = row[1]
        self.subjectList = list(self.subject.keys())
        self.displaySubject.clearContents()
        self.displaySubject.setRowCount(len(self.subjectList))
        for i in range(len(self.subjectList)):
            self.displaySubject.setItem(i,0,QTableWidgetItem(f'{self.subjectList[i]}({self.subject[self.subjectList[i]]})'))
            spinBox = QSpinBox(self)
            spinBox.setMinimum(1)
            spinBox.setMaximum(9)
            self.displaySubject.setCellWidget(i,1,spinBox)

    def openSettingSubject(self):
        SettingSubjectClass(self)
    
    def openLoadSetting(self):
        dlg = LoadSettingClass(self)
        dlg.exec_()
        self.loadDB()

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
        self.setWindowIcon(QIcon("image/icon.png"))
        self.add.clicked.connect(self.addSubject)
        self.subjectDelete.clicked.connect(self.delSubject)
        self.subjectNameInput.returnPressed.connect(self.addSubject)
        self.save.clicked.connect(self.saveSetting)
        self.show()

    def addSubject(self):
        self.subjectDisplay.setRowCount(self.subjectDisplay.rowCount()+1)
        self.subjectDisplay.setItem(self.subjectDisplay.rowCount()-1,0,QTableWidgetItem(str(self.subjectNameInput.text())))
        self.subjectDisplay.setItem(self.subjectDisplay.rowCount()-1,1,QTableWidgetItem(str(self.weight.value())))
    
    def delSubject(self):
        self.subjectDisplay.removeRow(self.subjectDisplay.currentRow())
    
    def saveSetting(self):
        setting = sqlite3.connect(f'settings/{self.settingNameInput.text()}.db')
        remoter = setting.cursor()
        remoter.execute(f'''CREATE TABLE "{self.settingNameInput.text()}" (
            "name" TEXT, "weight" INTEGER)''')
        for i in range(self.subjectDisplay.rowCount()):
            remoter.execute(f'INSERT INTO "{self.settingNameInput.text()}" VALUES ("{self.subjectDisplay.item(i, 0).text()}",{self.subjectDisplay.item(i, 1).text()})')
        setting.commit()
        setting.close()

class LoadSettingClass(QDialog):
    def __init__(self,parent):
        self.emitter = None
        super(LoadSettingClass,self).__init__(parent)
        uic.loadUi("ui/loadSubject.ui", self)
        self.setWindowIcon(QIcon("image/icon.png"))
        self.show()
        self.refindDirs = []
        dirs = os.listdir('settings')
        for i in range(len(dirs)):
            arrDirs = dirs[i].split('.')
            if arrDirs[-1] == "db":
                del arrDirs[-1]
                self.displaySubject.addItem('.'.join(arrDirs))
                self.refindDirs.append('.'.join(arrDirs))
        self.load.clicked.connect(self.closer)

    def closer(self):
        global settingName
        settingName = self.refindDirs[self.displaySubject.currentRow()]
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv) 

    myWindow = MainClass() 

    myWindow.show()

    app.exec_()