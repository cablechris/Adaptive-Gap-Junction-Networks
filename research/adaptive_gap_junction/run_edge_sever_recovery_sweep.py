from __future__ import annotations

import json

from .sweeps import run_edge_sever_recovery_sweep


if __name__ == "__main__":
    payload = run_edge_sever_recovery_sweep()
    print(json.dumps(payload, indent=2))
