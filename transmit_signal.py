import argparse
import os
import random
import sys
from datetime import datetime

base_dir = os.path.dirname(os.path.abspath(__file__))


def find_neuron_path(neuron_id):
    if 1 <= neuron_id <= 16340:
        # Cerebrum
        i = neuron_id - 1
        lobes = ["Frontal_Lobe", "Parietal_Lobe", "Occipital_Lobe", "Temporal_Lobe"]
        lobe_idx = i % len(lobes)
        gyrus_idx = (i // len(lobes)) % 10
        col_idx = (i // (len(lobes) * 10)) % 10
        return os.path.join(
            base_dir,
            "1_Cerebrum",
            lobes[lobe_idx],
            f"Gyrus_{gyrus_idx + 1}",
            f"Column_{col_idx + 1}",
            f"Neuron_{neuron_id}",
        ), "Cerebrum"
    elif 16341 <= neuron_id <= 85140:
        # Cerebellum
        i = neuron_id - 16341
        lobule_idx = i % 10
        zone_idx = (i // 10) % 10
        microzone_idx = (i // 100) % 10
        return os.path.join(
            base_dir,
            "2_Cerebellum",
            f"Lobule_{lobule_idx + 1}",
            f"Zone_{zone_idx + 1}",
            f"Microzone_{microzone_idx + 1}",
            f"Neuron_{neuron_id}",
        ), "Cerebellum"
    elif 85141 <= neuron_id <= 85484:
        # Brainstem
        parts = ["Midbrain", "Pons", "Medulla_Oblongata"]
        i = neuron_id - 85141
        part_idx = i % len(parts)
        nucleus_idx = (i // len(parts)) % 5
        return os.path.join(
            base_dir,
            "3_Brainstem",
            parts[part_idx],
            f"Nucleus_{nucleus_idx + 1}",
            f"Neuron_{neuron_id}",
        ), "Brainstem"
    elif 85485 <= neuron_id <= 85742:
        # Limbic System
        parts = ["Hippocampus", "Amygdala", "Cingulate_Gyrus"]
        i = neuron_id - 85485
        part_idx = i % len(parts)
        nucleus_idx = (i // len(parts)) % 5
        return os.path.join(
            base_dir,
            "4_Limbic_System",
            parts[part_idx],
            f"Subnucleus_{nucleus_idx + 1}",
            f"Neuron_{neuron_id}",
        ), "Limbic System"
    elif 85743 <= neuron_id <= 86000:
        # Diencephalon
        parts = ["Thalamus", "Hypothalamus", "Epithalamus"]
        i = neuron_id - 85743
        part_idx = i % len(parts)
        nucleus_idx = (i // len(parts)) % 5
        return os.path.join(
            base_dir,
            "5_Diencephalon",
            parts[part_idx],
            f"Nucleus_{nucleus_idx + 1}",
            f"Neuron_{neuron_id}",
        ), "Diencephalon"
    return None, "Unknown"


def get_synapses(neuron_id):
    # Seed random with neuron_id to make connections deterministic but organic
    random.seed(neuron_id)
    connections = []

    # 1. Local connection (same column/microzone/nucleus)
    # Connects to 1 or 2 neighboring neurons
    num_local = random.randint(1, 2)
    for _ in range(num_local):
        local_offset = random.choice([-2, -1, 1, 2])
        neighbor = neuron_id + local_offset
        if 1 <= neighbor <= 86000:
            connections.append(neighbor)

    # 2. Regional projection (connects to another region)
    # Cerebrum projects to Cerebellum or Diencephalon (Thalamus)
    if neuron_id <= 16340:
        # Thalamus (Diencephalon) is a major sensory relay
        thalamus_neuron = random.randint(85743, 86000)
        connections.append(thalamus_neuron)
    # Cerebellum projects to Brainstem or Cerebrum
    elif 16341 <= neuron_id <= 85140:
        cerebrum_neuron = random.randint(1, 16340)
        connections.append(cerebrum_neuron)
    # Brainstem projects to Cerebrum or Cerebellum
    elif 85141 <= neuron_id <= 85484:
        cerebellum_neuron = random.randint(16341, 85140)
        connections.append(cerebellum_neuron)
    # Limbic System projects to Cerebrum
    elif 85485 <= neuron_id <= 85742 or 85743 <= neuron_id <= 86000:
        cerebrum_neuron = random.randint(1, 16340)
        connections.append(cerebrum_neuron)

    return list(set(connections))


def cleanup_signals():
    print("[Clean] Cleaning up all signal files in E:\\rgai brain...")
    count = 0
    for root, dirs, files in os.walk(base_dir):
        if "signal.txt" in files:
            file_path = os.path.join(root, "signal.txt")
            try:
                os.remove(file_path)
                count += 1
            except Exception as e:
                print(f"Error removing {file_path}: {e}")
    print(f"[Done] Cleared {count} signal.txt files successfully.")


def run_simulation(start_id, message, max_hops):
    print("[Brain] Starting Neural Synaptic Communication...")
    print(f"Start Neuron: Neuron_{start_id}")
    print(f"Signal Message: '{message}'")
    print(f"Max Hops: {max_hops}\n")

    visited = set()
    queue = [
        (start_id, 0, f"Start (Neuron_{start_id})")
    ]  # (neuron_id, hop_count, path_string)

    steps = []

    while queue:
        current_id, hop, path_str = queue.pop(0)
        if current_id in visited or hop > max_hops:
            continue

        visited.add(current_id)
        path, region = find_neuron_path(current_id)

        if not path:
            continue

        # Write the signal file to represent communication
        signal_file = os.path.join(path, "signal.txt")
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]

        try:
            with open(signal_file, "w", encoding="utf-8") as f:
                f.write("--- Action Potential (Signal) ---\n")
                f.write(f"Timestamp: {timestamp}\n")
                f.write(f"Neuron ID: Neuron_{current_id}\n")
                f.write(f"Brain Region: {region}\n")
                f.write(f"Hop Count: {hop}\n")
                f.write(f"Signal Message: {message}\n")
                f.write(f"Transmission Path: {path_str}\n")
                f.write(f"Folder Path: {path}\n")
        except Exception as e:
            print(f"Error writing signal to {path}: {e}")

        steps.append((hop, current_id, region, path))

        # Get synaptic connections for next hop
        if hop < max_hops:
            synapses = get_synapses(current_id)
            for target_id in synapses:
                if target_id not in visited:
                    next_path_str = f"{path_str} -> Neuron_{target_id}"
                    queue.append((target_id, hop + 1, next_path_str))

    # Display the communication flow
    print("SIGNAL PROPAGATION PATHWAY:")
    for hop, n_id, reg, folder in steps:
        indent = "  " * hop
        arrow = "|-- [Signal] " if hop > 0 else "[Start] "
        print(
            f"{indent}{arrow}[Neuron_{n_id} in {reg}] (Signal file written: {os.path.basename(folder)}\\signal.txt)"
        )

    print(f"\nTotal neurons activated: {len(steps)}")
    print(
        f"Created signal.txt files in all {len(steps)} folders to log active communication."
    )


def main():
    parser = argparse.ArgumentParser(
        description="Simulate synaptic communication between brain folder neurons."
    )
    parser.add_argument(
        "--start", type=int, default=1, help="Starting neuron ID (1 - 86000)"
    )
    parser.add_argument(
        "--message",
        type=str,
        default="Action Potential Triggered",
        help="Signal message",
    )
    parser.add_argument(
        "--hops", type=int, default=3, help="Number of hops/levels of transmission"
    )
    parser.add_argument(
        "--cleanup", action="store_true", help="Delete all signal.txt files"
    )

    args = parser.parse_args()

    if args.cleanup:
        cleanup_signals()
    else:
        if not (1 <= args.start <= 86000):
            print("Error: Starting neuron ID must be between 1 and 86000.")
            sys.exit(1)
        run_simulation(args.start, args.message, args.hops)


if __name__ == "__main__":
    main()
