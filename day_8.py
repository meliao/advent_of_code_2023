import logging
import argparse
from src.logging_args_setup import setup_args

# import numba
import math

logging.getLogger("numba").setLevel(logging.WARNING)
DAY = "8"


def parse_to_dict(input_line: str) -> tuple[str, dict[str, str]]:
    "Return val is <node name> , {'left': <left_node_name>, 'right': <right_node_name>"
    first, last = input_line.split("=")
    out_1 = first.strip()
    l, r = last.strip().lstrip("(").rstrip(")").split(",")
    out_2 = {}
    out_2["L"] = l.strip()
    out_2["R"] = r.strip()
    # out_2 = {"L": l.strip(), "R": r.strip()}
    return out_1, out_2


def problem_1(input_file: str) -> None:
    with open(input_file, "r") as f:
        instructions = f.readline().strip()
        graph_dd = {}

        f.readline()
        # l = f.readline()
        # k, v = parse_to_dict(l)
        # first_node = k
        # graph_dd[k] = v
        for l in f:
            k, v = parse_to_dict(l)
            graph_dd[k] = v

        logging.debug("Here are the instructions: %s", instructions)
        logging.debug("Here is the graph: %s", graph_dd)

        logging.info(
            "Got a graph with %i nodes and instructions of length %i",
            len(graph_dd),
            len(instructions),
        )

        out = traverse_graph(graph_dd, instructions, first_node="AAA")
        logging.info("SOln 1: %i", out)


def traverse_graph(graph_dd: dict, instructions: str, first_node: str) -> int:
    current_node = first_node
    step_counter = 0

    instruction_len = len(instructions)

    while current_node != "ZZZ":
        which = instructions[step_counter % instruction_len]
        new_node = graph_dd[current_node][which]
        logging.debug(
            "Step %i: Moving %s from %s gets us to %s",
            step_counter,
            which,
            current_node,
            new_node,
        )

        current_node = new_node
        step_counter += 1
    return step_counter


def traverse_graph_2(
    graph_dd: dict, instructions: str, first_node: str, max_steps: int = 1_000_000
) -> set[int]:
    current_node = first_node
    step_counter = 0

    instruction_len = len(instructions)

    out = set()

    states = set()

    while step_counter < max_steps:
        instruction_loc = step_counter % instruction_len

        state = (current_node, instruction_loc)
        if state in states:
            logging.debug("State has already been reached.")
            break
        else:
            states.add(state)
        which = instructions[instruction_loc]
        new_node = graph_dd[current_node][which]
        # logging.debug(
        #     "Step %i: Moving %s from %s gets us to %s",
        #     step_counter,
        #     which,
        #     current_node,
        #     new_node,
        # )

        current_node = new_node
        step_counter += 1

        if current_node.endswith("Z"):
            out.add(step_counter)
    return out


# MAX = 100
MAX = 1_000_000


def problem_2(input_file: str) -> None:
    with open(input_file, "r") as f:
        instructions = f.readline().strip()
        graph_dd = {}

        f.readline()

        a_nodes = []
        for l in f:
            k, v = parse_to_dict(l)

            if k.endswith("A"):
                a_nodes.append(k)
            graph_dd[k] = v

        logging.debug("Here are the instructions: %s", instructions)
        logging.debug("Here is the graph: %s", graph_dd)

        logging.info(
            "Got a graph with %i nodes and instructions of length %i",
            len(graph_dd),
            len(instructions),
        )
        logging.info("There are %i **A nodes", len(a_nodes))
        logging.debug("Here are the  **A nodes: %s", a_nodes)

        common_steps = None
        for a_node in a_nodes:
            out = traverse_graph_2(graph_dd, instructions, a_node, MAX)

            logging.info("Starting at %s, we are at **Z on steps: %s", a_node, out)

            if common_steps is None:
                common_steps = out
            else:
                common_steps = common_steps.union(out)

            # logging.info("Node %s, we have %i common steps", a_node, len(common_steps))

            # if not len(common_steps):
            #     exit(1)
        # logging.info("With MAX=%i, we have %i steps in common", MAX, len(common_steps))
        logging.info("Soln 2=%i", math.lcm(*common_steps))


def main(a: argparse.Namespace) -> None:
    if a.d:
        fp_1 = f"inputs/{DAY}_2_debug.txt"
        fp_2 = f"inputs/{DAY}_2_debug.txt"

    else:
        fp_1 = f"inputs/{DAY}_1.txt"
        fp_2 = f"inputs/{DAY}_1.txt"

    if a.s:
        problem_2(fp_2)
    else:
        problem_1(fp_1)


if __name__ == "__main__":
    a = setup_args()

    if a.d:
        logging.getLogger().setLevel(logging.DEBUG)
    else:
        logging.getLogger().setLevel(logging.INFO)

    main(a)
