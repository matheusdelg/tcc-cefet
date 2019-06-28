# Descrição
Trabalho de Conclusão de Curso em Engenharia Mecatrônica do CEFET-MG Campus Divinópolis. Implementação de uma rede neural artificial para pré-compensação de não-linearidade em sistema mecânico.

## Resumo
O projeto de controladores baseados na alocação de polos da função de transferência do sistema requer que os modelos dinâmicos sejam lineares. Contudo, algumas não-linearidades intrínsecas do sistema podem causar inadequações de critérios de desempenho. O trabalho consiste na implementação de um filtro não-linear baseado em redes neurais artificiais, com o objetivo de mitigar os efeitos não-lineares do sistema.  

## Requisitos
- [Python 3](https://www.python.org/downloads/) 
- Módulos [TensorFlow](https://www.tensorflow.org/install), [Keras](https://keras.io/#installation), [NumPy](https://docs.scipy.org/doc/numpy-1.15.0/user/install.html), [SciPy](https://www.scipy.org/install.html), [SKLearn](https://scikit-learn.org/stable/install.html), [EzODF](https://pypi.org/project/ezodf/), [Control](https://python-control.readthedocs.io/en/0.8.0/intro.html#installation) e [Matplotlib](https://matplotlib.org/3.1.0/users/installing.html) 
- [Matlab](https://www.mathworks.com/downloads/) (r2016b ou superior com pacote Simulink)

## Como funciona
Para um sistema de dinâmica linear modelada por <a href="https://www.codecogs.com/eqnedit.php?latex=G(s)" target="_blank"><img src="https://latex.codecogs.com/gif.latex?G(s)" title="G(s)" /></a> e característica estática não linear <a href="https://www.codecogs.com/eqnedit.php?latex=B(\cdot&space;)" target="_blank"><img src="https://latex.codecogs.com/gif.latex?B(\cdot&space;)" title="B(\cdot )" /></a>, o filtro <a href="https://www.codecogs.com/eqnedit.php?latex=F^{*}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?F^{*}" title="F^{*}" /></a> processa o sinal de controle <a href="https://www.codecogs.com/eqnedit.php?latex=U(s)" target="_blank"><img src="https://latex.codecogs.com/gif.latex?U(s)" title="U(s)" /></a> de forma a gerar um sinal <a href="https://www.codecogs.com/eqnedit.php?latex=W(s)" target="_blank"><img src="https://latex.codecogs.com/gif.latex?W(s)" title="W(s)" /></a> que excita a dinâmica linear do sistema, fazendo com que a mesma responda com <a href="https://www.codecogs.com/eqnedit.php?latex=B^{-1}(Y(s))" target="_blank"><img src="https://latex.codecogs.com/gif.latex?B^{-1}(Y(s))" title="B^{-1}(Y(s))" /></a>,em que <a href="https://www.codecogs.com/eqnedit.php?latex=Y(s)" target="_blank"><img src="https://latex.codecogs.com/gif.latex?Y(s)" title="Y(s)" /></a> é a saída linear esperada, como mostra a Figura abaixo:


