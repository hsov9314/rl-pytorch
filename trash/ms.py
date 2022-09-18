import pygame
import random

pygame.init()

bg_color = (192, 192, 192)
grid_color = (128, 128, 128)

game_width = 10  # Change this to increase size
game_height = 10  # Change this to increase size
numMine = 9  # Number of mines
grid_size = (
    32  # Size of grid (WARNING: macke sure to change the images dimension as well)
)
border = 16  # Top border
top_border = 100  # Left, Right, Bottom border
display_width = grid_size * game_width + border * 2  # Display width
display_height = grid_size * game_height + border + top_border  # Display height

gameDisplay = pygame.display.set_mode((display_width, display_height))  # Create display
timer = pygame.time.Clock()  # Create timer
pygame.display.set_caption("Minesweeper")  # S Set the caption of window

# Import files
spr_emptyGrid = pygame.image.load("Sprites/empty.png")
spr_flag = pygame.image.load("Sprites/flag.png")
spr_grid = pygame.image.load("Sprites/Grid.png")
spr_grid1 = pygame.image.load("Sprites/grid1.png")
spr_grid2 = pygame.image.load("Sprites/grid2.png")
spr_grid3 = pygame.image.load("Sprites/grid3.png")
spr_grid4 = pygame.image.load("Sprites/grid4.png")
spr_grid5 = pygame.image.load("Sprites/grid5.png")
spr_grid6 = pygame.image.load("Sprites/grid6.png")
spr_grid7 = pygame.image.load("Sprites/grid7.png")
spr_grid8 = pygame.image.load("Sprites/grid8.png")
spr_grid7 = pygame.image.load("Sprites/grid7.png")
spr_mine = pygame.image.load("Sprites/mine.png")
spr_mineClicked = pygame.image.load("Sprites/mineClicked.png")
spr_mineFalse = pygame.image.load("Sprites/mineFalse.png")


# Create global values
grid = []  # The main grid
mines = []  # Pos of the mines

# Create class grid
class Grid:
    def __init__(self, xGrid, yGrid, type):

        self.xGrid = xGrid  # X pos of grid
        self.yGrid = yGrid  # Y pos of grid
        self.clicked = False  # Boolean var to check if the grid has been clicked
        self.mineClicked = (
            False  # Bool var to check if the grid is clicked and its a mine
        )
        self.mineFalse = False  # Bool var to check if the player flagged the wrong grid
        self.flag = False  # Bool var to check if player flagged the grid
        # Create rectObject to handle drawing and collisions
        self.rect = pygame.Rect(
            border + self.xGrid * grid_size,
            top_border + self.yGrid * grid_size,
            grid_size,
            grid_size,
        )
        self.val = type  # Value of the grid, -1 is mine

    def drawGrid(self):
        # Draw the grid according to bool variables and value of grid
        if self.mineFalse:
            MineSweeper.gameDisplay.blit(spr_mineFalse, self.rect)
        else:
            print(self.clicked)
            if self.clicked:
                if self.val == -1:
                    if self.mineClicked:
                        MineSweeper.gameDisplay.blit(spr_mineClicked, self.rect)
                    else:
                        MineSweeper.gameDisplay.blit(spr_mine, self.rect)
                else:
                    if self.val == 0:
                        MineSweeper.gameDisplay.blit(spr_emptyGrid, self.rect)
                    elif self.val == 1:
                        MineSweeper.gameDisplay.blit(spr_grid1, self.rect)
                    elif self.val == 2:
                        MineSweeper.gameDisplay.blit(spr_grid2, self.rect)
                    elif self.val == 3:
                        MineSweeper.gameDisplay.blit(spr_grid3, self.rect)
                    elif self.val == 4:
                        MineSweeper.gameDisplay.blit(spr_grid4, self.rect)
                    elif self.val == 5:
                        MineSweeper.gameDisplay.blit(spr_grid5, self.rect)
                    elif self.val == 6:
                        MineSweeper.gameDisplay.blit(spr_grid6, self.rect)
                    elif self.val == 7:
                        MineSweeper.gameDisplay.blit(spr_grid7, self.rect)
                    elif self.val == 8:
                        MineSweeper.gameDisplay.blit(spr_grid8, self.rect)

            else:
                if self.flag:
                    MineSweeper.gameDisplay.blit(spr_flag, self.rect)
                else:
                    MineSweeper.gameDisplay.blit(spr_grid, self.rect)

    def revealGrid(self):
        self.clicked = True
        # Auto reveal if it's a 0
        if self.val == 0:
            for x in range(-1, 2):
                if self.xGrid + x >= 0 and self.xGrid + x < game_width:
                    for y in range(-1, 2):
                        if self.yGrid + y >= 0 and self.yGrid + y < game_height:
                            if not MineSweeper.grid[self.yGrid + y][
                                self.xGrid + x
                            ].clicked:
                                MineSweeper.grid[self.yGrid + y][
                                    self.xGrid + x
                                ].revealGrid()
        elif self.val == -1:
            # Auto reveal all mines if it's a mine
            for m in MineSweeper.mines:
                if not MineSweeper.grid[m[1]][m[0]].clicked:
                    MineSweeper.grid[m[1]][m[0]].revealGrid()

    def updateValue(self):
        # Update the value when all grid is generated
        if self.val != -1:
            for x in range(-1, 2):
                if self.xGrid + x >= 0 and self.xGrid + x < game_width:
                    for y in range(-1, 2):
                        if self.yGrid + y >= 0 and self.yGrid + y < game_height:
                            if (
                                MineSweeper.grid[self.yGrid + y][self.xGrid + x].val
                                == -1
                            ):
                                self.val += 1


class MineSweeper:
    gameDisplay = pygame.display.set_mode((display_width, display_height))
    grid = []
    mines = []
    unrevealed_grid = []

    def __init__(self):
        self.timer = pygame.time.Clock()  # Create timer
        pygame.display.set_caption("Minesweeper")  # S Set the caption of window

        self.gameState = "Playing"  # Game state
        self.mineLeft = numMine  # Number of mine left

        self.grid = []
        self.mines = []

        MineSweeper.gameDisplay.fill(bg_color)
        self._generate_mines()
        self._generate_entire_grid()
        self._update_grid()

        self.w = True
        self.draw_grids()
        self.timer = pygame.time.Clock()

    def _generate_mines(self):
        MineSweeper.mines = [
            [random.randrange(0, game_width), random.randrange(0, game_height)]
        ]

        for c in range(numMine - 1):
            pos = [random.randrange(0, game_width), random.randrange(0, game_height)]
            same = True
            while same:
                for i in range(len(MineSweeper.mines)):
                    if pos == MineSweeper.mines[i]:
                        pos = [
                            random.randrange(0, game_width),
                            random.randrange(0, game_height),
                        ]
                        break
                    if i == len(MineSweeper.mines) - 1:
                        same = False
            MineSweeper.mines.append(pos)
        # print(MineSweeper.mines)

    def _generate_entire_grid(self):
        for j in range(game_height):
            line = []
            for i in range(game_width):
                if [i, j] in MineSweeper.mines:
                    line.append(Grid(i, j, -1))
                else:
                    line.append(Grid(i, j, 0))
                MineSweeper.unrevealed_grid.append([i, j])
            MineSweeper.grid.append(line)
        print(MineSweeper.unrevealed_grid)

    def _update_grid(self):
        for i in MineSweeper.grid:
            for j in i:
                j.updateValue()

    def _update_ui(self):
        MineSweeper.gameDisplay.fill(bg_color)
        self.check_won()
        pygame.display.flip()

    def _update_unrevealed_grid(self):
        MineSweeper.unrevealed_grid = []
        for idi, i in enumerate(MineSweeper.grid):
            for idj, j in enumerate(i):
                if j.mineClicked == False:
                    MineSweeper.unrevealed_grid.append([idi, idj])

    def play_step(self, coord):
        i, j = coord
        # If player left clicked of the grid
        MineSweeper.grid[j][i].revealGrid()
        # Toggle flag off
        if MineSweeper.grid[j][i].flag:
            mineLeft += 1
            MineSweeper.grid[j][i].flag = False
        # If it's a mine
        if MineSweeper.grid[j][i].val == -1:
            self.gameState = "Game Over"
            MineSweeper.grid[j][i].mineClicked = True
        self._update_unrevealed_grid()
        self._update_ui()
        self.timer.tick(40)
        print("play step done")

        return MineSweeper.unrevealed_grid

    # def play_step(self):
    #     for event in pygame.event.get():
    #         # Check if player close window
    #         if event.type == pygame.QUIT:
    #             self.gameState = "Exit"
    #         # Check if play restart
    #         if self.gameState == "Game Over" or self.gameState == "Win":
    #             if event.type == pygame.KEYDOWN:
    #                 if event.key == pygame.K_r:
    #                     self.gameState = "Exit"
    #                     gameLoop()
    #         else:
    #             if event.type == pygame.MOUSEBUTTONUP:
    #                 print("button up")
    #                 for i in self.grid:
    #                     for j in i:
    #                         if j.rect.collidepoint(event.pos):
    #                             if event.button == 1:
    #                                 # If player left clicked of the grid
    #                                 print("before reveal")
    #                                 j.revealGrid()
    #                                 print("after reveal")
    #                                 # Toggle flag off
    #                                 if j.flag:
    #                                     self.mineLeft += 1
    #                                     j.falg = False
    #                                 # If it's a mine
    #                                 if j.val == -1:
    #                                     self.gameState = "Game Over"
    #                                     j.mineClicked = True
    #                             elif event.button == 3:
    #                                 # If the player right clicked
    #                                 if not j.clicked:
    #                                     if j.flag:
    #                                         j.flag = False
    #                                         self.mineLeft += 1
    #                                     else:
    #                                         j.flag = True
    #                                         self.mineLeft -= 1
    #     self.check_won()
    #     pygame.display.update()

    def check_won(self):
        self.w = True
        self.draw_grids()
        if self.w and self.gameState != "Exit":
            self.gameState = "Win"
        # print(self.gameState)

    def draw_grids(self):
        for i in MineSweeper.grid:
            for j in i:
                j.drawGrid()
                # print(j.val)
                # print(j.clicked)
                if j.val != -1 and not j.clicked:
                    self.w = False


