# -*- coding: utf-8 -*-
"""
Created on Wed Jun  2 18:53:05 2021

@author: umutu
"""
import numpy as np

dt = float(input("please enter dt: "))

class TwoBodyModel:
    
    x = 0
    y = 0
    
    def coordinate(self):
        return (str(self.x)+","+str(self.y))
    
class TwoBodyController:
    
    q = float(input("please enter mass ratio: "))
    e = float(input("please enter eccentricity: "))
    mm1 = 1
    mm2 = q
    mm12 = mm1 + mm2
    n = np.sqrt((1+q)*(1+e))
    u = [1,0,0,n]
    m1 = TwoBodyModel()
    m2 = TwoBodyModel()

    def derivative(self):
     
        du = [0,0,0,0]
        r = [self.u[0],self.u[1]]
        rr = np.sqrt(np.power(r[0],2) + np.power(r[1],2))
        
        for i in range(0,2):
            du[i] = self.u[i+2]
            du[i+2] = -(1 + self.q) * r[i]/(np.power(rr,3))
        
        return du    
    
    def eulerMethod(self, dt):
        self.u[0] = self.derivative()[0]*dt + self.u[0]
        self.u[1] = self.derivative()[1]*dt + self.u[1]
        self.u[2] = self.derivative()[2]*dt + self.u[2]
        self.u[3] = self.derivative()[3]*dt + self.u[3]
        
    def rungeKuttaMethod(self, h):
        a = [h/2, h/2, h, 0]
        b = [h/6, h/3, h/3, h/6]
        u0 = []
        ut = []
        dimension = self.u.__len__()
        
        for i in range (0,dimension):
            u0.append(self.u[i])
            ut.append(0)
        
        for j in range (0,4):
            du = self.derivative()
        
            for i in range (0,dimension):
                self.u[i] = u0[i] + a[j]*du[i]
                ut[i] = ut[i] + b[j]*du[i]
        
        for i in range (0,dimension):
            self.u[i] = u0[i] + ut[i]
            
    
    def NewPosition(self):
        r = 1
        a1 = (self.mm2 / self.mm12) * r
        a2 = (self.mm1 / self.mm12) * r
        
        self.m1.x = -a2*self.u[0]
        self.m1.y = -a2*self.u[1]
        
        self.m2.x = a1*self.u[0]
        self.m2.y = a1*self.u[1]
        

             

t = 0
T = float(input("please enter ending time: "))
a = TwoBodyController()
f = open("coordinates.txt","w")
print("")
print("please choose one:")
print("enter 'e' for euler method")
print("enter 'r' for runge-kutta method")

method = input(":")

while t < T :
    a.NewPosition()
    s = str(a.m1.coordinate())+","+str(a.m2.coordinate())+"\n"
    f.write(s)
    if method == "r":
        a.rungeKuttaMethod(dt)
    else:
        a.eulerMethod(dt)
    t = t + dt 

f.close()
 
