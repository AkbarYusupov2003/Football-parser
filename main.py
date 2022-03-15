import sys
import requests
from PyQt6 import QtCore, QtGui, QtWidgets
from parse_data import get_league_table, get_previous_match, get_previous_matches, get_upcoming_matches


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setFixedSize(960, 1080)
        MainWindow.setWindowTitle("Manchester United")
        MainWindow.setWindowIcon(QtGui.QIcon('images/mu.png'))
        MainWindow.move(0, 0)
        self.scroll = QtWidgets.QScrollArea()
        self.scroll.setObjectName('scroll')
        self.central_widget = QtWidgets.QWidget(MainWindow)
        self.central_widget.setObjectName("central_widget")
        self.central_widget.resize(960, 1950)
        self.scroll.setWidget(self.central_widget)
        self.central_widget.setStyleSheet(
            """
            #central_widget{
                background: qlineargradient( x1:0 y1:0, x2:1 y2:0, stop:0 rgb(0, 173, 239), stop:1 rgb(37, 66, 255) );
            }        
            """
        )

        self.epl = QtWidgets.QLabel(self.central_widget)
        self.epl.setGeometry(QtCore.QRect(360, 0, 240, 55))
        self.epl.setPixmap(QtGui.QPixmap("images/epl.png"))
        self.epl.setScaledContents(True)

        self.show_table()
        self.show_previous_match()
        self.show_loader_buttons()

        MainWindow.setCentralWidget(self.scroll)

    def show_table(self):
        table = QtWidgets.QTableWidget(self.central_widget)
        table.setGeometry(15, 60, 883, 834)
        table.setColumnCount(11)
        table.setRowCount(20)
        table.verticalScrollBar().setDisabled(True)
        table.horizontalScrollBar().setDisabled(True)
        table.setFont(QtGui.QFont('Arial', 12))
        table.setIconSize(QtCore.QSize(100, 40))
        table.verticalHeader().setDefaultSectionSize(40)
        table.horizontalHeader().setFont(QtGui.QFont('Arial', 14))
        table.EditTrigger = False

        table.horizontalHeader().setStyleSheet(
            """
            ::section{Background-color:rgb(175, 248, 255);border-radius:30px;}
            """
        )
        table.setStyleSheet(
            """
            QTableWidget{
                border: 2px solid black;
                border-radius: 5px;
                background-color: rgb(255, 255, 255);
                padding-bottom: 0px;
            }
            QTableWidget::nth-child(1){
                background:black;
            }
            QTableWidget::item::focus
            {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #8ae234, stop: 1  #4e9a06);
                border: 0px;
            }
            """
        )

        table.setHorizontalHeaderLabels(
            ['Team', 'Played', 'Won', 'Drawn', 'Lost', 'GF', 'GA', 'GD', 'Points', 'Form', 'Next']
        )

        table.horizontalHeaderItem(6).setToolTip('Goals For')
        table.horizontalHeaderItem(7).setToolTip('Goals Against')
        table.horizontalHeaderItem(8).setToolTip('Goals Difference')

        league_table_data = get_league_table()
        for i in range(len(league_table_data)):
            if i <= 4:
                pass
            elif i >= 18:
                pass
            table.setItem(i, 0, QtWidgets.QTableWidgetItem(league_table_data[i][1]))
            table.setItem(i, 1, QtWidgets.QTableWidgetItem(league_table_data[i][2]))
            table.setItem(i, 2, QtWidgets.QTableWidgetItem(league_table_data[i][3]))
            table.setItem(i, 3, QtWidgets.QTableWidgetItem(league_table_data[i][4]))
            table.setItem(i, 4, QtWidgets.QTableWidgetItem(league_table_data[i][5]))
            table.setItem(i, 5, QtWidgets.QTableWidgetItem(league_table_data[i][6]))
            table.setItem(i, 6, QtWidgets.QTableWidgetItem(league_table_data[i][7]))
            table.setItem(i, 7, QtWidgets.QTableWidgetItem(league_table_data[i][8]))
            table.setItem(i, 8, QtWidgets.QTableWidgetItem(league_table_data[i][9]))
            table.setItem(i, 9, QtWidgets.QTableWidgetItem(league_table_data[i][10]))
            opponent_widget = QtWidgets.QTableWidgetItem()
            response = requests.get(league_table_data[i][11])
            pixmap = QtGui.QPixmap()
            pixmap.loadFromData(response.content)
            icon = QtGui.QIcon(pixmap)
            opponent_widget.setIcon(icon)
            table.setItem(i, 10, opponent_widget)
        table.resizeColumnsToContents()

    def show_previous_match(self):
        previous_match = get_previous_match()
        team1 = QtWidgets.QLabel(self.central_widget)
        team1.setGeometry(QtCore.QRect(140, 907, 96, 96))
        pixmap1 = QtGui.QPixmap()
        logo1 = requests.get(previous_match[1][0])
        pixmap1.loadFromData(logo1.content)
        team1.setPixmap(QtGui.QPixmap(pixmap1))
        team1.setScaledContents(True)

        info = QtWidgets.QLabel(self.central_widget)
        info.setGeometry(QtCore.QRect(290, 917, 400, 100))
        info.setObjectName('previous_match_info')
        info.setStyleSheet('#previous_match_info {font-weight:bold;}')
        info.setFont(QtGui.QFont('Arial', 14))
        info.setAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter)
        info.setText(previous_match[0])

        score = QtWidgets.QLabel(self.central_widget)
        score.setObjectName('previous_match_score')
        score.setGeometry(QtCore.QRect(450, 1015, 80, 35))
        score.setStyleSheet('#previous_match_score {font-weight:bold;background:white}')
        score.setAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter)
        score.setFont(QtGui.QFont('Arial', 22))
        if previous_match[1][1] > previous_match[2][1]:
            score.setText(
                f'<font color="#7FCC7F">{previous_match[1][1]}</font> - <font color="red">{previous_match[2][1]}</font>')
        elif previous_match[1][1] < previous_match[2][1]:
            score.setText(
                f'<font color="red">{previous_match[1][1]}</font> - <font color="#7FCC7F">{previous_match[2][1]}</font>')
        else:
            score.setText(
                f'<font color="gray">{previous_match[1][1]} - {previous_match[2][1]}</font>')

        team2 = QtWidgets.QLabel(self.central_widget)
        team2.setGeometry(QtCore.QRect(724, 907, 96, 96))
        pixmap2 = QtGui.QPixmap()
        logo2 = requests.get(previous_match[2][0])
        pixmap2.loadFromData(logo2.content)
        team2.setPixmap(QtGui.QPixmap(pixmap2))
        team2.setScaledContents(True)

    def show_loader_buttons(self):
        self.load_previous = QtWidgets.QPushButton(self.central_widget)
        self.load_previous.setObjectName('load_previous_matches')
        self.load_previous.setGeometry(QtCore.QRect(190, 1080, 220, 75))
        self.load_previous.setFont(QtGui.QFont('Arial', 12))
        self.load_previous.setText('Load previous matches')
        self.load_previous.setStyleSheet(
            """
            #load_previous_matches{
                background-color: rgb(192, 192, 192);
                color: white;
                border-style: outset;
                border-width: 5px;
                border-radius: 10px;
                border-color:black;
                font-weight:bold;
                padding: 6px;
                min-width:10px;
            }
            """
        )
        self.load_previous.clicked.connect(self.load_previous_matches)

        self.load_upcoming = QtWidgets.QPushButton(self.central_widget)
        self.load_upcoming.setObjectName('load_upcoming_matches')
        self.load_upcoming.setGeometry(QtCore.QRect(570, 1080, 220, 75))
        self.load_upcoming.setFont(QtGui.QFont('Arial', 12))
        self.load_upcoming.setText('Load upcoming matches')
        self.load_upcoming.setStyleSheet(
            """
            #load_upcoming_matches{
                background-color: rgb(0, 204, 102);
                color: white;
                border-style: outset;
                border-width: 5px;
                border-radius: 10px;
                border-color:black;
                font-weight:bold;
                padding: 6px;
                min-width:10px;
            }
            """
        )
        self.load_upcoming.clicked.connect(self.load_upcoming_matches)

    def load_previous_matches(self):
        self.load_previous.setEnabled(False)
        previous_matches = get_previous_matches()
        pos = [1180, 1330, 1480, 1630, 1780]

        for i in range(len(previous_matches)):
            league = QtWidgets.QLabel(self.central_widget)
            league.setGeometry(QtCore.QRect(125, pos[i], 350, 30))
            league.setObjectName('previous_matches_league')
            league.setStyleSheet(
                """
                #previous_matches_league{
                    color:white;
                    font-weight:bold;
                    background-color:#011b51;
                }
                """
            )
            league.setAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter)
            league.setFont(QtGui.QFont('Arial', 14))
            league.setText(previous_matches[i][2])
            league.show()

            date = QtWidgets.QLabel(self.central_widget)
            date.setGeometry(QtCore.QRect(125, pos[i]+30, 350, 30))
            date.setObjectName('previous_matches_date')
            date.setStyleSheet(
                """
                #previous_matches_date{
                    color:black;
                    background-color:#eaeaea;
                }
                """
            )
            date.setAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter)
            date.setFont(QtGui.QFont('Arial', 12))
            date.setText(previous_matches[i][1])
            date.show()

            score = QtWidgets.QLabel(self.central_widget)
            score.setGeometry(QtCore.QRect(125, pos[i]+60, 350, 30))
            score.setObjectName('previous_matches_score')
            score.setStyleSheet(
                """
                #previous_matches_score{
                    font-weight:bold;
                    background-color:white;
                }
                """
            )
            score.setAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter)
            score.setFont(QtGui.QFont('Arial', 10))
            score.setText(previous_matches[i][0])
            score.show()

    def load_upcoming_matches(self):
        self.load_upcoming.setEnabled(False)
        upcoming_matches = get_upcoming_matches()
        pos = [1180, 1330, 1480, 1630, 1780]

        for i in range(len(upcoming_matches)):
            league = QtWidgets.QLabel(self.central_widget)
            league.setGeometry(QtCore.QRect(505, pos[i], 350, 30))
            league.setObjectName('upcoming_matches_league')
            league.setStyleSheet(
                """
                #upcoming_matches_league{
                    color:white;
                    font-weight:bold;
                    background-color:#011b51;
                }
                """
            )
            league.setAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter)
            league.setFont(QtGui.QFont('Arial', 14))
            league.setText(upcoming_matches[i][2])
            league.show()

            date = QtWidgets.QLabel(self.central_widget)
            date.setGeometry(QtCore.QRect(505, pos[i]+30, 350, 30))
            date.setObjectName('upcoming_matches_date')
            date.setStyleSheet(
                """
                #upcoming_matches_date{
                    color:black;
                    background-color:#eaeaea;
                }
                """
            )
            date.setAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter)
            date.setFont(QtGui.QFont('Arial', 12))
            date.setText(upcoming_matches[i][1])
            date.show()

            score = QtWidgets.QLabel(self.central_widget)
            score.setGeometry(QtCore.QRect(505, pos[i]+60, 350, 30))
            score.setObjectName('upcoming_matches_score')
            score.setStyleSheet(
                """
                #upcoming_matches_score{
                    font-weight:bold;
                    background-color:white;
                }
                """
            )
            score.setAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter)
            score.setFont(QtGui.QFont('Arial', 10))
            score.setText(upcoming_matches[i][0])
            score.show()


app = QtWidgets.QApplication(sys.argv)

MainWindow = QtWidgets.QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(MainWindow)
MainWindow.show()

sys.exit(app.exec())
