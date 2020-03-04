import math 
angle = [-180,-150, -120, -90, -60, -30, 0, 30, 60, 90, 120, 150, 180]
for i in angle :
    x = math.cos(i)
    y = math.sin(i)
    print ('The coordinate %d : [ %f , %f ]'%(i,x,y))

