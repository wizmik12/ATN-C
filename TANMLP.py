# -*- coding: utf-8 -*-

from sympy import *
from itertools import *

#-----------------------------HEXADECIMAL Y DECIMAL--------------------------------------
def elemento(hexastring,i):
    
    if i<len(hexastring):
        n=(hexastring[i])

        if n=='1' or n=='2' or n=='3' or n=='4' or n=='5' or n=='6' or n=='7' or n=='8' or n=='9' or n=='0':
            return n
        elif n=='a':
            return 10
        elif n=='b':
            return 11
        elif n=='c':
            return 12
        elif n=='d':
            return 13
        elif n=='e':
            return 14
        elif n=='f':
            return 15
        
        
    else: print 'Elige una posición válida del string'
    
def hextodec_it(hexastring):
    n=0
    for i in range(0,len(hexastring)):
        n=n+int(elemento(hexastring,i))*(16**(len(hexastring)-i-1))
       
    return n
    
def hexadec(n):
        if n==1 or n==2 or n==3 or n==4 or n==5 or n==6 or n==7 or n==8 or n==9 or n==0:
            return str(n)
        elif n==10:
            return 'a'
        elif n==11:
            return 'b'
        elif n==12:
            return 'c'
        elif n==13:
            return 'd'
        elif n==14:
            return 'e'
        elif n==15:
            return 'f'
        
def dectohex(entero):
    i=1
    hexa1=''
    while entero/16>0:
            hexa=hexadec(entero%16) 
            entero=entero/16
            i=i+1
            hexa1=hexa+hexa1
    hexa1=hexadec(entero)+hexa1         
    return hexa1

    
def lista_palabras(mensaje):
    j=0
    lista=[]
    
    for i in range(0,len(mensaje)):
        if mensaje[i]==' ':
            lista=lista+[str(mensaje[j:i])]
            j=i+1
        if i==len(mensaje)-1:
            lista=lista+[str(mensaje[j:i+1])]
    return lista
    
def str_to_hexalist(mensaje):
    lista=lista_palabras(mensaje)
    for i in range(0,len(lista)):
        lista[i]=lista[i].encode('hex')
        
    return lista
    
def hexalist_to_str(lista):
    mensaje=''
    for i in range(0,len(lista)):
        if i==len(lista)-1:
            mensaje=mensaje+lista[i].decode('hex')
        else:
            mensaje=mensaje+lista[i].decode('hex')+' '
        
        
    return mensaje
    
def hexalist_to_dec(lista):
    for i in range(0,len(lista)):
        lista[i]=hextodec_it(lista[i])
    return lista
    
def declist_to_hex(lista):
    for i in range(0,len(lista)):
        lista[i]=dectohex(int(lista[i]))
    return lista

#--------------------------------CRIPTOGRAFÍA--------------------------------------------
#Para codificar afín
def cod_afin(mensaje,a,b,n):
    hexalista=str_to_hexalist(mensaje)
    declista=hexalist_to_dec(hexalista)
    for i in range(0,len(declista)):
        declista[i]=((declista[i]*a)+b)%n
    return declista

#Para decodificar afín
def deco_afin(declista,a,b,n):
    a_inv=gcdex(a%n,n)[0]
    for i in range(0,len(declista)):
        declista[i]=((declista[i]-b)*a_inv)%n
    hexlista=declist_to_hex(declista)
    mensaje=hexalist_to_str(hexlista)
    return mensaje

#Para codificar RSA
def cod_rsa(mensaje,e,n):
    hexalista=str_to_hexalist(mensaje)
    declista=hexalist_to_dec(hexalista)
    for i in range(0,len(declista)):
        declista[i]=pow(declista[i],e,n)
    return declista

#Para decodificar RSA
def deco_rsa(declista,e,p,q):
    n=p*q
    phi=(p-1)*(q-1)
    u=gcdex(e,phi)[0]
    u=u%phi
    for i in range(0,len(declista)):
        declista[i]=pow(declista[i],int(u),n)
    hexlista=declist_to_hex(declista)
    mensaje=hexalist_to_str(hexlista)
    return mensaje

#---------------------------------FACTOR BASE---------------------------------------------

def baseprim(b):
    #Hacemos una lista con el -1 y los primeros 'b' primos
    base=[-1]
    for i in range(1,b+1):
        base.append(prime(i))
    return base

def abmod(x,n):
    #Definimos x1 como el resto de x dividido por n
    x1=x%n
    #Comprobamos si x1 es menor o igual que (n/2)
    if x1<=(n/2):
        #Si cumple la condición devolvemos x1
        return x1
    else:
        #Si no la cumple devolvemos x1-n
        return x1-n
        

def mayorpot(p,m):
    #Comprobamos si p es -1
    if p==-1:
        if m<0:
            return 1
        else:
            return 0
    #Quitamos casos triviales
    if p==0:
        return "Es una trivialidad preguntarse cual es la mayor potencia de 0 que divide a m"
    if p==1:
        return 1
    #Comprobamos si p divide a m
    if m%p!=0:
        return 0
    #Si p divide a m usamos de variable auxiliar a, con la cual iremos haciendo las potencias de p
    #Y comprobar hasta que potencia se divide a m, usamos i como variable auxiliar para ver el exponente de la potencia
    else:
        i=1
        a=p
        while m%(a*p)==0:
            i=i+1
            a=a*p
        #Devuelve el exponente de la mayor potencia que divide a m
        return i

def bnumer(b,base,n):
    #Hacemos la b^2 mod n con nuestra función abmod
    #Llamamos b1 a ese número
    b1=abmod(b**2,n)
    #Hacemos la mayor potencia de los primos que divida a este número
    #Y los vamos multiplicando en la variable prod
    prod=1
    for i in range(0,len(base)):
        #Llamamos x a la mayor potencia
        x=base[i]**mayorpot(base[i],b1)
        prod=prod*x
    #Comprobamos si el producto es el número b
    if prod==b1:
        return true
    else:
        return false
    

def vec_alfa(b,base,n):
    #Comprueba si b es un b-numero
    if bnumer(b,base,n)==false:
        return
    else:
        #Definimos el vector alfa como los exponentes asociados al bnumero en la base
        vecalfa=[]
        #Definimos b1 como b^2 mod n con nuestra función abmod
        b1=b1=abmod(b**2,n)
        for i in range(0,len(base)):
            vecalfa=vecalfa+[mayorpot(base[i],b1)]
        return vecalfa

def parp(lista):
    #Devolvemos true si todos los elementos de la lista son pares, en otro caso false.
    for i in range(0,len(lista)):
        if lista[i]%2!=0:
            return false
    return true

