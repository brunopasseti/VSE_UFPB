class Request():


    def __init__ (self):
        self.id = 0
        self.gridLocation = [0, 0]

    def getId(self):
        return self.id

    def setId(self, id):
        self.id = id
        return self

    def getGridLocation(self):
        return self.gridLocation
    def setGridLocation(self, gridLocation):
        self.gridLocation = gridLocation
    def setGridLocation(self, x, y):
        self.gridLocation = [x,y]
        pass
