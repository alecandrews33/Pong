

class vector():

    def __init__(self,x,y):
        self.x = x
        self.y = y


    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def add_vec(self, vector):
        self.x = self.x + vector.x
        self.y = self.y + vector.y
        