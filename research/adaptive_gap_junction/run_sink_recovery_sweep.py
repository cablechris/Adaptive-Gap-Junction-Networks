from __future__ import annotations

import json

from .sweeps import run_sink_recovery_sweep


def main() -> None:
    payload = run_sink_recovery_sweep()
    print(json.dumps(payload["metadata"], indent=2))
    print(json.dumps(payload["rows"], indent=2))


if __name__ == "__main__":
    main()
