# 🧠 Roshan's AI Brain - Cerebrum

Welcome to the **Cerebrum** module of **Roshan's AI Brain Project**. The Cerebrum is the largest part of the brain and is responsible for high-level cognitive functions.

---

## 🌟 Anatomy of Roshan's Cerebrum Folder

This directory contains **16,340 folder-based Neurons** (Neuron_1 to Neuron_16340) organized structurally as follows:

```
1_Cerebrum/
├── Frontal_Lobe/
│   ├── Gyrus_1...10/
│   │   └── Column_1...10/
│   │       └── Neuron_X/
├── Parietal_Lobe/
├── Occipital_Lobe/
└── Temporal_Lobe/
```

### 🧠 Functional Regions of the Lobes:
1. **Frontal Lobe**: Decisions, motor control, reasoning, and personality.
2. **Parietal Lobe**: Sensory processing (touch, temperature, pain) and spatial awareness.
3. **Occipital Lobe**: Visual processing.
4. **Temporal Lobe**: Auditory processing, memory, and language interpretation.

---

## ⚡ Synaptic Communication System

To simulate how biological neurons communicate via electrical signals (action potentials), a neurotransmitter signal script has been deployed in the root folder: `E:\rgai brain\transmit_signal.py`.

### 🔗 How Folders Communicate:
Each folder (neuron) is connected to neighboring neuron folders (columns/gyri) and projects to other brain parts (like the Cerebellum or Thalamus).

#### Running a Communication Simulation:
Open PowerShell and run the following command to trigger a neural signal from `Neuron_1`:
```powershell
python "E:\rgai brain\transmit_signal.py" --start 1 --message "Trigger sensory input" --hops 4
```

This will:
1. Find `Neuron_1` folder in `1_Cerebrum`.
2. Write a `signal.txt` (Action Potential) inside it.
3. Transmit the signal to connected folders in the **Cerebellum** or **Diencephalon**, writing `signal.txt` in those sub-folders.
4. Print a beautiful trace of the neural pathway in the console.

To clean up all active signals on the drive, run:
```powershell
python "E:\rgai brain\transmit_signal.py" --cleanup
```

---
> [!NOTE]
> Created by Antigravity AI assistant for Roshan's AI Brain Project.
