import joblib
import matplotlib.pyplot as plt
import tabulate
import yaml


def gen_report():
    jobs = []

    yield "<!-- WARNING, this file is generated by report.py. MANUAL CHANGES WILL BE LOST -->"
    yield ""
    yield "Just following allong [this great parallel optimization case study](https://ppc.cs.aalto.fi/ch2/)."
    yield ""
    yield "# V0"
    with open("v0.yml") as f:
        v0_benchmarks = yaml.load(f, Loader=yaml.Loader)
    yield ""
    table = []
    ns = []
    durations = []
    for benchmark in v0_benchmarks:
        n = benchmark["n"]
        duration = benchmark["duration"]["nanoseconds"] / 1e9
        table.append([n, f"{duration}s"])
        ns.append(n)
        durations.append(duration)
    yield from tabulate.tabulate(table, headers=["Size", "Duration"], tablefmt="github").splitlines()
    yield ""
    yield "![V0](v0.png)"

    jobs.append(joblib.delayed(make_duration_vs_n)(ns, durations, "v0.png"))

    joblib.Parallel(n_jobs=-1)(jobs)


def make_duration_vs_n(ns, durations, file_name):
    fig, ax = plt.subplots(1, 1, figsize=(12, 4), layout="constrained")

    ax.plot(ns, durations, ".-")
    ax.set_title("Duration vs. size")
    ax.set_xlim(left=0)
    ax.set_xlabel("Size")
    ax.set_ylim(bottom=0)
    ax.set_ylabel("Duration (s)")

    fig.savefig(file_name, dpi=300)
    plt.close(fig)

if __name__ == "__main__":
    for line in gen_report():
        print(line)
