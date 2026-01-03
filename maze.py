import pygame
import random

pygame.init()

SIZE = 40
SCR_WID = 0
SCR_HEI = 0
COL1 = (0, 255, 0)
COL2 = (0, 120, 120)
COL3 = (255, 0, 0)
COL4 = (0, 40, 40)
MARGIN = 10

cellWidth = int(input("Enter Number of Cells in Width (MAX: 40): "))
cellHeight = int(input("Enter Number of Cells in Height (MAX: 30): "))

if cellWidth * SIZE <= 1600 and cellHeight * SIZE <= 1200:
    SCR_WID = cellWidth * SIZE + MARGIN * 2
    SCR_HEI = cellHeight * SIZE + MARGIN * 2
else:
    print("Cannot do it, map too big")
    pygame.quit()
    quit()

SCREEN = pygame.display.set_mode((SCR_WID, SCR_HEI))

class Tile:
    def __init__(self, col, row):
        self.col = col
        self.row = row
        self.x = self.col * SIZE + MARGIN
        self.y = self.row * SIZE + MARGIN
        self.color = (0, 0, 50)
        self.rect = pygame.Rect(self.x, self.y, SIZE, SIZE)
        self.walls = [1,1]
        self.visited = False
        self.visitedTwice = False

    def drawTiles(self):
        
        pygame.draw.rect(SCREEN, self.color, self.rect)

    def drawWalls(self): 

        if self.row == 0:
            pygame.draw.line(SCREEN, COL1, (self.x, self.y), (self.x + SIZE, self.y))

        if self.col == 0:
            pygame.draw.line(SCREEN, COL1, (self.x, self.y), (self.x, self.y + SIZE))
        
        if bool(self.walls[0]): 

            pygame.draw.line(SCREEN, COL1, (self.x + SIZE, self.y), (self.x + SIZE, self.y + SIZE)) 

        if bool(self.walls[1]): 

            pygame.draw.line(SCREEN, COL1, (self.x, self.y + SIZE), (self.x + SIZE, self.y + SIZE))

grid = []

for row in range(cellHeight):
    tileRow = []
    
    for col in range(cellWidth):
        tile = Tile(col, row)
        tileRow.append(tile)
    
    grid.append(tileRow)

currentTile = grid[0][0]
currentTile.visited = True

stack = [currentTile]

def draw():
    
    for tileRow in grid:
        for tile in tileRow:
            tile.drawTiles()
    
    for tileRow in grid:
        for tile in tileRow:
            tile.drawWalls()
    
    pygame.display.flip()

def update():
    
    global currentTile

    for tileRow in grid:
        for tile in tileRow:
            if tile.visited:
                if tile.visitedTwice:
                    tile.color = COL4
                else:
                    tile.color = COL2
            if tile == currentTile:
                tile.color = COL3
    
    if currentTile.visited:
        currentTile.visitedTwice = True
    currentTile.visited = True

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()

    door = nextDoor(currentTile)
    
    if len(door) > 0:
        pick = random.choice(door)
        breakDoor(currentTile, pick)
        currentTile = pick
        stack.append(pick)
    elif len(stack) > 0:
        currentTile = stack[-1]
        stack.pop(-1)

def nextDoor(currentTile):

    door = []

    col = currentTile.col
    row = currentTile.row

    if col < cellWidth - 1 and not grid[row][col + 1].visited:
        door.append(grid[row][col + 1])

    if col and not grid[row][col - 1].visited:
        door.append(grid[row][col - 1])

    if row < cellHeight - 1 and not grid[row + 1][col].visited:
        door.append(grid[row + 1][col])

    if row and not grid[row - 1][col].visited:
        door.append(grid[row - 1][col])

    return door

def breakDoor(currentTile, pick):

    if pick.col - currentTile.col > 0:
        currentTile.walls[0] = 0

    if pick.col - currentTile.col < 0:
        pick.walls[0] = 0

    if pick.row - currentTile.row > 0:
        currentTile.walls[1] = 0
        
    if pick.row - currentTile.row < 0:
        pick.walls[1] = 0

run = True

while run:
    
    draw()
    update()

pygame.quit()