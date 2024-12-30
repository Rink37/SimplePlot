import numpy as np
from mpl_toolkits.axes_grid1 import make_axes_locatable
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.collections import LineCollection
#from matplotlib.colors import ListedColormap, BoundaryNorm
from matplotlib.legend_handler import HandlerTuple

#plot and construct_subplot are default functions which take correctly formatted arguments and produce plots

plt.rcParams["font.family"] = "serif"
plt.rcParams["font.serif"] = ["Times new roman"] #Font is a personal choice - ideally times new roman would be used but this font is only available when using windows
plt.rcParams.update({"text.usetex":False}) #Enable latex formatting if it's installed on current device
matplotlib.rcParams.update({'font.size': 12})


def plot(data, layout = []):
    if isinstance(data, dict):
        data = [data]
    if layout == []:
        layout = [[1,1]]*len(data)
    if not isinstance(layout[0], list) and not isinstance(layout[0], np.ndarray):
        layout = [layout]
    if len(layout) != len(data):
        layout += [[1,1]]*(len(data)-len(layout))
    length = 0
    for i in layout:
        length = length+i[0]*i[1]
    sl = np.sqrt(length)
    shape = [0,0]
    shape[0] = int(sl)
    shape[1] = int(length)-shape[0]
    if shape[0]+shape[1]-1 != length:
        shape[1] += 1
    if shape[1] <= 0:
        shape[1] = 1
    pos = np.zeros([len(layout), 4])
    occ = np.zeros(shape)
    xd = 0
    yd = 0
    cc = True
    for i in range(len(layout)):
        for x in range(shape[1]):
            for y in range(shape[0]):
                if occ[y,x] == 0 and cc:
                    xd = x
                    yd = y
                    cc = False
        cc = True
        pos[i,0] = yd
        pos[i,1] = yd+(layout[i])[0]
        pos[i,2] = xd
        pos[i,3] = xd+(layout[i])[1]
        occ[int(pos[i,0]):int(pos[i,1]), int(pos[i,2]):int(pos[i,3])] = 1
    fig = plt.figure(figsize = (6, 3), dpi = 300, layout = 'constrained')
    gs = fig.add_gridspec(shape[0], shape[1])
    for i in range(len(layout)):
        p = pos[i]
        locals()['ax'+str(i)] = fig.add_subplot(gs[int(p[0]):int(p[1]), int(p[2]):int(p[3])])
        dat = data[i]
        construct_subplot_nicer(dat, locals()['ax'+str(i)])
    plt.show()
     
