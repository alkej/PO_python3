import pygame
import GUI.pygame_textinput as pygame_textinput
from GUI.add_new_organizm import *

from Swiat import *

import random

pygame.init()
# Create TextInput-object
textinput = pygame_textinput.TextInput()


clock = pygame.time.Clock()


class Game:
    def __init__(self, window_size):
        self.window_size = window_size
        self.screen = pygame.display.set_mode(window_size)

        self.width = window_size[0]
        self.height = window_size[1]

        self.color = [pygame.Color('white'), pygame.Color('black'),
                      pygame.Color('red'), pygame.Color('blue'), pygame.Color('grey')]

        self.game_started = False
        self.to_add = False
        self.to_add_x = 0
        self.to_add_y = 0

        self.world_width = 0
        self.world_height = 0

        self.border_size = 120
        self.cell_size = 30
        self.y_draw_delta = 5

        self.width_x = 0
        self.height_y = 0

        # buttons
        self.but_x = 10
        self.but_y = 10
        self.but_w = 100
        self.but_h = 35

        self.next_tour_button = pygame.Rect(self.but_x, self.but_y, self.but_w, self.but_h)
        self.save_game_button = pygame.Rect(self.but_x, self.but_y + self.but_h + 5, self.but_w, self.but_h)
        self.komentator_button = pygame.Rect(self.but_x, self.but_y + (self.but_h + 5)*2, self.but_w, self.but_h)
        self.start_new_game_button = pygame.Rect(self.but_x, self.but_y + (self.but_h + 5)*3, self.but_w, self.but_h)

        self.buttons = []
        self.buttons.append(self.next_tour_button)
        self.buttons.append(self.save_game_button)
        self.buttons.append(self.komentator_button)
        self.buttons.append(self.start_new_game_button)

        # text for buttons

        self.ft_font = pygame.font.Font('Blogger_Sans.otf', 18)

        self.next_tour_surf = self.ft_font.render("Next tour", 1, self.color[1])
        self.save_game_surf = self.ft_font.render("Save game", 1, self.color[1])
        self.komentator_surf = self.ft_font.render("Commentator", 1, self.color[1])
        self.start_new_game_surf = self.ft_font.render("New Game", 1, self.color[1])

        self.buttons_text = []
        self.buttons_text.append(self.next_tour_surf)
        self.buttons_text.append(self.save_game_surf)
        self.buttons_text.append(self.komentator_surf)
        self.buttons_text.append(self.start_new_game_surf)

        self.lista_organizow = self.get_list_of_organisms()

        self.swiat = None

        self.go()

    def transform_size(self, data):
        try:
            self.world_width = int(data.split(" ")[0])
            self.world_height = int(data.split(" ")[1])

            if self.world_width > 0 and self.world_height > 0:
                self.swiat = Swiat(self.world_width, self.world_height)
                self.game_started = True
                self.screen = pygame.display.set_mode([self.world_width * 50, self.world_height * 45])

                self.width_x = self.world_width * self.cell_size + self.border_size
                self.height_y = self.world_height * self.cell_size

        except ValueError:
            print("It is not an integer")

    def draw_grid(self):
        for i in range(self.y_draw_delta, self.height_y + self.y_draw_delta + 1, self.cell_size):
            pygame.draw.line(self.screen, self.color[2], (self.border_size, i), (self.width_x, i))

        for i in range(self.border_size, self.width_x + self.y_draw_delta + 1, self.cell_size):
            pygame.draw.line(self.screen, self.color[2], (i, self.y_draw_delta), (i, self.height_y + self.y_draw_delta))

    def draw_animals(self):
        for i in range(0, self.swiat.height):
            for k in range(0, self.swiat.width):
                if self.swiat.moje_organizmy[i][k] is not None:
                    pygame.draw.rect(self.screen, self.swiat.moje_organizmy[i][k].color,
                                     pygame.Rect(self.border_size + k * self.cell_size,
                                                 self.y_draw_delta + 1 + i * self.cell_size,
                                                 self.cell_size, self.cell_size))

    def get_list_of_organisms(self):
        buttons = [[] for i in range(0, OrganizmyList.size())]

        for i in range(0, OrganizmyList.size()):
            buttons[i].append(pygame.Rect(self.but_x, self.but_y + (self.but_h + 5)*i, self.but_w, self.but_h))

        for i in range(0, OrganizmyList.size()):
            temp = []
            temp.append(self.ft_font.render(str(OrganizmyList(i+1).name), 1, self.color[1]))
            temp.append(OrganizmyList(i+1))
            buttons[i].append(temp)

        return buttons

    def go(self):
        while True:
            self.screen.fill((225, 225, 225))

            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.game_started:
                        if not self.to_add:
                            poz_x = (pygame.mouse.get_pos()[0] - self.border_size) // self.cell_size
                            poz_y = pygame.mouse.get_pos()[1] // self.cell_size

                            if 0 < poz_x < self.swiat.width and 0 < poz_y < self.swiat.height:

                                if self.swiat.moje_organizmy[poz_y][poz_x] is None:
                                    self.to_add = True
                                    self.to_add_x = poz_x
                                    self.to_add_y = poz_y

                            if self.next_tour_button.collidepoint(pygame.mouse.get_pos()):
                                self.swiat.wykonaj_ture()
                        else:
                            for i in range(0, len(self.lista_organizow)):
                                if self.lista_organizow[i][0].collidepoint(pygame.mouse.get_pos()):
                                    if 0 < self.to_add_x < self.swiat.width and 0 < self.to_add_y < self.swiat.height:
                                        self.swiat.moje_organizmy[self.to_add_y][self.to_add_x] = \
                                            OrganizmyList.create_new_organizm(
                                                self.lista_organizow[i][1][1],
                                                self.swiat, self.to_add_x, self.to_add_y)
                                        self.swiat.update_queue()
                                    self.to_add_x = 0
                                    self.to_add_y = 0

                                    self.to_add = False

                elif event.type == pygame.KEYDOWN:
                    if self.game_started:
                        #           3    4      2     1
                        # direction (UP, DOWN , LEFT, RIGHT)
                        if event.key == pygame.K_UP:
                            self.to_add = False
                            self.swiat.set_czlowiek_direction_global(3)
                        elif event.key == pygame.K_DOWN:
                            self.swiat.set_czlowiek_direction_global(4)
                        elif event.key == pygame.K_LEFT:
                            self.swiat.set_czlowiek_direction_global(2)
                        elif event.key == pygame.K_RIGHT:
                            self.swiat.set_czlowiek_direction_global(1)
                    if self.to_add:
                        if event.key == pygame.K_ESCAPE:
                            self.to_add = False

            # Feed textinput with events every frame
            if textinput.update(events):
                self.transform_size(textinput.get_text())

            if not self.game_started:
                self.screen.blit(textinput.get_surface(), (10, 10))
            elif self.to_add:
                    buttons = self.lista_organizow
                    for i in range(0, len(buttons)):
                        pygame.draw.rect(self.screen, self.color[4], buttons[i][0], 0)
                        self.screen.blit(buttons[i][1][0], (buttons[i][0].x, buttons[i][0].y))

            else:
                for button in self.buttons:
                    pygame.draw.rect(self.screen, self.color[4], button, 0)

                for i in range(0, len(self.buttons_text)):
                    self.screen.blit(self.buttons_text[i], (10, i * (self.but_h + 5) + self.but_y))

                self.draw_grid()
                self.draw_animals()

            pygame.display.update()
            clock.tick(30)


GUI = Game([150, 100])
