import pygame as pg
from pygame.locals import *


class SimpleButton:
    STATE_IDLE = 'idle'
    STATE_ARMED = 'armed'
    STATE_DISARMED = 'dismarmed'

    def __init__(self, window, loc, up, down):
        self.window=window
        self.loc=loc
        self.surfaceup=pg.image.load(up)
        self.surfacedown = pg.image.load(down)

        self.rect = self.surfaceup.get_rect()
        self.rect[0] = loc[0]
        self.rect[1] = loc[1]

        self.state = SimpleButton.STATE_IDLE

    def handleEvent(self, eventObj):
        # jeśli wykryta akcja to nie ruch myszy, puszczenie przycisku ani wcisniecie zwroc False
        if eventObj.type not in (MOUSEMOTION, MOUSEBUTTONUP, MOUSEBUTTONDOWN):
            return False
        # ustal miejsce zdarzenia na kolizję przycisku i myszy
        eventPointInButtonRect = self.rect.collidepoint(eventObj.pos)
        # jeśli stan jest rowny stałej IDLE to zmień stan na wciśnięty ARMED
        if self.state == SimpleButton.STATE_IDLE:
            # jeśli znajduje się w polu przycisku i wcisniety jest klawisz
            if eventObj.type == MOUSEBUTTONDOWN and eventPointInButtonRect:
                self.state = SimpleButton.STATE_ARMED
        # jeśli przycisk jest wciśniety
        elif self.state == SimpleButton.STATE_ARMED:
            # jeśli akcja to puszczenie myszy i pozycja na przycisku to zmień stan na niewciśnięty
            if eventObj.type == MOUSEBUTTONUP and eventPointInButtonRect:
                self.state = SimpleButton.STATE_IDLE
                return True
            # jeśli wykryto ruch myszy i wskaznik nie jest nad przyciskiem
            if eventObj.type==MOUSEMOTION and not eventPointInButtonRect:
                self.state = SimpleButton.STATE_DISARMED
        # jeśli przycisk nie jest wcisniety
        elif self.state == SimpleButton.STATE_DISARMED:
            # ale jest nad przyciskiem to ustal na wcisniety
            if eventPointInButtonRect:
                self.state = SimpleButton.STATE_ARMED
            # jesli natomiast puscimy to ustal stan na niewcisniety
            elif eventObj.type == MOUSEBUTTONUP:
                self.state = SimpleButton.STATE_IDLE
        return False

    def draw(self):
        if self.state == SimpleButton.STATE_ARMED:
            self.window.blit(self.surfacedown, self.loc)
        else:
            self.window.blit(self.surfaceup, self.loc)
