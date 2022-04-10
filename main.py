import time
from Grid import Grid

# Intialize Constants
SCREEN_SIZE = 800
GRID_SIZE = 100





def test():
    myGrid = Grid(SCREEN_SIZE, GRID_SIZE)
    myGrid.createGrid()
    #myGrid.importGrid
    myGrid.addDrivers(1)

    # Handle all drivers
    myGrid.handleDrivers()


def main():
    myGrid = Grid(SCREEN_SIZE, GRID_SIZE)
   
    myGrid.createGrid()

    myGrid.addDrivers(3)
    #myGrid.drawonGrid()
    while True:
        
        #for event in myGrid.getGridEvent():
        myGrid.imageGrid()
            #myGrid.handleMousePressedEvent()
            #myGrid.handleButtonPressedEvent(event)
            #myGrid.drawGrid()
            
            

    #myGrid.importGrid
    

   

      


if __name__ == "__main__":
    main()