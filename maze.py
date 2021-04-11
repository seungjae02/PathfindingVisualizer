from settings import *
import pygame, random


class Maze:
    def __init__(self, app, wallPos):
        self.app = app
        self.visited = []
        self.walls = wallPos
        # x-range index on drawable surface is 1 to 52
        # y range index is 1 to 30
        self.xMax = 53
        self.yMax = 31

    def generateSolid(self):
        for y in range(1, self.yMax):
            for x in range(1, self.xMax):
                self.walls.append((x,y))
                self.draw((x,y), BLACK)
        self.redrawGrid()

        self.generateMaze()

    def generateMaze(self):
        x_pos = random.randint(1,self.xMax)
        y_pos = random.randint(1,self.yMax)
        start_pos = (x_pos, y_pos)

        print(len(self.walls))
        self.recursiveDFS(start_pos)

        print(len(self.walls))

    def checkValid(self, pos):
        if pos not in wall_nodes_coords_list and pos in self.walls:
            return True
        return False

    def recursiveDFS(self, pos):
        movesLeft = ['L', 'R', 'U', 'D']
        i, j = pos

        while movesLeft:
            chooseRandMove = random.randint(0, len(movesLeft)-1)
            currMove = movesLeft.pop(chooseRandMove)
            # Temporary variabes to not update the original pos of the current node
            xTemp = i
            yTemp = j

            if currMove == 'L':
                xTemp -= 2
            elif currMove == 'R':
                xTemp += 2
            elif currMove == 'U':
                yTemp += 2
            else:
                yTemp -= 2

            newPos = (xTemp, yTemp)

            if self.checkValid(newPos):
                self.walls.remove(newPos)
                # calculate difference between curr pos and neighbouring pos
                xDiff = newPos[0] - i
                yDiff = newPos[1] - j

                # Determine the middle wall position to remove
                middleWallPos = (i+xDiff/2, j+yDiff/2)

                # Remove the middle wall as well
                self.walls.remove((middleWallPos))

                self.drawMaze(middleWallPos, AQUAMARINE)
                self.drawMaze(newPos, AQUAMARINE)

                self.recursiveDFS(newPos)

        return

    def draw(self, pos, colour):
        i, j = pos
        pygame.draw.rect(self.app.screen, colour, (i * 24 + 240, j * 24, 24, 24), 0)

    def redrawGrid(self):
        # Redraw grid (for aesthetic purposes lol)
        for x in range(52):
            pygame.draw.line(self.app.screen, ALICE, (GS_X + x * 24, GS_Y), (GS_X + x * 24, GE_Y))
        for y in range(30):
            pygame.draw.line(self.app.screen, ALICE, (GS_X, GS_Y + y * 24), (GE_X, GS_Y + y * 24))

    def drawMaze(self, pos, colour):
        i, j = pos
        self.draw(pos, colour)

        # Redraw grid (for aesthetic purposes lol)
        for x in range(52):
            pygame.draw.line(self.app.screen, ALICE, (GS_X + x * 24, GS_Y), (GS_X + x * 24, GE_Y))
        for y in range(30):
            pygame.draw.line(self.app.screen, ALICE, (GS_X, GS_Y + y * 24), (GE_X, GS_Y + y * 24))

        pygame.display.update()
