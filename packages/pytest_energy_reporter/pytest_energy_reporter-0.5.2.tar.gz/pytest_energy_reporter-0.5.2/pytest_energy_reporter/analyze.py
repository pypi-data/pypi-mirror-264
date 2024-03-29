import argparse
import json
import os

import matplotlib.pyplot as plt
import numpy as np

from pytest_energy_reporter.util import print_table_str

if __name__ == "__main__":
  parser = argparse.ArgumentParser(description="Visualize energy report measurements.")
  parser.add_argument('file_link', type=str, help='The relative path to the energy report file.')
  parser.add_argument('-s', '--save', type=str, help='The directory to save the visualization in. If not provided, the visualization will just be displayed without being saved.')

  args = parser.parse_args()
  file_path = os.path.join(os.getcwd(), args.file_link)
  
  print(f"File link: {file_path}")
  with open(file_path, 'r') as file:
    data = json.load(file)
  
  results = data["results"]
  _cases = results["cases"]
  
  _filtered_cases = [case for case in _cases if 'lambda' not in case["name"]]
  
  # cases = sorted(_filtered_cases, key=lambda x: np.mean(x["energy"]), reverse=True)
  cases = _filtered_cases
  
  ticks = [i + 1 for i in range(len(cases))]
  names = []
  for case in cases:
    name = case["name"]
    removed_postfix = name.split("::")[-1]
    remove_test = removed_postfix.split("test_")[-1]
    case_n = len(case["energy"])
    tick_name = f"{remove_test} (n={case_n})"
    names.append(tick_name)
  energies = [x["energy"] for x in cases]
  avg_energies = [np.mean(x["energy"]) for x in cases]
  powers = [x["power"] for x in cases]
  avg_powers = [np.mean(x["power"]) for x in cases]
  timing = [x["execution_time"] for x in cases]
  avg_timing = [np.mean(x["execution_time"]) for x in cases]
  edp = [[x * y / 1000 for (x, y) in zip(timing[i], energies[i])] for i in range(len(cases))]
  avg_edp = [np.mean(x) for x in edp]
  
  figures = [
    (energies, avg_energies, "Energy [J]", "figure_j"),
    (powers, avg_powers, "Power [W]", "figure_w"),
    (timing, avg_timing, "Time [ms]", "figure_t"),
    (edp, avg_edp, "Energy Delay Product [j s]", "figure_edp")
  ]
  
  # ----------------- Plotting -----------------
  for figure in figures:
    dist, avg, label, pth = figure
    fig = plt.figure()
    fig.set_size_inches(5, 4)
    plt.boxplot(dist)
    plt.bar(ticks, avg, alpha=0.2)
    plt.violinplot(dist)
    plt.ylim(bottom=0)
    plt.title(f"{label} per test case")
    plt.ylabel(f"{label}")
    # plt.title("Average Power [W]")
    # plt.ylabel("Average Power [W]")
    plt.xticks(ticks=ticks, labels=names)
    plt.grid(linestyle="--", linewidth=0.5)
    plt.show(block=False)
    plt.xticks(rotation=-45, ha='left')
    plt.tight_layout()
    
    save_path = os.path.join(os.getcwd(), args.save) if args.save else None
    
    if args.save:
      plt.savefig(os.path.join(save_path, pth), dpi=300, bbox_inches='tight')
  
  # ----------------- Statistics -----------------
  metrics =  ["energy", "power", "execution_time"]
  units = ["J", "W", "ms"]  
  
  for metric, unit in zip(metrics, units):
    
    headers = [f"Case", f"Max ({unit})", f"Min ({unit})", f"Mean ({unit})", f"Abs diff ({unit})", f"Std ({unit})", f"CV"]
    rows = []
    
    max_std = 0
    max_cv = 0
    
    for index, case in enumerate(cases):
      max_energy = np.max(case[metric])
      min_energy = np.min(case[metric])
      abs_diff = max_energy - min_energy
      std = np.std(case[metric])
      mean = np.mean(case[metric])
      cv = std / mean
      
      rows.append([names[index], f"{max_energy:.2f}", f"{min_energy:.2f}", f"{mean:.2f}", f"{abs_diff:.2f}", f"{std:.2f}", f"{cv:.4f}"])
      
      max_std = max(max_std, std)
      max_cv = max(max_cv, cv)
    
    table = print_table_str(headers, rows)
    
    # print the table
    print()
    print(f"{metric.capitalize()} per test case:")
    print("\n".join(table))
    print()
    print(f"Max CV: {max_cv}")
    print(f"Max STD: {max_std}")
    print()
  
  plt.show()
  
  