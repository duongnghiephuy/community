# Function to plot the result of vote and return graph object for use in template

from plotly.offline import plot
import plotly.graph_objs as go


def result_graph(question):
    x = []
    y = []
    result = question.get_result_dict()
    for key, value in result.items():
        x.append(key)
        y.append(value)
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
