
import epdobase as eb
import matplotlib.pyplot as pl
#import golgis as gg
import numpy as np

pl.rc("font",size=12)

from mpl_toolkits.mplot3d import Axes3D

ceiling = 2.0 # 20.0

pl.ion()

ep = eb.cl_epdobase()

ep.load('Test_4_Lake-Waban-Boathouse.csv','csv')
ep.numerize()

x = ep.ndct['x']/100.0
y = ep.ndct['y']/100.0
z = ep.ndct['z']/100.0

inds = np.nonzero((z < ceiling)*(x < 10)*(x>-10)*(y<10))[0]

xp = x[inds]
yp = y[inds]
zp = z[inds]

fig = pl.figure(1)
ax = fig.add_subplot(111, projection='3d')

ax.scatter(xp,yp,zp,'.',c=zp)

ax.set_xlabel('x [m]')
ax.set_ylabel('y [m]')
ax.set_zlabel('z [m]')

pl.figure(2)
pl.scatter(xp,yp,20,zp,'.')
pl.colorbar()
pl.axis('equal')
pl.xlabel('x [m]')
pl.ylabel('y [m]')
#pl.clabel('z [m]')
pl.savefig('cloud.png',dpi=200)


# >> Finally, compute the gridmap by regridding the data:

#gdmp = gg.gridmap_from_irregpt(xp, yp, [zp], rect = (-10, 10, 0, 10))
#gdmp.maps.append(gdmp.maps[0].data)

#gdmp.draw(mapnum=1,fignum=3, colormap="rainbow")
#pl.colorbar()
#pl.savefig('undertree_dem.png',dpi=200)
