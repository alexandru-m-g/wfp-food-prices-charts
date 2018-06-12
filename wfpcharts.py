from glob import glob
import os.path
import pandas as pd
import datetime
from plotly.offline import plot
import plotly.graph_objs as go
from os import makedirs


def process(input_path,output_prefix):
    makedirs(os.path.split(output_prefix)[0],exist_ok=True)
    df = pd.read_csv(input_path)
    hxl = df.ix[0]
    df=df.ix[1:]
    df["datetime"] = df.date.apply(lambda x:datetime.datetime.strptime(x,"%Y-%m-%d"))
    df["ym"] = df.datetime.apply(lambda x:x.year+(x.month-1)/12.0)

    plots = []
    for key, index in sorted(df.groupby(["cmname","unit","mktname"]).groups.items()):
        commodity, unit, market = key
        g=df.ix[index]
        plots.append(go.Scatter(x=g.date,y=g.price,mode = 'lines+markers',name='%(commodity)s (%(unit)s) - %(market)s'%locals()))
    plot(plots,show_link=False,filename=output_prefix+".html")



if __name__ == "__main__":
    for path in glob("data/*.csv"):
        output_prefix=os.path.join("charts",os.path.split(path)[1].replace(".csv",""))
        print (path)
        process(path,output_prefix)