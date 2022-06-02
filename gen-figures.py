import os
import re
import sys

import joblib
import matplotlib.pyplot as plt
import matplotlib.ticker
import yaml


def main(file_name):
    image_regex = re.compile(r"!\[.*\]\((.*)\)")
    jobs = []
    with open(file_name) as f:
        for line in f:
            m = image_regex.fullmatch(line.rstrip())
            if m:
                jobs.append(joblib.delayed(generate)(m.group(1)))
    joblib.Parallel(n_jobs=-1)(jobs)


def generate(file_name):
    print(f"Generating {file_name}")

    base_name, ext = os.path.splitext(file_name)
    assert ext == ".png"
    if base_name.startswith("cpu-size-") or base_name.startswith("gpu-size-"):
        processor = base_name[0:3]
        suffix = "-seq" if processor == "cpu" else ""
        low_version, high_version = base_name[9:].split("-")
        low_version = int(low_version)
        high_version = int(high_version)

        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), layout="constrained")

        for version in range(low_version, high_version + 1):
            with open(f"build/{processor}-v{version}{suffix}.yml") as f:
                benchmarks = yaml.load(f, Loader=yaml.Loader)
                ns = []
                durations = []
                for benchmark in benchmarks:
                    ns.append(benchmark["n"])
                    durations.append(benchmark["duration"]["nanoseconds"] / 1e9)
                ax1.plot(ns, durations, '.-', label=f"Version {version}", color=f"C{version}")
                ax2.plot(ns, [2 * n ** 3 / duration / 1e9 for (n, duration) in zip(ns, durations)], ".-", label=f"Version {version}", color=f"C{version}")

        ax1.set_xlim(left=0, right=5000)
        ax1.set_xlabel("Size")
        ax1.set_ylim(bottom=0)
        ax1.set_ylabel("Duration (s)")
        ax1.legend()

        ax2.set_xlim(left=0, right=5000)
        ax2.set_xlabel("Size")
        ax2.set_ylim(bottom=0)
        ax2.set_ylabel("Billions of useful operations per second")
        ax2.legend()

        fig.savefig(file_name, dpi=300)
        plt.close(fig)
    elif base_name.startswith("cpu-paral-"):
        low_version, high_version, size = base_name[10:].split("-")
        low_version = int(low_version)
        high_version = int(high_version)
        size = int(size)

        versions = list(range(low_version, high_version + 1))
        flavors = {
            "seq": "Single-thread",
            "paral-4": "4 threads",
            "paral-14": "14 threads",
            "paral-28": "28 threads",
        }

        fig, axes = plt.subplots(1, 4, figsize=(12, 4), layout="constrained")
        for ax, flavor in zip(axes, flavors):
            ops = []
            for version in versions:
                with open(f"build/cpu-v{version}-{flavor}.yml") as f:
                    benchmarks = yaml.load(f, Loader=yaml.Loader)
                for benchmark in benchmarks:
                    if benchmark["n"] == size:
                        duration = benchmark["duration"]["nanoseconds"] / 1e9  # seconds
                        ops.append(2 * size ** 3 / duration / 1e9)  # billions ops/s

            ax.plot(versions, ops, ".-", color="c")
            ax.set_title(flavors[flavor])
            ax.set_ylim(bottom=0)
            ax.set_xlabel("Version")
            ax.set_xlim(left=low_version - 0.5, right=high_version + 0.5)
            ax.xaxis.set_major_locator(matplotlib.ticker.MaxNLocator(integer=True))


        for ax in axes:
            ax.set_ylim(top=axes[-1].get_ylim()[1])

        axes[0].set_ylabel("Billions of useful operations per second")

        fig.savefig(file_name, dpi=300)
        plt.close(fig)
    elif base_name.startswith("gpu-paral-"):
        low_version, high_version, size = base_name[10:].split("-")
        low_version = int(low_version)
        high_version = int(high_version)
        size = int(size)

        versions = list(range(low_version, high_version + 1))

        fig, ax = plt.subplots(1, 1, figsize=(12, 4), layout="constrained")
        ops = []
        for version in versions:
            with open(f"build/gpu-v{version}.yml") as f:
                benchmarks = yaml.load(f, Loader=yaml.Loader)
            for benchmark in benchmarks:
                if benchmark["n"] == size:
                    duration = benchmark["duration"]["nanoseconds"] / 1e9  # seconds
                    ops.append(2 * size ** 3 / duration / 1e9)  # billions ops/s

        ax.plot(versions, ops, ".-", color="c")
        ax.set_ylim(bottom=0)
        ax.set_xlabel("Version")
        ax.set_xlim(left=low_version - 0.5, right=high_version + 0.5)
        ax.xaxis.set_major_locator(matplotlib.ticker.MaxNLocator(integer=True))
        ax.set_ylabel("Billions of useful operations per second")

        fig.savefig(file_name, dpi=300)
        plt.close(fig)
    else:
        assert False


if __name__ == "__main__":
    main(sys.argv[1])