def ssuma(lista1,lista2):
    #Sumamos elemento a elemento dos listas
    if len(lista1)!=len(lista2):
        print 'No tienen la misma dimensión las dos listas'
        return
    #Definimos la lista en la que vamos a sumar estas dos
    listsuma=[]
    for i in range(0,len(lista1)):
        listsuma=listsuma+[lista1[i]+lista2[i]]
    return listsuma

def aux(k,r):
    #Lista con el número total de elementos r
    lista=range(0,r)
    #Lista de listas con las posibles combinaciones de elementos de lista tomados de k en k
    aux=list(combinations(lista, k))
    return aux

def ssuman(lista):
    #Sumar n listas, que son los elementos de una lista.
    suma=lista[0]
    for i in range(1,len(lista)):
        suma=ssuma(suma,lista[i])
    return suma
        

def suma(lista,k):
    r=len(lista)
    #lista es una lista de listas
    #comprobamos que la longitud de la lista sea mayor que k
    if len(lista)<=k:
        return
    #definimos la salida de la función que es una lista con todas las ssumas de k en k
    aux1=aux(k,r)
    m=factorial(r)/(factorial(k)*factorial(r-k))
    lista1=[[]]

    for i in range(0,m):
        if i>0:
            lista1.append([])
        for j in aux1[i]:
            if j==aux1[i][0]:
                lista1[i]=lista1[i]+lista[j]
            elif j==aux1[i][1]:
                lista1[i]=[lista1[i]]+[lista[j]]
            else:
                lista1[i]=lista1[i]+[lista[j]]
    lista2=[]
    for i in range(0,m):
        lista2.append(ssuman(lista1[i]))
    return lista2
            
    
def bi(n,k,i,base):
    #Definimos la lista L1
    L1=[]
    for l in range(1,k+1):
        L1=L1+[floor(sqrt(l*n))]
    #Definimos la lista L2
    L2=[]
    for l in range(0,len(L1)):
        for j in range(0,i):
            L2=L2+[L1[l]+j]
    #Seleccionamos aquellos números de L2 que sean B-números
    BN=[]
    for l in range(0,len(L2)):
        if bnumer(L2[l],base,n)==true:
            BN=BN+[L2[l]]
    return BN

#También devolvemos True o False para saber si hemos podido resolver la ecuación
def soleq(n,h,k,i):
    #Definimos n1 y bp como los valores de n y h
    n1=n
    bp=h
    #Definimos la base con los primeros primos
    B=baseprim(bp)
    #NOs quedamos con los B-números
    BN=bi(n1,k,i,B)
    #Construimos la lista de los alfa vectores asociados a estos B-números
    alfavec=[]
    for i in range(0,len(BN)):
        alfavec.append(vec_alfa(BN[i],B,n1))
    #Elegimos como j el número de alfa vectores que queremos sumar lo empezamos en 1 y lo podemos ir
    #subiendo hasta que consigamos una solución no trivial
    #j tiene que ser 1 o mayor
    #Cuando j es 1 vamos a mirar si hay alfavectores pares y luego comprobaremos uno a uno si dan soluciones
    #Cuando j es mayor que 1 iremos comprobando 1 a 1 si dan solución.
    #Usamos i_0 como contador para saber por qué valor de j vamos comprobando
    #Usamos i_1 como contador para saber dentro de cada valor de j, por qué combinación de alfavectores pares vamos
    i_0=1 
    i_1=0
    for j in range(i_0,len(alfavec)):
        sumajpar=[]
        in_a=[]
        if j==1:
            for i in range(0,len(alfavec)):
                if parp(alfavec[i])==true:
                    #Si encontramos un alfavector par, lo guardamos éste y su posición
                    sumajpar.append(alfavec[i])
                    in_a.append(i)
            #Comprobamos con cada alfavector par
            for l in range(0,len(in_a)):
                eles_a=in_a
                
                #Calculamos t
                t=1
                t=(t*BN[eles_a[l]])%n
                p=[]
                e=[]
                for i in range (0,len(sumajpar)):
                    if sumajpar[l][i]!=0:
                        p.append(B[i])
                        e.append(sumajpar[l][i]/2)
                #Calculamos s
                s=1
                for i in range(0,len(p)):
                    s=(s*pow(p[i],e[i],n))%n
        #Comprobamos que sea una solución no trivial
                if gcd(s+t,n)!=1:
                    return[true,(t,s)]
        #Entramos en este if si no hay ningun alfavector par y tenemos que probar con sumas (j mayor que 1)
        if sumajpar==[]:
            in_a=0
            while sumajpar==[]:
                i_1=0
                j=j+1
                #Ponemos una condición de parada que es que j llegue a 15, 
                #o si el j es mayor que la longitud de alfavec, no podemos hacer las sumas
                if j>=len(alfavec) or j==15:
                    return [false,"No hemos resuelto la ecuación"]
                #Lista con todas las sumas de j en j de alfavectores
                sumaj=suma(alfavec,j)
                for i in range(i_1,len(sumaj)):
                    #Comprobamos una a una si la suma de alfavectores es par
                     if parp(sumaj[i])==true:
                        #Si es par procedemos a comprobar si da solución
                        sumajpar=sumaj[i]
                        in_a=i
                        i_0=j
                        i_1=i   
    #Vemos cual es la combinación que se ha sumado para obtener el par
                        eles_a =aux(j,len(BN))
                        #Calculamos t 
                        t=1
                        for i in range(0,len(eles_a[in_a])):
                            t=(t*BN[eles_a[in_a][i]])%n
                        p=[]
                        e=[]
                        for i in range (0,len(sumajpar)):
                            if sumajpar[i]!=0:
                                p.append(B[i])
                                e.append(sumajpar[i]/2)
                        #Calculamos s
                        s=1
                        for i in range(0,len(p)):
                            s=(s*pow(int(p[i]),int(e[i]),int(n)))%n
        #Comprobamos que sea una solución no trivial
                        if gcd(s+t,n)!=1 and gcd(s-t,n)!=1:
                            return[true,(t,s)]
    return [false]

def fac(n,h):
    n1=n
    h1=h
    i=5
    k=5
    factorizacion=true
    sol=soleq(n1,h1,k,i)
    if sol[0]==true:
        s=sol[1][0]
        t=sol[1][1]
    else:
        while sol[0]==false:
            k=k+5
            i=i+5
            sol=soleq(n1,h1,k,i)
            if sol[0]==true:
                s=sol[1][0]
                t=sol[1][1]
            if i==100:
                factorizacion=false
                break
    if factorizacion==false:
        print 'Peligro de bucle infinito, elige otro h'
    else: 
        return (gcd(s+t,n),n/gcd(s+t,n))

#Esta función asignará la base según los Pbs
def elecbase(Pbs):
#Lista de los Pbs
    Pbs1=Pbs
#Ceamos una lista donde guardar la factorización de todos los b números
    factorb=[]
