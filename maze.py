import pygame
import random
import math
import sys

pygame.init()

SIZE = 40
SCR_WID = 0
SCR_HEI = 0
WALL_COL = (0, 255, 0)
PATH_ONCE = (0, 120, 120)
PATH_TWICE = (0, 40, 40)
FOLLOW_COL = (255, 0, 0)
END_COL = (0, 0, 255)
CLOSE_COL = (40, 40, 40)
OPEN_COL = (100, 80, 80)
FINAL_COL = (80, 120, 80)
MARGIN = 10

pressedAlr = False
mazeFinished = False
pathCreated = False
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
        self.distance = math.inf

    def drawTiles(self):
        
        pygame.draw.rect(SCREEN, self.color, self.rect)

    def drawWalls(self): 

        if self.row == 0:
            pygame.draw.line(SCREEN, WALL_COL, (self.x, self.y), (self.x + SIZE, self.y))

        if self.col == 0:
            pygame.draw.line(SCREEN, WALL_COL, (self.x, self.y), (self.x, self.y + SIZE))
        
        if bool(self.walls[0]): 

            pygame.draw.line(SCREEN, WALL_COL, (self.x + SIZE, self.y), (self.x + SIZE, self.y + SIZE)) 

        if bool(self.walls[1]): 

            pygame.draw.line(SCREEN, WALL_COL, (self.x, self.y + SIZE), (self.x + SIZE, self.y + SIZE))

grid = []

for row in range(cellHeight):
    tileRow = []
    
    for col in range(cellWidth):
        tile = Tile(col, row)
        tileRow.append(tile)
    
    grid.append(tileRow)

currentTile = grid[0][0]
endTile = grid[cellHeight - 1][cellWidth - 1]
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
    
    global currentTile, pressedAlr, mazeFinished, run, endTile, pathCreated

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()
            sys.exit()
            return

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p and mazeFinished:
                if not pressedAlr:
                    aStar()
                    pressedAlr = True
                else:
                    print("There is already an instance.")

    if pathCreated:
        return

    if not pathCreated:
        for tileRow in grid:
            for tile in tileRow:
                if tile.visited:
                    tile.color = PATH_TWICE if tile.visitedTwice else PATH_ONCE
                if tile == currentTile:
                    tile.color = FOLLOW_COL

    if currentTile.visited:
        currentTile.visitedTwice = True
    
    currentTile.visited = True
    endTile.color = END_COL

    if not mazeFinished:
        
        door = nextDoor(currentTile)

        if door:
            pick = random.choice(door)
            breakDoor(currentTile, pick)
            currentTile = pick
            stack.append(pick)
        elif stack:
            currentTile = stack.pop()
        else:
            mazeFinished = True
            print("Maze generation finished!")

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

def aStar():
    
    global pathCreated

    start = grid[0][0]
    end = grid[cellHeight - 1][cellWidth - 1]

    openGrid = []
    closedGrid = []

    for rowTile in grid:
        for tile in rowTile:
            tile.distance = math.inf
            tile.parent = None
            tile.heuristic = abs(tile.col - end.col) + abs(tile.row - end.row)

    start.distance = 0
    openGrid.append(start)

    while openGrid:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        currentTile = openGrid[0]
        shortestDistance = currentTile.distance + currentTile.heuristic

        for tile in openGrid:
            f = tile.distance + tile.heuristic
            if f < shortestDistance:
                shortestDistance = f
                currentTile = tile

        if currentTile == end:
            buildBridge(end)
            print("Path is Found!")
            pathCreated = True
            return

        openGrid.remove(currentTile)
        closedGrid.append(currentTile)

        if currentTile != start:
            currentTile.color = CLOSE_COL

        col = currentTile.col
        row = currentTile.row

        neighbors = []

        if col < cellWidth - 1 and currentTile.walls[0] == 0:
            neighbors.append(grid[row][col + 1])

        if col > 0 and grid[row][col - 1].walls[0] == 0:
            neighbors.append(grid[row][col - 1])

        if row < cellHeight - 1 and currentTile.walls[1] == 0:
            neighbors.append(grid[row + 1][col])

        if row > 0 and grid[row - 1][col].walls[1] == 0:
            neighbors.append(grid[row - 1][col])

        for neighbor in neighbors:
            if neighbor in closedGrid:
                continue

            newDistance = currentTile.distance + 1

            if newDistance < neighbor.distance:
                neighbor.distance = newDistance
                neighbor.parent = currentTile

                if neighbor not in openGrid:
                    openGrid.append(neighbor)
                    if neighbor != end:
                        neighbor.color = OPEN_COL

        draw()
        pygame.display.flip()
        pygame.time.delay(10) 
        
    print("something went wrong")

def buildBridge(path):
    current = path.parent
    while current:
        if current != grid[0][0]:
            current.color = FINAL_COL
        current = current.parent

run = True
clock = pygame.time.Clock()
delta_time = 1

while run:
    
    draw()
    update()

    delta_time = clock.tick(120) / 1000
    delta_time = max(0.1, min(0.001, delta_time))

pygame.quit()