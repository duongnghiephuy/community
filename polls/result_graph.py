from matplotlib.pyplot import title
from plotly.offline import plot
import plotly.graph_objs as go
import numpy as np


def result_graph(question):
    x = []
    y = []
    for choice in question.choice_set.all():
        x.append(choice.choice_text)
        y.append(choice.votes)
    fig = go.Figure(data=go.Bar(name="VotePlot", x=x, y=y))
    fig.update_layout(
        title_text=question.question_text, xaxis_title="Choice", yaxis_title="Votes"
    )

    fig.update_layout(
        {
            "plot_bgcolor": "rgba(0, 0, 0, 0)",
            "paper_bgcolor": "rgba(0, 0, 0, 0)",
        }
    )

    vote_result_obj = plot({"data": fig}, output_type="div")
    return vote_result_obj