#Inicializamos nuestra lista B
    B=[-1]
#Lista que usaremos de apoyo para construir la B, guardaremos en ella los números que no se repitan
#en las factorizaciones, junto al número de los Pbs del cual es factor.
    Baux=[]
#Guardamos las factorizaciones de los números en factorb, junto a la posición del número
#al cual corresponde la factorización en Pbs
    for i in range(0,len(Pbs1)):
        factorb.append([list(factorint(Pbs1[i])),i])
    
#Bucles anidados en los cuales compararemos los factores de los números de Pbs para guardar directamente
#en B los que se repitan dos o más veces y los que salga sólo una vez los guardaremos en Baux
#Para comprobar a continuación si tienen exponente par en la factorización del número del cual es factor
#usamos a como variable booleana para comprobar que no metemos dos veces el mismo valor en B
#b también será una variable booleana y esta llevará os indicará cuando un número sólo sale una vez

    for i in range(0,len(factorb)):
        for j in range(0,len(factorb[i][0])):
            b=false
            for k in range(i+1,len(factorb)):
                for l in range(0,len(factorb[k][0])):
                    a=false
                    if factorb[i][0][j]==factorb[k][0][l]:
                        b=true
                        for m in range(0,len(B)):
                            if(factorb[i][0][j]==B[m]):
                                a=true
                        if a==false:
                             B.append(factorb[i][0][j])
            
            for m in range(0,len(B)):
                if(factorb[i][0][j]==B[m]):
                    b=true
            if b==false:
                Baux.append([factorb[i][0][j],i])

#Comprobamos si tienen exponente par los almacenados en Baux para añadirlos a B             
    for i in range(0,len(Baux)):
        if mayorpot(Baux[i][0],Pbs1[Baux[i][1]])%2==0:
            B.append(Baux[i][0])
    
    return B
    

#Función para ordenar una lista
def orden1(list):
    for i in range(1,len(list)):
        for j in range(0,len(list)-1):
            if(list[j] > list[j+1]):
                k = list[j+1]
                list[j+1] = list[j]
                list[j] = k;
    return list

def soleqfc(n,s):
    #Definimos n1 y bp como los valores de n y h
    n1=n
    F = continued_fraction_periodic(0,1,n)
    L1= [F[0]]+F[1]
    if s<=len(L1):
        L2=list(continued_fraction_convergents(L1[:s]))
    elif s>len(L1):
        return [false,"No se ha podido factorizar el numero con este s, tienes que elegir un s mas pequeño"]

    Pbs=[]
    for i in range(0,len(L2)):
        Pbs.append(fraction(L2[i])[0])
    B=elecbase(Pbs)
    B=orden1(B)
    #Elegimos el k y el i y ponemos una condición para terminar el programa
    sol=false
    k1=0
    i1=0
    while sol==false:
        #En cada iteración vamos aumentando los valores de k y de i
        k1=k1+10
        i1=i1+10
        #Nos quedamos con los B-números
        BN=bi(n1,k1,i1,B)
        #Construimos la lista de los alfa vectores asociados a estos B-números
        alfavec=[]
        for i in range(0,len(BN)):
            alfavec.append(vec_alfa(BN[i],B,n1))
        #Hacemos un algoritmo análogo al de la función soleq
        i_0=1 
        i_1=0
        for j in range(i_0,len(alfavec)):
            sumajpar=[]
            in_a=[]
            if j==1:
                #Comprobamos si hay alfavectores pares
                for i in range(0,len(alfavec)):
                    if parp(alfavec[i])==true:
                        sumajpar.append(alfavec[i])
                        in_a.append(i)
                #Comprobamos si los alfavectores pares dan solución 
                for l in range(0,len(in_a)):
                    eles_a=in_a
                    #Calculamos t
                    t=1
                    t=(t*BN[eles_a[l]])%n
                    p=[]
                    e=[]
                    for i in range (0,len(sumajpar)):
                        if sumajpar[l][i]!=0:
                            p.append(B[i])
                            e.append(sumajpar[l][i]/2)
                    #Calculamos s
                    s=1
                    for i in range(0,len(p)):
                        s=(s*pow(p[i],e[i],n))%n
        #Comprobamos que sea una solución no trivial
                    if gcd(s+t,n)!=1:
                        return[true,(t,s)]
            #Comprobamos si hay sumas pares de alfavectores
            if sumajpar==[]:
                in_a=0
                while sumajpar==[]:
                    i_1=0
                    j=j+1
                    if j>=len(alfavec) or j==15:
                        break
                    #Condición para no hacer un bucle infinito
                    elif k==100:
                        return [false]
                    sumaj=suma(alfavec,j)
                    for i in range(i_1,len(sumaj)):
                        if parp(sumaj[i])==true:
                            sumajpar=sumaj[i]
                            in_a=i
                            i_0=j
                            i_1=i   
                        #Vemos que combinación da lugar al vector par
                            eles_a =aux(j,len(BN))
                        #calculamos t
                            t=1
                            for i in range(0,len(eles_a[in_a])):
                                t=(t*BN[eles_a[in_a][i]])%n
                            p=[]
                            e=[]
                            for i in range (0,len(sumajpar)):
                                if sumajpar[i]!=0:
                                    p.append(B[i])
                                    e.append(sumajpar[i]/2)
                            #Calculamos s
                            s=1
                            for i in range(0,len(p)):
                                s=(s*pow(int(p[i]),int(e[i]),int(n)))%n
        #Comprobamos que sea una solución no trivial
                            if gcd(s+t,n)!=1 and gcd(s-t,n)!=1:
                                return[true,(t,s)]
    return [false]

def facfc(n):
    n1=n
    #Damos un valor de s y un valor máximo de s por defecto, se podrá modificar según el problema al que nos enfrentemos
    s=6
    #Comprobamos si conseguimos factorizar el número para el s dado
    sol=soleqfc(n1,s)
    print sol
    if sol[0]==true:
        q=sol[1][0]
        t=sol[1][1]
    else:
        while sol[0]==false:
        #Vamos ejecutando el método para cada valor de s hasta conseguir solución
            sol=soleqfc(n1,s)
            if sol[0]==true:
                q=sol[1][0]
                t=sol[1][1]
            #Aumentamos el número s
            s=s+3
            #Condición sobre un s máximo para no hacer un bucle infinito
            if s>45:
                return "No hemos podido factorizar el numero"
    #Devolvemos la factorización
    return (gcd(q+t,n),n/gcd(q+t,n))


    
#-------------------------FACTORIZACIÓN EN DOMINIOS EUCLÍDEOS (d negativo)-----------------------------
def norma(alpha):
    #Función para calcular la norma de un elemento alpha
    norma=simplify(alpha*alpha.conjugate())
    return norma

