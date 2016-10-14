import sys, time
import random
from PyQt4 import QtCore, QtGui, uic

game_status = "paused"
fin_button = False
snake = []
direc = 4
class Servidor(QtGui.QMainWindow):

    def __init__(self):
        super(Servidor, self).__init__()
        uic.loadUi('servidor.ui', self)        
        self.doubleSpinBox.valueChanged.connect(self.resizeTableColumns) #double spin box for resizing columns
        self.doubleSpinBox_2.valueChanged.connect(self.resizeTableRows) #double spin box for resizing rows
        self.pushButton_2.clicked.connect(self.startGame) #button to start, pause and resume game
        self.tableWidget.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.doubleSpinBox_3.valueChanged.connect(self.waitingTime)
        self.tableWidget.horizontalHeader().setResizeMode(QtGui.QHeaderView.Stretch)
        self.tableWidget.verticalHeader().setResizeMode(QtGui.QHeaderView.Stretch)
        self.show()


    def startGame(self):
        global game_status
        global fin_button

        if fin_button == False:
            self.pushButton_3 = QtGui.QPushButton(self.centralwidget)
            self.pushButton_3.setObjectName("pushButton_3")
            self.pushButton_3.setText("¿Terminar el juego?")
            self.gridLayout.addWidget(self.pushButton_3, 0, 1, 1, 1)
            self.pushButton_3.clicked.connect(self.endGame) #button to end game
            self.createSnake()
            fin_button = True
        if game_status == "paused":
            self.pushButton_2.setText("Pausar el juego")
            game_status = "playing"
            
            self.waitingTime()
        else:
            self.pushButton_2.setText("Reanudar juego")
            game_status = "paused"

    def endGame(self):
      global snake
      global game_status
      global fin_button

      game_status = "paused"
      fin_button = False
      self.pushButton_2.setText("¡Juega otra vez, bro!")
      snake = []
      self.doubleSpinBox.setValue(0.0)
      self.doubleSpinBox_2.setValue(0.0)
      self.doubleSpinBox_3.setValue(0.0)

    def createSnake(self):
        for x in range(0, 15):
         snake.append([0,x])
        self.colorSnake(snake)
        

    def colorSnake(self, snake):

      for body in snake:
         self.tableWidget.setItem(body[0],body[1], QtGui.QTableWidgetItem())
         self.tableWidget.item(body[0],body[1]).setBackground(QtGui.QColor(random.randint(0,255), random.randint(0, 255),random.randint(0,255)))
         
    def moveSnake(self,snake,direc):
      self.tableWidget.item(snake[0][0],snake[0][1]).setBackground(QtGui.QColor(255,252,252))
      limit_col = int(self.doubleSpinBox.value())-1
      limit_row = int(self.doubleSpinBox_2.value())-1
      head = snake[-1]
      snake.pop(0)
      
      #Up
      if direc == 1:
        if head != [0, snake[-1][1]]: 
          snake.append([snake[-1][0]-1,snake[-1][1]])
        else:
          snake.append([limit_row,snake[-1][1]])
      #Left
      if direc == 2:
        if head != [snake[-1][0],0]:
          snake.append([snake[-1][0],snake[-1][1]-1])
        else:
          snake.append([snake[-1][0], limit_row])
      #Down
      if direc == 3:
        if head != [limit_row, snake[-1][1]]:
          snake.append([snake[-1][0]+1,snake[-1][1]])
        else:
          snake.append([0,snake[-1][1]])
      #Right
      if direc == 4: 
        if head != [snake[-1][0],limit_col]:
         snake.append([snake[-1][0], snake[-1][1]+1])
        else:    
          snake.append([snake[-1][0], 0])

      for x in range(0,len(snake)-1):        
        self.colorSnake(snake)

      for body in snake:
        if snake.count(body)>1:
          self.endGame()
                 
    def waitingTime(self):
        global direc
        t = self.doubleSpinBox_3.value()
        while game_status == "playing":
         time.sleep(t)
         self.moveSnake(snake,direc)
         QtCore.QCoreApplication.processEvents()

    def keyPressEvent(self, event):
      global direc

      key = event.key()
      if key == QtCore.Qt.Key_Up and direc != 3:
        direc = 1
      if key == QtCore.Qt.Key_Left and direc != 4:
        direc = 2
      if key == QtCore.Qt.Key_Down and direc != 1:
        direc = 3 
      if key == QtCore.Qt.Key_Right and direc != 2:
        direc = 4

    def resizeTableRows(self):
        rows = int(self.tableWidget.rowCount())
        val = int(self.doubleSpinBox_2.value())
        if rows >= val:
          while rows >= val:
           self.tableWidget.removeRow(rows)
           rows -= 1
        elif rows < val:
          while rows < val:
           self.tableWidget.insertRow(rows)
           rows += 1

    def resizeTableColumns(self, columns):
        columns = int(self.tableWidget.columnCount())
        val = int(self.doubleSpinBox.value())
        if columns >= val:
          while columns >= val:
           self.tableWidget.removeColumn(columns)
           columns -= 1
        elif columns < val:
          while columns < val:
           self.tableWidget.insertColumn(columns)
           columns += 1

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    serv = Servidor()
    sys.exit(app.exec_())