def run_ms():
    game = MineSweeper()
    while True:
        coord = [int(s) for s in input("x, y").split(" ")]
        print(coord)
        grids = game.play_step(coord=coord)
        for i in grids:
            for j in i:
                print("[{}, {}]".format(i, j))
        # game.play_step()


def gameLoop():
    gameState = "Playing"  # Game state
    mineLeft = numMine  # Number of mine left
    global grid  # Access global var
    grid = []
    global mines
    t = 0  # Set time to 0

    # Generating mines
    mines = [[random.randrange(0, game_width), random.randrange(0, game_height)]]

    for c in range(numMine - 1):
        pos = [random.randrange(0, game_width), random.randrange(0, game_height)]
        same = True
        while same:
            for i in range(len(mines)):
                if pos == mines[i]:
                    pos = [
                        random.randrange(0, game_width),
                        random.randrange(0, game_height),
                    ]
                    break
                if i == len(mines) - 1:
                    same = False
        mines.append(pos)

    # Generating entire grid
    for j in range(game_height):
        line = []
        for i in range(game_width):
            if [i, j] in mines:
                line.append(Grid(i, j, -1))
            else:
                line.append(Grid(i, j, 0))
        grid.append(line)

    # Update of the grid
    for i in grid:
        for j in i:
            j.updateValue()

    # Main Loop
    while gameState != "Exit":
        print("loop")
        # Reset screen
        gameDisplay.fill(bg_color)

        # User inputs
        for event in pygame.event.get():
            # Check if player close window
            if event.type == pygame.QUIT:
                gameState = "Exit"
            # Check if play restart
            if gameState == "Game Over" or gameState == "Win":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        gameState = "Exit"
                        gameLoop()
            else:
                if event.type == pygame.MOUSEBUTTONUP:
                    for i in grid:
                        for j in i:
                            if j.rect.collidepoint(event.pos):
                                if event.button == 1:
                                    # If player left clicked of the grid
                                    j.revealGrid()
                                    # Toggle flag off
                                    if j.flag:
                                        mineLeft += 1
                                        j.falg = False
                                    # If it's a mine
                                    if j.val == -1:
                                        gameState = "Game Over"
                                        j.mineClicked = True
                                elif event.button == 3:
                                    # If the player right clicked
                                    if not j.clicked:
                                        if j.flag:
                                            j.flag = False
                                            mineLeft += 1
                                        else:
                                            j.flag = True
                                            mineLeft -= 1

        # Check if won
        w = True
        for i in grid:
            for j in i:
                j.drawGrid()
                if j.val != -1 and not j.clicked:
                    w = False
        if w and gameState != "Exit":
            gameState = "Win"

        # Draw Texts
        if gameState != "Game Over" and gameState != "Win":
            t += 1
        elif gameState == "Game Over":
            for i in grid:
                for j in i:
                    if j.flag and j.val != -1:
                        j.mineFalse = True
        else:
            pass
        # Draw time
        s = str(t // 15)
        screen_text = pygame.font.SysFont("Calibri", 50).render(s, True, (0, 0, 0))
        gameDisplay.blit(screen_text, (border, border))
        # Draw mine left
        screen_text = pygame.font.SysFont("Calibri", 50).render(
            mineLeft.__str__(), True, (0, 0, 0)
        )
        gameDisplay.blit(screen_text, (display_width - border - 50, border))

        pygame.display.update()  # Update screen

        timer.tick(15)  # Tick fps


run_ms()
pygame.quit()
quit()

# gameLoop()
# pygame.quit()
# quit()