def traza(alpha):
    #Función para calcular la traza de un elemento alpha
    traza=simplify(alpha+alpha.conjugate())
    return traza

def es_entero(alpha):
    #Comprobamos si el elemento alpha es entero algebraico o no
    norm=norma(alpha)
    traz=traza(alpha)
    #Comprobamos si la norma y la traza son enteras 
    if ask(Q.integer(traz))and ask(Q.integer(norm)):
        return true
    else:
        return false

def xy(alpha,d):
    #Extraemos las coordenadas de alpha en Q(sqrt(d))
    x=(alpha+alpha.conjugate())/2
    y=(alpha-alpha.conjugate())/(2*sqrt(d))
    return(x,y)

def ab(alpha,d):
    #Comprobamos si alpha es entero, si lo es calculamos sus coordenadas en una base entera
    if es_entero(alpha)==true:
        if d==-1 or d==-2:
            e=sqrt(d)
            a=(alpha+alpha.conjugate())/2
            b=(alpha-alpha.conjugate())/(2*sqrt(d))
        elif d==-3 or d==-7 or d==-11:
            e=Rational(1,2)+sqrt(d)*Rational(1,2)
            coord=xy(alpha,d)
            x_1=coord[0]*2
            y_1=coord[1]*2
            a=(x_1-y_1)/2
            b=y_1
        else:
            return "Introduzca un dominio euclideo"
        return(a,b)
    else:
        return"Introduzca un entero algebraico"

def divide(alpha,beta,d):
    #Comprobamos si alpha divide a beta, para ello vemos multiplicando por el conjugado si la fracción es un entero
    num=expand(simplify(beta*alpha.conjugate()))
    norm=norma(alpha)
    coord=xy(num,d)
    division=Rational(coord[0],norm)+Rational(coord[1],norm)*sqrt(d)
    return es_entero(division)

def cociente(alpha,beta,d):
    #Si alpha divide a beta calculamos su cociente
    if divide(alpha,beta,d)!=true:
        return false
    division=simplify(beta*alpha.conjugate())/norma(alpha)
    return division

def eqpell(n,d):
    #Resolución de la ecuación de Pell con d negativo
    sol=[]
    if d>=0:
        return "Introduce un d negativo"
    ymax=sqrt(n/-d)
    for y in range(0,ymax+1):
        x=n+d*(y**2)
        x=sqrt(x)
        if ask(Q.integer(x)):
            if y==0:
                sol.append((x,y))
                sol.append((-x,y))
            elif x==0:
                sol.append((x,y))
                sol.append((x,-y))
            else:
                sol.append((x,y))
                sol.append((-x,y))
                sol.append((x,-y))
                sol.append((-x,-y))
    return sol

def connorma(n,d):
    #Calculamos los elementos con norma n en O
    elementos=[]
    if d%4!=1:
        sol=eqpell(n,d)
        for i in range (0,len(sol)):
            a=sol[i][0]+sol[i][1]*sqrt(d)
            elementos.append(a)
        return elementos
    else:
        sol=eqpell(4*n,d)
        for i in range (0,len(sol)):
            x=sol[i][0]
            y=sol[i][1]
            if((x-y)%2==0):
                a=Rational(x,2)+Rational(y,2)*sqrt(d)
                elementos.append(a)
        return elementos

def es_unidad(alpha):
    #Comprobamos si alpha es unidad
    if es_entero(alpha)==false:
        print "No es entero algebraico alpha"
        return false
    if norma(alpha)==1:
        return true
    else:
        return false

def es_irreducible(alpha,d):
    #Comprobamos si alpha es irreducible en O
    if es_entero(alpha)==false:
        print "No es entero algebraico alpha"
        return false
    norm_alpha=norma(alpha)
    if isprime(norm_alpha)==true:
        return true
    elif isprime(sqrt(norm_alpha)):
        if connorma(sqrt(norm_alpha),d)==[]:
            return true
        else:
            return false
    else:
        return false

def contador(lista):
    #Función que su input es una lista y su output otra lista
    #La lista de salido son duplas con cada elemento de la lista de entrada acompañado con las veces que se repite en la lista de entrada
    aux=[]
    for i in range(0,len(lista)):
        bool1=false
        for j in range(0,len(aux)):
            if lista[i]==aux[j][0]:
                bool1=true
        if bool1==false:
            count=0
            for k in range(0,len(lista)):
                if lista[i]==lista[k]:
                    count=count+1
            aux.append((lista[i],count))
    return aux

def factoriza(alpha,d):
    #Función para factorizar alpha en un dominio euclídeo
    if d!=-1 and d!=-2 and d!=-3 and d!=-7 and d!=-11:
        print "Introduce un dominio euclídeo donde pueda factorizar"
        return false
    if es_irreducible(alpha,d):
        print "Es irreducible"
        return false     
    #Calculamos la norma de n y la lista con los factores de la norma
    norm=norma(alpha)
    fact=list(factorint(norm))
    factores=[]
    #Por cada factor de la norma de alpha vemos si algún elemento de esa norma divide a alpha
    for i in range(0,len(fact)):
        L1=connorma(fact[i],d)
        bool1=false
        for j in range(0,len(L1)):
            while(divide(L1[j],alpha,d))==true:
                #Añadimos el elemento a la lista de factores si divide a alpha
                factores.append(L1[j])
                alpha=cociente(L1[j],alpha,d)
                bool1=true
                #Cuando nos quede una unidad paramos de iterar
                if es_unidad(alpha):
                    factores.append(alpha)
                    break
        if bool1==false:
            #Esta condición es por si no hay irreducibles de norma p, buscarlos de p^2
            L1=connorma(fact[i]**2,d)
            for j in range(0,len(L1)):
                while(divide(L1[j],alpha,d))==true:
                    #Añadimos el elemento a la lista de factores si divide a alpha
                    factores.append(L1[j])
                    alpha=cociente(L1[j],alpha,d)
                    #Cuando tengamos una unidad paramos de iterar
                    if es_unidad(alpha):
                        factores.append(alpha)
                        break
    factores=contador(factores)
    return factores


#-------------------------FACTORIZACIÓN EN DOMINIOS EUCLÍDEOS II(d negativo y positivo)--------------------------

def xy2(alpha,d):
    #Calculamos las coordenadas racionales de alpha
    if d!=0:
        alpha2=simplify(alpha)
        x=alpha2.coeff(sqrt(d),0)
        y=alpha2.coeff(sqrt(d),1)
        return (x,y)
    else:
        print "Mete un d distinto de cero"
        return false

def norma2(alpha,d):
    #Calculamos la norma de alpha sea cual sea el d
    if d!=0:
        coord=xy2(alpha,d)
        conj=coord[0]-coord[1]*sqrt(d)
        norma=expand(simplify(alpha*conj))
        return norma
    else:
        print "Mete un d distinto de cero"
        return false    

def traza2(alpha,d):
    #Calculamos la traza de alpha sea cual sea el d
    if d!=0:
        coord=xy2(alpha,d)
        conj=expand(simplify(coord[0]-coord[1]*sqrt(d)))
        traza=expand(simplify(alpha+conj))
        return traza
    else:
        print "Mete un d distinto de cero"
        return false 

def es_entero2(alpha,d):
    #Comprobamos si el elemento alpha es entero algebraico o no
    norm=norma2(alpha,d)
    traz=traza2(alpha,d)
    #Comprobamos si la norma y la traza son enteras 
    return ask(Q.integer(traz))and ask(Q.integer(norm))

def ab2(alpha,d):
    #Si alpha es entero, calculamos sus coordenadas enteras
    if es_entero2(alpha,d)==true:
        if d<0:
            if d%4!=1:
                e=sqrt(d)
                a=(alpha+alpha.conjugate())/2
                b=(alpha-alpha.conjugate())/(2*sqrt(d))
            else:
                e=Rational(1,2)+sqrt(d)*Rational(1,2)
                coord=xy2(alpha,d)
                x_1=coord[0]*2
                y_1=coord[1]*2
                a=(x_1-y_1)/2
                b=y_1
            return[int(a),int(b)]
        elif d>0:
            if d%4==1:
                e=Rational(1,2)+sqrt(d)*Rational(1,2)
                coord=xy2(alpha,d)
                x_1=coord[0]*2
                y_1=coord[1]*2
                a=(x_1-y_1)/2
                b=y_1
                
            else:
                e=sqrt(d)
                coord=xy2(alpha,d)
                conj=coord[0]-coord[1]*sqrt(d)
                a=(alpha+conj)/2
                b=(alpha-conj)/(2*sqrt(d))
            return[int(a),int(b)]
        else:
            print "Introduce un d distinto de 0"
            return false
    else:
        return "Introduzca un entero algebraico"

def divide2(alpha,beta,d):
    #Comprobamos si alpha divide a beta, para ello vemos multiplicando por el conjugado si la fracción es un entero
    coord_alpha=xy2(alpha,d)
    conj=coord_alpha[0]-coord_alpha[1]*sqrt(d)
    num=expand(simplify(beta*conj))
    norm=norma2(alpha,d)
    coord_num=xy2(num,d)
    division=Rational(coord_num[0],norm)+Rational(coord_num[1],norm)*sqrt(d)
    return es_entero2(division,d)

def cociente2(alpha,beta,d):
    #Si alpha divide a beta calculamos su cociente
    if divide2(alpha,beta,d)!=true:
        return false
    coord_alpha=xy2(alpha,d)
    conj=coord_alpha[0]-coord_alpha[1]*sqrt(d)
    division=expand(simplify((beta*conj)/norma2(alpha,d)))
    return division

def es_unidad2(alpha,d):
    #Vemos si alpha es una unidad
    return abs(norma2(alpha,d))==1

def libre_de_cuadrados(d):
    #Vemos si d es libre de cuadrados, para ello hacemos una lista de sus factores
    #Y vemos si es divisible por alguno de ellos al cuadrado
    d1=abs(d)
    lista=list(factorint(d1))
    for i in range(0,len(lista)):
        if d1%(lista[i]**2)==0:
            return false
    return true

def pell(d):
    #Resolvemos la ecuación de Pell anterior
    if libre_de_cuadrados(d)==false:
        print "introduce un número libre de cuadrados"
        return false
    if d<=1 or type(d)!=int:
        print "Introduce un d entero positivo válido"
        return false
    #Calculamos la fracción continua periódica
    F = continued_fraction_periodic (0,1,d)
    L= [F[0]]+F[1]
    #Quitamos el ultimos elemento
    L.pop()
    #Calculamos la lista de convergentes
    convergentes=list(continued_fraction_convergents(L))
    
    #Damos la solución de la ecuación
    if len(L)%2==0:
        x=fraction(convergentes[len(convergentes)-1])[0]
        y=fraction(convergentes[len(convergentes)-1])[1]
        return (x,y)
    else:
        x=fraction(convergentes[len(convergentes)-1])[0]
        y=fraction(convergentes[len(convergentes)-1])[1]
        u=x+y*sqrt(d)
        u_2=expand(u**2)
        coord_u2=xy2(u_2,d)
        return coord_u2
        
def generalpell(n,d):
    #Resolvemos la ecuación general de Pell
    if libre_de_cuadrados(d)==false:
        print "introduce un número libre de cuadrados"
        return false
        
    if d>1:
        #Resolvemos la ecuación de Pell anterior
        sol_pell=pell(d)
        r=abs(sol_pell[0])
        s=abs(sol_pell[1])
        sol=[]
        if n==1:
            #Si n es 1, añadimos la solución de pell
            (s1,s2)=sol_pell
            if s1==0:
                sol.append((s1,s2))
                sol.append((s1,-s2))
            elif s2==0:
                sol.append((s1,s2))
                sol.append((-s1,s2))
            else:
                sol.append((s1,s2))
                sol.append((-s1,s2))
                sol.append((s1,-s2))
                sol.append((-s1,-s2))
        if n>0:
            #Calculamos la cota
            ymax=sqrt((n*(r-1))/(2*d))
            for y in range(0,ymax+1):
                x=n+d*(y**2)
                x=sqrt(x)
                if ask(Q.integer(x)):
                    if x==0:
                        sol.append((x,y))
                        sol.append((x,-y))
                    elif y==0:
                        sol.append((x,y))
                        sol.append((-x,y))
                    else:
                        sol.append((x,y))
                        sol.append((-x,y))
                        sol.append((x,-y))
                        sol.append((-x,-y))
            return sol
        elif n<0:
            #Calculamos las cotas
            ymin=sqrt(-n/d)
            ymax=sqrt((-n*(r+1))/(2*d))
            for y in range(ymin,ymax+1):
                x=n+d*(y**2)
                x=sqrt(x)
                #Vemos si x es un cuadrado
                if ask(Q.integer(x)):
                    if x==0:
                        sol.append((x,y))
                        sol.append((x,-y))
                    elif y==0:
                        sol.append((x,y))
                        sol.append((-x,y))
                    else:
                        sol.append((x,y))
                        sol.append((-x,y))
                        sol.append((x,-y))
                        sol.append((-x,-y))
            return sol
        else:
            print "Tenemos una ecuación trivial, mete un n válido"
            return false
    else:
        #Si el d es negativo llamamos a la de la práctica anterior
        return eqpell(n,d)

