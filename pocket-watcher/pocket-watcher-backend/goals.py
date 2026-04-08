import os
import plotly.graph_objects as go

def generate_goal_chart(income, savings_goal, total_spent=0):
    """
    Generates a savings goal gauge chart.
    Args:
        income (float): Total income.
        savings_goal (float): Savings goal.
        total_spent (float, optional): Total spending. Defaults to 0.
    Returns:
        dict: URLs and progress info for charts.
    """
    try:
        savings = income - total_spent
    except TypeError:
        savings = income  # fallback if total_spent not provided

    progress = max(0, min(savings / savings_goal, 1))
    percent = round(progress * 100, 1)

    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=savings,
        delta={'reference': savings_goal, 'increasing': {'color': "green"}},
        gauge={
            'axis': {'range': [None, savings_goal]},
            'bar': {'color': "green" if savings >= savings_goal else "orange"},
            'steps': [
                {'range': [0, savings_goal], 'color': '#eaeaea'}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': savings_goal
            }
        },
        title={'text': f"Progress to Saving Goal ({percent}%)"}
    ))

    static_dir = os.path.join(os.getcwd(), 'static')
    os.makedirs(static_dir, exist_ok=True)
    goal_path = os.path.join(static_dir, 'goal.html')
    fig.write_html(goal_path)

    return {
        "goal_url": "/static/goal.html",
        "savings": savings,
        "goal": savings_goal,
        "progress": percent
    }
