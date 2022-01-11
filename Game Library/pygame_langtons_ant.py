# Simple pygame program

# Langton's ant it's an universal Turing machine

# Import and initialize the pygame library
import pygame

SIZE = 500
WHITE = (255, 255, 255)
LIGHT_BLUE = (220, 220, 220)
BLACK = (20, 20, 20)
GREEN = (120, 255, 120)
N = 11
ORIGIN = (5, 5)
ANT_COLOR1 = (0, 0, 250)
ANT_COLOR2 = (0, 100, 100)
# N = int(input('Write the table size'))
board = {(x, y): False for x in range(N) for y in range(N)}  # dictionary


class Ant:
    def __init__(self, origin):
        self.loc = origin
        self.heading = 2

    def move_ant(self, board):
        # changing one spot in which the ant moved
        if board[self.loc]:
            self.heading = (self.heading - 1) % 4
            board[self.loc] = False
        else:
            self.heading = (self.heading + 1) % 4
            board[self.loc] = True

        move = [
            (0, -1),  # up
            (1, 0),  # right
            (0, 1),  # down
            (-1, 0)  # left
        ]

        self.loc = (self.loc[0] + move[self.heading][0], self.loc[1] + move[self.heading][1])

        return board

    def draw(self, board):
        offset_x = self.loc[0] * step
        offset_y = self.loc[1] * step
        pygame.draw.circle(screen, ANT_COLOR1, (offset_x + side // 2, offset_y + side // 2), side // 2)

        if self.heading == 0:
            hx, hy = (0.5, 0.25)
        elif self.heading == 1:
            hx, hy = (0.75, 0.5)
        elif self.heading == 2:
            hx, hy = (0.5, 0.75)
        elif self.heading == 3:
            hx, hy = (0.25, 0.5)

        pygame.draw.circle(screen, ANT_COLOR2, (offset_x + int(side * hx), offset_y + int(side * hy)), side // 4)


ant = Ant(ORIGIN)
pygame.init()

clock = pygame.time.Clock()

# Set up the drawing window
screen = pygame.display.set_mode([SIZE, SIZE])

# each step the ant takes
step = SIZE / N
side = int(round(step))

# Run until the user asks to quit
running = True
while running:

    # Fill the background with white
    screen.fill(LIGHT_BLUE)

    board = ant.move_ant(board)

    # iterating over the dictionary board
    for key, value in board.items():
        x = int(step * key[0])
        y = int(step * key[1])
        if value:
            pygame.draw.rect(screen, BLACK, (x, y, side, side))

    for i in range(0, N + 1):
        i_step = int(round(i * step))
        pygame.draw.line(screen, GREEN, (i_step, 0), (i_step, SIZE), width=3)
        pygame.draw.line(screen, GREEN, (0, i_step), (SIZE, i_step), width=3)

    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    ant.draw(board)
    clock.tick(2)
    # Flip the display
    pygame.display.flip()

# Done! Time to quit.
pygame.quit()
