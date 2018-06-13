from glob import glob
import os.path
import pandas as pd
import datetime
from plotly.offline import plot
import plotly.graph_objs as go
from os import makedirs
import math


def process(input_path,output_prefix):
    makedirs(os.path.split(output_prefix)[0],exist_ok=True)
    df = pd.read_csv(input_path)
    hxl = df.ix[0]
    df=df.ix[1:]
    df["datetime"] = df.date.apply(lambda x:datetime.datetime.strptime(x,"%Y-%m-%d"))
    df["ym"] = df.datetime.apply(lambda x:x.year+(x.month-1)/12.0)
    df["price"]=df.price.apply(float)

    plots = []
    for key, index in sorted(df.groupby(["cmname","unit","mktname"]).groups.items()):
        commodity, unit, market = key
        g=df.ix[index]
        plots.append(go.Scatter(x=g.date,y=g.price,mode = 'lines+markers',name='%(commodity)s (%(unit)s) - %(market)s'%locals()))
    plot(plots,show_link=False,filename=output_prefix+"_all.html",auto_open=False)

    plots = []
    for key, index in sorted(df.groupby(["cmname","unit"]).groups.items()):
        commodity, unit = key
        g=df.ix[index]
        gd = g.groupby(["date"])
        x=gd.price.mean().index
        y=gd.price.mean()
        y_min=gd.price.min()
        y_max=gd.price.max()

        plots.append(go.Scatter(
            x=x,y=y,name='%(commodity)s (%(unit)s)'%locals(),
            error_y=dict(
                type='data',
                symmetric=False,
                array=y_max-y,
                arrayminus=y-y_min
            )
            )
        )
    plot(plots,show_link=False,filename=output_prefix+"_band.html",auto_open=False)

    plots = []
    for key, index in sorted(df.groupby(["cmname","unit"]).groups.items()):
        commodity, unit = key
        g=df.ix[index]
        gd = g.groupby(["date"])
        x=gd.price.median().index
        y=gd.price.median()

        plots.append(go.Scatter(
            x=x,y=y,name='%(commodity)s (%(unit)s)'%locals(),mode = 'lines+markers'
            )
        )
    plot(plots,show_link=False,filename=output_prefix+"_median.html",auto_open=False)

    plots = []
    for key, index in sorted(df.groupby(["cmname","unit"]).groups.items()):
        commodity, unit = key
        g=df.ix[index]
        invmean = 100.0/g.price.mean()
        quantity = math.pow(10,math.trunc(math.log10(invmean)))
        qlabel = quantity
        if quantity<1:
            qlabel = "1/"+str(int(1/quantity))
        if qlabel==1:
            qlabel=""

        gd = g.groupby(["date"])
        x=gd.price.median().index
        y=gd.price.median()*quantity

        plots.append(go.Scatter(
            x=x,y=y,name='%(commodity)s (%(qlabel)s %(unit)s)'%locals(),mode = 'lines+markers'
            )
        )
    plot(plots,show_link=False,filename=output_prefix+"_scaledmedian.html",auto_open=False)

    plots = []
    for key, index in sorted(df.groupby(["cmname","unit"]).groups.items()):
        commodity, unit = key
        g=df.ix[index]
        invmean = 100.0/g.price.mean()
        quantity = invmean
        qlabel = quantity

        gd = g.groupby(["date"])
        x=gd.price.median().index
        y=gd.price.median()*quantity

        plots.append(go.Scatter(
            x=x,y=y,name='%(commodity)s (%(qlabel)s %(unit)s)'%locals(),mode = 'lines+markers'
            )
        )
    plot(plots,show_link=False,filename=output_prefix+"_normmedian.html",auto_open=False)

    plots = []
    for key, index in sorted(df.groupby(["cmname","unit"]).groups.items()):
        commodity, unit = key
        g=df.ix[index]
        x=g.date
        y=g.price
        plots.append(go.Scatter(
            x=x,y=y,name='%(commodity)s (%(unit)s)'%locals(),mode = 'markers'
            )
        )
    plot(plots,show_link=False,filename=output_prefix+"_allscat.html",auto_open=False)


if __name__ == "__main__":
    for path in glob("data/*.csv"):
        output_prefix=os.path.join("charts",os.path.split(path)[1].replace(".csv",""))
        print (path)
        process(path,output_prefix)