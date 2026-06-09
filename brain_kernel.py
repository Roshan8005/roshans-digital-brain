# Roshan Kumar Sah's Digital Brain Kernel
# Location: Root / brain_kernel.py

import os
import sys
import json
import urllib.request
import urllib.error
from datetime import datetime

# Prevent console crashes due to unicode/emoji characters on Windows cmd/powershell
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

base_dir = os.path.dirname(os.path.abspath(__file__))

# Insert paths to allow importing from sub-modules
sys.path.append(os.path.join(base_dir, "4_Limbic_System"))
sys.path.append(os.path.join(base_dir, "2_Cerebellum"))
sys.path.append(os.path.join(base_dir, "1_Cerebrum", "Frontal_Lobe", "Projects", "RGAI-1_Vedic_Kernel"))

try:
    from Amygdala import security_guard
    from memory_retrieval import search_memory
    from ingest_knowledge import check_and_update
except ImportError as e:
    print(f"[Kernel Warning] Failed to import sub-modules: {e}")

# Initialize Roshan's VedaKernel in Brahman-Mode (Root custodian)
veda_kernel = None
try:
    import veda_core
    print("[Kernel] Activating Roshan's VedaKernel...")
    veda_kernel = veda_core.VedaKernel()
    veda_kernel.connect_to_akasha()
    veda_kernel.sync_user("Roshan Kumar Sah")
except Exception as e:
    print(f"[Kernel Warning] Failed to load Roshan's VedaKernel: {e}")

WEIGHTS_FILE = os.path.join(base_dir, "4_Limbic_System", "neuroplasticity_weights.json")

_WEIGHTS_CACHE = None

def load_neuroplasticity_weights():
    global _WEIGHTS_CACHE
    if _WEIGHTS_CACHE is not None:
        return _WEIGHTS_CACHE
        
    if os.path.exists(WEIGHTS_FILE):
        try:
            with open(WEIGHTS_FILE, "r", encoding="utf-8") as f:
                _WEIGHTS_CACHE = json.load(f)
                return _WEIGHTS_CACHE
        except Exception:
            pass
            
    _WEIGHTS_CACHE = {
        "1_Cerebrum": 0,
        "2_Cerebellum": 0,
        "3_Brainstem": 0,
        "4_Limbic_System": 0,
        "5_Diencephalon": 0
    }
    return _WEIGHTS_CACHE

def save_neuroplasticity_weights(weights):
    global _WEIGHTS_CACHE
    _WEIGHTS_CACHE = weights
    try:
        with open(WEIGHTS_FILE, "w", encoding="utf-8") as f:
            json.dump(weights, f, indent=4)
    except Exception as e:
        print(f"[Kernel Warning] Failed to save neuroplasticity weights: {e}")

def call_ollama(prompt, context):
    """
    Attempts to call a local Ollama instance (defaulting to Llama3).
    Returns response string, or None if Ollama is offline.
    """
    url = "http://localhost:11434/api/generate"
    system_prompt = (
        "You are Roshan Kumar Sah's Digital Brain. You must answer questions using "
        "the provided folder memories context. Be precise, helpful, and scientific."
    )
    payload = {
        "model": "llama3",
        "prompt": f"Memory Context:\n{context}\n\nUser Question: {prompt}",
        "system": system_prompt,
        "stream": False
    }
    
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode('utf-8'),
        headers={'Content-Type': 'application/json'},
        method='POST'
    )
    try:
        with urllib.request.urlopen(req, timeout=5) as response:
            res_data = json.loads(response.read().decode('utf-8'))
            return res_data.get("response", "")
    except Exception:
        return None

def call_gemini_api(prompt, context):
    """
    Attempts to call the Gemini API securely if GEMINI_API_KEY environment variable is set.
    """
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        return None
        
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    system_instruction = (
        "You are Roshan Kumar Sah's Digital Brain (Antigravity). You must answer questions using "
        "the provided folder memories context from Roshan's laptop."
    )
    
    # Format according to Google Generative Language API
    payload = {
        "contents": [{
            "parts": [{
                "text": f"System Context:\n{system_instruction}\n\nMemory Context:\n{context}\n\nUser Question: {prompt}"
            }]
        }]
    }
    
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode('utf-8'),
        headers={'Content-Type': 'application/json'},
        method='POST'
    )
    try:
        with urllib.request.urlopen(req, timeout=8) as response:
            res_data = json.loads(response.read().decode('utf-8'))
            candidates = res_data.get("candidates", [])
            if candidates:
                parts = candidates[0].get("content", {}).get("parts", [])
                if parts:
                    return parts[0].get("text", "")
            return None
    except Exception as e:
        return None

