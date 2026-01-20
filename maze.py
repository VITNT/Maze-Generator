import pygame
import random
import math
import sys

pygame.init()

SIZE = 40
SCR_WID = 0
SCR_HEI = 0
MARGIN = 5

WALL_COL = (0, 255, 0)
PATH_ONCE = (0, 120, 120)
PATH_TWICE = (0, 40, 40)
FOLLOW_COL = (255, 0, 0)
END_COL = (0, 0, 255)
CLOSE_COL = (40, 40, 40)
OPEN_COL = (100, 80, 80)
FINAL_COL = (80, 120, 80)
PLAYER_COL = (255, 255, 255)

playerBox = pygame.Rect(SIZE / 2 + MARGIN, SIZE / 2 + MARGIN, 30, 30)
playerCol = 0
playerRow = 0

playMode = False
showPath = False
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

    def drawTiles(self, surface):
        
        pygame.draw.rect(surface, self.color, self.rect)

    def drawWalls(self, surface): 

        if self.row == 0:
            pygame.draw.line(surface, WALL_COL, (self.x, self.y), (self.x + SIZE, self.y))

        if self.col == 0:
            pygame.draw.line(surface, WALL_COL, (self.x, self.y), (self.x, self.y + SIZE))
        
        if bool(self.walls[0]): 

            pygame.draw.line(surface, WALL_COL, (self.x + SIZE, self.y), (self.x + SIZE, self.y + SIZE)) 

        if bool(self.walls[1]): 

            pygame.draw.line(surface, WALL_COL, (self.x, self.y + SIZE), (self.x + SIZE, self.y + SIZE))

grid = []
walls = []
finalPath = []

for row in range(cellHeight):
    tileRow = []
    
    for col in range(cellWidth):
        tile = Tile(col, row)
        tileRow.append(tile)
    
    grid.append(tileRow)

currentTile = grid[0][0]
startTile = grid[0][0]
endTile = grid[cellHeight - 1][cellWidth - 1]

currentTile.visited = True
endTile.color = END_COL

stack = [currentTile]

def draw():
    
    SCREEN.fill((0, 0, 0))

    for tileRow in grid:
        for tile in tileRow:
            pygame.draw.rect(SCREEN, tile.color, tile.rect)

    for tileRow in grid:
        for tile in tileRow:
            tile.drawWalls(SCREEN)

    if showPath:
        for tile in finalPath:
            if tile not in (startTile, endTile):
                pygame.draw.rect(SCREEN, FINAL_COL, pygame.Rect(tile.x + 4, tile.y + 4, SIZE - 5, SIZE - 5))

    if playMode:
        pygame.draw.rect(SCREEN, PLAYER_COL, playerBox)

    pygame.display.flip()

def update():
    
    global currentTile, mazeFinished, run, endTile, pathCreated, showPath, playMode

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()
            sys.exit()
            return

        if event.type == pygame.KEYDOWN and mazeFinished:
            if event.key == pygame.K_p and not pathCreated:
                aStar()
                showPath = True
            elif event.key == pygame.K_o and not pathCreated:
                playMode = True

    for tileRow in grid:
        for tile in tileRow:
            if tile in (startTile, endTile):
                continue
            if tile.visited:
                if tile.visitedTwice:
                    tile.color = PATH_TWICE 
                else:
                    tile.color = PATH_ONCE

    if currentTile != endTile:
        currentTile.color = FOLLOW_COL
        
    if currentTile.visited:
        currentTile.visitedTwice = True
    
    currentTile.visited = True

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

    start = startTile
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
        
    print("something went wrong, please let us know what happened")

def buildBridge(path):
    
    finalPath.clear()
    current = path

    while current:
        finalPath.append(current)
        current = current.parent

def play():
    
    global playMode, showPath, playerCol, playerRow, run

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:

            if (event.key == pygame.K_LEFT or event.key == pygame.K_a) and playerCol > 0:
                if grid[playerRow][playerCol - 1].walls[0] == 0:
                    playerCol -= 1

            elif (event.key == pygame.K_RIGHT or event.key == pygame.K_d and playerCol < cellWidth - 1):
                if grid[playerRow][playerCol].walls[0] == 0:
                    playerCol += 1

            elif (event.key == pygame.K_UP or event.key == pygame.K_w and playerRow > 0):
                if grid[playerRow - 1][playerCol].walls[1] == 0:
                    playerRow -= 1

            elif (event.key == pygame.K_DOWN or event.key == pygame.K_s and playerRow < cellHeight - 1):
                if grid[playerRow][playerCol].walls[1] == 0:
                    playerRow += 1
            
            if playerRow == endTile.row and playerCol == endTile.col:
                print("You reached the end!")
                playMode = False
        
        elif event.type == pygame.QUIT:
            playMode = False
            run = False
            pygame.quit()
            sys.exit()
            return

    playerBox.x = grid[playerRow][playerCol].x + 4
    playerBox.y = grid[playerRow][playerCol].y + 4

run = True
clock = pygame.time.Clock()
delta_time = 1

while run:
    
    draw()
    if playMode:
        play()
    update()

    delta_time = clock.tick(120) / 1000
    delta_time = max(0.1, min(0.001, delta_time))

pygame.quit()