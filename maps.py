from mpl_toolkits.basemap import basemap
import numpy as np
import matplotlib.pyplot as plt

m = Basemap(projection = 'mill', llcrnrlat = -90, urcrnrlat=90,\
llcrnrlon=-180,urcrnrlon=180,resolution = 'c') #miller cyndrical map look of whole world, these are corner parameters listed here

m.drawcoastlines() #draw lines on the coast
m.fillcontinents() #fill continents

m.drawmapboundary()
plt.title('Title')
plt.show()


