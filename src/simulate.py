"""Run the baseline vs. record-attempt flight simulations and report results.

Usage:
    python src/simulate.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from rocketpy import Flight

from config import BASELINE, RECORD_ATTEMPT
from environment import build_environment
from motor import build_motor
from report import print_comparison, print_flight_report
from rocket import build_rocket

PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUTPUTS_DIR = PROJECT_ROOT / "outputs"

RAIL_LENGTH = 5.2  # m, standard competition launch rail
INCLINATION = 85  # deg from horizontal
HEADING = 0  # deg


def run(config, env, save_plots=True):
    motor = build_motor()
    rocket = build_rocket(config, motor)
    flight = Flight(
        rocket=rocket,
        environment=env,
        rail_length=RAIL_LENGTH,
        inclination=INCLINATION,
        heading=HEADING,
    )
    result = print_flight_report(config.name, rocket, motor, flight, env)

    if save_plots:
        OUTPUTS_DIR.mkdir(exist_ok=True)
        tag = config.name.lower().replace(" ", "_")
        flight.altitude.plot(0, flight.t_final, samples=400, filename=str(OUTPUTS_DIR / f"{tag}_altitude.png"))
        flight.speed.plot(0, flight.t_final, samples=400, filename=str(OUTPUTS_DIR / f"{tag}_speed.png"))

    return result, flight


def main():
    env = build_environment()
    print(f"Launch site: {env.latitude:.4f}, {env.longitude:.4f}  (elev {env.elevation} m ASL)")

    results = []
    for config in (BASELINE, RECORD_ATTEMPT):
        result, _ = run(config, env)
        results.append(result)

    print_comparison(results)


if __name__ == "__main__":
    main()