def construct_subplot(data, ax):
    if 'xs' not in data and 'ys' not in data and 'image' not in data:
        print('No plottable data found')
        return
    elif 'xs' not in data and 'ys' not in data and 'image' in data:
        im = ax.imshow(data['image'])
        if 'ylabel' in data:
            ax.set_ylabel(data['ylabel'])
        if 'xlabel' in data:
            ax.set_xlabel(data['xlabel'])
        if 'title' in data:
            plt.title(data['title'])
        if 'xax' in data:
            ax.xaxis.set_visible(data['xax'])
        if 'yax' in data:
            ax.yaxis.set_visible(data['yax'])
        divider = make_axes_locatable(ax)
        cax = divider.append_axes("right", size = "5%", pad = 0.05)
        plt.colorbar(im, cax = cax)
    else:
        plot_hist = False
        if 'image' in data:
            im = ax.imshow(data['image'])
        xs = enforce_shape(data['xs'])
        ys = enforce_shape(data['ys'])
        if xs.shape != ys.shape:
            print('Data is not in arrays with the same shape')
            return
        if 'xerr' in data:
            xerror = enforce_shape(data['xerr'])
        else:
            xerror = [None]*xs.shape[0]
        if 'yerr' in data:
            yerror = enforce_shape(data['yerr'])
        else:
            yerror = [None]*ys.shape[0]
        if 'method' in data:
            if isinstance(data['method'], str):
                if data['method'] == 'scatter':
                    l = 0
                    ls = [l]*xs.shape[0]
                    m = ['x']*xs.shape[0]
                elif data['method'] == 'line':
                    l = 1
                    ls = [l]*xs.shape[0]
                    m = [None]*xs.shape[0]
                elif data['method'] == 'hist':
                    plot_hist = True
                    l = 0
                    ls = [l]*xs.shape[0]
                    m = [None]*xs.shape[0]
                else:
                    l = 1
                    ls = [l]*xs.shape[0]
                    m = [None]*xs.shape[0]
            else:
                ls = [1]*xs.shape[0]
                m = [1]*xs.shape[0]
                for i in range(len(data['method'])):
                    if data['method'][i] == 'scatter':
                        ls[i] = 0
                        m[i] = 'x'
                    elif data['method'][i] == 'line':
                        ls[i] = 1
                        m[i] = None
                    elif data['method'][i] == 'hist':
                        plot_hist = True
                    else:
                        ls[i] = 1
                        m[i] = None
        else:
            l = 1
            ls = [l]*xs.shape[0]
            m = [None]*xs.shape[0]
        if 'linestyle' in data:
            if isinstance(data['linestyle'], str):
                linestyle = [data['linestyle']]*xs.shape[0]
            else:
                linestyle = []
                for i in range(len(data['linestyle'])):
                    linestyle += [data['linestyle'][i]]
        else:
            linestyle = ['-']*xs.shape[0]
        if 'colour' in data:
            col = data['colour']
        else:
            col = [None]*xs.shape[0]
        if 'temps' in data:
            temps = data['temps']
            if len(temps) > 1:
                norm = plt.Normalize(np.array(temps[len(temps)-1]).min(), np.array(temps[0]).max()+15)
            else:
                norm = plt.Normalize(np.array(temps).min(), np.array(temps).max()+15)
            for i in range(xs.shape[0]):
                points = np.array([np.array(xs[i]), np.array(ys[i])]).T.reshape(-1,1,2)
                segments = np.concatenate([points[:-1], points[1:]], axis = 1)
                lc = LineCollection(segments, cmap = 'plasma', norm=norm)
                lc.set_array(np.array(temps)[i])
                lc.set_linewidth(l)
                if i != 0 and i != xs.shape[0]-1:
                    lc.set_alpha(0)
                if not plot_hist:
                    if temps[i][0] == temps[i][-1]:
                        col[i] = matplotlib.cm.get_cmap('plasma')(norm(temps[i][0]))
                    markers, caps, bars = ax.errorbar(xs[i], ys[i], yerr = yerror[i], xerr = xerror[i], elinewidth = 1, lw = ls[i], marker = m[i], capsize = 3, color = col[i], linestyle = linestyle[i])
                    if temps[0][0] != temps[0][-1]:
                        markers.set_alpha(0)
                        [bar.set_alpha(1) for bar in bars]
                        [cap.set_alpha(1) for cap in caps]
                        line = ax.add_collection(lc)
                else:
                    col[i] = matplotlib.cm.get_cmap('plasma')(norm(temps[i][0]))
                    ax.hist(ys[i], orientation = 'horizontal', color = col[i])
            if 'cblabel' in data:
                if data['cblabel'] != False:
                    if plot_hist:
                        line = ax.add_collection(lc)
                    divider = make_axes_locatable(ax)
                    cax = divider.append_axes("right", size = "5%", pad = 0.05)
                    cbar = plt.colorbar(line, cax = cax)
                    cbar.set_label(data['cblabel'])
                    if plot_hist:
                        line.remove()
            else:
               if plot_hist:
                   line = ax.add_collection(lc)
               divider = make_axes_locatable(ax)
               cax = divider.append_axes("right", size = "5%", pad = 0.05)
               cbar = plt.colorbar(line, cax = cax)
               if plot_hist:
                   line.remove()
        else:
            if 'grouplabels' in data:
                litems = []
            for i in range(xs.shape[0]):
                if not plot_hist:
                    txs = xs[i][np.where(xs[i] != None)]
                    tys = ys[i][np.where(ys[i] != None)]
                    if type(yerror[i]) == np.ndarray:
                        tyerror = yerror[i][np.where(yerror[i] != None)]
                        if len(tyerror) == 0:
                            tyerror = None
                    else:
                        tyerror = yerror[i]
                    if type(xerror[i]) == np.ndarray:
                        txerror = xerror[i][np.where(xerror[i] != None)]
                        if len(txerror) == 0:
                            txerror = None
                    else:
                        txerror = xerror[i]
                    if 'grouplabels' in data:
                        litems += [ax.errorbar(txs, tys, yerr = tyerror, xerr = txerror, elinewidth = 1, lw = ls[i], marker = m[i], capsize = 3, color = col[i], linestyle = linestyle[i])]
                    else:
                        markers, caps, bars = ax.errorbar(txs, tys, yerr = tyerror, xerr = txerror, elinewidth = 1, lw = ls[i], marker = m[i], capsize = 3, color = col[i], linestyle = linestyle[i], barsabove = False)
                else:
                    ax.hist(ys[i], orientation = 'horizontal', color = col[i])
        if 'ylabel' in data:
            if isinstance(data['ylabel'], list) or isinstance(data['ylabel'], np.ndarray):
                print('There is only one y label, so this does not need to be a list or array')
                ax.set_ylabel(data['ylabel'][0])
            else:
                ax.set_ylabel(data['ylabel'])
        if 'xlabel' in data:
            if isinstance(data['xlabel'], list) or isinstance(data['xlabel'], np.ndarray):
                print('There is only one x label, so this does not need to be a list or array')
                ax.set_xlabel(data['xlabel'][0])
            else:
                ax.set_xlabel(data['xlabel'])
        if 'labels' in data:
            plt.legend(data['labels'], fontsize = 8)
        if 'grouplabels' in data:
            itdex = data['grouplabels'][0]
            #require that itdex is of some format [(0, 1, 2), (3, 4, 5)] e.g
            for i in range(len(itdex)):
                tlist = list(itdex[i])
                for j in range(len(tlist)):
                    tlist[j] = litems[itdex[i][j]]
                itdex[i] = tuple(tlist)
            ax.legend(itdex, data['grouplabels'][1], numpoints = 1, handler_map = {tuple: HandlerTuple(ndivide = None)})
        if 'title' in data:
            plt.title(data['title'])
        if 'image' in data:
            divider = make_axes_locatable(ax)
            cax = divider.append_axes("right", size = "5%", pad = 0.05)
            plt.colorbar(im, cax = cax)
        if 'xax' in data:
            ax.xaxis.set_visible(data['xax'])
        if 'yax' in data:
            ax.yaxis.set_visible(data['yax'])
        if 'xsc' in data:
            ax.set_xlim(data['xsc'])
        if 'ysc' in data:
            ax.set_ylim(data['ysc'])
        if 'xlog' in data:
            ax.set_xscale('log', base = data['xlog'])
        if 'ylog' in data:
            ax.set_yscale('log', base = data['ylog'])
        if 'verrlines' in data:
            for l in data['verrlines']:
                ax.axvline(l, linestyle = 'dashed', color = (0.4, 0.4, 0.4), zorder = 100, lw = 1)
        if 'vlines' in data:
            trans = ax.get_xaxis_transform()
            for l in data['vlines']:
                ax.axvline(l, linestyle = 'dashed', color = 'k', zorder = 100, lw = 1)
                if 'vllabels' in data:
                    ax.text(l-0.0001, 1.05, data['vllabels'][int(np.where(data['vlines'] == l)[0][0])], transform = trans, rotation = 90)
        if 'herrlines' in data:
            for l in data['herrlines']:
                ax.axhline(l, linestyle = 'dashed', color = (0.4, 0.4, 0.4), zorder = 100, lw = 1)
        if 'hlines' in data:
            trans = ax.get_xaxis_transform()
            for l in data['hlines']:
                ax.axhline(l, linestyle = 'dashed', color = 'k', zorder = 100, lw = 1)
                if 'hllabels' in data:
                    ax.text(l-0.0001, 1.05, data['hllabels'][int(np.where(data['hlines'] == l)[0][0])], transform = trans, rotation = 90)

