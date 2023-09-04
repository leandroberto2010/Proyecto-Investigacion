from test import generated_power, calc_wind_speed
import random

free = "\033[1;47m" + ' '       #Espacio vacio
turbine = "\033[1;42m" + 'T'    #Turbina
forbidden = "\033[1;41m" + 'F'  #Espacio prohibido
distance = 4*24.1                  #Distancia entre turbinas en metros
wind =  12                       #Velocidad del viento en m/s

class Surface:
    def __init__(self, width = 10, height = 10, turbines = 0):
        self.power=0
        self.fitness = 0
        self.surface = []
        self.height = height
        self.width = width
        for _ in range(height):
            row = []
            for _ in range(width):
                row.append(free)
            self.surface.append(row)
        self.randomize(turbines)

    def set_surface(self, surface):
        self.surface = surface
        self.height = len(surface)
        self.width = len(surface[0])

    def set_forbidden_cells(self, locations):
        for location in locations:
            x, y = location
            self.surface[x][y] = forbidden

    def randomize(self, turbines):
        for _ in range(random.randint(0, turbines)):
            location = (random.randint(0, self.height-1), random.randint(0, self.width-1))
            while not self.place_turbine(location):
                location = (random.randint(0, self.height-1), random.randint(0, self.width-1))

    def place_turbine(self, location):
        x, y = location
        if self.surface[x][y] != free:
            return False
        else:
            self.surface[x][y] = turbine
            return True
        
    def toggle_cell(self):
        x = random.randint(0, self.height-1)
        y = random.randint(0, self.width-1)
        while self.surface[x][y]!= turbine:
            x = random.randint(0, self.height-1)
            y = random.randint(0, self.width-1) 
        self.surface[x][y] = free

    def swap_cell(self):
        x = random.randint(0, self.height-1)
        y = random.randint(0, self.width-1)
        while self.surface[x][y]!= turbine:
            x = random.randint(0, self.height-1)
            y = random.randint(0, self.width-1)
        self.surface[x][y]=free
        x = random.randint(0, self.height-1)
        y = random.randint(0, self.width-1)
        while self.surface[x][y]!=free:
            x = random.randint(0, self.height-1)
            y = random.randint(0, self.width-1)
        self.surface[x][y]=turbine
        cont=self.turbine_count()

            

    def turbine_count(self):
        count = 0
        for row in self.surface:
            for spot in row:
                if spot == turbine:
                    count += 1
        return count

    def get_size(self):
        return self.height*self.width
    
    def get_total_power(self):
        power = 0
        for spot in self.surface[0]:
            if spot == turbine:
                power += generated_power()

        for i in range(1, self.height):
            for j in range(self.width):
                if (self.surface[i][j] == turbine):
                    if (self.surface[i - 1][j] == turbine):
                        power += generated_power(calc_wind_speed(distance))
                    else:
                        power += generated_power(wind)
        return power
    
    def get_average_power(self):
        if self.turbine_count() != 0:
            return self.get_total_power() / self.turbine_count()
        else:
            return 0
    
    def print_surface(self):
        for row in self.surface:
            for spot in row:
                print(spot, end="")
            print("\033[0m")

    def objective_function(self):
        return self.get_total_power()