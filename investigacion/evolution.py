from surface import Surface
import stats
import random

forbidden_locations = []
cross_rate = 0.3
mut_rate = 0.05
cycles = 100
population = []
padres = []
next_generation = []
maximos = []
minimos = []
promedios = []
elite_population = []
elitismo = True

def init(population_size = 10, height = 10, width = 10, turbines = 25):
    for _ in range(population_size):
        surface = Surface(height=height, width=width, turbines=turbines)
        population.append(surface)

def evaluar(population):
    total = 0
    for ind in population:
        total += ind.objective_function()
    for ind in population:    
        ind.fitness = ind.objective_function() / total
    population.sort(key = lambda ind: (ind.fitness), reverse=True)

def torneo():
    contendientes = []
    while (len(padres)<2):
        for _ in range(4):
            posicion = random.randint(0, len(population)-1)
            contendientes.append(population[posicion])  
        padres.append(max(contendientes, key=lambda cont: cont.fitness))
        (max(contendientes, key=lambda cont: cont.fitness))   
        contendientes.clear()

def ruleta():
    for _ in range(2):
        acum = 0   
        for ind in population:
            peso = random.random()
            acum += ind.fitness
            if acum >= peso:
                padres.append(ind)
                break

def seleccion(metodo):
    if (metodo == "ruleta"):
        return ruleta()
    if (metodo == "torneo"):
        return torneo()
    
def crossover():
    def obtener_cromosoma(padres, cross_point):
        return padres[0].surface[:cross_point] + padres[1].surface[cross_point:]
    
    def realizar_crossover():
        cross_point = random.randint(0, padres[0].height)
        child1 = Surface()
        child2 = Surface()

        child1.set_surface(obtener_cromosoma(padres, cross_point))
        child2.set_surface(obtener_cromosoma(padres[::-1], cross_point))
        return child1, child2, cross_point
    
    if cross_rate >= random.random():
        child1, child2, cross_point = realizar_crossover()

        if child1.turbine_count() > 25 or child2.turbine_count() > 25:
            return crossover()
        '''print("--------------CROSSOVER------------------")
        print("CROSSPOINT: ", cross_point)
        print("PADRE 1")
        padres[0].print_surface()
        print("PADRE 2--------------------------------------")
        padres[1].print_surface()
        print("CHILD 1--------------------------------------")
        child1.print_surface()
        print("CHILD 2--------------------------------------")
        child2.print_surface()
        print("--------------------------------------")'''
        mutacion(child1)
        mutacion(child2)

        next_generation.append(child1)
        next_generation.append(child2)
    else:
        for padre in padres:
            mutacion(padre)
        next_generation.extend(padres)

def mutacion(ind):
    isFull = False
    if ind.turbine_count() >= 25: isFull = True
    if mut_rate > random.random():
        ind.toggle_cell(isFull)

def elite(population):
    for _ in range(2):
        elite_population.append(population.pop(0))



init(population_size=10, height=10, width=10, turbines=25)
evaluar(population)
stats.save_data(population, maximos, minimos, promedios)
for k in range(cycles):
    population.sort(key=lambda x: x.fitness, reverse=True)
    if elitismo:
        elite(population)
    while (len(next_generation) < len(population)):
        padres.clear()
        seleccion('torneo')
        crossover()
    population.clear
    population.extend(next_generation)
    if elitismo:
        population.extend(elite_population)
        elite_population.clear()
    evaluar(population)
    stats.save_data(population, maximos, minimos, promedios)
    next_generation.clear()
    '''print("-------------CICLO NUMERO ", k, "----------------------")
    i=0
    for parque in population:
        print(i)
        parque.print_surface()
        print('Turbinas:', parque.turbine_count())
        print('Potencia total: ', parque.get_total_power())
        print('Potencia media:', parque.get_average_power())
        print('Fitness:', parque.fitness)
        i+=1'''

for ind in population:
    ind.print_surface()
    print('Turbinas:', ind.turbine_count())
    print('Potencia total: ', ind.get_total_power())
    print('Potencia media:', ind.get_average_power())
    print('Fitness:', ind.fitness)
    print('---------')

stats.grafica(maximos, minimos, promedios)