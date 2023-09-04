from surface import Surface
import stats
import random
import copy

cross_rate = 0.3
mut_rate = 0.05
cycles = 500
population = []
padres = []
next_generation = []
maximos = []
minimos = []
promedios = []
elite_population = []
elitismo = False
hijos = []

def init(population_size = 10, height = 10, width = 10, turbines = 25):
    for _ in range(population_size):
        surface = Surface(height=height, width=width, turbines=turbines)
        population.append(surface)

def evaluar(population):
    total = 0
    for ind in population:
        ind.power = ind.get_total_power()
        total += ind.get_total_power()
    for ind in population:    
        ind.fitness = ind.get_total_power() / total
    population.sort(key = lambda ind: (ind.power), reverse=True)

def torneo():
    contendientes = []
    while (len(padres)<2):
        for _ in range(10):
            posicion = random.randint(0, len(population)-1)
            contendientes.append(population[posicion])  
        padres.append(max(contendientes, key=lambda cont: cont.fitness))
        contendientes.clear()

def ruleta():
    while len(padres)<2:
        acum = 0   
        for ind in population:
            peso = random.random()
            acum += ind.fitness
            if acum >= peso:
                padres.append(ind)
                break
    return padres

def seleccion(metodo):
    if (metodo == "ruleta"):
        return ruleta()
    if (metodo == "torneo"):
        return torneo()
    
def crossover(padres, hijos):
    hijos.clear()
    cross_point = random.randint(0, padres[0].height-1)

    if cross_rate >= random.random():
        child1=Surface()
        child2=Surface()

        child1.set_surface(padres[0].surface[:cross_point] + padres[1].surface[cross_point:])
        child2.set_surface(padres[1].surface[:cross_point] + padres[0].surface[cross_point:])

        while child1.turbine_count() > 25:
            child1.toggle_cell()
            
        while child2.turbine_count() > 25:
            child2.toggle_cell()
        
        hijos.append(child1)
        hijos.append(child2)
    else:
        hijos=[copy.deepcopy(p) for p in padres]
    return hijos


def mutacion(ind):
    if mut_rate > random.random():
        ind.swap_cell()
    return ind

def elite(population):
    elite_population.clear()
    for _ in range(2):
        elite_population.append(population.pop(0))

init(population_size=50, height=10, width=10, turbines=25)
evaluar(population)
stats.save_data(population, maximos, minimos, promedios)
for _ in range(cycles):
    if elitismo:
        elite(population)
    while len(next_generation)<len(population):
        padres.clear()
        seleccion('torneo')
        hijos=[copy.deepcopy(c) for c in crossover(padres, hijos)]
        for h in hijos:
            next_generation.append(mutacion(h))
    population.clear()
    population=[copy.deepcopy(ind) for ind in next_generation]
    next_generation.clear()
    if elitismo:
        for e in elite_population:
            population.append(e)
    evaluar(population)
    stats.save_data(population, maximos, minimos, promedios)


for ind in population:
    ind.print_surface()
    print('Turbinas:', ind.turbine_count())
    print('Potencia total: ', ind.get_total_power())
    print('Potencia media:', ind.get_average_power())
    print('Fitness:', ind.fitness)
    print('---------')

print('Configuracion optima: ')
population[0].print_surface()
print('Turbinas:', population[0].turbine_count())
print('Potencia total: ', population[0].get_total_power())
print('Potencia media:', population[0].get_average_power())
print('Fitness:', population[0].fitness)
print('---------')

stats.grafica(maximos, minimos, promedios)