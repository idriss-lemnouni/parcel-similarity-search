import argparse
from collections import defaultdict
from csv import DictReader
from math import dist
from pathlib import Path
from statistics import mean, pstdev


def profiles(path):
    plots = defaultdict(dict)
    with path.open(encoding="utf-8-sig", newline="") as stream:
        for row in DictReader(stream):
            key = (row["Block"], row["Variety"])
            dose = float(row["nitro"])
            if dose in plots[key]:
                raise ValueError(f"Mesure dupliquée : {key}, dose {dose}")
            plots[key][dose] = float(row["yield"])
    if any(set(values) != {0, .2, .4, .6} for values in plots.values()):
        raise ValueError("Chaque parcelle doit comporter les quatre doses.")
    return {key: tuple(values[dose] for dose in (0, .2, .4, .6)) for key, values in plots.items()}


def neighbors(plots, target, limit):
    candidates = {key: vector for key, vector in plots.items() if key[0] != target[0]}
    if not candidates:
        raise ValueError("Aucun candidat dans un autre bloc.")
    columns = list(zip(*candidates.values()))
    scales = [pstdev(column) or 1 for column in columns]
    query = plots[target]

    def score(vector):
        return dist([value / scale for value, scale in zip(vector, scales)],
                    [value / scale for value, scale in zip(query, scales)])

    return sorted((score(vector), key, vector) for key, vector in candidates.items())[:limit]


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("csv", type=Path)
    parser.add_argument("--block", default="I")
    parser.add_argument("--variety", default="Victory")
    args = parser.parse_args()
    target = (args.block, args.variety)
    plots = profiles(args.csv)
    if target not in plots:
        parser.error(f"Parcelle inconnue : {target}")
    print("bloc,variete,distance,rendements_par_dose")
    for score, (block, variety), vector in neighbors(plots, target, 5):
        print(f'{block},{variety},{score:.4f},"{vector}"')
    matches = [neighbors(plots, key, 1)[0][1][1] == key[1] for key in plots]
    print(f"Variété retrouvée au rang 1 en validation par bloc : {sum(matches)}/{len(matches)}")
