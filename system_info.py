#!/usr/bin/env python3
"""Script to display system information: CPUs, GPUs, and RAM."""

import os
import subprocess


def get_cpu_info():
    """Get CPU count and info."""
    cpu_count = os.cpu_count()

    # Try to get CPU model name on Linux
    cpu_model = None
    try:
        with open('/proc/cpuinfo', 'r') as f:
            for line in f:
                if line.startswith('model name'):
                    cpu_model = line.split(':')[1].strip()
                    break
    except FileNotFoundError:
        pass

    return cpu_count, cpu_model


def get_memory_info():
    """Get RAM information in GB."""
    try:
        with open('/proc/meminfo', 'r') as f:
            for line in f:
                if line.startswith('MemTotal'):
                    # Value is in kB
                    mem_kb = int(line.split()[1])
                    mem_gb = mem_kb / (1024 * 1024)
                    return mem_gb
    except FileNotFoundError:
        pass

    return None


def get_gpu_info():
    """Get GPU information using nvidia-smi if available."""
    gpus = []

    # Try nvidia-smi for NVIDIA GPUs
    try:
        result = subprocess.run(
            ['nvidia-smi', '--query-gpu=name,memory.total', '--format=csv,noheader,nounits'],
            capture_output=True, text=True, timeout=10
        )
        if result.returncode == 0:
            for line in result.stdout.strip().split('\n'):
                if line:
                    parts = line.split(', ')
                    name = parts[0]
                    memory = f"{int(parts[1])} MB" if len(parts) > 1 else "Unknown"
                    gpus.append({'name': name, 'memory': memory})
    except (FileNotFoundError, subprocess.TimeoutExpired):
        pass

    # Try lspci as fallback
    if not gpus:
        try:
            result = subprocess.run(
                ['lspci'], capture_output=True, text=True, timeout=10
            )
            if result.returncode == 0:
                for line in result.stdout.split('\n'):
                    if 'VGA' in line or '3D controller' in line:
                        gpus.append({'name': line.split(': ')[-1], 'memory': 'Unknown'})
        except (FileNotFoundError, subprocess.TimeoutExpired):
            pass

    return gpus


def main():
    print("=" * 50)
    print("SYSTEM INFORMATION")
    print("=" * 50)

    # CPU Info
    cpu_count, cpu_model = get_cpu_info()
    print(f"\nCPUs: {cpu_count}")
    if cpu_model:
        print(f"  Model: {cpu_model}")

    # Memory Info
    mem_gb = get_memory_info()
    print(f"\nRAM: {mem_gb:.1f} GB" if mem_gb else "\nRAM: Unknown")

    # GPU Info
    gpus = get_gpu_info()
    print(f"\nGPUs: {len(gpus)}")
    if gpus:
        for i, gpu in enumerate(gpus):
            print(f"  [{i}] {gpu['name']} ({gpu['memory']})")
    else:
        print("  No GPUs detected")

    print("=" * 50)


if __name__ == '__main__':
    main()
