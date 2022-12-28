from rectangle import *
import sys

WHITE = (255,255,255)
WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480
FRAMES = 30
N_RECT = 10
FIRST_RECTANGLE = 'pierwszy'
SECOND_RECTANGLE = 'drugi'

pygame.init()
window= pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), 0, 32)
clock = pygame.time.Clock()

rec_list=[]
for i in range(N_RECT):
    oRectangle = Rectangle(window)
    rec_list.append(oRectangle)
whichRectangle = FIRST_RECTANGLE

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == MOUSEBUTTONDOWN:
            # przeleć po obiektach kwadratow
            for oRectangle in rec_list:
                # jesli kliknieto w kwadrat
                if oRectangle.clickedInside(event.pos):
                    print('Kliknięto: ', whichRectangle, ' prostokąt.')
                    # jesli aktuany kwadrat to pierwszy ustaw jego pozycje i przygotuj sie do drugiego
                    if whichRectangle == FIRST_RECTANGLE:
                        oFirstRectangle = oRectangle
                        whichRectangle = SECOND_RECTANGLE
                    # jesli przygotowano drugi ustaw jego pozycje i kontynuuj program
                    elif whichRectangle == SECOND_RECTANGLE:
                        oSecondRectangle = oRectangle
                        # jesli pierwszy i drugi kwadrat sa takie same
                        if oFirstRectangle == oSecondRectangle:
                            print('Prostokąty mają taką samą wielkość')
                            rec_list.remove(oFirstRectangle)
                            rec_list.remove(oSecondRectangle)
                        elif oFirstRectangle < oSecondRectangle:
                            print('Pierwszy prostokąt jest mniejszy od drugiego')
                        else:
                            print('Pierwszy prostokąt jest większy od drugiego')
                        whichRectangle = FIRST_RECTANGLE
                        print("#"*70)
    window.fill(WHITE)
    for oRectangle in rec_list:
        oRectangle.draw()
    pygame.display.update()
    clock.tick(FRAMES)

