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
            x, y, n = (int(r) for r in row)
            for _ in range(int(n)):
                out.append([x, y])

    return out


def get_running_number_generator():
    def running_number() -> Generator[int, None, None]:
        n = 0
        while True:
            n = n + 1
            yield str(n)

    return running_number()


if __name__ == "__main__":
    method = Method.FORWARD_GREEDY_NATIVE

    panel_id = get_running_number_generator()
    panels = [Panel(next(panel_id), 1220, 2440) for _ in range(10)]
    item_id = get_running_number_generator()
    items = [
        Item(next(item_id) + f" ({x}x{y})", x, y, True) for x, y in read_input_data()
    ]
    result = calculate(method, Params(1, True, panels, items))
    with Path("out.pdf").open("wb") as f:
        data = generate(result, OutputFormat.PDF, None, OutputSettings())
        f.write(data)
    with Path("out.json").open("w") as f:
        f.write(json.dumps(result_to_json(result), indent=4))
