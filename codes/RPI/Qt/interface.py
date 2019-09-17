#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 10 17:31:54 2019

@author: matheus
"""

from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtCore import QTimer
import sys
from LayoutResources import Ui_mainWindow
import numpy as np
from utils import Network, Input, Output, BacklashRegulator, Plant
import time


class MainApp (QWidget):
    ''' Classe principal. A princípio, monolítica. '''
 
    def __init__ (self):
        ''' Construtor não modularizado '''
        # Construtor da classe pai:
        super().__init__()
        self.ui = Ui_mainWindow()
        self.ui.setupUi(self)
        self.show()
        # Construtor de parâmetros:
        self.setupParams()
        # Construtor dos componentes de controle:
        self.setupControl()
        #  Construtor de parâmetros:
        self.setupCallbacks()
        # Construtor dos componentes do PyQt:
        self.setupWidgets()        
    
    def setupWidgets (self):
        ''' Incializa Widgets do PyQt: '''
        # Atualiza a referencia quando mudado o dial:
        def updateRef ():
            self.rk = 6.283 * self.ui.dial.value() / 100.0;
            self.ui.labelReferencia.setText ("{:.6f}".format(self.rk))
        # Atualiza valor do backlash estimado:
        def updateAlpha (upDown):
            if upDown > 0 and self.alpha < self.BACKLASH_MAX:
                self.alpha += self.BACKLASH_STEP # 0.1 mm/click
                self.ui.labelBacklashEstimado.setText("{:.6f}".format(self.alpha))
                #self.regulator.apply (upDown)
            elif upDown < 0 and self.alpha >= self.BACKLASH_STEP:
                self.alpha -= self.BACKLASH_STEP # -0.1 mm/click
                self.ui.labelBacklashEstimado.setText("{:.6f}".format(self.alpha))
                #self.regulator.apply (upDown)
            print (self.alpha)
            self.network.alpha = self.alpha
            self.plant.alpha = self.alpha
            
        def updateFeedback ():
            # Alterna estado T/F:
            self.feedbackLock = not self.feedbackLock
            # Se desligar a rede, reiniciar controladores:
            if not self.feedbackLock:
                self.ek1 = 0.; self.uk1 = 0.
                self.feedbackTime = time.time()
                self.plant = Plant (self.alpha)
            # Mostra estado
            print (self.feedbackLock)
                
        # Conecta slots:
        self.ui.btnBacklashUp.clicked.connect (lambda : updateAlpha (1))
        self.ui.btnBacklashDown.clicked.connect (lambda : updateAlpha (-1))
        self.ui.dial.valueChanged.connect (updateRef)
        self.ui.checkBoxMalha.stateChanged.connect (updateFeedback)
        
            
    def setupParams (self):
        ''' Inicializa parâmetros do programa: '''
        self.feedbackLock = False
        self.simulTime = 0.5
        self.initialTime = time.time()
        self.Ts = 0.0125
        self.rk = 0.
        self.yk = 0.
        self.alpha = 0.
        self.cek = 57.; self.cek1 = -38.98; self.cuk1 = 0.3679
        self.ek1 = 0.; self.uk1 = 0.
        self.BACKLASH_MAX = 0.1
        self.BACKLASH_STEP = 5.3267e-4
        self.rPlot = []
        self.yPlot = []
        
        
    def setupControl(self):
        ''' Inicializa blocos de controle: '''
        self.network = Network(self.alpha)
        self.plant = Plant (self.alpha)
        #self.input = Input (9, 10)
        #self.output = Output (11, 12)
        #self.regulator = BacklashRegulator (13, 14)
        
    def setupCallbacks(self):
        ''' Inicializa processo de callbacks: '''
        # Usa QTimer para rodar processo:
        self.timer = QTimer(self)
        # Conecta slots:
        self.timer.timeout.connect (self.feedbackSystem)
        #self.timer.timeout.connect (self.backlashRegulator)
        self.timer.timeout.connect (self.updateGraphics)
        
        self.timer.start (int(self.Ts * 1000))
    
    def feedbackSystem (self):
        ''' Executa tarefa de controle: '''
        if self.feedbackLock:
            # Atualiza backlash:
            self.network.alpha = self.alpha
            # Calcula uk:
            self.yk = self.plant.yk #self.input.value
            ek = (self.rk - self.yk)
            uk  = (self.cek * ek) + (self.cek1 * self.ek1) 
            uk += (self.cuk1 * self.uk1)
            # Aplica na RNA:
            xk = np.reshape ([uk, self.uk1], (1, 2))
            if self.ui.actionRede_neural.isChecked():
                wk = self.network.apply(xk)
            else:
                wk = self.network.bypass(xk)
            # Aplica na planta:
            #self.output.apply (wk)
            self.plant.apply(wk)
            #print (self.yk)
            # Atualiza sinais:
            self.uk1 = uk
            self.ek1 = ek
        
    def updateGraphics (self):
        self.rPlot.append (self.rk)
        self.yPlot.append (self.yk)
        
        if (len (self.yPlot) >= self.simulTime / self.Ts):
            
            t = np.linspace (0, self.simulTime, len (self.yPlot))
           
            self.ui.MplWidget.canvas.axes.clear()
            self.ui.MplWidget.canvas.axes.grid(True)
            
            self.ui.MplWidget.canvas.axes.step(t, self.rPlot)
            self.ui.MplWidget.canvas.axes.step(t, self.yPlot)
            
            self.ui.MplWidget.canvas.axes.legend(('referência', 'planta'))
        
            self.ui.MplWidget.canvas.draw()
            
            self.rPlot = []
            self.yPlot = []
            
        ''' Demorado 
        # Insere a referência atual para printar:
        self.rPlot.append(self.rk)
        self.yPlot.append(self.yk)
        # Cria um intervalo de tempo de 0 até o tempo atual:
        currTime = time.time() - self.initialTime
        t = np.linspace (0, currTime, len (self.rPlot))
        # Se o tempo de simulação não for excedido, plotar:
        if currTime < self.simulTime:
            # Seta propriedades do plot:
            self.ui.MplWidget.canvas.axes.clear()
            self.ui.MplWidget.canvas.axes.grid(True)
            
            # Plota resultados:
            self.ui.MplWidget.canvas.axes.step(t, self.rPlot)
            self.ui.MplWidget.canvas.axes.step(t, self.yPlot)
            
            self.ui.MplWidget.canvas.axes.legend(('referência', 'planta'))
        
            self.ui.MplWidget.canvas.draw()
        else:
            self.rPlot = []
            self.yPlot = []
            self.initialTime = time.time()
        '''

app = QApplication(sys.argv)
w = MainApp()
w.show()
sys.exit(app.exec_())
