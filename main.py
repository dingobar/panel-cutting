import json
from pathlib import Path
import csv
from typing import Generator
from opcut.common import (
    Method,
    Params,
    Panel,
    Item,
    OutputFormat,
    OutputSettings,
    result_to_json,
)
from opcut.calculate import calculate
from opcut.generate import generate


def read_input_data():
    out = []
    with Path("input.csv").open() as file:
        reader = csv.reader(file)
        next(reader)  # skip header

        for row in reader:
            name, x, y, n = tuple(row)
            for _ in range(int(n)):
                out.append([f"{name} ({x}x{y})", int(x), int(y)])

    return out


if __name__ == "__main__":
    method = Method.FORWARD_GREEDY_NATIVE

    panels = [Panel("lang", 100, 3310), Panel("kort", 100, 1480)]
    items = [
        Item(name, x, y, True) for name, x, y in read_input_data()
    ]
    result = calculate(method, Params(1, True, panels, items))
    with Path("out.pdf").open("wb") as f:
        data = generate(result, OutputFormat.PDF, None, OutputSettings())
        f.write(data)
    with Path("out.json").open("w") as f:
        f.write(json.dumps(result_to_json(result), indent=4))
