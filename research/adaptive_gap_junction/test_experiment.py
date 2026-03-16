from __future__ import annotations

import random
import unittest

from .disorder import apply_disorder, apply_quenched_edge_removals
from .experiment import build_sweep_config, has_spanning_cluster, run_bond_dilution_sweep
from .initialization import initial_state
from .model import DisorderKind, DisorderSpec, LesionKind, LesionSpec, SimulationConfig
from .run_baseline import build_baseline_config
from .simulator import run_simulation


class AdaptiveGapJunctionTests(unittest.TestCase):
    def test_baseline_config_uses_empirical_epsilon_scale(self) -> None:
        config = build_baseline_config()
        self.assertGreaterEqual(config.epsilon, 1e-3)
        self.assertLessEqual(config.epsilon, 1e-2)

    def test_sink_lesion_is_not_a_topological_cut(self) -> None:
        config = SimulationConfig(
            lattice_size=4,
            lesion=LesionSpec(kind=LesionKind.SINK, nodes=(5,), clamp_voltage=-1.0),
        )
        _voltages, _conductances, active_nodes, sink_nodes, neighbors = initial_state(config)
        self.assertIn(5, active_nodes)
        self.assertIn(5, sink_nodes)
        self.assertTrue(neighbors[5])

    def test_topological_cut_removes_node_from_active_graph(self) -> None:
        config = SimulationConfig(
            lattice_size=4,
            lesion=LesionSpec(kind=LesionKind.TOPOLOGICAL_CUT, nodes=(5,)),
        )
        _voltages, _conductances, active_nodes, _sink_nodes, neighbors = initial_state(config)
        self.assertNotIn(5, active_nodes)
        for adjacent in neighbors.values():
            self.assertNotIn(5, adjacent)

    def test_bond_dilution_zeroes_edges_without_removing_nodes(self) -> None:
        config = SimulationConfig(
            lattice_size=4,
            disorder=DisorderSpec(
                kind=DisorderKind.DILUTION,
                distribution="bernoulli bond dilution",
                strength=1.0,
                seed=3,
            ),
        )
        voltages, conductances, active_nodes, _sink_nodes, neighbors = initial_state(config)
        active_before = set(active_nodes)
        _site_offsets, edge_scales = apply_disorder(config, voltages, conductances, random.Random(config.disorder.seed))
        self.assertEqual(active_before, active_nodes)
        self.assertTrue(edge_scales)
        self.assertTrue(all(scale == 0.0 for scale in edge_scales.values()))
        updated_conductances, _updated_neighbors = apply_quenched_edge_removals(conductances, neighbors, edge_scales)
        self.assertFalse(updated_conductances)

    def test_initial_condition_starts_in_stable_spatial_pattern(self) -> None:
        config = SimulationConfig(lattice_size=4)
        voltages, _conductances, _active_nodes, _sink_nodes, _neighbors = initial_state(config)
        left_half = [voltages[row * 4 + col] for row in range(4) for col in range(2)]
        right_half = [voltages[row * 4 + col] for row in range(4) for col in range(2, 4)]
        self.assertTrue(all(value < 0.0 for value in left_half))
        self.assertTrue(all(value > 0.0 for value in right_half))

    def test_baseline_run_returns_finite_voltage_data(self) -> None:
        history = run_simulation(build_baseline_config())
        self.assertTrue(history)
        final_state = history[-1]
        self.assertEqual(len(final_state.voltages), 16 * 16)
        self.assertTrue(all(isinstance(voltage, float) for voltage in final_state.voltages))

    def test_spanning_cluster_detects_horizontal_path(self) -> None:
        active_nodes = {0, 1, 2, 3}
        occupied_edges = {(0, 1): 1.0, (1, 2): 1.0, (2, 3): 1.0}
        self.assertTrue(has_spanning_cluster(4, occupied_edges, active_nodes))

    def test_sweep_config_uses_bond_dilution(self) -> None:
        config = build_sweep_config(lattice_size=16, dilution_fraction=0.4, replicate=2)
        self.assertEqual(config.disorder.kind, DisorderKind.DILUTION)
        self.assertAlmostEqual(config.epsilon, 0.01)

    def test_small_bond_dilution_sweep_returns_rows(self) -> None:
        payload = run_bond_dilution_sweep(lattice_sizes=(16,), dilution_grid=(0.0, 0.5), replicates=2)
        self.assertEqual(payload["metadata"]["percolation_target_pc"], 0.5)
        self.assertEqual(len(payload["rows"]), 2)
        self.assertEqual(len(payload["runs"]), 4)


if __name__ == "__main__":
    unittest.main()
