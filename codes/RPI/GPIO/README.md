## Módulo de GPIO no RPi
O Microcomputador Raspberry Pi é usado como sistema digital de controle da planta, além de gerenciar diferentes funcionalidades. Esta página descreve os principais passos tomados para a instalação dos módulos de comunicação de _General Purpose Input/Output_ (GPIO) do Raspberry.

### Requisitos
- Raspberry Pi 3 Model B 
- [Raspbian](https://www.raspberrypi.org/downloads/raspbian/)
- [Python 3] (https://www.python.org/downloads/)
- [GPIOZero](https://gpiozero.readthedocs.io/en/stable/)

### Instalando
Será usada a versão 3 do Python. No terminal, execute o script:
```bash
sudo apt update
sudo apt install python3-gpiozero
```

### Usando a GPIOZero
Para entender o uso dos pinos de GPIO, é preciso conhecer o _pinout_ do RPi, como mostrado na Figura abaixo:
![RPi3MB/B+ pinout](https://www.jameco.com/Jameco/workshop/circuitnotes/raspberry_pi_circuit_note_fig2a.jpg)
A página de documentação da biblioteca [GPIOZero](https://gpiozero.readthedocs.io/en/stable/index.html) oferece diversos exemplos de uso. Em um exemplo, será ligado um LED conectado entre o 6º pino (GND) e o 11º pino (GPIO17) do Raspberry. O código então será:
```python
from gpiozero import LED
from time import sleep

led = LED(17) # Também funciona com led = LED("BOARD11")
delay_time = 1 # 1 segundo de delay

while True:
    led.on ()
    sleep (delay_time)
    led.off ()
    sleep (delay_time)
```

Para drenar uma corrente de <a href="https://www.codecogs.com/eqnedit.php?latex=i&space;=&space;10mA" target="_blank"><img src="https://latex.codecogs.com/gif.latex?i&space;=&space;10mA" title="i = 10mA" /></a>, pela Lei de Ohm, com <a href="https://www.codecogs.com/eqnedit.php?latex=V&space;=&space;3.3V" target="_blank"><img src="https://latex.codecogs.com/gif.latex?V&space;=&space;3.3V" title="V = 3.3V" /></a> e <a href="https://www.codecogs.com/eqnedit.php?latex=V&space;=&space;Ri" target="_blank"><img src="https://latex.codecogs.com/gif.latex?V&space;=&space;Ri" title="V = Ri" /></a>, <a href="https://www.codecogs.com/eqnedit.php?latex=R&space;=&space;330\Omega" target="_blank"><img src="https://latex.codecogs.com/gif.latex?R&space;=&space;330\Omega" title="R = 330\Omega" /></a>. É importante ressaltar que o computador tem faixa de operação de <a href="https://www.codecogs.com/eqnedit.php?latex=0V-3.3V" target="_blank"><img src="https://latex.codecogs.com/gif.latex?0V-3.3V" title="0V-3.3V" /></a>, não devendo ser excedida. As características elétricas dos pinos de GPIO são mostradas na Tabela a seguir, e devem ser seguidas com atenção:


| Características da GPIO |     | Valor | Unidade |
|-------------------------|:---:|------:|--------:|
|Output low voltage       | VOL | < 0.4 |    V    |
|Output high voltage      | VOH | > 2.9 |    V    |
|Input low voltage        | VIL | < 0.54|    V    |
|Input high voltage       | VIH | > 2.31|    V    |
|Histerese                |     |0.66 ~ 2.08| V |
|Resistência Pull Up/Down |  | 100| KΩ|
|Corrente Pull Up/Down| | <50 |  μA|

### Referências
- [GPIO Electrical Specifications](http://www.mosaic-industries.com/embedded-systems/microcontroller-projects/raspberry-pi/gpio-pin-electrical-specifications#rpi-gpio-input-voltage-and-output-current-limitations)
- [Raspberry Pi Pinout Diagram](https://www.jameco.com/Jameco/workshop/circuitnotes/raspberry-pi-circuit-note.html)
