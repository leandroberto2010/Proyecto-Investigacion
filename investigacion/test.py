import math

# Constantes
WIND_SPEED = 12
Ct = 0.8                   #Coeficiente de empuje
SURFACE_ROUGHNESS = 0.694  #Rugocidad del terreno
HEIGHT = 60                 #Altura del buje
TURBINE_RADIUS = 24.1         #Radio de la turbina
K = 1/(2*math.log(HEIGHT/SURFACE_ROUGHNESS))   #Coeficiente de disminucion de estela
WAKE_RADIUS = TURBINE_RADIUS*1                  #Radio de la estela
D = 48.2                    #Diametro de la turbina

def generated_power(wind_speed = WIND_SPEED):
    if wind_speed == 12:
        return 640.5
    else:
        return  0.5 * 1.2 * 1.825 *  wind_speed * 0.42 #0.42 es el Cp de la turbina a una velocidad de 7m/s

def calc_wind_speed(distance, wind_speed = WIND_SPEED):
    return wind_speed*(1-(1-math.sqrt(1-Ct))/(1+(2*K*distance)/D)**2)

