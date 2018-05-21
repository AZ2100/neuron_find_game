import pygame
import util
import os
import sys
import time

DISPLAY_SIZE = (1024, 512)
#H_WINDOW_SIZE = (256, 256)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 102, 102)
#LRED = (255, 129, 129)
DRED = (255, 0, 0)
GREEN = (102, 255, 102)
BLUE = (102, 102, 255)
LBLUE = (117, 192, 242)
LLBLUE = (48, 169, 249)
GRAY = (224, 224, 224)
#DGRAY = (81, 81, 81)
#AQUA = (57, 204, 226)
YELLOW = (236, 231, 77)
#ORANGE = (240, 160, 70)

class game():

    def __init__(self, data_path="../game_data"):
        self.clock = None
        self._display_surf = None
        ### Do the pygame init stuff
        self.init()

        ### Load Data
        self.data = util.load_data(data_path)

        ### MAKE BUTTONS
        self.font = pygame.font.Font('freesansbold.ttf', 100)
        self.small_font = pygame.font.Font('freesansbold.ttf', 30)
        self.very_small_font = pygame.font.Font('freesansbold.ttf', 10)
        x = DISPLAY_SIZE[0] / 2

        self.undo = button(x, 0, DISPLAY_SIZE[0] / 2, DISPLAY_SIZE[1] / 4, "Undo", self.font, RED, BLACK)
        self.skip = button(x, DISPLAY_SIZE[1] / 4 - 1.9, DISPLAY_SIZE[0] / 2, DISPLAY_SIZE[1] / 3.9, "Skip",
                           self.font, LLBLUE, BLACK)
        self.done = button(x, DISPLAY_SIZE[1] / 2, DISPLAY_SIZE[0] / 2, DISPLAY_SIZE[1] / 2, "Done",
                           self.font, GREEN, BLACK)
        #self.help = button(DISPLAY_SIZE[0]-40, DISPLAY_SIZE[1]-40, 40, 40, "?", self.small_font, WHITE, BLACK)
        self.boarder = pygame.Surface((DISPLAY_SIZE[0] / 2, DISPLAY_SIZE[1])).convert()
        self.boarder.fill(WHITE)

        self.next_image = button(x - 50, DISPLAY_SIZE[1] - 40, 100, 50, "Next", self.small_font, LBLUE, BLACK)
        self.filtered = button(x - 50, -5, 100, 50, "Filter", self.small_font, LBLUE, BLACK)
        self.metrics = button(0, 0, 200, 20, "", self.very_small_font, None, WHITE)
        self.fix = button(-5, DISPLAY_SIZE[1] - 40, 70, 50, "Fix", self.small_font, YELLOW, None)

        self.gameLoop()

    def init(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self._display_surf = pygame.display.set_mode(DISPLAY_SIZE)
        pygame.display.update()
        background = pygame.Surface(DISPLAY_SIZE)
        background = background.convert()
        background.fill(GRAY)
        self._display_surf.blit(background, (0, 0))
        pygame.display.flip()

    def drawGame(self, image, circles):
        self._display_surf.blit(image, (0, 0))
        for circle in circles:
            pygame.draw.circle(self._display_surf, DRED, circle, 8, 2)

    def play(self, image, circles, subject):
        self._display_surf.blit(self.boarder, (DISPLAY_SIZE[0] / 2, 0))
        self.undo.draw(self._display_surf)
        self.skip.draw(self._display_surf)
        self.done.draw(self._display_surf)
        #self.help.draw(self._display_surf)
        playing = True
        raw_metric = None
        filtered_metric = None
        while playing:
            self.drawGame(image, circles)
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if image.get_rect().collidepoint(event.pos):
                        if pygame.key.get_pressed()[pygame.K_x]:
                            close = util.close_circle(event.pos, circles)
                            if not (close is None):
                                circles.pop(close)
                        else:
                            circles.append(event.pos)
                    elif self.undo.rect.collidepoint(event.pos):
                        try:
                            circles.pop(-1)
                        except:
                            pass

                    # elif self.help.rect.collidepoint(event.pos):
                    #     self.help_window = pygame.display.set_mode(H_WINDOW_SIZE)
                    #     self.help.draw(self.help_window)
                    #     playing = False

                    elif self.skip.rect.collidepoint(event.pos):
                        return None

                    elif self.done.rect.collidepoint(event.pos):
                        if len(circles) > 0:
                            raw_metric = util.score_string(circles, self.data[subject]['raw-circles'])
                            filtered_metric = util.score_string(circles, self.data[subject]['filtered-circles'])
                            self.metrics.change_text(raw_metric)
                            print("Moving on")
                            playing = False
                        else:
                            print ("You haven't circled any neurons.")

            pygame.display.flip()
            self.clock.tick(10)

        return raw_metric, filtered_metric

    def seeing(self, image, circles, image_done_raw, image_done_filtered, raw_metric, filtered_metric):
        seeing = True
        raw = True
        while seeing:
            self.drawGame(image, circles)
            if raw:
                self._display_surf.blit(image_done_raw, (DISPLAY_SIZE[0] / 2, 0))
            else:
                self._display_surf.blit(image_done_filtered, (DISPLAY_SIZE[0] / 2, 0))
            self.next_image.draw(self._display_surf)
            self.filtered.draw(self._display_surf)
            self.metrics.draw(self._display_surf)
            self.fix.draw(self._display_surf)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.next_image.rect.collidepoint(event.pos):
                        print("Moving on")
                        seeing = False

                    elif self.filtered.rect.collidepoint(event.pos):
                        raw = not raw
                        text = "Raw" if not raw else "Filter"
                        self.filtered.change_text(text)
                        self.metrics.change_text(raw_metric if raw else filtered_metric)
                    elif self.fix.rect.collidepoint(event.pos):
                        return True

            pygame.display.flip()
            self.clock.tick(10)

        return False

    def gameLoop(self):
        raw_metric = None
        filtered_metric = None

        for subject in self.data:
            pygame.display.set_caption(subject)
            width = int(DISPLAY_SIZE[0] / 2)
            height = DISPLAY_SIZE[1]
            image = pygame.transform.scale(pygame.image.load(self.data[subject]['image-clean']),
                                           (width, height)).convert()
            image_done_raw = pygame.transform.scale(pygame.image.load(self.data[subject]['image-raw']),
                                                    (width, height)).convert()
            image_done_filtered = pygame.transform.scale(pygame.image.load(self.data[subject]['image-filtered']),
                                                         (width, height)).convert()

            circles = []
            playing = True
            skip = False
            while playing:
                output = self.play(image, circles, subject)
                if output is None:
                    skip = True
                    break
                raw_metric, filtered_metric = output
                playing = self.seeing(image, circles, image_done_raw, image_done_filtered, raw_metric, filtered_metric)

            if not skip:
                this_path = os.path.join(self.data[subject]['out_path'], str(time.time()))
                util.csv_save(circles, this_path + "-gold_circles.csv")
                util.save_string("RAW: " + raw_metric, this_path + "-metic.txt")
                util.save_string("FILTERED: " + filtered_metric, this_path + "-metic.txt")


class button():
    def __init__(self, x, y, w, h, text, font, color, textcolor):
        self.color = color
        border = 4
        #self.rect = pygame.Rect(x + 2*border, y + 2*border, w - 4 * border, h - 4 * border)
            #thicker borders
        self.rect = pygame.Rect(x + border, y + border, w - 2 * border, h - 2 * border)
            #thinner borders
        self.font = font
        if textcolor is not None:
            self.text_color = textcolor
        else:
            self.text_color = BLACK
        if color is None:
            self.text_color = WHITE
        self.text = font.render(text, True, self.text_color)
        self.topleft = (self.rect.center[0] - self.text.get_rect().center[0],
                        self.rect.center[1] - self.text.get_rect().center[1])

    def change_text(self, new_text):
        self.text = self.font.render(new_text, True, self.text_color)
        self.topleft = (self.rect.center[0] - self.text.get_rect().center[0],
                        self.rect.center[1] - self.text.get_rect().center[1])

    def draw(self, display_surf):
        if self.color is not None:
            pygame.draw.rect(display_surf, self.color, self.rect)
        display_surf.blit(self.text, self.topleft)
