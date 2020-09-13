import matplotlib.pyplot as plt
import numpy as np

fig = plt.figure(num = 1)

t = np.linspace(0, 200, 1001)
#declaramos las listas donde se van a poner la posicion para graficar y su estatus
posicion = []
status = []
#altura inicial
y0 = 200
m = 80
g = -9.81
w = g*m
largoCuerda = 50
#punto critico
pc = y0 - largoCuerda
gama = 3
k = 15.2
#velocidad y el timempo del punto critico para la face inicial 
v = 0
tpc = 3.32543
h = y0

#las condiciones iniciales para la funcion con caida libre
c2CL = ((m*g)/gama - v)*(m/gama)
c1CL = h-c2CL

#las coniciones ideales para la caida libre y las variables de la funcion de caida con resorte
l =-(gama/(2*m))
mu = (np.sqrt(np.absolute(gama**2 -4*m*k))/(2*m))

c1CR= pc -(m*g)/k -y0 + largoCuerda
c2CR= (v-l*c1CR)/mu

#print(f"c1: {c1CL}")
#print(f"c2: {c2CL}")
def yCaidaLibre(t):
    #funcion para la caida libre para la primera fase (cuando no se necesita hacer un switch)
    return c1CL + c2CL*np.exp(-gama*(t)/m) + m*g*(t)/gama
def yCaidaLibreT(t):
    #funcion caida libre de transicion es para cuando se estan intercambiando las ecuaciones de caida resorte y caida libre
    return c1CL + c2CL*np.exp(-gama*((t-tpc))/m) + m*g*((t-tpc))/gama
def yResorte(t):
    #funcion para la caida con resorte
    return np.exp(l*(t-tpc))*(c1CR*np.cos(mu*(t-tpc)) + c2CR*np.sin(mu*(t-tpc))) + m*g/k +y0 - largoCuerda
def vCaidaLibre(t):
    #funcion para obtener la velocidad de la caida libre de la primera fase se ocupa para obtener la velocidad final
    #que se va a converir en un parametro para las condiciones iniciales 
    return -(c2CL*gama*np.exp((-gama*(t))/m))/m + m*g/gama
def vCaidaLibreT(t):
    #funcion para obtener la velocidad de la caida libre de transicion se ocupa para obtener la velocidad final
    #que se va a converir en un parametro para las condiciones iniciales 
    return -(c2CL*gama*np.exp((-gama*((t-tpc)))/m))/m + m*g/gama
def vResorte(t):
    #funcion para obtener la velocidad de la caida con resorte se ocupa para obtener la velocidad final
    #que se va a converir en un parametro para las condiciones iniciales 
    return (l*np.exp(l*(t-tpc)))*(c1CR*np.cos(mu*(t-tpc)) + c2CR*np.sin(mu*(t-tpc))) + (np.exp(l*(t-tpc)))*(-mu*c1CR*np.sin(mu*(t-tpc)) + mu*c2CR*np.cos(mu*(t-tpc)))

#se declaran parametros iniciales para el for loop que va a guardar una lista con los valores para graficar
inicio = True
transicion = False
yR = False
for i in t:
    #checa si la "y" que tiene que medir es del resorte o de la caida libre
    if(yR):
        y = yResorte(i)
    else:
        #checa si es para la primera fase o si ya es una caida libre de transicion
        if inicio:
            y = yCaidaLibre(i)
        else:
            y = yCaidaLibreT(i)
    #checa si tiene que guardar la "y" de caida libre o caida resorte
    if(y >= pc):
        yR = False
        #checa si esta transicionando entre caida libre y resorte o viceversa 
        if(transicion):
            #ajusta los valores para las condiciones iniciales y las ajusta
            v = vResorte(i)
            tpc = i
            h = pc
            c2CL = ((m*g)/gama - v)*(m/gama)
            c1CL = h-c2CL
        if inicio:
            status.append("CaidaLibreNormal")
            y = yCaidaLibre(i)
        else:
            status.append("CaidaLibreTransicion")
            y = yCaidaLibreT(i)
        #print(f"y: {y} vcaidaResorte {vResorte(i)} t: {i} tp: {tp} c1CL: {c1CL} c2CL: {c2CL}" )
        posicion.append(y)
        transicion = False
    #condicion para el resorte
    elif(y <= pc):
        yR = True
        #checa si esta en transicion, pero debido a la estructura del programa y las iteraciones invierte el booleano
        if(not transicion):
            if inicio:
                v = vCaidaLibre(i)
            else:
                v = vCaidaLibreT(i)
            inicio = False
            tpc = i
            h = pc
            c1CR= pc -(m*g)/k -y0 + largoCuerda
            c2CR= (v-l*c1CR)/mu
        status.append("CaidaResorte")
        y = yResorte(i)
        #print(f"y: {y} vcaidaLibre: {v} t: {i} tpc: {tpc} c1CR: {c1CR} c2CR: {c2CR}" )
        posicion.append(y)
        transicion = True 

#grafica la informacion necesaria
for i in range(len(t)):
    print(f"- t: {round(t[i], 2)}, y: {round(posicion[i], 1)}, status: {status[i]} -")

plt.subplot(1,1,1)
plt.grid(True, which='both')
plt.axhline(y=0, color='k')
plt.axvline(x=0, color='k') 
plt.title(f"switch")
plt.tight_layout()
plt.xlim([0,200])
plt.ylim([-50,250]) 
plt.xlabel(r"$t$")
plt.ylabel(r"$y$")
plt.plot(t,posicion, "g")



plt.show()


