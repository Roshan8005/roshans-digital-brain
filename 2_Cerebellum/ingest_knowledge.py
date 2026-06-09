import os
import json
from datetime import datetime

import os
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
memory_file = os.path.join(base_dir, "4_Limbic_System", "Hippocampus", "knowledge_index.json")

# Directories to ignore during scanning
IGNORE_DIRS = {'.git', 'node_modules', 'venv', '.gradle', '.idea', 'bin', 'obj', 'dist', 'build', '__pycache__', 'target', 'out'}
VALID_EXTENSIONS = (".txt", ".md", ".json", ".py")

def scan_and_index():
    print("[Cerebellum] Scanning brain folders for new knowledge...")
    index = {}
    
    for root, dirs, files in os.walk(base_dir, followlinks=True):
        # Filter directories in-place to prevent entering ignored ones
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
        
        # Skip index and weights files
        if "knowledge_index.json" in files:
            files.remove("knowledge_index.json")
        if "neuroplasticity_weights.json" in files:
            files.remove("neuroplasticity_weights.json")
            
        for file in files:
            if file.endswith(VALID_EXTENSIONS):
                file_path = os.path.join(root, file)
                rel_path = os.path.relpath(file_path, base_dir)
                
                # Identify region based on path
                region = "General"
                if "1_Cerebrum" in rel_path:
                    region = "Cerebrum"
                elif "2_Cerebellum" in rel_path:
                    region = "Cerebellum"
                elif "3_Brainstem" in rel_path:
                    region = "Brainstem"
                elif "4_Limbic_System" in rel_path:
                    region = "Limbic_System"
                elif "5_Diencephalon" in rel_path:
                    region = "Diencephalon"
                
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read()
                        
                    index[rel_path] = {
                        "region": region,
                        "filename": file,
                        "last_updated": datetime.fromtimestamp(os.path.getmtime(file_path)).strftime("%Y-%m-%d %H:%M:%S"),
                        "snippet": content
                    }
                except Exception as e:
                    print(f"Failed to read {rel_path}: {e}")
                    
    # Write the compiled index to Hippocampus
    os.makedirs(os.path.dirname(memory_file), exist_ok=True)
    with open(memory_file, "w", encoding="utf-8") as f:
        json.dump(index, f, indent=4)
        
    print(f"[Done] Successfully built brain memory index! Saved to {memory_file}")

def check_and_update():
    """
    Checks if any file has been modified after the index file was created.
    If yes, triggers scan_and_index() automatically.
    """
    if not os.path.exists(memory_file):
        scan_and_index()
        return
        
    index_time = os.path.getmtime(memory_file)
    needs_update = False
    
    for root, dirs, files in os.walk(base_dir, followlinks=True):
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
        
        for file in files:
            if file.endswith(VALID_EXTENSIONS) and file not in ("knowledge_index.json", "neuroplasticity_weights.json"):
                file_path = os.path.join(root, file)
                # Check modification time
                if os.path.getmtime(file_path) > index_time:
                    needs_update = True
                    break
        if needs_update:
            break
            
    if needs_update:
        print("[Auto-Updater] Changes detected in brain folders. Updating index...")
        scan_and_index()
    else:
        # Index is already up to date
        pass

if __name__ == "__main__":
    scan_and_index()