def es_irreducible2(alpha,d):
    #Comprobamos si alpha es irreducible en O, para ello vemos primero si es entero
    if es_entero2(alpha,d)==false:
        print "No es entero algebraico alpha"
        return false
    norm_alpha=abs(norma2(alpha,d))
    #Miramos si la norma en valor absoluto es un primo de Z
    if isprime(norm_alpha)==true:
        return true
    #A continuación comprobamos sí la norma no es un cuadrado perfecto
    elif ask(Q.integer(sqrt(norm_alpha)))==false:
        return false
    #Si es un cuadrado perfecto, vemos si es de la forma un primo al cuadrado
    elif isprime(sqrt(norm_alpha)):
        #Comprobamos si hay elementos con más o menos la norma de la raíz de la norma de alpha que es un primo
        if connorma2(sqrt(norm_alpha),d)==[] and connorma2(-sqrt(norm_alpha),d)==[]:
            return true
        else:
            return false
    else:
        return false

def connorma2(n,d):
    #Calculamos los elementos con norma n en O, para ello reslvemos la ecuación de Pell general
    if libre_de_cuadrados(d)==false:
        print "Mete un d libre de cuadrados"
        return false
    
    if n<0 and d<=0:
        return []
    
    elementos=[]
    if d%4!=1:
        sol=generalpell(n,d)
        for i in range (0,len(sol)):
            a=sol[i][0]+sol[i][1]*sqrt(d)
            elementos.append(a)
        return elementos
    else:
        sol=generalpell(4*n,d)
        for i in range (0,len(sol)):
            x=sol[i][0]
            y=sol[i][1]
            if((x-y)%2==0):
                a=Rational(x,2)+Rational(y,2)*sqrt(d)
                elementos.append(a)
        return elementos

def factoriza2(alpha,d):
    if d==0:
        print "Elige un d distinto de 0"
        return false
    if d<0:
        #Devolvemos un diccionario con los factores de alpha y sus exponentes
        return dict(factoriza(alpha,d))
    else:
        if es_irreducible2(alpha,d):
            print "Es irreducible"
            return false     
        #Calculamos la norma de n y la lista con los factores de la norma
        norm=norma2(alpha,d)
        fact=list(factorint(norm))
        factores=[]
        #Por cada factor de la norma de alpha vemos si algún elemento de esa norma divide a alpha
        for i in range(0,len(fact)):
            L1=connorma2(fact[i],d)
            L1=L1+connorma2(-fact[i],d)
            bool1=false
            for j in range(0,len(L1)):
                while(divide2(L1[j],alpha,d))==true:
                    #Añadimos el elemento a la lista de factores si divide a alpha
                    factores.append(L1[j])
                    alpha=cociente2(L1[j],alpha,d)
                    bool1=true
                    #Cuando nos quede una unidad paramos de iterar
                    if es_unidad2(alpha,d):
                        factores.append(alpha)
                        break
            if bool1==false:
                #Esta condición es por si no hay irreducibles de norma p, buscarlos de p^2
                L1=connorma2(fact[i]**2,d)
                for j in range(0,len(L1)):
                    while(divide2(L1[j],alpha,d))==true:
                        #Añadimos el elemento a la lista de factores si divide a alpha
                        factores.append(L1[j])
                        alpha=cociente2(L1[j],alpha,d)
                        #Cuando tengamos una unidad paramos de iterar
                        if es_unidad2(alpha,d):
                            factores.append(alpha)
                            break
        #Contamos cuantas veces sale cada factor para que aparezca junto a él su exponente
        factores=contador(factores)
        #Convertimos la lista de factores en un diccionario
        return dict(factores)

#------------------------------------------------FACTORIZACIÓN DE IDEALES-----------------------------------

def cero(matriz):
    #Función para una matriz de 2xn, intercambiar columnas de tal manera que en la primera fila
    #los ceros queden al final
    
    #Comprobamos que sea 2xn
    for i in range(len(matriz)):
        if len(matriz[i])!=2:
            print "Mete una matriz de dimensiones válidas"
            return false
    #Esta función lo que hace es recorrer la primera fila de la matriz y en cuanto detecta un cero,
    #La recorre desde atrás hasta detectar el primer lugar donde no hay un cero para intercambiar las columnas
    n=len(matriz)
    for i in range (0,n):
        if matriz[i][0]==0:
            for j in range(n-1,i,-1):
                if matriz[j][0]!=0:
                    aux=matriz[j]
                    matriz[j]=matriz[i]
                    matriz[i]=aux
            
    return matriz

def cero2(lista):
    #Función para desplazar todos los ceros al final
    n=len(lista)
    #Recorre la lista y cuando detecta un 0, la recorre desde atrás hasta ver el primer lugar donde no hay un cero,
    #para intercambiar los elementos
    for i in range (0,n):
        if lista[i]==0:
            for j in range(n-1,i,-1):
                if lista[j]!=0:
                    aux=lista[j]
                    lista[j]=lista[i]
                    lista[i]=aux
            
    return lista

def LR(matriz):
    #Función para "escalonar" una matriz 2xn con elementos en un anillo, devuelvo los elementos no nulos de esa matriz
    
    #Comprobamos que sea 2xn
    for i in range(len(matriz)):
        if len(matriz[i])!=2:
            print "Mete una matriz de dimensiones válidas"
            return false
    #Condición para entrar en el primer bucle
    fin=false
    for i in range(1,len(matriz)):
            if matriz[i][0]!=0:
                fin=true
    #Primera parte: hacemos ceros en la primera fila
    while(fin):
        #Echamos todos los ceros de la primera fila al final
        matriz=cero(matriz)
        #Ponemos la columna que tiene el mínimo de la primera fila en primera posición
        minimo=abs(matriz[0][0])
        min_num=0
        for i in range(0,len(matriz)):
            if abs(matriz[i][0])<minimo and matriz[i][0]!=0:
                minimo=abs(matriz[i][0])
                min_num=i                
        aux=matriz[0]
        matriz[0]=matriz[min_num]
        matriz[min_num]=aux
        #Calculamos el cociente para empezar a restar números y hace ceros
        #cociente=int(matriz[1][0]/matriz[0][0])
        cociente=int(Rational(matriz[1][0],matriz[0][0]))
        #Hacemos las restas para hacer ceros en los lugares que no hay ceros, en ambas filas    
        for i in range(1,len(matriz)):
             if matriz[i][0]!=0:
                matriz[i][1]=matriz[i][1]-matriz[0][1]*cociente
        for i in range(1,len(matriz)):
            if matriz[i][0]!=0:
                matriz[i][0]=matriz[i][0]-matriz[0][0]*cociente
        #Condición para acabar el bucle
        fin=false
        for i in range(1,len(matriz)):
            if matriz[i][0]!=0:
                fin=true
    
    #Nos quedamos con la primera columna
    [a,b]=matriz[0]
    #Nos quedamos con los c's
    matriz2=[]
    for i in range(1,len(matriz)):
        matriz2.append(matriz[i][1])
    #Segunda parte: Hacer ceros en la segunda fila (nos hemos quedado con la segunda fila como si fuera una lista)
    #Condición para entrar al bucle
    fin=false
    for i in range(1,len(matriz2)):
            if matriz2[i]!=0:
                fin=true
    while(fin):
        #Echamos los ceros al final
        matriz2=cero2(matriz2)
        #Ponemos el menor al principio
        minimo=abs(matriz2[0])
        min_num=0
        for i in range(0,len(matriz2)):
            if abs(matriz2[i])<minimo and matriz2[i]!=0:
                minimo=abs(matriz2[i])
                min_num=i
        aux=matriz2[0]
        matriz2[0]=matriz2[min_num]
        matriz2[min_num]=aux
        #Dividimos para ir haciendo ceros
        #cociente=int(matriz2[1]/matriz2[0])
	cociente=int(Rational(matriz2[1],matriz2[0]))
        for i in range(1,len(matriz2)):
             if matriz2[i]!=0:
                matriz2[i]=matriz2[i]-matriz2[0]*cociente
        #Condición para acabar el bucle
        fin=false
        for i in range(1,len(matriz2)):
            if matriz2[i]!=0:
                fin=true
    #Devolvemos el a, b y c
    return [a,b,matriz2[0]]

