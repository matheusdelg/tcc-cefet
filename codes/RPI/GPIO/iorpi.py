#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep  7 15:31:40 2019
Discretização do controlador e funções úteis ao RPi:

@author: matheus
"""
from gpiozero import DigitalInputDevice, PWMOutputDevice, DigitalOutputDevice
from numpy import reshape, dot
from time import sleep

class Input:
    ''' Classe Encoder: Recebe informações dos pinos da GPIO e calcula
    o deslocamento. Armazena em Encoder.output. '''
    
    def __init__(self, pinA, pinB, rate = 1):
        ''' Construtor da classe. Entradas: pinA, pinB - canais do encoder
                                            rate [= 1] - 1 / (N * PPR).'''        
        # Entradas da GPIO:
        self.encA = DigitalInputDevice (pinA, pull_up = True)
        self.encB = DigitalInputDevice (pinB, pull_up = True)
        # Dados do encoder:
        self.value = 0
        self.rate = rate
        # Estados dos pinos:
        self.AState = False
        self.BState = False
        # Callbacks:
        self.encA.when_actived = self.changeA
        self.encB.when_actived = self.changeB
        self.encA.when_deactived = self.changeA
        self.encB.when_deactived = self.changeB
        
    def changeA (self):
        ''' Chamado quando pinA altera de estado. Altera o estado de A
            e compara com o de B para descobrir sentido de rotação. '''
        # Altera estado:
        self.AState = not self.AState
        # Se A é diferente de B, A mudou antes de B
        if (self.AState != self.BState):
            self.value += self.rate
        # Se A é igual a B, B mudou antes de A
        else:
            self.output -= self.rate
            
    def changeB (self):
        ''' Chamado quando pinB altera de estado. Altera o estado de B.'''
        self.lastB = self.BState


class Output:
    ''' Classe PWM + ZOH: Recebe informações do controlador e calcula
    o PWM para a GPIO. Armazena em Output.out.pulse. '''
    def __init__ (self, leftPin, rightPin):
        ''' Construtor da classe: cria um objeto de saída de PWM no
        pino desejado.'''
        self.rLeft  = PWMOutputDevice (leftPin)
        self.rRight = PWMOutputDevice (rightPin)
        
    def apply (self, value):
        ''' Para t_{on} = Ts = 5ms, calcula t_{off} para PWM, a 
        partir do duty cycle 'value': '''
        if abs (value) >= 1:
            return
        # Calcula valor do PWM:
        t_on = 0.005
        t_off = t_on * value / (1. - abs (value))
        # Define sentido de rotação:
        if value > 0:
            self.rLeft.pulse (fade_in_time = t_on, fade_out_time = t_off)
            self.rRight.off()
        else:
            self.rLeft.off()
            self.rRight.pulse (fade_in_time = t_on, fade_out_time = t_off)         


class BacklashRegulator:
    ''' Classe para regulação do backlash. Motor CC com Ponte-H. '''
    def __init__ (self, leftPin, rightPin, simul = False):
        ''' Construtor da classe. Atribui pinos na GPIO. '''
        if simul:
            self.pLeft  = PWMOutputDevice(leftPin)
            self.pRight = PWMOutputDevice(rightPin)
            self.tFeed = 0.5 # Avanço do motor
            self.t_on = 0.05
            self.power = 0.5 # Potencia do motor
    
    def apply (self, value):
        ''' Aplica um pulso ao motor CC para giro da barra. '''
        # Define sentido de rotação:
        if value > 0:
            self.pLeft.pulse (fade_in_time = self.t_on * self.power,
                        fade_out_time = self.t_on * (1. - self.power))
            sleep (self.tFeed)
            self.pRight.off()
        else:
            self.pRight.pulse (fade_in_time = self.t_on * self.power,
                        fade_out_time = self.t_on * (1. - self.power))
            sleep (self.tFeed)
            self.pLeft.off()
