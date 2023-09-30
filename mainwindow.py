from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import os
os.environ['QT_QPA_PLATFORM'] = 'wayland'

import cv2
import numpy as np
from operation import Operation

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cores, Filtros, Binarização e Morfologia")
        self.setGeometry(100, 100, 350, 500)

        self.selected_image = None
        self.selected_operation = None
        self.operations_toDo = []
        self.colors = ["Cinza", "XYZ", "YCrCb", "HSV", "HLS", "CIE L*a*b*"]
        self.array = [
            cv2.COLOR_BGR2GRAY,
            cv2.COLOR_BGR2XYZ,
            cv2.COLOR_BGR2YCrCb,
            cv2.COLOR_BGR2HSV,
            cv2.COLOR_BGR2HLS,
            cv2.COLOR_BGR2LAB
        ]
        self.default_operations =  [
            Operation("Cor", 0),
            Operation("Gaussian Blur", 5, 0), 
            Operation("Canny", 100, 200),
            Operation("Binarizar", 127, 255),
            Operation("Erosão", 3, 1),
            Operation("Dilatação", 3, 1)
        ]

        #-------------------------------
        
        main_layout = QHBoxLayout()
        self.lateral_widget = QWidget()
        self.lateral_layout = QVBoxLayout()

        self.open_button = QPushButton("Abrir Imagem")
        self.open_button.setFixedSize(100, 25)
        self.open_button.clicked.connect(self.open_image)
        self.lateral_layout.addWidget(self.open_button, alignment=Qt.AlignCenter)

        self.operation_list = QListWidget()
        self.operation_list.itemClicked.connect(self.get_current_operation) 
        self.lateral_layout.addWidget(self.operation_list)
        for operation in self.default_operations:
            self.operation_list.addItem(operation.name)

        #-------------------------------
        
        self.operation_layout = QVBoxLayout()
        self.operation_layout.addWidget(QLabel("Tipo de Cor"))
        self.combobox = QComboBox()
        self.combobox.addItems(self.colors)
        self.combobox.currentIndexChanged.connect(self.selectionchange1)
        self.operation_layout.addWidget(self.combobox)
        self.operation_widget = QWidget()
        self.operation_widget.setLayout(self.operation_layout)
        self.lateral_layout.addWidget(self.operation_widget)
        self.operation_widget.hide()

        #-------------------------------
        self.operation_layout2 = QVBoxLayout()
        
        self.operation_layout2.addWidget(QLabel("Tamanho do Kernel"))
        self.slider_layout2 = QHBoxLayout()
        self.kernel_size = QSlider(Qt.Horizontal)
        self.kernel_size.setMinimum(1)
        self.kernel_size.setMaximum(31)
        self.kernel_size.setValue(5)
        self.kernel_size.setTickPosition(QSlider.TicksBelow)
        self.kernel_size.setTickInterval(2)
        self.kernel_size.valueChanged.connect(self.selectionchange2)
        self.label2 = QLabel("5")
        self.label2.setFont(QFont("Sanserif", 11))
        self.slider_layout2.addWidget(self.kernel_size)
        self.slider_layout2.setSpacing(20)
        self.slider_layout2.addWidget(self.label2)
        self.operation_layout2.addLayout(self.slider_layout2)
        
        self.operation_layout2.addWidget(QLabel("Desvio Padrão"))
        self.slider_layout3 = QHBoxLayout()
        self.desvio_padrao = QSlider(Qt.Horizontal)
        self.desvio_padrao.setMinimum(0)
        self.desvio_padrao.setMaximum(10)
        self.desvio_padrao.setValue(0)
        self.desvio_padrao.setTickPosition(QSlider.TicksBelow)
        self.desvio_padrao.setTickInterval(1)
        self.desvio_padrao.valueChanged.connect(self.selectionchange3)
        self.label3 = QLabel("0")
        self.label3.setFont(QFont("Sanserif", 11))
        self.slider_layout3.addWidget(self.desvio_padrao)
        self.slider_layout3.setSpacing(20)
        self.slider_layout3.addWidget(self.label3)
        self.operation_layout2.addLayout(self.slider_layout3)
        
        self.operation_widget2 = QWidget()
        self.operation_widget2.setLayout(self.operation_layout2)
        self.lateral_layout.addWidget(self.operation_widget2)
        self.operation_widget2.hide()

        #-------------------------------
        
        self.operation_layout3 = QVBoxLayout()
        
        self.operation_layout3.addWidget(QLabel("Limiar Mínimo"))
        self.slider_layout4 = QHBoxLayout()
        self.limiar_minimo = QSlider(Qt.Horizontal)
        self.limiar_minimo.setMinimum(0)
        self.limiar_minimo.setMaximum(255)
        self.limiar_minimo.setValue(100)
        self.limiar_minimo.setTickPosition(QSlider.TicksBelow)
        self.limiar_minimo.setTickInterval(10)
        self.limiar_minimo.valueChanged.connect(self.selectionchange4)
        self.label4 = QLabel("100")
        self.label4.setFont(QFont("Sanserif", 11))
        self.slider_layout4.addWidget(self.limiar_minimo)
        self.slider_layout4.setSpacing(20)
        self.slider_layout4.addWidget(self.label4)
        self.operation_layout3.addLayout(self.slider_layout4)
        
        self.operation_layout3.addWidget(QLabel("Limiar Máximo"))
        self.slider_layout5 = QHBoxLayout()
        self.limiar_maximo = QSlider(Qt.Horizontal)
        self.limiar_maximo.setMinimum(0)
        self.limiar_maximo.setMaximum(255)
        self.limiar_maximo.setValue(200)
        self.limiar_maximo.setTickPosition(QSlider.TicksBelow)
        self.limiar_maximo.setTickInterval(10)
        self.limiar_maximo.valueChanged.connect(self.selectionchange5)
        self.label5 = QLabel("200")
        self.label5.setFont(QFont("Sanserif", 11))
        self.slider_layout5.addWidget(self.limiar_maximo)
        self.slider_layout5.setSpacing(20)
        self.slider_layout5.addWidget(self.label5)
        self.operation_layout3.addLayout(self.slider_layout5)
        
        self.operation_widget3 = QWidget()
        self.operation_widget3.setLayout(self.operation_layout3)
        self.lateral_layout.addWidget(self.operation_widget3)
        self.operation_widget3.hide()

        #-------------------------------
        
        self.operation_layout4 = QVBoxLayout()
        
        self.operation_layout4.addWidget(QLabel("Limiar"))
        self.slider_layout6 = QHBoxLayout()
        self.limiar = QSlider(Qt.Horizontal)
        self.limiar.setMinimum(0)
        self.limiar.setMaximum(255)
        self.limiar.setValue(127)
        self.limiar.setTickPosition(QSlider.TicksBelow)
        self.limiar.setTickInterval(10)
        self.limiar.valueChanged.connect(self.selectionchange6)
        self.label6 = QLabel("127")
        self.label6.setFont(QFont("Sanserif", 11))
        self.slider_layout6.addWidget(self.limiar)
        self.slider_layout6.setSpacing(20)
        self.slider_layout6.addWidget(self.label6)
        self.operation_layout4.addLayout(self.slider_layout6)
        
        self.operation_layout4.addWidget(QLabel("Valor Máximo"))
        self.slider_layout7 = QHBoxLayout()
        self.valor_maximo = QSlider(Qt.Horizontal)
        self.valor_maximo.setMinimum(0)
        self.valor_maximo.setMaximum(255)
        self.valor_maximo.setValue(255)
        self.valor_maximo.setTickPosition(QSlider.TicksBelow)
        self.valor_maximo.setTickInterval(10)
        self.valor_maximo.valueChanged.connect(self.selectionchange7)
        self.label7 = QLabel("255")
        self.label7.setFont(QFont("Sanserif", 11))
        self.slider_layout7.addWidget(self.valor_maximo)
        self.slider_layout7.setSpacing(20)
        self.slider_layout7.addWidget(self.label7)
        self.operation_layout4.addLayout(self.slider_layout7)
        
        self.operation_widget4 = QWidget()
        self.operation_widget4.setLayout(self.operation_layout4)
        self.lateral_layout.addWidget(self.operation_widget4)
        self.operation_widget4.hide()
        
        #-------------------------------
        
        self.operation_layout5 = QVBoxLayout()
        
        self.operation_layout5.addWidget(QLabel("Tamanho do Kernel"))
        self.slider_layout8 = QHBoxLayout()
        self.kernel_size2 = QSlider(Qt.Horizontal)
        self.kernel_size2.setMinimum(1)
        self.kernel_size2.setMaximum(31)
        self.kernel_size2.setValue(3)
        self.kernel_size2.setTickPosition(QSlider.TicksBelow)
        self.kernel_size2.setTickInterval(2)
        self.kernel_size2.valueChanged.connect(self.selectionchange8)
        self.label8 = QLabel("3")
        self.label8.setFont(QFont("Sanserif", 11))
        self.slider_layout8.addWidget(self.kernel_size2)
        self.slider_layout8.setSpacing(20)
        self.slider_layout8.addWidget(self.label8)
        self.operation_layout5.addLayout(self.slider_layout8)

        self.operation_layout5.addWidget(QLabel("Iterações"))
        self.slider_layout9 = QHBoxLayout()
        self.iteracoes = QSlider(Qt.Horizontal)
        self.iteracoes.setMinimum(1)
        self.iteracoes.setMaximum(10)
        self.iteracoes.setValue(1)
        self.iteracoes.setTickPosition(QSlider.TicksBelow)
        self.iteracoes.setTickInterval(1)
        self.iteracoes.valueChanged.connect(self.selectionchange9)
        self.label9 = QLabel("1")
        self.label9.setFont(QFont("Sanserif", 11))
        self.slider_layout9.addWidget(self.iteracoes)
        self.slider_layout9.setSpacing(20)
        self.slider_layout9.addWidget(self.label9)
        self.operation_layout5.addLayout(self.slider_layout9)
        
        self.operation_widget5 = QWidget()
        self.operation_widget5.setLayout(self.operation_layout5)
        self.lateral_layout.addWidget(self.operation_widget5)
        self.operation_widget5.hide()
        
        
        #-------------------------------
        
        self.operation_layout6 = QVBoxLayout()
        
        self.operation_layout6.addWidget(QLabel("Tamanho do Kernel"))
        self.slider_layout10 = QHBoxLayout()
        self.kernel_size3 = QSlider(Qt.Horizontal)
        self.kernel_size3.setMinimum(1)
        self.kernel_size3.setMaximum(31)
        self.kernel_size3.setValue(3)
        self.kernel_size3.setTickPosition(QSlider.TicksBelow)
        self.kernel_size3.setTickInterval(2)
        self.kernel_size3.valueChanged.connect(self.selectionchange10)
        self.label10 = QLabel("3")
        self.label10.setFont(QFont("Sanserif", 11))
        self.slider_layout10.addWidget(self.kernel_size3)
        self.slider_layout10.setSpacing(20)
        self.slider_layout10.addWidget(self.label10)
        self.operation_layout6.addLayout(self.slider_layout10)

        self.operation_layout6.addWidget(QLabel("Iterações"))
        self.slider_layout11 = QHBoxLayout()
        self.iteracoes2 = QSlider(Qt.Horizontal)
        self.iteracoes2.setMinimum(1)
        self.iteracoes2.setMaximum(10)
        self.iteracoes2.setValue(1)
        self.iteracoes2.setTickPosition(QSlider.TicksBelow)
        self.iteracoes2.setTickInterval(1)
        self.iteracoes2.valueChanged.connect(self.selectionchange11)
        self.label11 = QLabel("1")
        self.label11.setFont(QFont("Sanserif", 11))
        self.slider_layout11.addWidget(self.iteracoes2)
        self.slider_layout11.setSpacing(20)
        self.slider_layout11.addWidget(self.label11)
        self.operation_layout6.addLayout(self.slider_layout11)
        
        self.operation_widget6 = QWidget()
        self.operation_widget6.setLayout(self.operation_layout6)
        self.lateral_layout.addWidget(self.operation_widget6)
        self.operation_widget6.hide()
        
        #-------------------------------
        
        self.open_button = QPushButton("Aplicar Operação")
        self.open_button.clicked.connect(self.apply_operation)
        #dimuir o tamanho do botão e alinhar no meio
        self.open_button.setFixedSize(100, 25)
        self.open_button.setDisabled(True)
        self.lateral_layout.addWidget(self.open_button, alignment=Qt.AlignCenter)
        
        self.history_list = QListWidget()
        self.history_list.itemClicked.connect(self.remove_item)
        self.lateral_layout.addWidget(self.history_list)

        self.clear_button = QPushButton("Limpar Histórico")
        self.clear_button.clicked.connect(self.clear_history)
        self.lateral_layout.addWidget(self.clear_button)

        self.lateral_widget.setLayout(self.lateral_layout)
        main_layout.addWidget(self.lateral_widget)

        main_widget = QWidget()
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

    def changeValues(self, values, type):
        index = None
        
        for i in range(len(self.operations_toDo)):
            if self.operations_toDo[i][0] == type:
                index = i
                break
        
        if index is not None:
            self.operations_toDo[index][1] = values
            self.operations()
        
        
    def selectionchange1(self, value):
        self.default_operations[0].args = (value,)	

    def selectionchange2(self, value):
        #nao deixa o tamanho do kernel ser par
        if value % 2 == 0:
            value += 1
            self.kernel_size.setValue(value)
        
        values = (value, self.default_operations[1].args[1])
        self.default_operations[1].args = values
        self.changeValues(values, "Gaussian Blur")
        self.label2.setText(str(value))
            
    def selectionchange3(self, value):
        values = (self.default_operations[1].args[0], value)
        self.default_operations[1].args = values
        self.changeValues(values, "Gaussian Blur")
        self.label3.setText(str(value))
      

    def selectionchange4(self, value):
        values = (value, self.default_operations[2].args[1])
        self.default_operations[2].args = values
        self.changeValues(values, "Canny")
        self.label4.setText(str(value))
   
    def selectionchange5(self, value):
        values = (self.default_operations[2].args[0], value)
        self.default_operations[2].args = values
        self.changeValues(values, "Canny")
        self.label5.setText(str(value))
        
    def selectionchange6(self, value):
        values = (value, self.default_operations[3].args[1])
        self.default_operations[3].args = values
        self.changeValues(values, "Binarizar")
        self.label6.setText(str(value))
             
    def selectionchange7(self, value):
        values = (self.default_operations[3].args[0], value)
        self.default_operations[3].args = values
        self.changeValues(values, "Binarizar")
        self.label7.setText(str(value))
        
    def selectionchange8(self, value):
        values = (value, self.default_operations[4].args[1])
        self.default_operations[4].args = values
        self.changeValues(values, "Erosão")
        self.label8.setText(str(value))
        
    def selectionchange9(self, value):
        values = (self.default_operations[4].args[0], value)
        self.default_operations[4].args = values
        self.changeValues(values, "Erosão")
        self.label9.setText(str(value))
        
    def selectionchange10(self, value):
        values = (value, self.default_operations[5].args[1])
        self.default_operations[5].args = values
        self.changeValues(values, "Dilatação")
        self.label10.setText(str(value))
        
    def selectionchange11(self, value):
        values = (self.default_operations[5].args[0], value)
        self.default_operations[5].args = values
        self.changeValues(values, "Dilatação")
        self.label11.setText(str(value))
        
    def get_current_operation(self, item):
        self.selected_operation = item.text()

        for obj in self.default_operations:
            if obj.name == self.selected_operation:
                self.selected_operation = obj
                break
          
        name = self.selected_operation.name
        
        self.operation_widget.hide()
        self.operation_widget2.hide()
        self.operation_widget3.hide()
        self.operation_widget4.hide()
        self.operation_widget5.hide()
        self.operation_widget6.hide()

        if name == "Cor":
            self.operation_widget.show()
        elif name == "Gaussian Blur":
            self.operation_widget2.show()
        elif name == "Canny":
            self.operation_widget3.show()
        elif name == "Binarizar":
            self.operation_widget4.show()
        elif name == "Erosão":
            self.operation_widget5.show()
        elif name == "Dilatação":
            self.operation_widget6.show()

    def apply_operation(self):
        if self.selected_image is not None:
            args = self.selected_operation.args
            name = self.selected_operation.name
            item_history = None

            if args is not None:
                if name == "Cor":
                    item_history = name + " " + self.colors[args[0]]
                else:
                    item_history = name

            if item_history not in [self.history_list.item(i).text() for i in range(self.history_list.count())]:
                self.operations_toDo.append([name, [*args]])
                self.operations()

    #... (todos os métodos da classe MainWindow)