def es_ideal_entero(I,d):
    #Función que compruebe si los generadores del ideal son enteros
    for i in range(0,len(I)):
        if es_entero2(I[i],d)==false:
            return false
    return true

def Relatores_ideal(I,d):
    #Función para calcular los relatores de un ideal
    #Primero vemos si es entero el ideal
    if es_ideal_entero(I,d)==false:
        print "Introduce un ideal de O: ",I," no lo es"
        return false
    #Seleccionamos la base entera correspondiente
    if d%4==1:
        e=Rational(1,2)+sqrt(d)*Rational(1,2)
    else:
        e=sqrt(d)
    #Hacemos la matriz de relatores
    Relatores=[]
    for i in range(0,len(I)):
        x=I[i]
        Relatores.append(ab2(x,d))
        x=expand(simplify(e*I[i]))
        Relatores.append(ab2(x,d))
    return Relatores

def base_entera(I,d):
    #Con esta función queremos devolver a partir de los generadores de un ideal, una base entera
    #Vemos si el ideal es entero
    if es_ideal_entero(I,d)==false:
        print "Introduce un ideal de O: ",I," no lo es"
        return false
    #Seleccionamos la base entera de O
    if d%4==1:
        e=Rational(1,2)+sqrt(d)*Rational(1,2)
    else:
        e=sqrt(d)
    #Calculamos los relatores, LR y obtenemos la base
    A=Relatores_ideal(I,d)
    A=LR(A)
    a=A[0]
    b=A[1]
    c=A[2]
    return [a+expand(simplify(b*e)),expand(simplify(c*e))]
    

def norma_id(I,d):
    #Función para calcular la norma de un ideal
    Relatores=Relatores_ideal(I,d)
    a=LR(Relatores)
    return abs(a[0]*a[2])

def es_O(I,d):
    #Función para ver si un ideal es el total
    return abs(norma_id(I,d))==1

def pertenece(gamma,I,d):
    #Función para ver si gamma pertenece a I
    Relatores=Relatores_ideal(I,d)
    coord_gamma=ab2(gamma,d)
    a=LR(Relatores)
    #Resolvemos el sistema tras hacerle LR y vemos si la solución es entera
    x_1=Rational(coord_gamma[0],a[0])
    x_2=Rational(coord_gamma[1]-expand(simplify(a[1]*x_1)),a[2])
    return ask(Q.integer(x_1))and ask(Q.integer(x_2))

def divide_id(I,J,d):
    #Función que comprueba si I divide a J
    #Equivalentemente si J está contenido en I
    #Comprobamos si los generadores de J están en I
    divide=true
    for i in range(0,len(J)):
        divide=pertenece(J[i],I,d)
        if divide==false:
            return false  
    return true

def productodos(I,J,d):
    #Hacemos el producto de dos ideales
    I=base_entera(I,d)
    J=base_entera(J,d)
    IJ=[]
    for i in range(0,len(I)):
        for j in range(0,len(J)):
            IJ.append(expand(simplify(I[i]*J[j])))
    return base_entera(IJ,d)

def producto(lista,d):
    #Hacemos el producto de una lista de ideales
    n=len(lista)
    prod=productodos(lista[0],lista[1],d)
    for i in range(2,n):
        prod=productodos(prod,lista[i],d)
    return prod

def divisores(p,d):
    #Calculamos los divisores de un primo p
    #Seleccionamos la base entera de O
    if d%4==1:
        e=Rational(1,2)+sqrt(d)*Rational(1,2)
    else:
        e=sqrt(d)
    #Lista donde guardaremos las raíces del polinomio
    raices=[]
    for i in range(0,p):
        #Evaluamos todas las posibilidades y vemos si es raíz
        evalua=i**2-expand(simplify((traza2(e,d))*i))+norma2(e,d)
        evalua=evalua%p
        #Si es raíz la añadimos a nuestra lista
        if evalua==0:
            raices.append(i)
    #Si es irreducible
    if raices==[]:
        return [[p]]
    #Si es reducible
    else:
        if len(raices)==1:
            return [[p,e-raices[0]]]
        else:
            return [[p,e-raices[0]],[p,e-raices[1]]]

def es_primo_id(I,d):
    #Vemos si un ideal I es primo
    #Si la norma es primo, el ideal es primo
    if isprime(norma_id(I,d))==true:
        return true
    #Si la norma es un primo al cuadrado vemos si el polinomio fp es reducible
    elif isprime(abs(sqrt(norma_id(I,d)))) and ask(Q.integer(sqrt(norma_id(I,d)))):
        if divisores(sqrt(abs(norma_id(I,d))),d)==[[sqrt(abs(norma_id(I,d)))]]:
            return true
        else:
            return false
    else:
        return false

