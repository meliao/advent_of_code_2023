import logging
import argparse
from src.logging_args_setup import setup_args
import numpy as np
import parse

logging.getLogger("parse").setLevel(logging.WARNING)
DAY = "5"


def problem_1(input_file: str) -> None:
    seeds, dag = parse_into_dag(input_file)

    min_target = np.inf

    for s in seeds:
        logging.debug("######################")
        logging.debug("NEW SEED %i", s)
        t = traverse_DAG_forward(s, dag)

        min_target = min(t, min_target)

    logging.info("Soln 1: %i", min_target)


def problem_2(input_file: str) -> None:
    seeds, dag = parse_into_dag(input_file)

    l = len(seeds)
    min_target = np.inf

    for i in range(0, l, 2):
        s = seeds[i]
        r = seeds[i + 1]
        logging.debug("######################")
        logging.debug("NEW SEED %i and RANGE: %i", s, r)
        t = traverse_DAG_forward_range(s, r, dag)

        min_target = min(t, min_target)

    logging.info("Soln 1: %i", min_target)


class DAGMixer:
    """This class represents the shifting operations that happen in this graph
    structure. A set of these mixer objects fully characterize one level of the DAG
    """

    def __init__(
        self, level: int, source_min: int, target_min: int, range: int
    ) -> None:
        self.level = level
        self.source_min = source_min
        self.target_min = target_min
        self.range = range
        self.min_connected_sink = np.inf

    def is_source_in(self, source: int) -> bool:
        return (source >= self.source_min) and (source < self.source_min + self.range)

    def map_source_to_target(self, x: int) -> bool:
        return self.target_min + (x - self.source_min)


class DAGLevel:
    def __init__(self, level: int, mixers: list[DAGMixer], data: np.ndarray) -> None:
        self.level = level
        self.mixers = mixers
        self.data = data
        self.source_cutoffs = np.sort(data[:, 1])

    def map_to_next_level(self, source: int):
        for m in self.mixers:
            if m.is_source_in(source):
                return m.map_source_to_target(source)

        return source

    def map_range_to_range(self, x_min: int, x_range: int) -> list[tuple[int, int]]:
        """This is the solution for problem 2. It maps a range of indices to a
        set of ranges of indices at the next level of the DAG.

        Args:
            x_min (int): starting index
            x_range (int): number of nodes in this contigupus range of indices

        Returns:
            list[tuple[int, int]]: Set of ranges of indices in the next level of the
            DAG. Each tuple is (start_idx, range_len)
        """

        # These are the cutoffs that break up our input range
        eff_cutoffs = self.source_cutoffs[
            np.logical_and(
                self.source_cutoffs > x_min, self.source_cutoffs < x_min + x_range
            )
        ]

        out_lst = []

        x_max = x_min + x_range
        x = x_min

        # For each cutoff, we make a new tuple that represents one contiguous
        # section of the output indices
        for e in eff_cutoffs:
            x_new = self.map_to_next_level(x)
            range_new = e - x
            out_lst.append((x_new, range_new))
            x = e

        x_new = self.map_to_next_level(x)
        out_lst.append((x_new, x_max - x))

        return out_lst


def traverse_DAG_forward(source_idx: int, dag: list[DAGLevel]) -> int:
    """Given a starting index, traverses the DAG and returns the
    final node index
    """
    s = source_idx
    for level in dag:
        s_new = level.map_to_next_level(s)
        logging.debug(
            "traverse_DAG_forward: level %i source %i, maps to %i",
            level.level,
            s,
            s_new,
        )
        s = s_new

    return s


def traverse_DAG_forward_range(
    source_idx_start: int, source_idx_range: int, dag: list[DAGLevel]
) -> int:
    """Maps a contiguous range of indices through the DAG, and returns the minimum index
    at the final level.

    Args:
        source_idx_start (int): Start index at initial level of the DAG
        source_idx_range (int): Number of nodes included in the traversal
        dag (list[DAGLevel]): Representation of the DAG

    Returns:
        int: _description_
    """
    t_lst = [(source_idx_start, source_idx_range)]
    for level in dag:
        # t_lst_new is a list of (start_idx, range_len) tuples
        t_lst_new = []

        for x in t_lst:
            t_lst_new.extend(level.map_range_to_range(x[0], x[1]))

        logging.debug(
            "Level %i, t_lst: %s, t_lst_new: %s", level.level, t_lst, t_lst_new
        )
        t_lst = t_lst_new

    # Return the min start idx
    return min(x[0] for x in t_lst)


def lines_to_numpy(s: str, cast=None) -> np.ndarray:
    """Embarrasing, also using the cast arg breaks things."""
    l = s.strip().split("\n")
    if cast:
        ll = [map(cast, x.split()) for x in l]
    else:
        ll = [x.split() for x in l]
    return np.array(ll).astype(np.int64)


def parse_into_dag(input_file: str) -> tuple[list[int], list[DAGLevel]]:
    """Parser

    Args:
        input_file (str): Filepath

    Returns:
        tuple[list[int], list[DAGLevel]]: First return value is a list of ints, that's
        the seeds from the first line of the file. Second return value is a list of
        DAGLevel objects, thats the representation of the graph.
    """
    with open(input_file, "r") as f:
        l_0 = f.readline()
        _, seeds = l_0.split(":")
        seed_vals = [int(x) for x in seeds.split()]
        logging.debug("Found seeds: %s", seed_vals)
        file_str = f.read().strip()
        maps_lst = file_str.split("\n\n")
        map_parse_str = "{}-to-{} map"
        s_lst_out = []
        for i, m in enumerate(maps_lst):
            # logging.debug(m)
            _, map_data_str = m.split(":")
            # logging.debug(map_name)
            # logging.debug("Map_to: %s, Map_from: %s", map_to, map_from)
            map_data = lines_to_numpy(map_data_str)
            mixer_lst = []
            for map_line in map_data:
                new_dag_mixer = DAGMixer(
                    level=i,
                    source_min=map_line[1],
                    target_min=map_line[0],
                    range=map_line[2],
                )
                mixer_lst.append(new_dag_mixer)

            s_lst_out.append(DAGLevel(i, mixer_lst, map_data))

    return seed_vals, s_lst_out


def main(a: argparse.Namespace) -> None:
    if a.d:
        fp_1 = f"inputs/{DAY}_1_debug.txt"
        fp_2 = f"inputs/{DAY}_1_debug.txt"

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
