##Biblioteca Main 

from Grafo import *
import random
import graphviz

# Grafo malla
def grafoMalla(m, n, dirigido=False):
   
    print("Generando grafo de malla con ")

    if m <= 1:
        m = 2
    if n <= 1:
        n = 2

    nuevo_grafo = Grafo(dirigido=dirigido)

    # Generamos nodos
    for i in range(m):
        for j in range(n):
            nuevo_grafo.agregarNodo(str(i)+","+str(j))
    
    # Generamos aristas
    for i in range(m):
        for j in range(n):
            if ( i + 1 < m): 
                nuevo_grafo.agregarArista(i*n + j, (i+1)*n + j)
            if ( j + 1 < n):
                nuevo_grafo.agregarArista(i*n + j, i*n + j+1)
    return nuevo_grafo


# Grafo Erdos-Renyi
def grafoErdosRenyi(n, m, dirigido=False, auto=False):
   
    if n <= 0:
        n = 1
    if m < n-1:
        m = n-1

    nuevo_grafo = Grafo(dirigido=dirigido)
    for i in range(n):
        nuevo_grafo.agregarNodo(i)

    print(m)
    m = min(m,((n*(n-1) if dirigido else n*(n-1)/2) - (n if not auto else 0) ) + n)
    print(m)
    
    while len(nuevo_grafo.aristas) < m :
        i = random.randint(0,n-1)
        j = random.randint(0,n-1)
        if (auto or i != j):

            existe = False
            for a in nuevo_grafo.aristas.values():
                if (a.nodo1.id == i and a.nodo2.id == j):
                    existe = True

                if not dirigido and a.nodo1.id == j and a.nodo2.id == i:
                    existe = True
            if existe:
                continue
            
            # Agregamos nodo
            nuevo_grafo.agregarArista(i,j)
    return nuevo_grafo

# Grafo Gilbert
def grafoGilbert(n, p, dirigido=False, auto=False):
   
    if n <= 0:
        n = 1
    if 0 > p and p < 1:
        p = 0.5 # Valor por defecto en caso de que se proporcione valor erroneo
    
    nuevo_grafo = Grafo(dirigido=dirigido)
    for i in range(n):
        nuevo_grafo.agregarNodo(i)
    for i in range(n):
        for j in range(n):
            #if (not auto and i != j) or auto:
            if (auto or i != j):
                if not dirigido:
                    existe = False
                    for a in nuevo_grafo.aristas.values():
                        if (a.nodo1.id == i and a.nodo2.id == j) or \
                            (a.nodo1.id == j and a.nodo2.id == i):
                            existe = True
                            break
                    if existe:
                        continue

                if random.random() < p:
                    nuevo_grafo.agregarArista(i,j)
                

    return nuevo_grafo

# Grafo Geografico Simple
def grafoGeograficoSimple(n, r, dirigido=False, auto=False):
  
    if n <= 0:
        n = 1
    if 0 > r and r < 1:
        r = 0.2

    nuevo_grafo = Grafo(dirigido=dirigido)
    # Creamos puntos en un cuadro de 1x1
    for i in range(n):
        nuevo_grafo.agregarNodo([random.random(), random.random()])
    for i in range(n):
        for j in range(n):
            # Si la distancia es menor
            
            if auto and i == j:
                nuevo_grafo.agregarArista(i,j)
            elif i != j:
                # Verificar que no exista si es no dirigido
                if not dirigido:
                    existe = False
                    for a in nuevo_grafo.aristas.values():
                        if (a.nodo1.id == i and a.nodo2.id == j) or \
                            (a.nodo1.id == j and a.nodo2.id == i):
                            existe = True
                            break
                    if existe:
                        continue
                # Verificar si la distancia es 
                if (nuevo_grafo.nodos[i].data[0]-nuevo_grafo.nodos[j].data[0]) ** 2 + \
                    (nuevo_grafo.nodos[i].data[1]-nuevo_grafo.nodos[j].data[1]) ** 2 < r*r:
                    nuevo_grafo.agregarArista(i,j)


    return nuevo_grafo

# Grafo Barabasi-Albert
def grafoBarabasiAlbert(n, d, dirigido=False, auto=False):
  
    if n <= 0:
        n = 1
    if d <= 1:
        d = 2

    nuevo_grafo = Grafo(dirigido=dirigido)
    for i in range(n):
        nuevo_grafo.agregarNodo(i)

        # Conectar nodo

        # Revisamos por cada nodo el número de aristas
        for j in range(len(nuevo_grafo.nodos)):
            if auto or i != j:

                # Verificar que no exista si es no dirigido
                if not dirigido:
                    existe = False
                    for a in nuevo_grafo.aristas.values():
                        if (a.nodo1.id == i and a.nodo2.id == j) or \
                            (a.nodo1.id == j and a.nodo2.id == i):
                            existe = True
                            break
                    if existe:
                        continue

                conectadas = len([x for x in nuevo_grafo.aristas.values() if x.nodo1.id == j or x.nodo2.id == j])
                p = (d - conectadas) / d
                if p > random.random():
                    nuevo_grafo.agregarArista(i,j)

    return nuevo_grafo
# Grafo Dorogovtsev-Mendes
def grafoDorogovtsevMendes(n, dirigido=False):
   
    if n < 3:
        n = 3

    nuevo_grafo = Grafo(dirigido=dirigido)
    # Agregamos el primer triangulo
    for i in range(3):
        nuevo_grafo.agregarNodo(i)
    nuevo_grafo.agregarArista(0,1)
    nuevo_grafo.agregarArista(1,2)
    nuevo_grafo.agregarArista(2,0)

    # Agregamos el resto de nodos

    for i in range(3,n):
        nuevo_grafo.agregarNodo(i)
        arista = nuevo_grafo.aristas[random.randint(0, len(nuevo_grafo.aristas)-1)]

        nuevo_grafo.agregarArista(i, arista.nodo1.id)
        nuevo_grafo.agregarArista(i, arista.nodo2.id)

    return nuevo_grafo

#funcion para generar png
def generarPng( archivo, nombre_archivo_salida):
    dot = None
    with open(archivo) as f:
        dot = f.read()

    s = graphviz.Source(dot, filename=nombre_archivo_salida, format='png')
    s.view()
#esta es la parte que se cambia apra poder generar los demas grafos
g = grafoMalla(10,3, False)
g.guardar("g.dot", shape="circle", layout="fdp")

#manda a llamar a la funcion para generar el png
generarPng("g.dot", "g")


#sustituye las 2 lineas para generar el grafo deseado 

# g = grafoMalla(5,3, True)
# g.guardar("g.dot")

# g = grafoErdosRenyi(100,2000, False, False)
# g.guardar("g.dot")

# g = grafoGilbert(20, 0.2, dirigido=True, auto=False)
# g.guardar("g.dot")

# g = grafoGeograficoSimple(200, 0.2, dirigido=True, auto=False)
# g.guardar("g.dot")

# g = grafoBarabasiAlbert(100, 4, False, False)
# g.guardar("g.dot")

# g6 = grafoDorogovtsevMendes(100, False)
# g6.guardar("g6.dot")