def cociente_id(primo,I,d):
    #El input de esta función es un primo de Z que divida la norma, y dividimos el ideal por el ideal primo asociado a este primo de Z que divida a I
    #Devolvemos un par que consta del cociente y del dividendo de la división
    #Definimos el cociente en blanco
    cociente=[]
    #Buscamos la base entera de nuestro anillo de enteros
    if d%4==1:
        e=Rational(1,2)+sqrt(d)*Rational(1,2)
    else:
        e=sqrt(d)
    #Definimos los posibles divisores de nuestro ideal según este primo
    primo1=divisores(primo,d)
    #Si la longitud del primer término es 1, estamos en el caso que fp es irreducible
    if len(primo1[0])==1:
        p=primo1[0][0]
        #El inverso
        inv=[Rational(1,p),Rational(1,p)*e]
        #Calculamos el cociente
        for i in range(len(I)):
            cociente.append(expand(simplify(I[i]*inv[0])))
            cociente.append(expand(simplify(I[i]*inv[1])))
        #Como el cociente es un ideal calculamos sus generadores
        cociente=base_entera(cociente,d)
        return [cociente,[p]]
    else:
        #Estamos en el caso en el que fp es reducible con 1 sola raíz (doble)
        if len(primo1)==1:
            #Definimos p,a que son los generadores del ideal fraccionario
            p=primo1[0][0]
            a=primo1[0][1]
            #El inverso
            inv=[1,Rational(1,p)*a]
            #Calculamos el cociente
            for i in range(len(I)):
                cociente.append(expand(simplify(I[i]*inv[0])))
                cociente.append(expand(simplify(I[i]*inv[1])))
            #Sacamos los generadores del cociente
            cociente=base_entera(cociente,d)
            return [cociente,[p,a]]
        else:
            #Estamos en el caso en el que fp es reducible y tenemos que ver cual de las 
            #dos posibilidades divide a nuestro ideal
            if divide_id(primo1[0],I,d):
                #Caso en el que divide al ideal el primer elemento
                p=primo1[1][0]
                a=primo1[1][1]
                b=primo1[0][1]
                #El inverso
                inv=[1,Rational(1,p)*a]
                #Calculamos el cociente
                for i in range(len(I)):
                    cociente.append(expand(simplify(I[i]*inv[0])))
                    cociente.append(expand(simplify(I[i]*inv[1])))
                #Sacamos los generadores del cociente
                cociente=base_entera(cociente,d)
                return [cociente,[p,b]]
            else:
                #Estamos en el caso en el que fp tiene dos raíces distintas y la primera opción no dividía al ideal
                p=primo1[0][0]
                a=primo1[0][1]
                b=primo1[1][1]
                #el inverso
                inv=[1,Rational(1,p)*a]
                #calculamos el cociente
                for i in range(len(I)):
                    cociente.append(expand(simplify(I[i]*inv[0])))
                    cociente.append(expand(simplify(I[i]*inv[1])))
                #sacamos los generadores del ideal
                cociente=base_entera(cociente,d)
                return [cociente,[p,b]]

def factoriza_id(I1,d):
    if libre_de_cuadrados(d)!=true:
        print "Introduce un d libre de cuadrados"
        return false
    #Vemos si el ideal es entero
    if es_ideal_entero(I1,d)==false:
        print I1," no es entero"
        return false
    #Vemos si el ideal es O
    if es_O(I1,d):
        print "Este ideal es O"
        return {tuple(I1):1}
   
        
    #Calculamos la norma de n y la lista con los factores de la norma
    norm=norma_id(I1,d)
    fact=list(factorint(norm))
    #Lista donde guardar los factores del ideal
    factores=[]
    #Para cada valor de la lista de factores de la norma
    for i in range(0,len(fact)):
        #Comprobamos si el ideal es O
        if es_O(I1,d):
                break
        #Calculamos los divisores de este primo
        div=divisores(fact[i],d)
        #Para cada elemento de los divisores comprobamos si divide al ideal
        for j in range(0,len(div)):
            while divide_id(div[j],I1,d):
                    #Si lo divide, calculamos cociente y dividendo, y añadimos a la lista de factores el dividendo
                    cociente=cociente_id(fact[i],I1,d)
                    I1=cociente[0]
                    dividendo=cociente[1]
                    factores.append(dividendo)
    #Contamos los factores
    factores=contador(factores)
    #Devolvemos un diccionario con la factorización
    dic_fact={}
    for i in range(0,len(factores)):
        dic_fact[tuple(factores[i][0])]=factores[i][1]
        
    return dic_fact

def list_prim(cta):
    lista=[]
    prim=0
    i=1
    while(prim<cta):
        prim=prime(i)
        lista.append(prim)
        i=i+1
    return lista
        
def SG1_gen(Lpbc,d):
    SG1=[]
    for i in range(0,len(Lpbc)):
        prim=divisores(Lpbc[i],d)
        for j in range(0,len(prim)):
            SG1.append(prim[j])
    return SG1
    
def esprincipal(I,d):
    norma=norma_id(I,d)
    lista=connorma2(norma,d)+connorma2(-norma,d)
    if lista==[]:
        return false
    for i in range(0,len(lista)):
        if pertenece(lista[i],I,d)==true:
            return true
    
    return false

def SG2_gen(SG1,d):
    SG2=[]
    for i in range(0,len(SG1)):
        if esprincipal(SG1[i],d)==false:
            SG2.append(SG1[i])
    return SG2

def SG3_gen(SG2,d):
    aux=[]
    for i in range(0,len(SG2)):
        bool1=false
        for j in range(0,len(aux)):
            if norma_id(SG2[i],d)==norma_id(aux[j],d):
                bool1=true
        if bool1==false:
            aux.append(SG2[i])
    return aux

def orden(I,d):
    if esprincipal(I,d):
        return 1
    else:
        prod=producto([I,I],d)
        if esprincipal(prod,d):
            return 2
        i=2
        while esprincipal(prod,d)!=true:
            prod=producto([prod,I],d)
            esprincipal(prod,d)
            i=i+1
        return i

def orden_gen(lista,d):
    #Calcula el orden de una lista de elementos
    orden_g=[]
    for i in range(0,len(lista)):
        orden_g.append([lista[i],orden(lista[i],d)])
    return orden_g
        
def generadores_grupo_clase(d):
    #funcion que calcula los generadores del grupo de clase juntos con sus respectivos ordenes
    if d==0:
        print "d es cero"
        return false
    if d>0:
        s=2
        t=0
    elif d<0:
        s=0
        t=1
    if d%4==1:
        disc=d
    else:
        disc=4*d
    cte=((4.0/N(pi))**t)*0.5
    #cota de minkowski
    cta=cte*1.0*sqrt(abs(disc*1.0))
    #Lista de los primos hasta la cota
    Lpbc=list_prim(int(cta))#podemos probar tambien sin int
    SG1=SG1_gen(Lpbc,d)
    SG2=SG2_gen(SG1,d)
    SG3=SG3_gen(SG2,d)
    
    if SG3==[]:
        print "grupo trivial"
        return [1]
    #devolvemos los generadores del grupo con sus ordenes
    return orden_gen(SG3,d)

def exp(I,n,d):
#funcion que eleva un ideal a un exponente n
    if n==1:
        return I
    prod=producto([I,I],d)
    if n==2:
        return prod
    for i in range(2,n):
        prod=producto([prod,I],d)
    return prod

#http://mathworld.wolfram.com/ClassNumber.html