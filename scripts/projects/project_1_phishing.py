import pandas as pd
import altair as alt
import requests
import math
import os

def calculate_complexity(text):
    """Measures how random or 'jumbled' a website name is."""
    if not text: return 0
    # Clean the URL to focus on the domain name itself
    clean_text = text.replace("http://", "").replace("https://", "").split('/')[0]
    probs = [float(clean_text.count(c)) / len(clean_text) for c in set(clean_text)]
    return -sum(p * math.log(p, 2) for p in probs)

def run_project():
    print("🌐 Fetching live phishing data...")
    url = "https://openphish.com/feed.txt"
    
    try:
        response = requests.get(url, timeout=10)
        # Taking 50 live malicious samples for a cleaner visual
        malicious_urls = response.text.splitlines()[:50]
    except Exception as e:
        print(f"❌ Connection Error: {e}")
        return

    results = []
    
    # Process Malicious URLs
    for u in malicious_urls:
        results.append({
            'website': u[:40] + "...", # Truncate for tooltip neatness
            'length': len(u),
            'randomness_score': calculate_complexity(u),
            'type': 'Malicious'
        })
    
    # Process Known Safe URLs for comparison
    safe_list = ['google.com', 'apple.com', 'github.com', 'microsoft.com', 'amazon.com', 'netflix.com']
    for u in safe_list:
        results.append({
            'website': u,
            'length': len(u),
            'randomness_score': calculate_complexity(u),
            'type': 'Verified Safe'
        })

    df = pd.DataFrame(results)

    # 2. Create the Visual
    # Using fixed width (600) instead of 'container' to prevent blank renders
    chart = alt.Chart(df).mark_circle(size=150, opacity=0.8).encode(
        x=alt.X('length:Q', title='Website Address Length'),
        y=alt.Y('randomness_score:Q', title='Randomness Score (Complexity)'),
        color=alt.Color('type:N', 
                        scale=alt.Scale(domain=['Malicious', 'Verified Safe'], 
                                       range=['#ff4b2b', '#2ecc71']),
                        legend=alt.Legend(title="Site Status")),
        tooltip=['website', 'randomness_score', 'length']
    ).properties(
        width=600, 
        height=400,
        title='Phishing Website Fingerprint'
    ).interactive()

    # 3. Ensure directory exists and Save
    os.makedirs('docs/charts', exist_ok=True)
    
    # Important: Setting standalone=False ensures the data is bundled inside the JSON
    chart.save('docs/charts/project_1_phishing.json')
    print("✅ Success: docs/charts/project_1_phishing.json created.")

if __name__ == "__main__":
    run_project()