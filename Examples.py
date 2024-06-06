import SimplePlot as pt
import numpy as np

#PlotData is used to demonstrate every passable function taken by pt.plot()
plotdatastruct = {
    'xs':[], #Horizontal values - either a single array or an array of arrays
    'xerr':[], #Error of horizontal values
    'xlabel':[], #Label of the x axis
    'xax':[], #Toggles whether we display the x axis ticks - True for ticks, false for none
    'xsc':[], #Array formatted as [min, max] which sets the limits of the x axis
    'xlog':[], #if 'xlog' is in the dictionary, the x axis scale is set to be logarithmic with base of the value of 'xlog'
    'ys':[], #Vertical values - either a single array or an array of arrays
    'yerr':[], #Error of vertical values
    'ylabel':[], #Label of the y axis
    'yax':[], #Toggles whether we display the y axis ticks - True for ticks, false for none
    'ysc':[], #Array formatted as [min, max] which sets the limits of the y axis
    'ylog':[], #if 'ylog' is in the dictionary, the y axis scale is set to be logarithmic with base of the value of 'ylog'
    'labels':[], #These are the labels which are used in the legend - if there are no labels, there is no legend
    'title':[], #The title of the plot
    'vlines':[], #Vertical lines at the values given
    'verrlines':[], #Lighter vertical lines which represent the error of the vertical lines
    'hlines':[], #Horizontal lines at the values given
    'herrlines':[], #Lighter horizontal lines which represent the error of the horizontal lines
    'image':[], #A 2D image array which can be plotted
    'method':[], #The plot method - can be a scatter plot, a line plot or a histogram
    'linestyle':[], #The style of the line - this takes the standard pyplot arguments
    'colour':[], #An array representing the colour of each line
    'temps':[], #An array of values which is used to assign a colourmap to each value
    'cblabel':[], #If present, labels a colourbar with whatever is given after : Does nothing if there is no colourbar present. If False, colourbar is removed
    'grouplabels':[] #Used to label multiple lines at once rather than one at a time
    }


Plotdata = {'xs':[np.arange(0, 100, 5)], 'ys':[np.arange(0, 20, 1)], 'temps':[np.arange(0, 20, 1)], 'ylabel':'Test', 'xlabel':'xtest'}
Plotdata2 = Plotdata.copy()
Plotdata2.update({'title':'Hello'})
pt.plot([Plotdata]*2, [1,2])