import math

def td(T,RH):
    r=(17.27*T/(237.7+T)+math.log(RH/100))
    Td=237.7*r/(17.27-r)
    return Td
'''
Td=td(10.9,64)
print(Td)
'''
def Mechanical_mixing_height(T,Td,P,Uz,Z,Z0):
    mechanical_mixing_height=(121/6)*(6-P)*(T-Td)+0.169*P*(Uz+0.257)/12*0.0000579*math.log(Z/Z0)
    return mechanical_mixing_height

'''
print(Mechanical_mixing_height(10.9,Td,3,2.6,14,1.2))
'''




'''
a=td(1,2)
print(type())
print(a)

def asd(T,Td):
    print(T+Td)


asd(1,a)
'''


