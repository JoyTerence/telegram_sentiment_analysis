# import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

class Plot:
    def __init__(self, df):
        self.df = df
    
    def show(self):

        fig = px.bar(self.df, x="Date", y="Avg sentiment", title="Avg sentiment")
        fig.show()

        fig1 = px.bar(self.df, x="Date", y="Number of Msgs", title="Number of msgs")
        fig1.show()