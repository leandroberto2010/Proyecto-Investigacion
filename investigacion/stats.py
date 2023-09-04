import matplotlib.pyplot as plt
import pandas

def calc_promedio(poblacion):
    valor_total = 0
    for ind in poblacion:
        valor_total += ind.objective_function()
    promedio = valor_total/len(poblacion)
    return promedio

def save_data(poblacion, maximos, minimos, promedios):
    #Máximos
    valormax = max(poblacion, key=lambda x: x.fitness)
    maximos.append(valormax.objective_function())

    #Mínimos
    valormin = min(poblacion, key=lambda x: x.fitness)
    minimos.append(valormin.objective_function())

    #Promedios
    promedios.append(calc_promedio(poblacion))

def grafica(maximos, minimos, promedios):
    df = pandas.DataFrame(list(zip(maximos, minimos, promedios)), columns = ['Maximos', 'Mimimos', 'Promedios'])
    df.to_csv('..data.csv')
    plt.plot(maximos, color = "green", label = "Maximos")
    plt.plot(promedios, color = "yellow", label = "Promedios")
    plt.plot(minimos, color = "red", label = "Minimos")
    
    plt.legend()
    plt.ylabel("f(x)", fontsize = "20")
    plt.xlabel("Ciclo", fontsize = "20")
    plt.show()