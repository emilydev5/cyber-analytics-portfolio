import pandas as pd
import altair as alt
import requests
import math
from io import StringIO

def calculate_entropy(text):
    """Calculates the Shannon Entropy of a string to detect randomness."""
    if not text: return 0
    probs = [float(text.count(c)) / len(text) for c in set(text)]
    return -sum(p * math.log(p, 2) for p in probs)

def run_project():
    print("🌐 Fetching live phishing feed...")
    url = "https://openphish.com/feed.txt"
    try:
        response = requests.get(url, timeout=10)
        # Get first 100 entries for the demo visualization
        urls = response.text.splitlines()[:100]
    except Exception as e:
        print(f"❌ Error fetching data: {e}")
        return

    # 1. Feature Extraction
    results = []
    for u in urls:
        results.append({
            'url': u,
            'length': len(u),
            'entropy': calculate_entropy(u),
            'is_phishing': 1
        })
    
    # Add some 'Safe' baseline data for comparison
    safe_urls = ['google.com', 'apple.com', 'github.com', 'microsoft.com', 'amazon.com']
    for u in safe_urls:
        results.append({'url': u, 'length': len(u), 'entropy': calculate_entropy(u), 'is_phishing': 0})

    df = pd.DataFrame(results)

    # 2. Create Visualization
    chart = alt.Chart(df).mark_circle(size=100).encode(
        x=alt.X('length:Q', title='URL Length'),
        y=alt.Y('entropy:Q', title='URL Entropy'),
        color=alt.Color('is_phishing:N', 
                        scale=alt.Scale(domain=[1, 0], range=['#ff4b2b', '#2ecc71']),
                        legend=alt.Legend(title="Threat Level", labelExpr="datum.value == 1 ? 'Malicious' : 'Verified Safe'")),
        tooltip=['url', 'entropy']
    ).properties(
        width='container',
        height=400,
        title='Phishing Domain Analysis (Live Feed)'
    ).interactive()

    # 3. Export
    chart.save('docs/charts/project_1_phishing.json')
    print("✅ Project 1 live chart exported to docs/charts/")

if __name__ == "__main__":
    run_project()