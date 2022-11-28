from PyQt5 import QtCore, QtGui, QtWidgets
import sqlite3
from evaluation.evaluation import evaluate

class Ui_MainWindow(object):
    def __init__(self):
        self.count_BAT=0
        self.count_WK=0
        self.count_BOW=0
        self.count_AR=0
        self.PointAvl=1000
        self.Pointused=0
        self.teams=set()
        self.AllTeams=[]
        self.playersSelectedList=[]

    # Sql command for Connecting FantasyCricket Database
    def connectdb(self):
        cricket=sqlite3.connect('fantasycricket.db')
        objcricket=cricket.cursor()
        return objcricket

    # Method for displaying BatsMan in ListWidget(playersList)
    def BAT_players(self):
        objcricket=self.connectdb()
        self.PlayersList.clear()
        objcricket.execute('''SELECT Players FROM Stats WHERE ctg="BAT" ''')
        for i in objcricket.fetchall():
            if i[0] not in self.playersSelectedList:
                self.PlayersList.addItem(i[0])

    # Method for displaying Bowlers in ListWidget(playersList)
    def BOW_players(self):
        objcricket=self.connectdb()
        self.PlayersList.clear()
        objcricket.execute('''SELECT Players FROM Stats WHERE ctg="BWL" ''')
        for i in objcricket.fetchall():
            if i[0] not in self.playersSelectedList:
                self.PlayersList.addItem(i[0])

    # Method for displaying AllRounders in ListWidget(playersList)
    def AR_players(self):
        objcricket=self.connectdb()
        self.PlayersList.clear()
        objcricket.execute('''SELECT Players FROM Stats WHERE ctg="AR" ''')
        for i in objcricket.fetchall():
            if i[0] not in self.playersSelectedList:
                self.PlayersList.addItem(i[0])

    # Method for showing WicketKeeper in ListWidget
    def WK_players(self):
        objcricket=self.connectdb()
        self.PlayersList.clear()
        objcricket.execute('''SELECT Players FROM Stats WHERE ctg="WK" ''')
        for i in objcricket.fetchall():
            if i[0] not in self.playersSelectedList:
                self.PlayersList.addItem(i[0])
    
    # Method for Opening Team
    def open_team(self):
        self.teams=set()
        self.playersSelectedList=[]
        cricket=sqlite3.connect('fantasycricket.db')
        objcricket=cricket.cursor()
        objcricket.execute('''SELECT Name FROM Teams''')
        rows= objcricket.fetchall()
        for row in rows:
            self.teams.add(row[0])
        self.team, ok=QtWidgets.QInputDialog.getItem(MainWindow,"Open","Choose A Team",self.teams,0,False)
        if ok == True:
            self.entername.setText(self.team)
            self.PointAvl_count.setText("1000")
            self.Pointused_count.setText("0")
            self.AR_count.setText("0")
            self.WK_count.setText("0")
            self.BOW_count_3.setText("0")
            self.BAT_count.setText("0")
            self.SelectedPlayers.clear()
            self.PlayersList.clear()
            self.count_BAT=0
            self.count_WK=0
            self.count_BOW=0
            self.count_AR=0
            self.PointAvl=1000
            self.Pointused=0
            self.AllTeams=[]
            self.WK_Button.clicked.connect(self.WK_players) # ----------- WK Button
            self.BAT_Button.clicked.connect(self.BAT_players) #--------BAT BUTTON
            self.BOW_Button.clicked.connect(self.BOW_players) #=-------BOW BUTTON
            self.AR_Button.clicked.connect(self.AR_players) #--------AR BUTTON
                
            objcricket=self.connectdb()
            objcricket.execute('''SELECT Players,Name,value FROM Teams''')
            for i in objcricket.fetchall():
                if i[1] == self.team:
                    self.Pointused+=i[2]
                    self.Pointused_count.setText(str(self.Pointused))
                    self.PointAvl_count.setText(str(self.PointAvl-self.Pointused))
                    self.SelectedPlayers.addItem(i[0])
                    self.playersSelectedList.append(i[0])
                    
            objcricket.execute('''SELECT Players,ctg FROM Stats''')
            for i in objcricket.fetchall():
                if i[0] in self.playersSelectedList:
                    if i[1] == 'WK':
                        self.count_WK+=1
                        self.WK_count.setText(str(self.count_WK))
                    if i[1] == 'BWL':
                        self.count_BOW+=1
                        self.BOW_count_3.setText(str(self.count_BOW))
                    if i[1] == 'AR':
                        self.count_AR+=1
                        self.AR_count.setText(str(self.count_AR))
                    if i[1] == 'BAT':
                        self.count_BAT+=1
                        self.BAT_count.setText(str(self.count_BAT))
        else: pass

    # Method for Saving Team
    def save_team(self):
        cricket=sqlite3.connect('fantasycricket.db')
        objcricket=cricket.cursor()
        objcricket.execute('''SELECT Name FROM Teams''')
        self.teamlist=[]
        if self.entername.text() !="":
            if self.SelectedPlayers.count() == 11:
                for i in objcricket.fetchall():
                    self.teamlist.append(i[0])
                objcricket.execute('''SELECT Players,ctg,value FROM Stats''')
                self.k=0
                if self.entername.text() not in self.teamlist:
                    for i in objcricket.fetchall():
                        if i[0] in self.playersSelectedList:
                            objcricket.execute('''INSERT INTO Teams(Players,Name,value)
                            VALUES ("%s","%s","%i")'''%(self.playersSelectedList[self.k],self.entername.text(),i[2]))
                            cricket.commit()
                            self.k+=1
                    self.messagebox('Hurrayyy',"%s Team Saved Successfully"%(self.entername.text()))
                    self.PlayersList.clear()
                    self.SelectedPlayers.clear()
                    self.playersSelectedList=[]
                    self.count_BAT=0
                    self.count_WK=0
                    self.count_BOW=0
                    self.count_AR=0
                    self.PointAvl=1000
                    self.Pointused=0
                    self.entername.clear()
                    self.entername.setPlaceholderText("Enter Name")
                    self.PointAvl_count.setText("1000")
                    self.Pointused_count.setText("0")
                    self.AR_count.setText("0")
                    self.WK_count.setText("0")
                    self.BOW_count_3.setText("0")
                    self.BAT_count.setText("0")
                else:
                    self.messagebox('Sorry','%s Team Already Exist.\n(If You Want to Modify Team, Delete it and Save Modified Team)'%(self.entername.text()))
            else:
                self.messagebox('Error','There Should be 11 Players')
        else:
            self.messagebox('Error','Please Enter Team Name')


    # Method for Creating a New Team
    def new_team(self):
        self.messagebox('Welcome','''Please Enter Team Name in the Team Name section\n(Choose 11 Players Precisely)''')
        self.PlayersList.clear()
        self.SelectedPlayers.clear()
        self.playersSelectedList=[]
        self.count_BAT=0
        self.count_WK=0
        self.count_BOW=0
        self.count_AR=0
        self.PointAvl=1000
        self.Pointused=0
        self.WK_Button.clicked.connect(self.WK_players) # ----------- WK Button
        self.BAT_Button.clicked.connect(self.BAT_players) #--------BAT BUTTON
        self.BOW_Button.clicked.connect(self.BOW_players) #=-------BOW BUTTON
        self.AR_Button.clicked.connect(self.AR_players) #--------AR BUTTON
        self.entername.clear()
        self.entername.setPlaceholderText("Enter Name")
        self.PointAvl_count.setText("1000")
        self.Pointused_count.setText("0")
        self.AR_count.setText("0")
        self.WK_count.setText("0")
        self.BOW_count_3.setText("0")
        self.BAT_count.setText("0")

    # Message box
    def messagebox(self,title,message):
        mess=QtWidgets.QMessageBox()
        mess.setWindowTitle(title)
        mess.setText(message)
        mess.setStandardButtons(QtWidgets.QMessageBox.Ok)
        mess.setIcon(QtWidgets.QMessageBox.Information)
        mess.setWindowIcon(QtGui.QIcon('Icons\\message.png'))
        mess.exec_()

    # Method for Deleting Team
    def delete_team(self):
        objcricket=self.connectdb()
        objcricket.execute('''SELECT Name FROM Teams''')
        rows= objcricket.fetchall()
        self.teams=set()
        for row in rows:
            self.teams.add(row[0])
        self.team, ok=QtWidgets.QInputDialog.getItem(MainWindow,"Delete Team","Choose Team to Delete:",self.teams,0,False)
        if ok == True:
            cricket=sqlite3.connect('fantasycricket.db')
            objcricket=cricket.cursor()
            objcricket.execute('''SELECT Name FROM Teams''')
            for i in objcricket.fetchall():
                self.AllTeams.append(i[0])
            if self.team in self.AllTeams:
                objcricket.execute('''DELETE FROM Teams WHERE Name="%s"'''%(self.team))
                cricket.commit()
                self.messagebox('Hurrayyy!!','%s Team Successfully Deleted'%(self.team))
            elif self.team not in self.AllTeams :
                self.messagebox('Warning!!',"%s Team doesn't exists.\n Please enter Valid Team name to Delete in 'Team Name' Section"%(self.entername.text()))
        else: pass

    # Removing and adding Players in the ListWidget from PlayersList to SeletedPlayers
    def removePlayersList(self,item):
        objcricket=self.connectdb()
        objcricket.execute('''SELECT Players,ctg,value FROM Stats''')
        if self.SelectedPlayers.count()<12:
            self.PlayersList.takeItem(self.PlayersList.row(item))
            if item.text() not in self.playersSelectedList:
                for i in objcricket.fetchall(): 
                    if item.text() == i[0]:
                        if self.PointAvl >= i[2]:
                            if i[1] == 'BAT':
                                self.count_BAT+=1
                                self.BAT_count.setText("%s"%(self.count_BAT))
                                self.SelectedPlayers.addItem(item.text())
                                self.playersSelectedList.append(item.text())
                            elif i[1] == "WK":
                                self.count_WK+=1
                                if self.count_WK<=1:
                                    self.WK_count.setText('%s'%(self.count_WK))
                                    self.SelectedPlayers.addItem(item.text())
                                    self.playersSelectedList.append(item.text())
                                elif self.count_WK==2:
                                    self.messagebox('Warning', "You can't select more than 1 Wicket Keeper")
                                    break
                            elif i[1] == 'AR':
                                self.count_AR+=1
                                self.AR_count.setText('%s'%(self.count_AR))
                                self.SelectedPlayers.addItem(item.text())
                                self.playersSelectedList.append(item.text())
                            elif i[1] == 'BWL':
                                self.count_BOW+=1
                                self.BOW_count_3.setText('%s'%(self.count_BOW))
                                self.SelectedPlayers.addItem(item.text())
                                self.playersSelectedList.append(item.text()) 
                            self.PointAvl-=i[2]
                            self.Pointused+=i[2]
                            self.PointAvl_count.setText(str(self.PointAvl))
                            self.Pointused_count.setText(str(self.Pointused))
                        elif self.PointAvl < i[2]:
                            self.messagebox('Warning',"You don't you have enough Points")
                            break
            else:
                self.messagebox('Warning',"You Can't select same Player Again")
        else:
            self.messagebox('Warning',"You can't select more than 11 Players")

   
    # Removing and adding Players in the ListWidget from SeletedPlayers to PlayersList 
    def removeSelectedPlayers(self,item):
        self.PointAvl=int(self.PointAvl_count.text())
        objcricket=self.connectdb()
        objcricket.execute('''SELECT Players,ctg,value FROM Stats''')
        self.SelectedPlayers.takeItem(self.SelectedPlayers.row(item))
        for i in objcricket.fetchall():
            c=i[2]  
            if item.text()==i[0]:
                if i[1] == 'BAT':
                    self.count_BAT-=1
                    self.BAT_count.setText("%s"%(self.count_BAT))
                    self.PlayersList.addItem(item.text())
                    self.playersSelectedList.remove(item.text())
                elif i[1] == "WK":
                    self.count_WK=0
                    self.WK_count.setText('%s'%(self.count_WK))
                    self.PlayersList.addItem(item.text())
                    self.playersSelectedList.remove(item.text())
                elif i[1] == 'AR':
                    self.count_AR-=1
                    self.AR_count.setText('%s'%(self.count_AR))
                    self.PlayersList.addItem(item.text())
                    self.playersSelectedList.remove(item.text())
                elif i[1] == 'BWL':
                    self.count_BOW-=1
                    self.BOW_count_3.setText('%s'%(self.count_BOW))
                    self.PlayersList.addItem(item.text())
                    self.playersSelectedList.remove(item.text())
                self.PointAvl+=c
                self.Pointused-=c
                self.PointAvl_count.setText(str(self.PointAvl))
                self.Pointused_count.setText(str(self.Pointused))

    # Opening Imported file for evaluation
    def openEvaluate(self):
        self.window=QtWidgets.QWidget()
        self.ui= evaluate.Ui_Evaluation()
        self.ui.setupUi(self.window)
        self.window.show()

    # Method for showing Instructions for Fantasy Cricket Game
    def instruction(self):
        mess=QtWidgets.QMessageBox()
        mess.setWindowTitle('Welcome to Fantasy Cricket Game')
        message='''Here are Some Instructions:\n
1. Select 'New Team' in 'Manage Team' Menu or click  'Ctrl+N' to create a New Team\n
2. Select 'Save Team' in 'Manage Team Menu or click  Ctrl+S to Save the Team\n
3. Select 'Open Team' in 'Manage Team' Menu or click  Ctrl+O to Open Team\n
4. Select 'Delete Team' in 'Manage Team' Menu or click  Ctrl+Q to Delete a Team\n
5. Inorder to modify the Team, You can Delete that Team and re-create it\n'''
        mess.setText(message)
        mess.setStandardButtons(QtWidgets.QMessageBox.Ok)
        mess.setWindowIcon(QtGui.QIcon('Icons\\message.png'))
        mess.exec_()

    # Method for Displaying About Fantasy Cricket Game
    def about(self):
        mess=QtWidgets.QMessageBox()
        mess.setWindowTitle('Welcome to Fantasy Cricket Game')
        message='''Hi!  This is Fantasy Cricket Game\nCreated By \bAyushi Aggarwal\b\n
\aIn this Game, you can \n  --> Create a NEW team \n  --> Open and Edit a team \n  -->Delete a team\n  -->Evaluate Teams'''
        mess.setText(message)
        mess.setStandardButtons(QtWidgets.QMessageBox.Ok)
        mess.setWindowIcon(QtGui.QIcon('Icons\\message.png'))
        mess.exec_()

           
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(391, 650)
        MainWindow.setWindowIcon(QtGui.QIcon('Icons\\cricket.png'))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.AR_count = QtWidgets.QLabel(self.centralwidget)
        self.AR_count.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.AR_count.setFrameShadow(QtWidgets.QFrame.Raised)
        self.AR_count.setObjectName("AR_count")
        font = QtGui.QFont()
        font.setBold(True)
        self.AR_count.setFont(font)
        self.gridLayout.addWidget(self.AR_count, 2, 5, 1, 1)
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridLayout.addWidget(self.line, 2, 2, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(10, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 8, 7, 1, 2)
        self.BAT_label_2 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.BAT_label_2.setFont(font)
        self.BAT_label_2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.BAT_label_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.BAT_label_2.setObjectName("BAT_label_2")
        self.gridLayout.addWidget(self.BAT_label_2, 2, 11, 1, 1)
        self.BOW_label_2 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.BOW_label_2.setFont(font)
        self.BOW_label_2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.BOW_label_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.BOW_label_2.setObjectName("BOW_label_2")
        self.gridLayout.addWidget(self.BOW_label_2, 2, 0, 1, 1)
        self.BOW_count_3 = QtWidgets.QLabel(self.centralwidget)
        self.BOW_count_3.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.BOW_count_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.BOW_count_3.setObjectName("BOW_count_3")
        font.setBold(True)
        self.BOW_count_3.setFont(font)
        self.gridLayout.addWidget(self.BOW_count_3, 2, 1, 1, 1)
        self.Pointused_count = QtWidgets.QLabel(self.centralwidget)
        self.Pointused_count.setFrameShape(QtWidgets.QFrame.Box)
        self.Pointused_count.setFrameShadow(QtWidgets.QFrame.Raised)
        self.Pointused_count.setObjectName("Pointused_count")
        self.gridLayout.addWidget(self.Pointused_count, 6, 14, 1, 3)
        self.BAT_count = QtWidgets.QLabel(self.centralwidget)
        self.BAT_count.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.BAT_count.setFrameShadow(QtWidgets.QFrame.Raised)
        self.BAT_count.setObjectName("BAT_count")
        font.setBold(True)
        self.BAT_count.setFont(font)
        self.gridLayout.addWidget(self.BAT_count, 2, 12, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setBold(True)
        font.setItalic(False)
        font.setUnderline(False)
        font.setPointSize(10)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 0, 0, 1, 1)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.teamname_label = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        self.teamname_label.setFont(font)
        self.teamname_label.setObjectName("teamname_label")
        self.horizontalLayout_2.addWidget(self.teamname_label)
        self.entername = QtWidgets.QLineEdit(MainWindow)
        font = QtGui.QFont()
        self.entername.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.entername.setObjectName("entername")
        self.horizontalLayout_2.addWidget(self.entername)
        self.gridLayout.addLayout(self.horizontalLayout_2, 7, 11, 1, 6)
        spacerItem1 = QtWidgets.QSpacerItem(10, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 8, 5, 1, 1)
        self.SelectedPlayers = QtWidgets.QListWidget(self.centralwidget)
        self.SelectedPlayers.setObjectName("SelectedPlayers")
        font.setItalic(False)
        font.setUnderline(False)
        self.gridLayout.addWidget(self.SelectedPlayers, 8, 11, 1, 6)
        self.WK_count = QtWidgets.QLabel(self.centralwidget)
        self.WK_count.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.WK_count.setFrameShadow(QtWidgets.QFrame.Raised)
        self.WK_count.setObjectName("WK_count")
        font.setBold(True)
        self.gridLayout.addWidget(self.WK_count, 2, 16, 1, 1)
        self.WK_label_2 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.WK_label_2.setFont(font)
        self.WK_label_2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.WK_label_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.WK_label_2.setObjectName("WK_label_2")
        self.gridLayout.addWidget(self.WK_label_2, 2, 14, 1, 2)
        self.Direction = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(18)
        self.Direction.setFont(font)
        self.Direction.setObjectName("Direction")
        self.gridLayout.addWidget(self.Direction, 8, 6, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.WK_Button = QtWidgets.QRadioButton(self.centralwidget)
        font = QtGui.QFont()
        self.WK_Button.setObjectName("WK_Button")    
        self.horizontalLayout.addWidget(self.WK_Button)
        self.BAT_Button = QtWidgets.QRadioButton(self.centralwidget)
        font = QtGui.QFont()
        self.BAT_Button.setObjectName("BAT_Button")
        self.horizontalLayout.addWidget(self.BAT_Button)
        self.BOW_Button = QtWidgets.QRadioButton(self.centralwidget)
        font = QtGui.QFont()
        self.BOW_Button.setObjectName("BOW_Button")
        self.horizontalLayout.addWidget(self.BOW_Button)
        self.AR_Button = QtWidgets.QRadioButton(self.centralwidget)
        font = QtGui.QFont()
        self.AR_Button.setObjectName("AR_Button")
        self.horizontalLayout.addWidget(self.AR_Button)
        self.gridLayout.addLayout(self.horizontalLayout, 7, 0, 1, 5)
        self.PtsUsed_label = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.PtsUsed_label.setObjectName("PtsUsed_label")
        self.gridLayout.addWidget(self.PtsUsed_label, 6, 11, 1, 2)
        spacerItem2 = QtWidgets.QSpacerItem(20, 30, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.gridLayout.addItem(spacerItem2, 4, 0, 1, 1)
        self.line_3 = QtWidgets.QFrame(self.centralwidget)
        self.line_3.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.gridLayout.addWidget(self.line_3, 2, 13, 1, 1)
        self.PlayersList = QtWidgets.QListWidget(self.centralwidget)
        self.PlayersList.setObjectName("PlayersList")
        font.setBold(False)
        self.gridLayout.addWidget(self.PlayersList, 8, 0, 1, 5)
        self.line_2 = QtWidgets.QFrame(self.centralwidget)
        self.line_2.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.gridLayout.addWidget(self.line_2, 2, 8, 1, 1)
        self.line_4 = QtWidgets.QFrame(self.centralwidget)
        self.line_4.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_4.setObjectName("line_4")
        self.gridLayout.addWidget(self.line_4, 5, 0, 1, 16)
        self.AR_label_2 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.AR_label_2.setFont(font)
        self.AR_label_2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.AR_label_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.AR_label_2.setObjectName("AR_label_2")
        self.gridLayout.addWidget(self.AR_label_2, 2, 3, 1, 2)
        self.PtsAVL_label = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.PtsAVL_label.setObjectName("PtsAVL_label")
        self.gridLayout.addWidget(self.PtsAVL_label, 6, 0, 1, 2)
        self.PointAvl_count = QtWidgets.QLabel(self.centralwidget)
        self.PointAvl_count.setFrameShape(QtWidgets.QFrame.Box)
        self.PointAvl_count.setFrameShadow(QtWidgets.QFrame.Raised)
        self.PointAvl_count.setObjectName("PointAvl_count")
        self.gridLayout.addWidget(self.PointAvl_count, 6, 2, 1, 3)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 391, 18))
        self.menubar.setObjectName("menubar")
        self.menuManage_Team = QtWidgets.QMenu(self.menubar)
        self.menuManage_Team.setObjectName("menuManage_Team")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionNew_Team = QtWidgets.QAction(MainWindow)
        self.actionNew_Team.setObjectName("actionNew_Team")
        self.actionOpen_Team = QtWidgets.QAction(MainWindow)
        self.actionOpen_Team.setObjectName("actionOpen_Team")
        self.actionSave_Team = QtWidgets.QAction(MainWindow)
        self.actionSave_Team.setObjectName("actionSave_Team")
        self.actionQuit_Team = QtWidgets.QAction(MainWindow)
        self.actionQuit_Team.setObjectName("actionQuit_Team")
        self.actionEvaluate_Team = QtWidgets.QAction(MainWindow)
        self.actionEvaluate_Team.setObjectName("actionEvaluate_Team")
        self.actionDelete_Team=QtWidgets.QAction(MainWindow)
        self.actionDelete_Team.setObjectName("actionDelete_Team")
        self.actionInstruction_Team=QtWidgets.QAction(MainWindow)
        self.actionInstruction_Team.setObjectName("actionInstruction_Team")
        self.actionAbout=QtWidgets.QAction(MainWindow)
        self.actionAbout.setObjectName("actionAbout")
        self.PlayersList.itemDoubleClicked.connect(self.removePlayersList)     # Connecting Method removePlayersList 
        self.SelectedPlayers.itemDoubleClicked.connect(self.removeSelectedPlayers)  # Connecting Method SelectedPlayers

        self.menuManage_Team.addAction(self.actionNew_Team)
        self.menuManage_Team.addAction(self.actionOpen_Team)
        self.menuManage_Team.addAction(self.actionSave_Team)
        self.menuManage_Team.addAction(self.actionDelete_Team)
        self.menuManage_Team.addAction(self.actionEvaluate_Team)
        self.menuManage_Team.addAction(self.actionQuit_Team)
        self.menuHelp.addAction(self.actionInstruction_Team)
        self.menuHelp.addAction(self.actionAbout)
        self.menubar.addAction(self.menuManage_Team.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        # ====================Adding Icons======================<<
        self.actionNew_Team.setIcon(QtGui.QIcon('Icons\\newteam.png'))
        self.actionSave_Team.setIcon(QtGui.QIcon('Icons\\saveteam.png'))
        self.actionOpen_Team.setIcon(QtGui.QIcon('Icons\\openteam.png'))
        self.actionEvaluate_Team.setIcon(QtGui.QIcon('Icons\\evaluateteam.png'))
        self.actionDelete_Team.setIcon(QtGui.QIcon('Icons\\delete.png'))
        self.actionQuit_Team.setIcon(QtGui.QIcon('Icons\\quit.png'))
        self.actionInstruction_Team.setIcon(QtGui.QIcon('Icons\\instruction.png'))
        self.actionAbout.setIcon(QtGui.QIcon('Icons\\about.png'))

        #============= Connecting All Action methods===========<<
        self.actionSave_Team.triggered.connect(self.save_team)
        self.actionNew_Team.triggered.connect(self.new_team)
        self.actionOpen_Team.triggered.connect(self.open_team)
        self.actionDelete_Team.triggered.connect(self.delete_team)
        self.actionEvaluate_Team.triggered.connect(self.openEvaluate)
        self.actionQuit_Team.triggered.connect(exit)
        self.actionInstruction_Team.triggered.connect(self.instruction)
        self.actionAbout.triggered.connect(self.about)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.setTabOrder(self.WK_Button, self.BAT_Button)
        MainWindow.setTabOrder(self.BAT_Button, self.AR_Button)
        MainWindow.setTabOrder(self.AR_Button, self.BOW_Button)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Cricket Fantasy Game"))
        self.BAT_label_2.setText(_translate("MainWindow", "Batsman(BAT)"))
        self.BOW_label_2.setText(_translate("MainWindow", "Bowlers(BOW)"))
        self.label_6.setText(_translate("MainWindow", "Your Selection"))
        self.teamname_label.setText(_translate("MainWindow", "Team Name :"))
        self.WK_label_2.setText(_translate("MainWindow", "Wicket-keeper(WK)"))
        self.Direction.setText(_translate("MainWindow", ">>"))
        self.WK_Button.setText(_translate("MainWindow", "WK"))
        self.BAT_Button.setText(_translate("MainWindow", "BAT"))
        self.BOW_Button.setText(_translate("MainWindow", "BOW"))
        self.AR_Button.setText(_translate("MainWindow", "AR"))
        self.PtsUsed_label.setText(_translate("MainWindow", "Points Used :"))
        self.AR_label_2.setText(_translate("MainWindow", "AllRounders(AR)"))
        self.PtsAVL_label.setText(_translate("MainWindow", "Points Available :"))
        self.menuManage_Team.setTitle(_translate("MainWindow", "Manage Team"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))
        self.actionNew_Team.setText(_translate("MainWindow", "New Team"))
        self.actionNew_Team.setShortcut(_translate("MainWindow","Ctrl+N"))
        self.actionOpen_Team.setText(_translate("MainWindow", "Open Team"))
        self.actionOpen_Team.setShortcut(_translate("MainWindow","Ctrl+O"))
        self.actionSave_Team.setText(_translate("MainWindow", "Save Team"))
        self.actionSave_Team.setShortcut(_translate("MainWindow","Ctrl+S"))
        self.actionDelete_Team.setText(_translate("MainWindow","Delete Team"))
        self.actionDelete_Team.setShortcut(_translate("MainWindow","Ctrl+Q"))
        self.actionQuit_Team.setText(_translate("MainWindow","Quit"))
        self.actionQuit_Team.setShortcut(_translate("MainWindow","Esc"))
        self.actionEvaluate_Team.setText(_translate("MainWindow", "Evaluate Team"))
        self.actionInstruction_Team.setText(_translate("MainWindow","Instructions"))
        self.actionAbout.setText(_translate("Mainwindow","About"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