def line_plotter(subplot_data, ax, list_length):
    xs = subplot_data['xs']
    ys = subplot_data['ys']
    xerror = subplot_data['xerr']
    yerror = subplot_data['yerr']
    if not isinstance(subplot_data['ms'], list):
        subplot_data['ms'] = [subplot_data['ms']]*list_length
    if not isinstance(subplot_data['lws'], list):
        subplot_data['lws'] = [subplot_data['lws']]*list_length
    if not isinstance(subplot_data['colour'], list):
        subplot_data['colour'] = [subplot_data['colour']]*list_length
    for i in range(list_length):
        if type(yerror[i]) == np.ndarray:
            tyerror = yerror[i][np.where(yerror[i] != None)]
            if len(tyerror) == 0:
                tyerror = None
        else:
            tyerror = yerror[i]
        if type(xerror[i]) == np.ndarray:
            txerror = xerror[i][np.where(xerror[i] != None)]
            if len(txerror) == 0:
                txerror = None
        else:
            txerror = xerror[i]
        try:
            label= subplot_data['labels'][i]
        except:
            label = None
        ax.errorbar(xs[i], ys[i], xerr = txerror, yerr = tyerror, elinewidth = 1, capsize = 3, lw = subplot_data['lws'][i], marker = subplot_data['ms'][i], color = subplot_data['colour'][i], label = label, linestyle = subplot_data['linestyles'][i])
        
