import numpy as np
from mpl_toolkits.axes_grid1 import make_axes_locatable
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.collections import LineCollection
from matplotlib.colors import ListedColormap, BoundaryNorm
from matplotlib.legend_handler import HandlerLine2D, HandlerTuple

#plot and construct_subplot are default functions which take correctly formatted arguments and produce plots

plt.rcParams["font.family"] = "serif"
plt.rcParams["font.serif"] = ["Times New Roman"]
plt.rcParams.update({"text.usetex":True})
matplotlib.rcParams.update({'font.size': 12})

def plot(data, layout = []):
    if isinstance(data, dict):
        data = [data]
    if layout == []:
        layout = [[1,1]]*len(data)
    if not isinstance(layout[0], list) or not isinstance(layout[0], np.ndarray):
        layout = [layout]
    if len(layout) != len(data):
        layout += [[1,1]]*(len(data)-len(layout))
    print(layout)
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
        construct_subplot(dat, locals()['ax'+str(i)])
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
                    #cbar = plt.colorbar(line, ax=ax)
                    cbar.set_label(data['cblabel'])
                    if plot_hist:
                        line.remove()
            else:
               if plot_hist:
                   line = ax.add_collection(lc)
               divider = make_axes_locatable(ax)
               cax = divider.append_axes("right", size = "5%", pad = 0.05)
               cbar = plt.colorbar(line, cax = cax)
               #cbar = plt.colorbar(line, ax=ax)
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
            
            
def enforce_shape(item):
    maxm = 0
    for i in range(len(item)):
        if len(item[i]) > maxm:
            maxm = len(item[i])
    for i in range(len(item)):
        if len(item[i]) < maxm:
            item[i] = np.append(item[i] , [None]*(maxm - len(item[i])))
    item = np.array(item)
    return item
    