import sys
import os
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
from fastapi.testclient import TestClient

backend_path = os.path.abspath(os.path.join(os.getcwd(), 'PBL', '03_Source_Code', 'backend'))
if backend_path not in sys.path:
    sys.path.insert(0, backend_path)

from app.main import app
from app.auth import AuthService

client = TestClient(app)

tokens = {
    "Administrator": AuthService.create_access_token({"sub": "etmin_ludwik", "role": "admin"}),
    "Dosen": AuthService.create_access_token({"sub": "dosen_ojan", "role": "dosen"}),
    "Mahasiswa": AuthService.create_access_token({"sub": "mhs_arip", "role": "mahasiswa"}),
    "Unauthenticated": "invalid_token_123"
}

endpoints = [
    {"name": "Melihat\nLowongan", "path": "/lowongan/", "method": "GET"},
    {"name": "Membuat\nLowongan", "path": "/lowongan/", "method": "POST", "json": {
        "judul": "Test", "perusahaan": "Test", "lokasi": "Test", "tipe_pekerjaan": "Full-time", 
        "deskripsi": "Test", "persyaratan": "Test", "batas_lamaran": "2026-12-31"
    }},
    {"name": "Rekap Semua\nLamaran", "path": "/lamaran/all", "method": "GET"},
    {"name": "Ubah Status\nLamaran", "path": "/lamaran/1/status", "method": "PUT", "json": {"status_lamaran": "Diterima"}}
]

roles = list(tokens.keys())
endpoint_names = [ep["name"] for ep in endpoints]
results_matrix = []

for role in roles:
    row = []
    for ep in endpoints:
        headers = {"Authorization": f"Bearer {tokens[role]}"}
        if ep["method"] == "GET":
            res = client.get(ep["path"], headers=headers)
        elif ep["method"] == "POST":
            res = client.post(ep["path"], headers=headers, json=ep.get("json", {}))
        elif ep["method"] == "PUT":
            res = client.put(ep["path"], headers=headers, json=ep.get("json", {}))
        
        row.append(0 if res.status_code in [401, 403] else 1)
    results_matrix.append(row)

df = pd.DataFrame(results_matrix, columns=endpoint_names, index=roles)
annot_df = df.replace({1: 'Diizinkan', 0: 'Ditolak'})

plt.figure(figsize=(9, 4))
sns.set_theme(style="white")

from matplotlib.colors import ListedColormap
cmap = ListedColormap(['#ffebee', '#e8f5e9'])

ax = sns.heatmap(df, annot=annot_df, fmt="", cmap=cmap, cbar=False, 
                 linewidths=2, linecolor='white', annot_kws={"size": 11, "weight": "bold"})

for t, val in zip(ax.texts, df.values.flatten()):
    if val == 1:
        t.set_color('#2e7d32')
    else:
        t.set_color('#c62828')

plt.title("Hasil Pengujian Otorisasi REST API per Peran (RBAC)", pad=20, fontsize=13, fontweight='bold')
plt.xticks(fontsize=11)
plt.yticks(fontsize=11, rotation=0)

output_png = r"f:\KI_PBL\PBL\02_Design_Documents\rbac_matrix.png"
plt.savefig(output_png, dpi=300, bbox_inches='tight')
print(f"Graph saved to {output_png}")