from __future__ import annotations

import random
import unittest

from .analysis import (
    ap_mode_drive_threshold_linearized,
    ap_differential_at_minimum,
    classify_macrostate_from_objective,
    coarse_objective_gradient,
    cosine_similarity,
    correspondence_status_base_case,
    default_generative_model,
    drift_variance_in_feature_subspace,
    driven_fixed_point_linear,
    effective_smoothing_rate,
    feature_vector_from_voltages,
    feature_jacobian,
    first_ap_mode_laplacian_eigenvalue,
    homogenization_timescale,
    minimum_existence_condition,
    negative_log_joint_from_voltages,
    static_ap_drive_vector,
    voltage_drift_vector,
    weighted_laplacian_matrix,
)
from .disorder import apply_disorder, apply_quenched_edge_removals
from .experiment import (
    build_sweep_config,
    has_spanning_cluster,
    run_bond_dilution_sweep,
    run_edge_sever_recovery_sweep,
    run_sink_recovery_sweep,
)
from .initialization import initial_state
from .morphology import classify_macrostate
from .model import DisorderKind, DisorderSpec, LesionKind, LesionSpec, MacrostateKind, SimulationConfig
from .observables import ap_voltage_variance, polarity_contrast, spatial_variance
from .run_baseline import build_baseline_config
from .sweeps import default_midline_edge_cut, remove_edges_from_graph
from .simulator import run_simulation


