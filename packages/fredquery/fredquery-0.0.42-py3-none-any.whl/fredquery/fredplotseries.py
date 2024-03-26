#! env python

import os
import sys
import argparse
import webbrowser

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

try:
    from fredquery import fredseries
except ImportError as e:
    import fredseries

class PlotSeries():
    def __init__(self):
        """ create a plot with a list of FRED series_id's
        """
        # settings
        pd.options.plotting.backend = "plotly"

        self.fs = fredseries.FREDseries()
        self.seriesdict={}
        self.observationsdict={}
        self.seriesdata = {}       # when all have the same units
        self.unitseriesdata = {}  # when there are different units
        self.html = None

        self.df = None
        self.fig = None

    def getobservation(self, sid):
        """ getobservation(sid)

        get time series observations data for a FRED serieѕ_id
        sid - FRED series_id
        """
        aa = self.fs.returnobservation(sid)
        self.observationsdict[sid] = aa

    def getseries(self, sid):
        """ getseries(sid)

        get descriptive data for a FRED series_id
        sid - FRED series_id
        """
        aa = self.fs.returnseriesforsid(sid)
        self.seriesdict[sid] = aa

    def composeunitseriesdata(self):
        """ composeunitseriesdata()

        prepare the series data for the plots by units
        """
        for k in self.seriesdict.keys():
            saa = self.seriesdict[k] # two rows: keys, data
            assert saa[0][0] == 'id'
            assert saa[0][3] == 'title'
            assert saa[0][8] == 'units'
            sid    = saa[1][0]
            stitle = saa[1][3]
            units  = saa[1][8]

            oaa = self.observationsdict[k]

            print('%s %d' % (k, len(oaa)), file=sys.stderr)

            dates = [oaa[i][2] for i in range(len(oaa) )]
            vals  = [oaa[i][3] for i in range(len(oaa) )]

            if units not in self.unitseriesdata.keys():
                self.unitseriesdata[units] = {}
            if 'dates' not in self.unitseriesdata[units].keys():
                self.unitseriesdata[units]['dates'] = dates
            self.unitseriesdata[units][sid] = vals


    def composeunitseriesplot(self, units):
        """ composeunitseriesplot()

        compose plotly figure for later display with the series_id as
        the legend
        units - units of the observations
        """
        fig = go.Figure()

        dates = self.unitseriesdata[units]['dates']

        for k in self.unitseriesdata[units].keys():
            if k == 'dates': continue
            saa = self.seriesdict[k]
            sid    = saa[1][0]
            stitle = saa[1][3]
            units  = saa[1][8]
            fig.add_trace(go.Scatter(
                x=self.seriesdata['dates'],
                y=self.seriesdata[k],
                name=sid
            ) )

        fig.update_layout(
            title='FRED Time Series',
            yaxis_title=units,
            xaxis_title='dates',
        )
        return fig

    def composeunitseriesplotwnotes(self):
        """ composeunitseriesplotwnotes()

        compost plots with notes organized by units
        """
        htmla = []
        htmla.append('<html>')
        htmla.append('<title>FRED Series Plot</title>')

        for u in self.unitseriesdata.keys():
            fig = self.composeunitseriesplot(u)
            fightml = fig.to_html()
            for k in self.unitseriesdata[u].keys():
                if k == 'dates': continue
                sea = self.seriesdict[k]
                sid=sea[1][0]
                stitle=sea[1][3]
                htmla.append('<h3>%s:  %s</h3>' % (sid, stitle) )

                htmla.append('<table border="1">')
                hrowa = [sea[0][i] for i in range(len(sea[0])-1) if i != 3]
                hrow = '</th><th>'.join(hrowa)
                htmla.append('<tr>%s</tr>' % (''.join(hrow)) )

                drowa = [sea[1][i] for i in range(len(sea[1])-1) if i != 3]
                drow = '</td><td>'.join(drowa)
                htmla.append('<tr>%s</tr>' % (''.join(drow)) )
                htmla.append('</table>')

                htmla.append('<p>')
                htmla.append('%s: %s' % (sea[0][-1], sea[1][-1]) )
                htmla.append('</p>')

        htmla.append('</html>')

        self.html = ''.join(htmla)
        return self.html

    def composeseriesdata(self):
        """ composeseriesdata()

        prepare the series data for the plots
        """
        for k in self.seriesdict.keys():
            saa = self.seriesdict[k] # two rows: keys, data
            assert saa[0][0] == 'id'
            assert saa[0][3] == 'title'
            assert saa[0][8] == 'units'
            sid    = saa[1][0]
            stitle = saa[1][3]
            units  = saa[1][8]

            oaa = self.observationsdict[k]

            print('%s %d' % (k, len(oaa)), file=sys.stderr)

            dates = [oaa[i][2] for i in range(len(oaa) )]
            vals  = [oaa[i][3] for i in range(len(oaa) )]

            if 'dates' not in self.seriesdata.keys():
                self.seriesdata['dates'] = dates
            self.seriesdata[sid] = vals


    def composeseriesplot(self):
        """ composeseriesplot()

        compose plotly figure for later display with the series_id as
        the legend
        """
        self.fig = go.Figure()

        units = None

        for k in self.seriesdict.keys():
            saa = self.seriesdict[k]
            sid    = saa[1][0]
            stitle = saa[1][3]
            units  = saa[1][8]
            self.fig.add_trace(go.Scatter(
                x=self.seriesdata['dates'],
                y=self.seriesdata[k],
                name=sid
            ) )

        self.fig.update_layout(
            title='FRED Time Series',
            yaxis_title=units,
            xaxis_title='dates',
        )
        return self.fig

    def composeseriesplottitlelegend(self):
        """ composeseriesplottitlelegend()

        compose plotly figure with the series title as the legend
        """
        self.fig = go.Figure()

        units = None

        for k in self.seriesdict.keys():
            saa = self.seriesdict[k]
            sid    = saa[1][0]
            stitle = saa[1][3]
            units  = saa[1][8]
            self.fig.add_trace(go.Scatter(
                x=self.seriesdata['dates'],
                y=self.seriesdata[k],
                name=stitle
            ) )

        self.fig.update_layout(
            title='FRED Time Series',
            yaxis_title=units,
            xaxis_title='dates',
        )
        self.fig.update_layout(
           legend=dict( orientation='h')
        )
        return self.fig

    def composeseriesplotwnotes(self):
        htmla = []
        htmla.append('<html>')
        htmla.append('<title>FRED Series Plot</title>')

        fightml = self.fig.to_html()

        htmla.append(fightml)

        for k in self.seriesdict.keys():
           sea = self.seriesdict[k]
           sid=sea[1][0]
           stitle=sea[1][3]
           htmla.append('<h3>%s:  %s</h3>' % (sid, stitle) )

           htmla.append('<table border="1">')
           hrowa = [sea[0][i] for i in range(len(sea[0])-1) if i != 3]
           hrow = '</th><th>'.join(hrowa)
           htmla.append('<tr>%s</tr>' % (''.join(hrow)) )

           drowa = [sea[1][i] for i in range(len(sea[1])-1) if i != 3]
           drow = '</td><td>'.join(drowa)
           htmla.append('<tr>%s</tr>' % (''.join(drow)) )
           htmla.append('</table>')

           htmla.append('<p>')
           htmla.append('%s: %s' % (sea[0][-1], sea[1][-1]) )
           htmla.append('</p>')

        htmla.append('</html>')

        self.html = ''.join(htmla)
        return self.html

    def saveplotwnotes(self, fn):
        with open(fn, 'w') as fp:
            fp.write(self.html)

    def showplotwnotes(self, fn):
        webbrowser.open('file://%s' % (fn) )

    def showplot(self):
        self.fig.show()

def main():
    argp = argparse.ArgumentParser(description='plot a series list')
    argp.add_argument('--serieslist', required=True,
        help="comma separated list of FRED series_id's")
    argp.add_argument('--htmlfile', default='/tmp/p.html',
        help="path to file that will contain the plot")
    args = argp.parse_args()

    PS = PlotSeries()

    sida = args.serieslist.split(',')
    for sid in sida:
        PS.getseries(sid)
        PS.getobservation(sid)
    PS.composeseriesdata()
    PS.composeseriesplot()

    PS.composeseriesplotwnotes()
    PS.saveplotwnotes(args.htmlfile)
    PS.showplotwnotes(args.htmlfile)
    #PS.showplot()

if __name__ == '__main__':
    main()
