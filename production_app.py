# Roshan Kumar Sah's Digital Brain - Production FastAPI Server
# Location: Root / production_app.py

import os
import sys
import json
import subprocess
from fastapi import FastAPI, Query, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware

# Prevent console crashes due to encoding errors on cloud shells
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

base_dir = os.path.dirname(os.path.abspath(__file__))

# Insert paths to allow importing sub-modules
sys.path.append(base_dir)
sys.path.append(os.path.join(base_dir, "4_Limbic_System"))
sys.path.append(os.path.join(base_dir, "2_Cerebellum"))

try:
    from brain_kernel import process_query, load_neuroplasticity_weights
except ImportError as e:
    print(f"[Production Error] Failed to import brain kernel: {e}")

# Initialize FastAPI application
app = FastAPI(
    title="Roshan's Digital Brain API",
    description="Veda-Akasha Stack Core API for cognitive and RAG processing.",
    version="1.0.0"
)

# Enable CORS for public frontend domains (Vercel, Netlify, etc.)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, replace with your specific frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 1. Page Endpoint: Serve Web Dashboard
@app.get("/", response_class=HTMLResponse)
async def get_dashboard():
    html_path = os.path.join(base_dir, "2_Cerebellum", "dashboard.html")
    if os.path.exists(html_path):
        try:
            with open(html_path, "r", encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to read dashboard: {e}")
    raise HTTPException(status_code=404, detail="dashboard.html not found under Cerebellum.")

# 2. API Endpoint: Get Neuroplasticity Stats
@app.get("/api/stats")
async def get_stats():
    try:
        weights = load_neuroplasticity_weights()
        return JSONResponse(content=weights)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 3. API Endpoint: Get Connected Projects list
@app.get("/api/projects")
async def get_projects():
    projects_dir = os.path.join(base_dir, "1_Cerebrum", "Frontal_Lobe", "Projects")
    projects = []
    if os.path.exists(projects_dir):
        try:
            projects = [p for p in os.listdir(projects_dir) if not p.startswith('.')]
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    return JSONResponse(content=projects)

# 4. API Endpoint: Query the Brain
@app.get("/api/query")
async def query_brain(q: str = Query(..., description="Query prompt to process")):
    try:
        result = process_query(q)
        return JSONResponse(content=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 5. API Endpoint: Run Synaptic Simulator
@app.get("/api/simulate")
async def run_simulation(start: int = Query(1, description="Starting Neuron ID (1-86000)")):
    signal_script = os.path.join(base_dir, "transmit_signal.py")
    if not os.path.exists(signal_script):
        raise HTTPException(status_code=404, detail="transmit_signal.py script not found.")
        
    try:
        cmd = f'python "{signal_script}" --start {start} --message "Production_Cloud_Pulse" --hops 3'
        res = subprocess.run(cmd, shell=True, capture_output=True, text=True, encoding='utf-8', errors='replace')
        return JSONResponse(content={"output": res.stdout})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Running the app locally or in cloud
if __name__ == "__main__":
    import uvicorn
    # Bind to host 0.0.0.0 and dynamic port provided by cloud host environment
    port = int(os.environ.get("PORT", 8080))
    print(f"[Production] Starting Uvicorn server on port {port}...")
    uvicorn.run("production_app:app", host="0.0.0.0", port=port, reload=False)