class AdaptiveGapJunctionTests(unittest.TestCase):
    def test_first_ap_mode_eigenvalue_decreases_with_system_size(self) -> None:
        self.assertGreater(first_ap_mode_laplacian_eigenvalue(16), 0.0)
        self.assertGreater(
            first_ap_mode_laplacian_eigenvalue(16),
            first_ap_mode_laplacian_eigenvalue(32),
        )

    def test_effective_smoothing_rate_decreases_with_dilution(self) -> None:
        intact = effective_smoothing_rate(average_conductance=0.35, lattice_size=16, bond_occupation=1.0)
        diluted = effective_smoothing_rate(average_conductance=0.35, lattice_size=16, bond_occupation=0.5)
        self.assertGreater(intact, diluted)

    def test_linearized_drive_threshold_decreases_with_dilution(self) -> None:
        intact = ap_mode_drive_threshold_linearized(
            average_conductance=5.0,
            lattice_size=16,
            bond_occupation=1.0,
            target_amplitude=1.0,
            well_linear=0.1,
        )
        diluted = ap_mode_drive_threshold_linearized(
            average_conductance=5.0,
            lattice_size=16,
            bond_occupation=0.5,
            target_amplitude=1.0,
            well_linear=0.1,
        )
        self.assertGreater(intact, diluted)

    def test_linearized_drive_threshold_clips_to_zero_when_well_dominates(self) -> None:
        threshold = ap_mode_drive_threshold_linearized(
            average_conductance=0.1,
            lattice_size=16,
            bond_occupation=1.0,
            target_amplitude=1.0,
            well_linear=1.0,
        )
        self.assertEqual(threshold, 0.0)

    def test_homogenization_timescale_decreases_with_smoothing(self) -> None:
        slow = homogenization_timescale(
            average_conductance=0.2,
            lattice_size=16,
            bond_occupation=0.5,
            tau_v=1.0,
        )
        fast = homogenization_timescale(
            average_conductance=1.0,
            lattice_size=16,
            bond_occupation=1.0,
            tau_v=1.0,
        )
        self.assertGreater(slow, fast)

    def test_homogenization_timescale_is_infinite_without_smoothing(self) -> None:
        timescale = homogenization_timescale(
            average_conductance=0.0,
            lattice_size=16,
            bond_occupation=1.0,
            tau_v=1.0,
        )
        self.assertEqual(timescale, float("inf"))

    def test_minimum_existence_condition_tracks_linear_response_bound(self) -> None:
        self.assertTrue(minimum_existence_condition(a=1.0, average_conductance=0.2, lambda_max_laplacian=4.0))
        self.assertFalse(minimum_existence_condition(a=0.4, average_conductance=0.2, lambda_max_laplacian=4.0))

    def test_driven_fixed_point_linear_solves_two_site_system(self) -> None:
        laplacian = [
            [1.0, -1.0],
            [-1.0, 1.0],
        ]
        drive = [1.0, -1.0]
        fixed_point = driven_fixed_point_linear(drive, a=3.0, average_conductance=0.5, laplacian_matrix=laplacian)
        self.assertAlmostEqual(fixed_point[0], -0.5)
        self.assertAlmostEqual(fixed_point[1], 0.5)

    def test_ap_differential_at_minimum_uses_selected_partitions(self) -> None:
        laplacian = [
            [1.0, -1.0],
            [-1.0, 1.0],
        ]
        drive = [1.0, -1.0]
        differential = ap_differential_at_minimum(
            drive,
            a=3.0,
            average_conductance=0.5,
            laplacian_matrix=laplacian,
            anterior_mask=[True, False],
            posterior_mask=[False, True],
        )
        self.assertAlmostEqual(differential, -1.0)

    def test_feature_vector_from_voltages_matches_current_morphology_readout(self) -> None:
        config = SimulationConfig(lattice_size=4)
        voltages, _polarity_field, _polarity_target, _conductances, _active_nodes, _sink_nodes, _neighbors = initial_state(config)
        feature_vector = feature_vector_from_voltages(voltages, config)
        self.assertEqual(feature_vector, (1.0, -1.0, 2.0, 0.0))

    def test_default_generative_model_prefers_wt_for_wt_pattern(self) -> None:
        config = SimulationConfig(lattice_size=4)
        voltages, _polarity_field, _polarity_target, _conductances, _active_nodes, _sink_nodes, _neighbors = initial_state(config)
        best, scores = classify_macrostate_from_objective(voltages, config, default_generative_model(config))
        self.assertEqual(best, MacrostateKind.WT)
        self.assertLess(scores[MacrostateKind.WT], scores[MacrostateKind.CRYPTIC])
        self.assertLess(scores[MacrostateKind.WT], scores[MacrostateKind.DH])

    def test_default_generative_model_prefers_dh_for_uniform_anterior_pattern(self) -> None:
        config = SimulationConfig(lattice_size=4)
        voltages = [config.anterior_voltage for _ in range(config.lattice_size * config.lattice_size)]
        best, _scores = classify_macrostate_from_objective(voltages, config)
        self.assertEqual(best, MacrostateKind.DH)

    def test_negative_log_joint_distinguishes_wt_from_cryptic_for_baseline_pattern(self) -> None:
        config = SimulationConfig(lattice_size=4)
        voltages, _polarity_field, _polarity_target, _conductances, _active_nodes, _sink_nodes, _neighbors = initial_state(config)
        wt_score = negative_log_joint_from_voltages(voltages, config, MacrostateKind.WT)
        cryptic_score = negative_log_joint_from_voltages(voltages, config, MacrostateKind.CRYPTIC)
        self.assertLess(wt_score, cryptic_score)

    def test_correspondence_status_base_case_is_not_exact(self) -> None:
        self.assertEqual(correspondence_status_base_case(), "no_exact_correspondence_base_case")

    def test_feature_jacobian_rows_sum_to_expected_feature_weights(self) -> None:
        config = SimulationConfig(lattice_size=4)
        voltages, _polarity_field, _polarity_target, _conductances, _active_nodes, _sink_nodes, _neighbors = initial_state(config)
        jacobian = feature_jacobian(voltages, config)
        self.assertAlmostEqual(sum(jacobian[0]), 1.0)
        self.assertAlmostEqual(sum(jacobian[1]), 1.0)
        self.assertAlmostEqual(sum(jacobian[2]), 0.0)

    def test_coarse_objective_gradient_vanishes_at_wt_target(self) -> None:
        config = SimulationConfig(lattice_size=4)
        voltages, _polarity_field, _polarity_target, _conductances, _active_nodes, _sink_nodes, _neighbors = initial_state(config)
        gradient = coarse_objective_gradient(voltages, config, MacrostateKind.WT)
        self.assertTrue(all(abs(value) < 1e-12 for value in gradient))

    def test_voltage_drift_vector_returns_one_entry_per_site(self) -> None:
        config = SimulationConfig(lattice_size=4, noise_amplitude=0.0, stimulation_amplitude=0.0, injury_amplitude=0.0)
        voltages, polarity_field, _polarity_target, conductances, _active_nodes, _sink_nodes, neighbors = initial_state(config)
        site_offsets, edge_scales = apply_disorder(config, voltages, conductances, random.Random(config.disorder.seed))
        drift = voltage_drift_vector(
            config,
            voltages,
            polarity_field,
            conductances,
            neighbors,
            site_offsets,
            edge_scales,
        )
        self.assertEqual(len(drift), 16)

    def test_cosine_similarity_detects_opposite_vectors(self) -> None:
        self.assertAlmostEqual(cosine_similarity([1.0, 0.0], [-1.0, 0.0]), -1.0)

    def test_drift_variance_in_feature_subspace_is_one_for_row_space_vector(self) -> None:
        jacobian = [
            [1.0, 0.0],
            [0.0, 1.0],
            [1.0, -1.0],
        ]
        self.assertAlmostEqual(drift_variance_in_feature_subspace([1.0, 1.0], jacobian), 1.0)

    def test_weighted_laplacian_matrix_builds_two_site_graph(self) -> None:
        laplacian = weighted_laplacian_matrix(2, {(0, 1): 0.5})
        self.assertEqual(laplacian, [[0.5, -0.5], [-0.5, 0.5]])

    def test_static_ap_drive_vector_matches_polarity_partition(self) -> None:
        config = SimulationConfig(lattice_size=4)
        drive = static_ap_drive_vector(config)
        self.assertTrue(all(value < 0.0 for value in drive[:2]))
        self.assertTrue(all(value > 0.0 for value in drive[2:4]))

    def test_baseline_config_uses_empirical_epsilon_scale(self) -> None:
        config = build_baseline_config()
        self.assertGreaterEqual(config.epsilon, 1e-3)
        self.assertLessEqual(config.epsilon, 1e-2)

    def test_sink_lesion_is_not_a_topological_cut(self) -> None:
        config = SimulationConfig(
            lattice_size=4,
            lesion=LesionSpec(kind=LesionKind.SINK, nodes=(5,), clamp_voltage=-1.0),
        )
        _voltages, _polarity_field, _polarity_target, _conductances, active_nodes, sink_nodes, neighbors = initial_state(config)
        self.assertIn(5, active_nodes)
        self.assertIn(5, sink_nodes)
        self.assertTrue(neighbors[5])

    def test_topological_cut_removes_node_from_active_graph(self) -> None:
        config = SimulationConfig(
            lattice_size=4,
            lesion=LesionSpec(kind=LesionKind.TOPOLOGICAL_CUT, nodes=(5,)),
        )
        _voltages, _polarity_field, _polarity_target, _conductances, active_nodes, _sink_nodes, neighbors = initial_state(config)
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
        voltages, _polarity_field, _polarity_target, conductances, active_nodes, _sink_nodes, neighbors = initial_state(config)
        active_before = set(active_nodes)
        _site_offsets, edge_scales = apply_disorder(config, voltages, conductances, random.Random(config.disorder.seed))
        self.assertEqual(active_before, active_nodes)
        self.assertTrue(edge_scales)
        self.assertTrue(all(scale == 0.0 for scale in edge_scales.values()))
        updated_conductances, _updated_neighbors = apply_quenched_edge_removals(conductances, neighbors, edge_scales)
        self.assertFalse(updated_conductances)

    def test_initial_condition_starts_in_stable_spatial_pattern(self) -> None:
        config = SimulationConfig(lattice_size=4)
        voltages, _polarity_field, _polarity_target, _conductances, _active_nodes, _sink_nodes, _neighbors = initial_state(config)
        left_half = [voltages[row * 4 + col] for row in range(4) for col in range(2)]
        right_half = [voltages[row * 4 + col] for row in range(4) for col in range(2, 4)]
        self.assertTrue(all(value < 0.0 for value in left_half))
        self.assertTrue(all(value > 0.0 for value in right_half))

    def test_polarity_field_starts_with_ap_bias(self) -> None:
        config = SimulationConfig(lattice_size=4)
        _voltages, polarity_field, polarity_target, _conductances, _active_nodes, _sink_nodes, _neighbors = initial_state(config)
        left_half = [polarity_field[row * 4 + col] for row in range(4) for col in range(2)]
        right_half = [polarity_target[row * 4 + col] for row in range(4) for col in range(2, 4)]
        self.assertTrue(all(value < 0.0 for value in left_half))
        self.assertTrue(all(value > 0.0 for value in right_half))

    def test_polarity_contrast_detects_ap_pattern(self) -> None:
        config = SimulationConfig(lattice_size=4)
        voltages, _polarity_field, _polarity_target, _conductances, _active_nodes, _sink_nodes, _neighbors = initial_state(config)
        self.assertGreater(polarity_contrast(voltages, lattice_size=4), 0.0)

    def test_spatial_variance_distinguishes_nonuniform_pattern(self) -> None:
        self.assertEqual(spatial_variance([1.0, 1.0, 1.0, 1.0]), 0.0)
        self.assertGreater(spatial_variance([-1.0, -1.0, 1.0, 1.0]), 0.0)

    def test_ap_voltage_variance_returns_side_means_and_differential(self) -> None:
        anterior_mean, posterior_mean, ap_differential, variance = ap_voltage_variance(
            [-1.0, 1.0, -1.0, 1.0],
            lattice_size=2,
            axis="x",
        )
        self.assertAlmostEqual(anterior_mean, 1.0)
        self.assertAlmostEqual(posterior_mean, -1.0)
        self.assertAlmostEqual(ap_differential, 2.0)
        self.assertGreater(variance, 0.0)

    def test_initial_pattern_classifies_as_wt(self) -> None:
        config = SimulationConfig(lattice_size=4)
        voltages, _polarity_field, _polarity_target, _conductances, _active_nodes, _sink_nodes, _neighbors = initial_state(config)
        assessment = classify_macrostate(voltages, config)
        self.assertEqual(assessment.macrostate, MacrostateKind.WT)

    def test_uniform_depolarized_pattern_classifies_as_dh(self) -> None:
        config = SimulationConfig(lattice_size=4)
        voltages = [config.anterior_voltage for _ in range(config.lattice_size * config.lattice_size)]
        assessment = classify_macrostate(voltages, config)
        self.assertEqual(assessment.macrostate, MacrostateKind.DH)

    def test_intermediate_posterior_bias_classifies_as_cryptic(self) -> None:
        config = SimulationConfig(lattice_size=4)
        voltages = []
        for row in range(config.lattice_size):
            for col in range(config.lattice_size):
                if col < config.lattice_size / 2:
                    voltages.append(0.0)
                else:
                    voltages.append(config.anterior_voltage)
        assessment = classify_macrostate(voltages, config)
        self.assertEqual(assessment.macrostate, MacrostateKind.CRYPTIC)

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

    def test_midline_edge_cut_breaks_horizontal_spanning(self) -> None:
        occupied_edges = {
            (0, 1): 1.0,
            (1, 2): 1.0,
            (2, 3): 1.0,
            (4, 5): 1.0,
            (5, 6): 1.0,
            (6, 7): 1.0,
            (8, 9): 1.0,
            (9, 10): 1.0,
            (10, 11): 1.0,
            (12, 13): 1.0,
            (13, 14): 1.0,
            (14, 15): 1.0,
        }
        neighbors = {
            0: (1,),
            1: (0, 2),
            2: (1, 3),
            3: (2,),
            4: (5,),
            5: (4, 6),
            6: (5, 7),
            7: (6,),
            8: (9,),
            9: (8, 10),
            10: (9, 11),
            11: (10,),
            12: (13,),
            13: (12, 14),
            14: (13, 15),
            15: (14,),
        }
        severed = {(min(i, j), max(i, j)) for i, j in default_midline_edge_cut(4)}
        lesioned_edges, _ = remove_edges_from_graph(occupied_edges, neighbors, severed)
        self.assertFalse(has_spanning_cluster(4, lesioned_edges, set(range(16))))

    def test_sweep_config_uses_bond_dilution(self) -> None:
        default_config = build_sweep_config(lattice_size=16, dilution_fraction=0.4, replicate=2)
        self.assertGreater(default_config.polarity_field.tau_h, default_config.tau_g)

        config = build_sweep_config(
            lattice_size=16,
            dilution_fraction=0.4,
            replicate=2,
            base_conductance=0.2,
            polarity_field_amplitude=0.02,
            polarity_field_tau_h=100.0,
            well_cubic=0.1,
        )
        self.assertEqual(config.disorder.kind, DisorderKind.DILUTION)
        self.assertAlmostEqual(config.epsilon, 0.01)
        self.assertAlmostEqual(config.base_conductance, 0.2)
        self.assertAlmostEqual(config.polarity_field.amplitude, 0.02)
        self.assertAlmostEqual(config.polarity_field.tau_h, 100.0)
        self.assertAlmostEqual(config.well_cubic, 0.1)

    def test_small_bond_dilution_sweep_returns_rows(self) -> None:
        payload = run_bond_dilution_sweep(lattice_sizes=(16,), dilution_grid=(0.0, 0.5), replicates=2)
        self.assertEqual(payload["metadata"]["percolation_target_pc"], 0.5)
        self.assertEqual(len(payload["rows"]), 2)
        self.assertEqual(len(payload["runs"]), 4)

    def test_small_sink_recovery_sweep_returns_rows(self) -> None:
        payload = run_sink_recovery_sweep(
            lattice_sizes=(16,),
            dilution_grid=(0.0, 0.5),
            replicates=2,
            lesion_steps=10,
            recovery_steps=20,
            lesion_current=0.6,
            base_conductance=0.2,
            polarity_field_amplitude=0.02,
            polarity_field_tau_h=100.0,
            well_cubic=0.1,
            suppress_field_during_recovery=True,
        )
        self.assertEqual(payload["metadata"]["lesion_current"], 0.6)
        self.assertEqual(payload["metadata"]["base_conductance"], 0.2)
        self.assertTrue(payload["metadata"]["suppress_field_during_recovery"])
        self.assertIn("mean_final_dh_propensity", payload["rows"][0])
        self.assertIn("mean_final_ap_differential", payload["rows"][0])
        self.assertIn("mean_final_spatial_variance", payload["rows"][0])
        self.assertIn("wt_fraction", payload["rows"][0])
        self.assertEqual(len(payload["rows"]), 2)
        self.assertEqual(len(payload["runs"]), 4)

    def test_small_edge_sever_recovery_sweep_returns_rows(self) -> None:
        payload = run_edge_sever_recovery_sweep(
            lattice_sizes=(16,),
            dilution_grid=(0.0, 0.5),
            replicates=2,
            lesion_steps=10,
            recovery_steps=20,
            lesion_current=0.6,
            base_conductance=0.2,
            polarity_field_amplitude=0.02,
            polarity_field_tau_h=100.0,
            well_cubic=0.1,
            suppress_field_during_recovery=True,
        )
        self.assertEqual(payload["metadata"]["lesion_kind"], "edge_sever")
        self.assertEqual(payload["metadata"]["lesion_current"], 0.6)
        self.assertEqual(payload["metadata"]["base_conductance"], 0.2)
        self.assertTrue(payload["metadata"]["suppress_field_during_recovery"])
        self.assertTrue(any("Recorded cryptic reference point" in note for note in payload["metadata"]["notes"]))
        self.assertIn("final_macrostate", payload["runs"][0])
        self.assertIn("final_ap_differential", payload["runs"][0])
        self.assertIn("final_dh_propensity", payload["runs"][0])
        self.assertIn("final_spatial_variance", payload["runs"][0])
        self.assertEqual(len(payload["rows"]), 2)
        self.assertEqual(len(payload["runs"]), 4)


if __name__ == "__main__":
    unittest.main()
