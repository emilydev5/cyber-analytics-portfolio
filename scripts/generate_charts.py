import altair as alt
import pandas as pd
import numpy as np

# 1. Create simple mock data for Project 21 (Circuit Uptime)
dates = pd.date_range("2026-01-01", periods=24, freq="H")
throughput = [100, 102, 98, 95, 105, 110, 30, 25, 28, 90, 100, 105] * 2

df = pd.DataFrame({
    'time': dates,
    'mbps': throughput,
    'status': ['Up' if x > 50 else 'Brownout' for x in throughput]
})

# 2. Create a simple Altair Chart
chart = alt.Chart(df).mark_line(point=True).encode(
    x=alt.X('time:T', title='Time (Last 24 Hours)'),
    y=alt.Y('mbps:Q', title='Throughput (Mbps)'),
    color=alt.Color('status:N', scale=alt.Scale(domain=['Up', 'Brownout'], range=['#00d1b2', '#ffdd57'])),
    tooltip=['time', 'mbps', 'status']
).properties(
    width='container',
    height=300,
    title='Network Circuit Throughput'
)

# 3. Export to the docs/charts folder
chart.save('docs/charts/uptime_chart.json')
print("✅ Chart exported to docs/charts/uptime_chart.json")