def process_query(query_str):
    """
    Core cognitive execution pipeline.
    1. Runs Auto-Updater (Cerebellum)
    2. Runs Input Safety scan (Amygdala)
    3. Runs Memory Lookup (Cerebellum)
    4. Updates neuroplasticity weights
    5. Dispatches to LLM (Ollama -> Gemini -> Fallback)
    """
    # Removed synchronous check_and_update() for extreme performance.
    # The cache automatically loads the pre-compiled index.
    
    # Route to Veda Kernel if requested
    if query_str.startswith("/veda "):
        mantra = query_str[6:].strip()
        if veda_kernel:
            try:
                freq_report = veda_kernel.calculate_vak_frequency(mantra)
                # Redirect print outputs from report_system_status
                system_status = veda_kernel.report_system_status()
                
                response_text = (
                    f"[Veda Kernel Execution - Active Mode]\n"
                    f"Input Mantra: '{mantra}'\n"
                    f"Vak Frequency: {freq_report['vak_frequency_hz']} Hz ({freq_report['harmony_status']})\n"
                    f"Resonance Multiplier: {freq_report['resonance_multiplier']}x\n"
                    f"Potential Voltage: {freq_report['potential_voltage']}V\n"
                    f"Gate Capacity: {freq_report['gate_capacity']}\n"
                    f"--------------------------------------------------\n"
                    f"{system_status}"
                )
                return {
                    "status": "SUCCESS",
                    "threat_level": "NONE",
                    "activated_regions": ["1_Cerebrum"],
                    "memories_found": 0,
                    "response": response_text
                }
            except Exception as e:
                return {
                    "status": "ERROR",
                    "threat_level": "NONE",
                    "response": f"Veda Kernel execution failed: {e}"
                }
        else:
            return {
                "status": "ERROR",
                "threat_level": "NONE",
                "response": "Veda Kernel is offline or failed to initialize."
            }
            
    # Step 2: Safety scan via Amygdala
    safety_check = security_guard.check_input(query_str)
    if not safety_check["is_safe"]:
        return {
            "status": "BLOCKED",
            "threat_level": safety_check["threat_level"],
            "reason": safety_check["reason"],
            "response": f"[Blocked by Amygdala Safety Firewall] Your query was flagged as unsafe. Reason: {safety_check['reason']}"
        }
        
    # Step 3: Memory Retrieval via Cerebellum
    memories = search_memory(query_str, limit=3)
    
    # Step 4: Neuroplasticity & Weight Updates
    weights = load_neuroplasticity_weights()
    activated_regions = []
    
    if memories:
        for mem in memories:
            region = mem["region"]
            folder_region = None
            if region == "Cerebrum":
                folder_region = "1_Cerebrum"
            elif region == "Cerebellum":
                folder_region = "2_Cerebellum"
            elif region == "Brainstem":
                folder_region = "3_Brainstem"
            elif region == "Limbic_System":
                folder_region = "4_Limbic_System"
            elif region == "Diencephalon":
                folder_region = "5_Diencephalon"
                
            if folder_region and folder_region in weights:
                weights[folder_region] += 1
                if folder_region not in activated_regions:
                    activated_regions.append(folder_region)
        save_neuroplasticity_weights(weights)
        
    # Step 5: Formulate response using Roshan's VedaKernel & Akasha Stack
    if veda_kernel:
        try:
            freq_report = veda_kernel.calculate_vak_frequency(query_str)
            system_status = veda_kernel.report_system_status()
            
            # Format retrieved memories
            memory_text = ""
            if memories:
                for idx, mem in enumerate(memories, 1):
                    snippet = mem['snippet']
                    preview = snippet[:400] + "..." if len(snippet) > 400 else snippet
                    memory_text += f"Source: {mem['file_path']}\n{preview}\n\n"
            
            # Generate conversational response using Gemini or Ollama
            ai_reply = call_gemini_api(query_str, memory_text)
            if not ai_reply:
                ai_reply = call_ollama(query_str, memory_text)
            
            if not ai_reply:
                ai_reply = "VedaKernel is currently running in pure memory mode (No LLM active). I found these memories but cannot formulate a conversational reply."

            response_text = (
                f"{ai_reply}\n\n"
                f"***\n"
                f"**[Akasha-Vedic Core Metrics]**\n"
                f"• Resonance: {freq_report['vak_frequency_hz']} Hz ({freq_report['harmony_status']})\n"
                f"• Potential: {freq_report['potential_voltage']}V | Gate: {freq_report['gate_capacity']}\n"
            )
            
            if memories:
                response_text += f"\n**[Memory Pathways Activated]**\n"
                for mem in memories:
                    response_text += f"- `{mem['file_path']}` (Lobe: {mem['region']})\n"
        except Exception as e:
            response_text = f"[Veda Kernel Error] Failed during core cognitive execution: {e}"
    else:
        # Fallback if VedaKernel is offline
        if memories:
            primary_match = memories[0]
            preview = primary_match["snippet"]
            preview = preview[:500] + "..." if len(preview) > 500 else preview
            response_text = (
                f"[Local Memory Preview - Veda Offline]\n"
                f"Source: {primary_match['file_path']}\n"
                f"--------------------------------------------------\n"
                f"{preview}\n"
                f"--------------------------------------------------"
            )
        else:
            response_text = "[No direct memory match found] Please feed relevant documents into the system."
            
    return {
        "status": "SUCCESS",
        "threat_level": "NONE",
        "activated_regions": activated_regions,
        "memories_found": len(memories),
        "response": response_text
    }

if __name__ == "__main__":
    print(process_query("What is the history of radiology?"))
