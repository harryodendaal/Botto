import plotly.graph_objs as go
from plotly.subplots import make_subplots

class PlotGraph:
    def __init__(self, _df, _symbol, _entry_signal = False, _exit_signal = False):
        self.df = _df
        self.symbol = _symbol
        self.entry_signal = _entry_signal
        self.exit_signal = _exit_signal
#tsratsartsratsratsartsar

    def plotGraph(self):
            fig = make_subplots(
                    rows=2, cols=1,
                    #subplot_titles=(self.symbol, "indicator"),
                    #shared_xaxes=True,
                    #vertical_spacing=0.3
                )

            # plot candlestick chart
            fig.add_trace(go.Candlestick(
                x=self.df['time'],
                open=self.df['open'],
                close=self.df['close'],
                high=self.df['high'],
                low=self.df['low'],
                name="Candlesticks"), row=1, col=1)

            if(self.entry_signal != False):
                #trade signals plot on main graph
                if self.entry_signal:
                    fig.add_trace(go.Scatter(
                        x=[item[0] for item in self.entry_signal],
                        y=[item[1] for item in self.entry_signal],
                        name="Entry signal",
                        mode="markers",
                        line=dict(color=('rgba(255, 255, 0, 50)'), width=50)), row=1, col=1)
                if self.exit_signal:
                    fig.add_trace(go.Scatter(
                        x=[item[0] for item in self.exit_signal],
                        y=[item[1] for item in self.exit_signal],
                        name="Exit Signals",
                        mode="markers",
                        line=dict(color=('rgba(0, 255, 0, 50)'), width=50)), row=1, col=1)
                if self.df.__contains__("low_boll"):
                    fig.add_trace(go.Scatter(
                        x=self.df["time"],
                        y=self.df["low_boll"],
                        name="low bb",
                        mode="lines",
                        line=dict(color=('rgba(0, 255, 0, 10)'), width=2)), row=1, col=1)
                if self.df.__contains__("fast"):
                    fig.add_trace(go.Scatter(
                        x=self.df["time"],
                        y=self.df["fast"],
                        name="fast",
                        mode="lines",
                        line=dict(color=('rgba(255, 0, 0, 10)'), width=2)), row=2, col=1)
                if self.df.__contains__("slow"):
                    fig.add_trace(go.Scatter(
                        x=self.df["time"],
                        y=self.df["slow"],
                        name="slow",
                        mode="lines",
                        line=dict(color=('rgba(0, 0, 255, 10)'), width=2)), row=2, col=1)

            #style and display
            fig.layout.template = 'plotly_dark'
            fig.update_layout(width=1500)
            fig.show()

