import numpy as np
import math
from math import sqrt, sin, pi
from collections import OrderedDict
import matplotlib.pyplot as plt

n = 101 #test value
h = 1/n
x = np.linspace(0,1,n)

##def f(x): # just a test to see whether fast marching is working
##    '''The function appearing in the eikonal equation
##    |u'(x)| = f(x).'''
##    return 1

def f(x):
    '''The function appearing in the Eikonal equation
    |u'(x)| = f(x).
    In the case of shape-from-shading, f(x) = sqrt((1/(I(x)^2))-1)
    where I(x) is the light intensity.'''
    try:
        return sqrt( (1/(sin((4*x))**2) ) - 1 )
    except:
        return math.inf # otherwise it was returning an error for division by 0


def ff(n): # applies f to the grid space
    x = np.linspace(0,1,n)
    ff = map(f, x)
    return list(ff)

def fastmarch(n):
    f = ff(n) 
    h = 1/(n-1)
    #Initialization
    t0 = 0
    Z = np.linspace(0,1,n) # grid points
    A = [math.floor(n/2)] #initial accepted set is just the point x = 1/2
    u = np.repeat(math.inf, n)
    u[math.floor(n/2)] = 1
    # update until there are n elements in A, meaning that all the nodes have been incorporated
    while len(A) < n:
        F = list(set(neighbors(A)) - set(A)) # define the front to be neighbors of the accepted set
        sc = np.zeros((len(F),2)) # to use when sorting scheme vals at front
        #schemeF = list(itertools.chain.from_iterable(map(scheme, F)))
        schemeF = []
        for i in F: #calculate the value of the scheme at the front
            if (i != 0) and (i != n-1):
                u[i] = h*(ff(n))[i] + min(u[i-1], u[i+1])
                schemeF.append(u[i])
            elif i == 0:
                u[i] = h*(ff(n))[i] + u[i+1]
                schemeF.append(u[i])
            else:
               u[i] = h*(ff(n))[i] + u[i-1]
               schemeF.append(u[i])
            sc[:,0] = F
            sc[:,1] = schemeF
        sc[sc[:,1].argsort()] # sorts based on the 2nd column - that is, the scheme values
        newacc = int(sc[0,0])
        A.append(newacc)
        F.remove(newacc)
    plt.plot(x,u)
    plt.show()
    return u

def neighbors(A):
    '''Finds the collection of neighbors of all elements in the accepted set'''
    x = np.linspace(0,1,n)
    ind = A
    #ind = np.nonzero(np.in1d(x, A))[0] # indices of accepted elements within x
    nb1 = [] #indices of neighbors
    for i in ind:
        if (i != 0) and (i != len(x)-1):
            nb1.append(i-1)
            nb1.append(i+1)
        elif i == 0: # only have the right neighbor
            nb1.append(i+1)
        else: # only have the left neighbor
            nb1.append(i-1)
        nb1 = list(OrderedDict.fromkeys(nb1))
    return nb1

def scheme(i): # calculates the scheme at index i
    s = []
    #u = np.repeat(math.inf, n)
    #u[math.floor(n/2)] = 1
    if (i != 0) and (i != n-1):
        s.append(h*(ff(n))[i] + min(u[i-1], u[i+1]))
        u[i] = h*(ff(n))[i] + min(u[i-1], u[i+1])
    elif i == 0:
        s.append(h*(ff(n))[i] + u[i+1])
        u[i] = h*(ff(n))[i] + u[i+1]
    else:
       s.append(h*(ff(n))[i] + u[i-1])
       u[i] = h*(ff(n))[i] + u[i-1]
    return s

# from http://code.activestate.com/recipes/578281-fmap-a-kind-of-inverse-of-the-built-in-python-map-/
def fmap(function_list, argument):
    result = argument
    for function in function_list:
        result = function(result)
    return result

def main():
    function_list = [scheme]
    for argument in range(5):
        fmap_result = fmap(function_list, argument)
        print("argument:", argument, ": fmap result:", fmap_result)