def hist_plotter(subplot_data, ax, list_length):
    print('Does nothing')
    
def bar_plotter(subplot_data, ax, list_length):
    print('Does nothing')
    
def add_text(data, ax):
    if not isinstance(data['text'][0], list):
        data['text'] = [data['text']]
    for i in range(len(data['text'])):
        ax.text(data['text'][i][0], data['text'][i][1], data['text'][i][2])
        
def plot_hlines(data, ax):
    default_hline = {'y':0, 'c':'black', 'ls':'--', 'label':'line'}
    hl_keys = list(default_hline.keys())
    hlines = data['hline']
    if isinstance(hlines, dict):
        hlines = [hlines]
    for i in range(len(hlines)):
        hline = hlines[i]
        for key in hl_keys:
            if key not in hline:
                hline.update({key:default_hline[key]})
        ax.axhline(y = hline['y'], color = hline['c'], linestyle = hline['ls'])

def plot_vlines(data, ax):
    default_vline = {'x':0, 'c':'black', 'ls':'--', 'label':'line'}
    vl_keys = list(default_vline.keys())
    vlines = data['vline']
    if isinstance(vlines, dict):
        vlines = [vlines]
    for i in range(len(vlines)):
        vline = vlines[i]
        for key in vl_keys:
            if key not in vline:
                vline.update({key:default_vline[key]})
        ax.axvline(x = vline['x'], color = vline['c'], linestyle = vline['ls'])
        
def plot_lines(data, ax):
    default_line = {'o':(0,0), 's':0, 'c':'black', 'ls':'--', 'label':'line'}
    l_keys = list(default_line.keys())
    lines = data['line']
    if isinstance(lines, dict):
        lines = [lines]
    for i in range(len(lines)):
        line = lines[i]
        for key in l_keys:
            if key not in line:
                line.update({key:default_line[key]})
        ax.axline(line['o'], slope = line['s'], color = line['c'], linestyle = line['ls'])

