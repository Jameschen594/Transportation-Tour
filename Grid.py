import pygame, math, random, copy, time
from Color import colorDictionary
from Node import Node
from Driver import Driver
from PathFinding import findPathAStar


from PIL import Image
from pygame. locals import*
import cv2

# Initialize Constants
APP_TITLE = "Transportation/Touring Service"

SURFACE_BACKGROUND = colorDictionary['WHITE']

NODE_DEFAULT_COLOR = colorDictionary['BLACK']
WALL_COLOR = colorDictionary['BLACK']
PASSENGER_COLOR = colorDictionary['YELLOW']
DRIVER_COLOR = colorDictionary['RED']

pygame.display.set_caption(APP_TITLE)

class Grid():
    # Constructor specifying window size and grid size (rows and columns)
    def __init__(self, winSize, gridSize):
        self.grid = []
        self.surface = pygame.display.set_mode((winSize, winSize))
        
        self.screenWidth = winSize
        self.screenHeight = winSize

        self.gridWidth = gridSize
        self.gridHeight = gridSize

        self.gap = winSize / gridSize

        self.selectedNode = None
        self.drivers = []

    # Initialize grid with empty nodes
    def createGrid(self):
        gridcount = 0
        screen = pygame.display.set_mode((self.screenWidth,self.screenHeight))
        #image = Image.open("/Users/jameschen/CS215/Transportation-Tour-Service/cebacity.png")
        #imrgb = image.convert("RGB")
        originalImage = cv2.imread("/Users/jameschen/CS215/Transportation-Tour-Service/cebacity.png")
        grayImage = cv2.cvtColor(originalImage,cv2.COLOR_BGR2GRAY)
        threshold_img = cv2.threshold(grayImage,100,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)[1]
        im_pil = Image.fromarray(grayImage)
        #imrgb = im_pil.convert("RGB")
        imrgb = im_pil.convert("P")
       

        for i in range(self.gridHeight):
            newRow = []
            for j in range(self.gridWidth):
                #if imrgb.getdata()[gridcount]>=(120,120,120):
                newNode = Node(i * self.gap, j * self.gap, self.gap, False, False, NODE_DEFAULT_COLOR)
                #else:
                     #newNode = Node(i * self.gap, j * self.gap, self.gap, False, False, NODE_DEFAULT_COLOR)
                newRow.append(newNode)
                gridcount+=1
            self.grid.append(newRow)



    # Initialize grid from file
    def importGrid(self, file):
        pass
    
    def addDrivers(self, n):
        for i in range(n):
            selectedNode = self.getRandomTraversableNode()

            selectedNode.setSpecial(True)
            selectedNode.setColor(DRIVER_COLOR)

            newDriver = Driver(selectedNode.getGridPos())

            self.drivers.append(newDriver)
    
    def getRandomTraversableNode(self):        
        while True:
            randomRow = random.randint(0, self.gridWidth-1)
            randomColumn = random.randint(0, self.gridHeight-1)
            selectedNode = self.getNode(randomRow, randomColumn)
            if not selectedNode.getWall():
                return selectedNode
    
    # Draw the grid with pygames

    def drawGrid(self):
         for row in self.grid:
            for node in row:
                 
                if node.getWall() or node.getSpecial():
                    pygame.draw.rect(self.surface, node.color, node.getRect())
                else:
                    pygame.draw.rect(self.surface, node.color, node.getRect(), 1)

    # Draw the grid with pygames
    def drawonGrid(self):
        
       
        screen = pygame.display.set_mode((self.screenWidth,self.screenHeight))
        image = Image.open("/Users/jameschen/CS215/Transportation-Tour-Service/cebacity.png")
        #image = pygame.image.load("/Users/jameschen/CS215/Transportation-Tour-Service/cebacity.png")
        #pygame.display.set_icon(image)
        mode = image.mode
        size =image.size
        data =  image.tobytes()
        py_image = pygame.image.fromstring(data,size,mode)

        rect = py_image.get_rect()
        rect.center = self.screenHeight/2,self.screenWidth/2
        running = True
        screen.blit(py_image,rect)
        #SURFACE_BACKGROUND =colorDictionary['YELLOW']
        #self.surface.fill(SURFACE_BACKGROUND)
        nodecount = 0
        for row in self.grid:
            for node in row:
               
                if node.getWall() or node.getSpecial() :
                    pygame.draw.rect(self.surface, node.color, node.getRect())
                else:
                    pygame.draw.rect(self.surface, node.color, node.getRect(), 1)
                nodecount+=1
            
        pygame.display.update()

    def resetGrid(self):
        for row in self.grid:
            for node in row:
                node.resetNode()
    
    def deleteGrid(self):
        pygame.quit()

    def getGridEvent(self):
        return pygame.event.get()

    def handleMousePressedEvent(self):
        # If left mouse button was pressed
        if pygame.mouse.get_pressed()[0]:
            mousePosX, mousePosY = pygame.mouse.get_pos()
            selectedNode = self.getMousePosNode(mousePosX, mousePosY)
            selectedNode.makeWall()
        # If right mouse button was pressed
        elif pygame.mouse.get_pressed()[2]:
            pass
    
    def handleButtonPressedEvent(self, event):
        # If user pressed a button
        if event.type == pygame.KEYDOWN:
            # If user pressed D key, reset node
            if event.key == pygame.K_d:
                mousePosX, mousePosY = pygame.mouse.get_pos()
                selectedNode = self.getMousePosNode(mousePosX, mousePosY)
                selectedNode.resetNode()
    
    def handleDrivers(self):
        for driver in self.drivers:
            
            # If drivers have a path, move to next path
            if driver.getPathLength() > 0:
                currentPos = driver.getPos()
                nextPos = driver.getNextPath()

                currentNode = self.getNode(currentPos[0], currentPos[1])
                nextNode = self.getNode(nextPos[0], nextPos[1])

                if not nextNode.getWall():

                    currentNode.removeOccupant(driver)
                    currentNode.setSpecial(False)
                    currentNode.setColor(NODE_DEFAULT_COLOR)

                    driver.setPos(nextPos)
                    nextNode.addOccupant(driver)
                    nextNode.setSpecial(True)
                    nextNode.setColor(DRIVER_COLOR)

            # If drivers have no path, create a random path
            else:
                destination = self.getRandomTraversableNode()
                path = findPathAStar(copy.deepcopy(self.grid), self.gridHeight, self.gridWidth, driver.getPos(), destination.getGridPos())
                driver.setPath(path)
            
            time.sleep(0.5)
    
    def handlePassengers(self):
        pass

    def getMousePosNode(self, mousePosX, mousePosY):
        x = math.floor(mousePosX / self.gap)
        y = math.floor(mousePosY / self.gap)
        return self.getNode(x, y)

    def getMousePos(self):
        return pygame.mouse.get_pos()

    def getNode(self, row, column):

        if (row < self.gridHeight and row >= 0) and (column < self.gridWidth and column >= 0): 
            return self.grid[row][column]
    
    def imageGrid(self):
        screen = pygame.display.set_mode((self.screenWidth,self.screenHeight))
        image = Image.open("/Users/jameschen/CS215/Transportation-Tour-Service/cebacity.png")
        imrgb = image.convert("RGB")
        #print(list(imrgb.getdata()))
        print(list(imrgb.getdata())[0])
        
        #data = Image.getdata()
        #image = pygame.image.load("/Users/jameschen/CS215/Transportation-Tour-Service/cebacity.png")
        #pygame.display.set_icon(image)
        mode = image.mode
        size =image.size
        data =  image.tobytes()
        py_image = pygame.image.fromstring(data,size,mode)

        rect = py_image.get_rect()
        rect.center = self.screenHeight/2,self.screenWidth/2
        running = True
        screen.blit(py_image,rect)
        self.drawonGrid()
        pygame.draw.rect(screen,"Blue",rect,2)
        while running:
        
            for event in self.getGridEvent():
                if event.type == QUIT:
                    running=False
            self.handleMousePressedEvent()
            self.handleButtonPressedEvent(event)
            self.drawGrid()
            self.handleDrivers()
                
            screen.blit(py_image,rect)
            #self.createGrid()
            pygame.draw.rect(screen,"Blue",rect,2)

        
            pygame.display.update()

        pygame.quit()
    
        




       
