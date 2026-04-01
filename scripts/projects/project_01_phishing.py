import pandas as pd
import altair as alt
import requests
import math
import os
import json

def calculate_complexity(text):
    """Measures Shannon Entropy (randomness) of the domain."""
    if not text: return 0
    clean_text = text.replace("http://", "").replace("https://", "").split('/')[0]
    # Basic Shannon Entropy formula
    probs = [float(clean_text.count(c)) / len(clean_text) for c in set(clean_text)]
    return -sum(p * math.log(p, 2) for p in probs)

def run_project():
    # 1. Anchor paths to the script location
    script_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.abspath(os.path.join(script_dir, "../../"))
    output_path = os.path.join(root_dir, 'docs/charts/project_01_phishing.json')

    print("🌐 Fetching live phishing data from OpenPhish...")
    try:
        response = requests.get("https://openphish.com/feed.txt", timeout=10)
        malicious_urls = response.text.splitlines()[:50]
    except Exception as e:
        print(f"❌ Connection Error: {e}")
        return

    results = []
    
    # Process Malicious
    for u in malicious_urls:
        results.append({
            'website': (u[:35] + '...') if len(u) > 35 else u,
            'length': len(u),
            'randomness_score': calculate_complexity(u),
            'type': 'Malicious'
        })
    
    # Process Known Safe (Standardize these for a baseline)
    safe_list = ['google.com', 'apple.com', 'github.com', 'microsoft.com', 'amazon.com', 'netflix.com']
    for u in safe_list:
        results.append({
            'website': u,
            'length': len(u),
            'randomness_score': calculate_complexity(u),
            'type': 'Verified Safe'
        })

    df = pd.DataFrame(results)

    # 2. Define the Altair Visual
    chart = alt.Chart(df).mark_circle(size=150, opacity=0.8).encode(
        x=alt.X('length:Q', title='Website Address Length'),
        y=alt.Y('randomness_score:Q', title='Complexity (Entropy)'),
        color=alt.Color('type:N', 
                        scale=alt.Scale(domain=['Malicious', 'Verified Safe'], 
                                       range=['#ff4b2b', '#2ecc71']),
                        legend=alt.Legend(title="Site Status")),
        tooltip=['website', 'randomness_score', 'length']
    ).properties(
        width='container', # 'container' works if the parent div has a width
        height=400,
        title='Phishing Website Fingerprint'
    ).interactive()

    # 3. FORCE SCHEMA V5 & SAVE
    # Convert to dict to manually override the schema version
    chart_dict = chart.to_dict()
    chart_dict["$schema"] = "https://vega.github.io/schema/vega-lite/v5.json"

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, 'w') as f:
        json.dump(chart_dict, f, indent=4)
        
    print(f"✅ Success: JSON saved to {output_path}")

if __name__ == "__main__":
    run_project()