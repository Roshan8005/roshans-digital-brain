# Roshan Kumar Sah's Digital Brain Interactive Terminal Dashboard
# Location: Root / brain_console.py

import os
import sys
import subprocess

# Prevent console crashes due to unicode/emoji characters on Windows cmd/powershell
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

from brain_kernel import process_query, load_neuroplasticity_weights

base_dir = r"E:\rgai brain"

def print_help():
    print("\nAvailable Commands:")
    print("  /query <prompt>     - Search the brain's knowledge base and read memories")
    print("  /veda <mantra>      - Run Roshan's VedaKernel logic calculation and system status")
    print("  /simulate <num>     - Run synaptic signal propagation starting from a Neuron (1-86000)")
    print("  /stats              - View brain neuroplasticity ranks and region weights")
    print("  /cleanup            - Clear all temporary signal files on the E drive")
    print("  /help               - Show this help list")
    print("  /exit               - Close the brain session")

def show_stats():
    weights = load_neuroplasticity_weights()
    print("\n==================================================")
    print("🧠 BRAIN REGION NEUROPLASTICITY WEIGHTS")
    print("==================================================")
    
    # Sort regions by weights to show ranks
    sorted_weights = sorted(weights.items(), key=lambda x: x[1], reverse=True)
    
    for rank, (region, weight) in enumerate(sorted_weights, 1):
        # Progress bar representation
        bar = "#" * min(weight, 20)
        print(f"Rank {rank}: {region:<16} | Weight: {weight:<4} [{bar:<20}]")
    print("==================================================")

def main():
    print("==================================================")
    print("🧠 ROSHAN'S DIGITAL BRAIN CONSOLE v1.0.0")
    print("==================================================")
    print("System active and secure. Powered by Google DeepMind Antigravity.")
    print("Type /help to see all commands.")
    print("==================================================")
    
    while True:
        try:
            user_input = input("\nbrain> ").strip()
            if not user_input:
                continue
                
            if user_input.startswith("/"):
                # Handle Slash Commands
                parts = user_input.split(" ", 1)
                cmd = parts[0].lower()
                arg = parts[1].strip() if len(parts) > 1 else ""
                
                if cmd == "/exit":
                    print("Shutting down brain session... Goodbye Roshan!")
                    break
                    
                elif cmd == "/help":
                    print_help()
                    
                elif cmd == "/stats":
                    show_stats()
                    
                elif cmd == "/cleanup":
                    signal_script = os.path.join(base_dir, "transmit_signal.py")
                    if os.path.exists(signal_script):
                        subprocess.run(f'python "{signal_script}" --cleanup', shell=True)
                    else:
                        print("[Error] Signal script transmit_signal.py not found.")
                        
                elif cmd == "/simulate":
                    if not arg.isdigit():
                        print("[Error] /simulate requires a numeric Neuron ID (e.g. /simulate 1)")
                        continue
                    neuron_id = int(arg)
                    if not (1 <= neuron_id <= 86000):
                        print("[Error] Neuron ID must be between 1 and 86000.")
                        continue
                        
                    signal_script = os.path.join(base_dir, "transmit_signal.py")
                    if os.path.exists(signal_script):
                        print(f"Propagating signal from Neuron_{neuron_id}...")
                        subprocess.run(f'python "{signal_script}" --start {neuron_id} --message "Console_Triggered_Signal"', shell=True)
                    else:
                        print("[Error] Signal script transmit_signal.py not found.")
                        
                elif cmd == "/query":
                    if not arg:
                        print("[Error] /query requires a search prompt (e.g. /query radiology)")
                        continue
                    res = process_query(arg)
                    print(f"\n[Status]: {res['status']}")
                    if "activated_regions" in res and res["activated_regions"]:
                        print(f"[Activated Lobes]: {', '.join(res['activated_regions'])}")
                    print(f"\n{res['response']}")
                    
                elif cmd == "/veda":
                    if not arg:
                        print("[Error] /veda requires a mantra input (e.g. /veda Agnimile)")
                        continue
                    res = process_query(user_input)
                    print(f"\n[Status]: {res['status']}")
                    print(f"\n{res['response']}")
                    
                else:
                    print(f"Unknown command: '{cmd}'. Type /help for assistance.")
            else:
                # Default behavior is querying
                res = process_query(user_input)
                print(f"\n[Status]: {res['status']}")
                if "activated_regions" in res and res["activated_regions"]:
                    print(f"[Activated Lobes]: {', '.join(res['activated_regions'])}")
                print(f"\n{res['response']}")
                
        except (KeyboardInterrupt, EOFError):
            print("\nShutting down brain session... Goodbye Roshan!")
            break

if __name__ == "__main__":
    main()
