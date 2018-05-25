import pygame
import util
import os
import sys
import time

DISPLAY_SIZE = (1024, 512)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 102, 102)
DRED = (255, 0, 0)
GREEN = (102, 255, 102)
BLUE = (102, 102, 255)
LBLUE = (117, 192, 242)
LLBLUE = (48, 169, 249)
GRAY = (224, 224, 224)
YELLOW = (236, 231, 77)

class game():

    def __init__(self, data_path="../game_data"):
        self.clock = None
        self._display_surf = None
        ### Do the pygame init stuff
        self.init()

        ### Load Data
        self.data = util.load_data(data_path)
        datalist = list(self.data.keys())

        ### MAKE BUTTONS
        self.font = pygame.font.Font('freesansbold.ttf', 100)
        self.small_font = pygame.font.Font('freesansbold.ttf', 30)
        self.very_small_font = pygame.font.Font('freesansbold.ttf', 10)
        x = DISPLAY_SIZE[0] / 2

        self.undo = button(x, DISPLAY_SIZE[1] / 4 - 2, DISPLAY_SIZE[0] / 2, DISPLAY_SIZE[1] / 4, "Undo", self.font, RED, BLACK)

        self.skip = button(x, DISPLAY_SIZE[1] / 2 - 2, DISPLAY_SIZE[0] / 2, DISPLAY_SIZE[1] / 4, "Skip",
                           self.font, LLBLUE, BLACK)
        self.done = button(x, DISPLAY_SIZE[1] / 1.33 - 2, DISPLAY_SIZE[0] / 2, DISPLAY_SIZE[1] / 4, "Done",
                           self.font, GREEN, BLACK)
        self.boarder = pygame.Surface((DISPLAY_SIZE[0] / 2, DISPLAY_SIZE[1])).convert()
        self.boarder.fill(WHITE)

        self.previous = button(x, 0, DISPLAY_SIZE[0] / 4, DISPLAY_SIZE[1] / 4, "Previous",
                           self.small_font, GRAY, BLACK)

        self.allimages = button(x + 255, 0, DISPLAY_SIZE[0] / 4, DISPLAY_SIZE[1] / 4, "Show All Images",
                                self.small_font, GRAY, BLACK)

        self.next_image = button(x - 50, DISPLAY_SIZE[1] - 40, 100, 50, "Next", self.small_font, LBLUE, BLACK)
        self.filtered = button(x - 50, -5, 100, 50, "Filter", self.small_font, LBLUE, BLACK)
        self.metrics = button(0, 0, 200, 20, "", self.very_small_font, None, WHITE)
        self.fix = button(-5, DISPLAY_SIZE[1] - 40, 70, 50, "Fix", self.small_font, YELLOW, None)

        self.gameLoop(None)
        print("End of program")

    def init(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self._display_surf = pygame.display.set_mode(DISPLAY_SIZE)
        pygame.display.update()
        background = pygame.Surface(DISPLAY_SIZE)
        background = background.convert()
        background.fill(WHITE)
        self._display_surf.blit(background, (0, 0))
        pygame.display.flip()

    def drawGame(self, image, circles):
        self._display_surf.blit(image, (0, 0))
        for circle in circles:
            pygame.draw.circle(self._display_surf, DRED, circle, 8, 2)

    def play(self, image, circles, subject, image_index):
        # display existing points in the list 'circles'
        self._display_surf.blit(self.boarder, (DISPLAY_SIZE[0] / 2, 0))
        self.previous.draw(self._display_surf)
        self.allimages.draw(self._display_surf)
        self.undo.draw(self._display_surf)
        self.skip.draw(self._display_surf)
        self.done.draw(self._display_surf)
        playing = True
        prev = False
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

                    elif self.skip.rect.collidepoint(event.pos):
                        return None

                    elif self.previous.rect.collidepoint(event.pos):
                        if (image_index >= 1): return 20

                    elif self.allimages.rect.collidepoint(event.pos):
                        return 123

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


    def menu(self):
        viewing = True
        datalist = list(self.data.keys())
        i = 0
        y = 0
        page_end = 10
        #index at the end of each page
        onscreen = 0
        #number of buttons on current screen

        pygame.display.update()
        background = pygame.Surface(DISPLAY_SIZE)
        background = background.convert()
        background.fill(WHITE)
        self._display_surf.blit(background, (0, 0))
        pygame.display.flip()
        pygame.display.update()

        allilist = []
        #will store all buttons of images

        self.mnext = button(600, DISPLAY_SIZE[1] - 42, 100, 42, "Next",
                          self.small_font, LBLUE, BLACK)
        self.mprevious = button(250, DISPLAY_SIZE[1] - 42, 150, 42, "Previous",
                         self.small_font, LBLUE, BLACK)

        while (i < page_end):
            self.n1 = button(0, 0 + y, DISPLAY_SIZE[0], DISPLAY_SIZE[1] / 10, datalist[i],
                             self.small_font, GRAY, BLACK)
            self.n1.draw(self._display_surf)
            allilist.append(self.n1)
            pygame.display.update()
            i += 1
            y += 47

        self.mnext.draw(self._display_surf)
        self.mprevious.draw(self._display_surf)


        selected = False
        while viewing:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:

                    if(page_end <= len(datalist)):
                        if (self.mnext.rect.collidepoint(event.pos)):
                            if (page_end+10 <= len(datalist)):
                                onscreen = 10
                                y = 0
                                page_end+=10
                                self._display_surf.blit(background, (0, 0))
                                while (i < page_end):
                                    self.n1 = button(0, 0 + y, DISPLAY_SIZE[0], DISPLAY_SIZE[1] / 10, datalist[i],
                                                     self.small_font, GRAY, BLACK)
                                    self.n1.draw(self._display_surf)
                                    allilist.append(self.n1)
                                    i += 1
                                    y += 47

                                self.mnext.draw(self._display_surf)
                                self.mprevious.draw(self._display_surf)
                                pygame.display.flip()
                                pygame.display.update()

                            elif (i != len(datalist)):
                                onscreen = len(datalist) - i
                                y = 0
                                self._display_surf.blit(background, (0, 0))
                                while (i < len(datalist)):
                                    self.n1 = button(0, 0 + y, DISPLAY_SIZE[0], DISPLAY_SIZE[1] / 10, datalist[i],
                                                     self.small_font, GRAY, BLACK)
                                    self.n1.draw(self._display_surf)
                                    allilist.append(self.n1)
                                    i += 1
                                    y += 47
                                    page_end+=1


                        elif (self.mprevious.rect.collidepoint(event.pos)):
                            if (page_end > 10):
                                y = 0
                                page_end -= onscreen
                                i -= (10 + onscreen)
                                print(i, page_end)
                                while (i < page_end):
                                    self.n1 = button(0, 0 + y, DISPLAY_SIZE[0], DISPLAY_SIZE[1] / 10, datalist[i],
                                                     self.small_font, GRAY, BLACK)
                                    self.n1.draw(self._display_surf)
                                    pygame.display.update()
                                    i += 1
                                    y += 47

                                self.mnext.draw(self._display_surf)
                                self.mprevious.draw(self._display_surf)

                                onscreen = 10

                    k = page_end-10
                    #index of each button on the current page
                    while (k < page_end):
                        if (allilist[k]).rect.collidepoint(event.pos):
                            print("Showing " + datalist[k])
                            selected = True
                            self.gameLoop(k)
                            break
                        k+=1

                    self.mnext = button(600, DISPLAY_SIZE[1] - 42, 100, 42, "Next",
                                        self.small_font, LBLUE, BLACK)
                    self.mnext.draw(self._display_surf)
                    self.mprevious = button(250, DISPLAY_SIZE[1] - 42, 150, 42, "Previous",
                                            self.small_font, LBLUE, BLACK)
                    self.mprevious.draw(self._display_surf)

            if (selected == True):
                viewing = False

            pygame.display.flip()
            self.clock.tick(10)

        return False





    def gameLoop(self, i1):
        raw_metric = None
        filtered_metric = None

        datalist = list(self.data.keys())
        if i1 == None:
            i = 0
        else:
            i = i1
        while (i < len(datalist)):
            pygame.display.set_caption(datalist[i])
            width = int(DISPLAY_SIZE[0] / 2)
            height = DISPLAY_SIZE[1]
            image = pygame.transform.scale(pygame.image.load(self.data[datalist[i]]['image-clean']),
                                           (width, height)).convert()
            image_done_raw = pygame.transform.scale(pygame.image.load(self.data[datalist[i]]['image-raw']),
                                                    (width, height)).convert()
            image_done_filtered = pygame.transform.scale(pygame.image.load(self.data[datalist[i]]['image-filtered']),
                                                         (width, height)).convert()

            circles = []
            playing = True
            skip = False
            previous = False
            alli = False
            while playing:
                # upload circles file for the corresponding image
                # if the file does not exist, then circles = []
                # if the file does exist, then circles = [content of the file]
                output = self.play(image, circles, datalist[i], i)
                if output == 20:
                    print("Showing " + datalist[i-1])
                    i-=2
                    previous = True
                    break
                elif output == 123:
                    alli = True
                    playing = self.menu()
                    break
                elif output is None:
                    skip = True
                    print("Showing " + datalist[i+1])
                    break
                raw_metric, filtered_metric = output
                playing = self.seeing(image, circles, image_done_raw, image_done_filtered, raw_metric, filtered_metric)


            if not skip and not previous and not alli:
                # Saving the metrics
                this_path = os.path.join(self.data[datalist[i]]['out_path'], str(time.time()))
                util.csv_save(circles, this_path + "-gold_circles.csv")
                util.save_string("RAW: " + raw_metric, this_path + "-metic.txt")
                util.save_string("FILTERED: " + filtered_metric, this_path + "-metic.txt")

            i+=1




class button():
    def __init__(self, x, y, w, h, text, font, color, textcolor):
        self.color = color
        border = 4
        self.rect = pygame.Rect(x + border, y + border, w - 2 * border, h - 2 * border)
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
