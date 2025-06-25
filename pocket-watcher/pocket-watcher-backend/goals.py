# goals.py

import os
import plotly.graph_objects as go

# You can connect this value from parser.py
# For now, we'll simulate it here
total_spending: '752.3'
def generate_goal_chart(income, savings_goal, total_spending):
    savings = income - 752.3
    progress = max(0, min(savings / savings_goal, 1))  
    percent = round(progress * 100, 1)

    # Build the figure
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

    # Save to HTML
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
