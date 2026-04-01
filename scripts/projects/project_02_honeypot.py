import os
import time
import pandas as pd
import altair as alt
import requests
from dotenv import load_dotenv
from sklearn.cluster import KMeans

# Setup Paths
script_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.abspath(os.path.join(script_dir, "../../"))
data_dir = os.path.join(root_dir, "data")
cache_file = os.path.join(data_dir, "honeypot_cache.csv")
load_dotenv(os.path.join(root_dir, ".env"))

os.makedirs(data_dir, exist_ok=True)

def fetch_with_cache():
    if os.path.exists(cache_file):
        df_cache = pd.read_csv(cache_file)
        # SELF-HEALING: If 'reports' is missing from cache, delete it and re-fetch
        if 'reports' in df_cache.columns:
            file_age = time.time() - os.path.getmtime(cache_file)
            if file_age < 86400:
                print(f"📦 Using valid cached data ({int(file_age/3600)}h old).")
                return df_cache
        else:
            print("⚠️ Cache is invalid (missing columns). Forcing refresh...")
            os.remove(cache_file)

    print("📡 Querying AbuseIPDB Blacklist...")
    api_key = os.getenv("ABUSEIPDB_API_KEY")
    url = 'https://api.abuseipdb.com/api/v2/blacklist'
    headers = {'Accept': 'application/json', 'Key': api_key}
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        if response.status_code == 200:
            df = pd.DataFrame(response.json().get('data', []))
            
            # Standardization
            if 'abuseConfidenceScore' in df.columns:
                df = df.rename(columns={'abuseConfidenceScore': 'score'})
            
            # Map reports field (AbuseIPDB often uses 'totalReports' or 'numReports')
            if 'totalReports' in df.columns:
                df = df.rename(columns={'totalReports': 'reports'})
            elif 'numReports' in df.columns:
                df = df.rename(columns={'numReports': 'reports'})
            else:
                df['reports'] = 1 

            df.to_csv(cache_file, index=False)
            return df
        else:
            print(f"❌ API Error {response.status_code}")
            return pd.DataFrame()
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return pd.DataFrame()

def run_analysis():
    df = fetch_with_cache()
    
    if df.empty or 'reports' not in df.columns:
        print("💡 No valid data to cluster.")
        return

    print("🧠 Clustering threat groups...")
    # Convert to numeric just in case CSV loaded them as strings
    df['reports'] = pd.to_numeric(df['reports'], errors='coerce').fillna(1)
    df['score'] = pd.to_numeric(df['score'], errors='coerce').fillna(0)

    kmeans = KMeans(n_clusters=3, n_init=10, random_state=42)
    df['threat_cluster'] = kmeans.fit_predict(df[['score', 'reports']])

    # Visualization logic remains the same...
    chart = alt.Chart(df.head(100)).mark_circle(size=200).encode(
        x=alt.X('reports:Q', title='Volume of Reports'),
        y=alt.Y('score:Q', title='Confidence Score'),
        color=alt.Color('threat_cluster:N', title='Cluster'),
        tooltip=['ipAddress', 'score', 'reports']
    ).properties(width='container', height=350, title='Malicious IP Clusters')

    chart.save(os.path.join(root_dir, 'docs/charts/project_02_honeypot.json'))
    print("✅ Analysis complete.")

if __name__ == "__main__":
    run_analysis()