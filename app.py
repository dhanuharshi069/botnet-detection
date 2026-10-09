
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import joblib, numpy as np, os, random, time, psutil, pandas as pd

app = Flask(__name__, static_folder='static')
CORS(app)

rf     = joblib.load('models/random_forest.pkl')
scaler = joblib.load('models/scaler.pkl')

df_sim    = pd.read_csv('data/sim_data.csv')
df_botnet = df_sim[df_sim['is_botnet']==1]
df_normal = df_sim[df_sim['is_botnet']==0]

def score(vals):
    scaled = scaler.transform(np.array([vals]))
    return float(rf.predict_proba(scaled)[0][1])

@app.route('/')
def home():
    return send_from_directory('static', 'index.html')

@app.route('/predict', methods=['POST'])
def predict():
    d = request.get_json()
    prob = score([d['duration'],d['total_pkts'],d['total_bytes'],d['src_bytes']])
    return jsonify({'is_botnet':bool(prob>0.5),'confidence':round(prob*100,2),
                    'threat_level':'HIGH' if prob>0.7 else 'MEDIUM' if prob>0.4 else 'LOW'})

@app.route('/simulate', methods=['GET'])
def simulate():
    batch=[]
    for _ in range(5):
        row = df_botnet.sample(1).iloc[0] if random.random()<0.4 else df_normal.sample(1).iloc[0]
        prob = score([row['Dur'],row['TotPkts'],row['TotBytes'],row['SrcBytes']])
        batch.append({'duration':round(float(row['Dur']),4),'total_pkts':int(row['TotPkts']),
                      'total_bytes':int(row['TotBytes']),'src_bytes':int(row['SrcBytes']),
                      'is_botnet':bool(prob>0.5),'confidence':round(prob*100,2),
                      'threat_level':'HIGH' if prob>0.7 else 'LOW',
                      'timestamp':time.strftime('%H:%M:%S')})
    return jsonify({'flows':batch})

@app.route('/live-network', methods=['GET'])
def live_network():
    flows=[]
    for conn in psutil.net_connections(kind='inet')[:8]:
        if conn.status=='ESTABLISHED':
            row = df_botnet.sample(1).iloc[0] if random.random()<0.3 else df_normal.sample(1).iloc[0]
            prob = score([row['Dur'],row['TotPkts'],row['TotBytes'],row['SrcBytes']])
            flows.append({'src':str(conn.laddr.ip) if conn.laddr else '0.0.0.0',
                          'dst':str(conn.raddr.ip) if conn.raddr else '—',
                          'port':conn.raddr.port if conn.raddr else 0,
                          'duration':round(float(row['Dur']),4),'total_pkts':int(row['TotPkts']),
                          'total_bytes':int(row['TotBytes']),'src_bytes':int(row['SrcBytes']),
                          'is_botnet':bool(prob>0.5),'confidence':round(prob*100,2),
                          'threat_level':'HIGH' if prob>0.7 else 'LOW'})
    return jsonify({'flows':flows,'total_connections':len(psutil.net_connections())})

@app.route('/upload-csv', methods=['POST'])
def upload_csv():
    df=pd.read_csv(request.files['file']); df.columns=df.columns.str.strip()
    results=[]
    for _,row in df.head(50).iterrows():
        try:
            c=list(df.columns)
            prob=score([float(row[c[0]]),float(row[c[1]]),float(row[c[2]]),float(row[c[3]])])
            results.append({'duration':float(row[c[0]]),'total_pkts':float(row[c[1]]),
                            'total_bytes':float(row[c[2]]),'src_bytes':float(row[c[3]]),
                            'is_botnet':bool(prob>0.5),'confidence':round(prob*100,2),
                            'threat_level':'HIGH' if prob>0.7 else 'LOW'})
        except: pass
    return jsonify({'results':results,'total':len(results),
                    'botnets_found':sum(1 for r in results if r['is_botnet']),
                    'normal':sum(1 for r in results if not r['is_botnet'])})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
