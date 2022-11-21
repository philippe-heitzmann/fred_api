import datetime
from typing import Type, List

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

COLORS = ['blue', 'orange', 'green', 'gray', 'purple', 'brown', 'red']*7

class Viz():
    '''Methods for creating a variety of visualizations such as barplots, lineplots, pairplots, heatmaps etc'''
    
    def __init__(self, figsize = (10,6)):
        self.figsize = figsize
        self.t=1
        print(f'Instantiated with figsize {figsize}')
    
    
    def _check_colors(self, **kwargs):
        vline_xs, hline_ys = 0,0
        if 'vline_xs' in kwargs:
            vline_xs = len(kwargs['vline_xs'])
        if 'hline_ys' in kwargs:
            hline_ys = len(kwargs['hline_ys'])
        colors = COLORS[:max(vline_xs, hline_ys)]
        return colors
    
    
    def _set_decorations(self, ax, **kwargs):
        '''Helper setting matplotlib figure decorations such as title, xlabel, ylabel, etc if provided as kwargs'''
        if 'title' in kwargs: 
            print(kwargs['title'])
            ax.set_title(kwargs['title'][0], fontsize = kwargs['title'][1])
        if 'xlabel' in kwargs: ax.set_xlabel(kwargs['xlabel'][0], fontsize = kwargs['xlabel'][1])
        if 'ylabel' in kwargs: ax.set_ylabel(kwargs['ylabel'][0], fontsize = kwargs['ylabel'][1])
        if 'xlim' in kwargs: plt.xlim(kwargs['xlim'][0], kwargs['xlim'][1])
        if 'ylim' in kwargs: plt.ylim(kwargs['ylim'][0], kwargs ['ylim'][1])
        if 'legend' in kwargs and kwargs['legend']: plt.legend(bbox_to_anchor= kwargs['legend'], loc = 'upper center')
        if 'xticklocs' in kwargs:
            ax.set_xticks(kwargs['xticklocs'])
            if 'xticklabels' in kwargs:
                ax.set_xticklabels(kwargs['xticklabels'])
        if 'rotation' in kwargs: plt.xticks(rotation = kwargs['rotation'])
        if 'vline_xs' in kwargs:
            trans = ax.get_xaxis_transform()
            vline_ys = [0.97 - idx * 0.05 for idx in range(len(kwargs['vline_xs']))]
            colors = self._check_colors(**kwargs)
            for vline_x, vline_y, label, color in zip(kwargs['vline_xs'], vline_ys, kwargs['labels'], colors):
                plt.axvline(vline_x, linestyle = '--', color = color, linewidth = 1)
                plt.text(vline_x, vline_y, label, transform = trans, fontsize = 10, color = 'black')
        if 'hline_ys' in kwargs:
            trans = ax.get_yaxis_transform()
            colors = self._check_colors(**kwargs)
            for hline, label, color in zip (kwargs['hline_ys'], kwargs['labels'], colors):
                plt.axhline(y = hline, linestyle = '--', color = color, linewidth = 0.5)
                plt.text(0.05, hline + 0.05, label, transform = trans, fontsize = 10, color = 'black')
        if 'annotations' in kwargs and kwargs['annotations']:
            annotation_adj = kwargs['annotation_adj'] if 'annotation_adj' in kwargs else 1
            rects = ax.patches
            for rect in rects:
                annotation = str(int(round(rect.get_height(),0))) if rect.get_height() != 0 else '' 
                ax.text(rect.get_x() + rect.get_width() / 2, rect.get_height() + annotation_adj, 
                        annotation, ha = 'center', va = 'bottom')
        plt.grid (False)
        return ax

    
    @staticmethod
    def get_xticks (series, n):
        return [x for x in range(0, len(series.unique()), n)]

        
    def download_fig(self, **kwargs):
        '''Download matplotlib figure'''
        if 'download' in kwargs and kwargs['download']:
            filename = 'plot' + '{:02d}'.format(datetime.datetime.now().month) + '{:02d}'.format(datetime.datetime.now().day) + '{:02d}'.format(datetime.datetime.now().hour) + '{:02d}'.format(datetime.datetime.now().minute) + '.png'
            plt.savefig(filename, bbox_inches = 'tight')
            print(f'Saved fig under filename {filename}')

            
    def _init(self, **kwargs):
        fig, ax = plt.subplots(figsize = self.figsize)
        return fig, ax                


    def _end(self, ax, **kwargs):
        ax = self._set_decorations(ax, **kwargs)
        fig = ax.get_figure()
        fig.tight_layout()
        self.download_fig(**kwargs)
        return fig


    def make_lineplot(self, *ys, x, linewidth = 2, marker = '.', markersize = 8, **kwargs):
        '''Create matplotlib lineplot'''
        fig, ax = self._init(**kwargs)
        for y in ys:
            plt.plot(x, y, linewidth = linewidth, marker = marker, markersize = markersize)
        fig = self._end(ax, **kwargs)
        return fig, ax
        
        
        
    def make_dual_lineplot(self, x: Type[pd.Series], y1: Type[pd.Series], y2: Type[pd.Series], **kwargs):
        '''TODO: finish implementing'''
        fig, ax = self._init(**kwargs)
        ax1 = plt.subplot()
        l1 = ax1.plot(x, y1, color='red')
        ax2 = ax1.twinx()
        l2, = ax2.plot(x, y2, color='orange')
        fig = self._end(ax, **kwargs)
        return fig, ax
    
    

    def make_scatter(self, *ys: List[pd.Series], x: pd.Series, linewidth = 3, c = None, **kwargs):
        '''Create matplotlib scatterplot'''
        fig, ax = self._init(**kwargs)
        for y in ys:
            plt.scatter(x, y, c = c)
        fig = self._end(ax, **kwargs)
        return fig

    
    def make_hist (self, *series, **kwargs):
        '''Create matplotlib histogram'''
        fig, ax = self._init(**kwargs)
        for s in series:
            n, bins, patches = ax.hist(s, bins = kwargs['bins'] if 'bins' in kwargs else 50)
        plt.gca().legend([s.name for s in series])
        fig = self._end(ax, **kwargs)
        return fig, ax
    

    def make_barplot(self, x: Type[pd.Series], height: Type[pd.Series], barwidth = 0.9, barh = False, **kwargs):
        '''Create simple matplotlib barplot'''
        fig, ax = self._init(**kwargs)
        if not barh:
            ax.bar(x, height, align='center') 
        else:
            y_pos= np.arange(len(list(height)))
            ax.barh(y_pos, height, align='center', width = barwidth)
            ax.set_yticks(y_pos)
            ax.invert_yaxis()
        fig = self._end(ax, **kwargs)
        return fig, ax
    
    
def get_hist(*series, label: str, figsize = (12,7), **kwargs):
    '''label = 'median: {} day of the month' '''
    vline_xs = [s.median() for s in series]
    labels = [label.format(int(round(vline_x,0))) for vline_x in vline_xs]
    viz1 = Viz(figsize=figsize)
    fig, ax = viz1.make_hist(*series, 
                             vline_xs = vline_xs,
                             labels = labels,
                             **kwargs)
    return fig, ax

