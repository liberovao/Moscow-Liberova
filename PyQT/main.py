import sqlite3
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget, QDialog, QMainWindow
ransw = False
level = ''
number = ''
class Login(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('login.ui',self)
        self.pushButton.clicked.connect(self.run)
        self.checkBox.clicked.connect(self.regist)
        self.level = 0
        self.number = 0
        ransw = False
        
    def regist(self):
        if len(cur.execute('''SELECT * FROM users WHERE name = "''' + self.log.text() + '''"''').fetchall()) == 0:
            #print('''INSERT INTO users (name, password, last_l, last_q) VALUES ("'''+self.log.text()+'''", "'''+self.passw.text()+'''", "1", "1")''')
            cur.execute('''INSERT INTO users (name, password, last_l, last_q) VALUES ("'''+self.log.text()+'''", "'''+self.passw.text()+'''", "1", "1")''')
            con.commit()
            self.run
        
        

    def run(self):
        mes = ''
        if self.log.text() == '':
            mes += 'Пустое значение имени \n'
        else: print(self.log.text())
        if self.passw.text() == '':
            mes += 'Пустое значение пароля \n'
        res = self.check()
        if len(res) == 0:
            mes += 'Неправильные данные'
        else:
            self.level, self.number = res[0]
        self.label_3.setText(mes)
        if mes == '':
            res = cur.execute('''SELECT level, number FROM quest WHERE (level = "''' + str(self.level) + '''" and number >= "''' + str(self.number) + '''") or (level > "''' + str(self.level) + '''") ORDER BY level, number''').fetchall()
            for elem in res:
                self.level, self.number = elem[0], elem[1]
                self.f = Quest(self)
                self.ransw = False
                self.f.setModal(True)          
                self.f.exec()
                if self.ransw == False:
                    print(self.ransw)
                    break
                if self.level == 3 and self.number == 7:
                    self.level = 1
                    self.number = 1
                res = cur.execute('''UPDATE users SET last_l = "''' + str(self.level) + '''", last_q = "''' + str(self.number) + '''" WHERE name = "''' + self.log.text() +'''"''')
                con.commit()
    def check(self):
        res = cur.execute('''SELECT last_l, last_q FROM users WHERE name = "''' + self.log.text() + '''" and password = "''' + self.passw.text() + '''"''').fetchall()
        return res
        
class Quest(QDialog):
    
    def __init__(self, parent):
        super().__init__()
        uic.loadUi('quest_d.ui',self)
        self.radioButton_1.toggled.connect(self.onClicked)
        self.radioButton_2.toggled.connect(self.onClicked)
        self.radioButton_3.toggled.connect(self.onClicked)
        self.radioButton_4.toggled.connect(self.onClicked)
        self.flower.clicked.connect(self.onClicked)
        self.level, self.number = parent.level, parent.number 
        self.parent = parent
        #print(self.level, self.number)
        self.right_answ = 0
        self.run()
        
    def run(self):

        
        self.information.setText('Уровень:'+str(self.level)+' вопрос:'+str(self.number))
        res = cur.execute('''SELECT text, right_answ FROM quest WHERE level = "''' + str(self.level) + '''" and number = "''' + str(self.number) + '''"''').fetchall()
        print('''SELECT text, right_answ FROM quest WHERE level = "''' + str(self.level) + '''" and number = "''' + str(self.number) + '''"''')
        text, self.right_answ = res[0]
        self.question.setText(text)
        res = cur.execute('''SELECT text FROM variant WHERE level = "''' + str(self.level) + '''" and number = "''' + str(self.number) + '''" ORDER BY variant''').fetchall()
        if self.level == 1 or self.level == 3:
            self.radioButton_1.setVisible(True)
            self.radioButton_2.setVisible(True)
            self.radioButton_3.setVisible(True)
            self.radioButton_4.setVisible(True)
            self.flower.setVisible(False)
            self.lineEdit.setVisible(False)
        
            self.radioButton_1.setText(res[0][0])
            self.radioButton_2.setText(res[1][0])
            self.radioButton_3.setText(res[2][0])
            self.radioButton_4.setText(res[3][0])
        else:
            self.radioButton_1.setVisible(False)
            self.radioButton_2.setVisible(False)
            self.radioButton_3.setVisible(False)
            self.radioButton_4.setVisible(False)
            self.flower.setVisible(True)
            self.lineEdit.setVisible(True)

    def onClicked(self, right_answ):
        radioButton = self.sender()
        if radioButton.isChecked():
            ans = radioButton.objectName()[-1]
            if self.level == 1 or self.level == 3:
                if int(ans) == int(self.right_answ):
                    print('Правильный ответ')
                    self.parent.ransw = True
                    self.close()
            
        #print(ans, self.right_answ)
        if str(self.lineEdit.text()).lower() == str(self.right_answ).lower():
            print('Правильный ответ')
            self.parent.ransw = True
            self.close()
        #else:
        #    print(lower(str(self.lineEdit.text())), lower(str(self.right_answ)))
                
con = sqlite3.connect("users.db")
cur = con.cursor()
app = QApplication(sys.argv)
ex = Login()
ex.show()


sys.exit(app.exec_())
con.close()