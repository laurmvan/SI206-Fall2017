from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt

m = Basemap(projection = 'mill', llcrnrlat = 20, urcrnrlat=50,\
llcrnrlon=-130,urcrnrlon=-60,resolution = 'c') #miller cyndrical map look of whole US, these are corner parameters listed here

m.drawcoastlines() #draw lines on the coast
m.drawcountries() #draw country lines
m.drawstates() #draw state lines
m.fillcontinents() #fill continents

lat,lon = 29.76666,-95.366666 # need to change this into a format basemap understands
#change this to an array
x,y = m(lon,lat)
m.plot(x,y,'ro') #plot the point


m.drawmapboundary()
plt.title('Current Location')
plt.show()

#x = lon
#y = lat (reverse what you would think)