def construct_subplot_nicer(data, ax):
    required_plotdata = ['xs', 'ys', 'image']
    keys = list(data.keys())
    canPlot = False
    for key in required_plotdata:
        if not canPlot and key in keys:
            canPlot = True
    if not canPlot:
        print('No plottable data is found')
        return
    if 'image' in data:
        ax.imshow(data['image'])
    subplot_data = {}
    dimensions = ['x', 'y'] # removes requirement for specifying x, y labels
    enforcable_data = ['s', 'err'] #names of all data fields which need shape enforcement performed on them
    for d in dimensions:
        for enforcable_type in enforcable_data:
            if d+enforcable_type in data:
                subplot_data.update({d+enforcable_type:enforce_shape(data[d+enforcable_type])}) #Data which we can pass to method-based construction
            else:
                if enforcable_type == 's':
                    subplot_data.update({d+enforcable_type:[[None]]})
                else:
                    subplot_data.update({d+enforcable_type:[None]*subplot_data[d+'s'].shape[0]})
            if d+enforcable_type in keys:
                keys.remove(d+enforcable_type)
    list_length = max(subplot_data['xs'].shape[0], subplot_data['ys'].shape[0])
    plot_parameters = {'line':{'lws':1, 'ms':None, 'colour':None},
                       'scatter':{'lws':0, 'ms':'x', 'colour':None},
                       'hist':{'lws':0, 'ms':None, 'colour':None},
                       'bar':{'lws':0, 'ms':None, 'colour':None}}
    plot_functions = {'line':line_plotter, 'scatter':line_plotter, 'hist':hist_plotter, 'bar':bar_plotter}
    plot_formatting = {'title':ax.set_title,
                       'xax':ax.xaxis.set_visible,
                       'yax':ax.yaxis.set_visible,
                       'xlabel':ax.set_xlabel,
                       'ylabel':ax.set_ylabel,
                       'xsc':ax.set_xlim,
                       'ysc':ax.set_ylim} #These are the non complex formatting items which we can do as simply function[label](data[label])
    complex_formatting = {'text':add_text,
                          'hline':plot_hlines,
                          'vline':plot_vlines,
                          'line':plot_lines} #These are more complex formatting items which handle plt functions that require that we give mutiple arguments so we pass to deliberate functions as function[label](data)
    if 'method' not in data or data['method'] not in plot_parameters:
        # Here we assume default plot types based on available data
        if 'xs' in data and 'ys' in data:
            method = 'line'
        elif 'xs' in data or 'ys' in data:
            method = 'hist'
    else:
        # If the method is an acceptable format, we use the entered parameter
        method = data['method']
    if 'method' in data:
        keys.remove('method')
    subplot_data.update(plot_parameters[method])
    if 'markerstyle' in data:
        subplot_data['ms'] = data['markerstyle']
    if 'colour' in data:
        subplot_data['colour'] = data['colour']
    if 'linestyle' in data:
        if isinstance(data['linestyle'], str):
            linestyle = [data['linestyle']]*list_length
        else:
            linestyle = []
            for i in range(len(data['linestyle'])):
                linestyle += [data['linestyle'][i]]
        subplot_data.update({'linestyles':linestyle})
        keys.remove('linestyle')
    else:
        subplot_data.update({'linestyles':['-']*list_length})
    if 'label' in data:
        subplot_data['labels'] = data['label']
        if isinstance(subplot_data['labels'], str):
            subplot_data['labels'] = [subplot_data['labels']]
    else:
        subplot_data['labels'] = []
    plot_functions[method](subplot_data, ax, list_length) # This is the line which directs to the appropriate plot function in the function manager
    for key in keys:
        if key in plot_formatting:
            plot_formatting[key](data[key])
        if key in complex_formatting:
            complex_formatting[key](data, ax)
    if 'label' in data:
        ax.legend()
    

def enforce_shape(item):
    maxm = 0
    if not isinstance(item[0], list) and not isinstance(item[0], np.ndarray):
        item = [item]
    for i in range(len(item)):
        if len(item[i]) > maxm:
            maxm = len(item[i])
    for i in range(len(item)):
        if len(item[i]) < maxm:
            item[i] = np.append(item[i] , [None]*(maxm - len(item[i])))
    try:
        item = np.array(item)
    except:
        print(item, len(item[0]), len(item[1]))
    return item
    