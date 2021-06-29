import plotly.graph_objects as go
from plotly.subplots import make_subplots

def plot_revenue_yields_vs_network_inflation(df):
    # Create figure with secondary y-axis
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    df_subset_0 = df.query("subset == 0")
    df_subset_1 = df.query("subset == 1")

    # Add traces
    fig.add_trace(
        go.Scatter(x=df_subset_0.timestep, y=df_subset_0.total_revenue_yields_pct, name="Revenue yields (%)"),
        secondary_y=False
    )

    fig.add_trace(
        go.Scatter(x=df_subset_0.timestep, y=df_subset_0.total_profit_yields_pct, name="Net yields @ 25 (%)"),
        secondary_y=False,
    )

    fig.add_trace(
        go.Scatter(x=df_subset_1.timestep, y=df_subset_1.total_profit_yields_pct, name="Net yields @ 1500 (%)"),
        secondary_y=False,
    )

    fig.add_trace(
        go.Scatter(x=df_subset_0.timestep, y=df_subset_0.supply_inflation_pct, name="ETH Supply inflation (%)"),
        secondary_y=True,
    )


    # Set x-axis title
    fig.update_xaxes(title_text="Epochs")

    # Set y-axes titles
    fig.update_yaxes(title_text="Revenue Yields", secondary_y=False)
    fig.update_yaxes(title_text="Network Inflation Rate (Annualized)", secondary_y=True)
    return fig
