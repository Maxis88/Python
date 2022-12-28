
from simplebutton import *
from SimpleText import *
from rectangle import *

window = pg.display.set_mode((800,600))
clock = pg.time.Clock()        
oButton = SimpleButton(window, (150, 30), 'images/buttonUp.png', 'images/buttonDown.png')
oButton1 = SimpleButton(window, (300, 30), 'images/buttonUp.png', 'images/buttonDown.png')
oButton2 = SimpleButton(window, (450, 30), 'images/buttonUp.png', 'images/buttonDown.png')
oSimpleText = SimpleText(window, (150, 100), 'Jakis tekst', (255,0,0))

while True:
    for event in pg.event.get():
        if event.type==QUIT:
            pg.quit()
        
        if oButton.handleEvent(event):
            print('Przycisk wciśnięty')
        if oButton1.handleEvent(event):
            print('Przycisk 2 wciśnięty')
        if oButton2.handleEvent(event):
            print('Przycisk 3 wciśnięty')
        
        window.fill((0,200,0))
        oSimpleText.draw()
        oButton.draw()
        oButton1.draw()
        oButton2.draw()
        pg.display.update()
        clock.tick(30)