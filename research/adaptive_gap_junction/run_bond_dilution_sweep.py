from __future__ import annotations

from .experiment import write_bond_dilution_sweep


def main() -> None:
    output_path = write_bond_dilution_sweep()
    print(f"wrote={output_path.as_posix()}")


if __name__ == "__main__":
    main()
