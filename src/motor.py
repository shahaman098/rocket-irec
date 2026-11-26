"""Cesaroni Pro75 M1670 — a real, commercially available (COTS) M-class
solid motor, legal for the IREC / Spaceport America Cup 10,000 ft AGL COTS
category.

Thrust curve: data/motors/Cesaroni_M1670.eng — the real manufacturer RASP
thrust-curve file (75mm diameter, 757mm case, 3.101 kg propellant,
5.231 kg total loaded mass). Grain and nozzle geometry below are the
manufacturer-published values for this motor.
"""
from pathlib import Path

from rocketpy import SolidMotor

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def build_motor():
    return SolidMotor(
        thrust_source=str(DATA_DIR / "motors" / "Cesaroni_M1670.eng"),
        dry_mass=1.815,
        dry_inertia=(0.125, 0.125, 0.002),
        nozzle_radius=33 / 1000,
        grain_number=5,
        grain_density=1815,
        grain_outer_radius=33 / 1000,
        grain_initial_inner_radius=15 / 1000,
        grain_initial_height=120 / 1000,
        grain_separation=5 / 1000,
        grains_center_of_mass_position=0.397,
        center_of_dry_mass_position=0.317,
        nozzle_position=0,
        burn_time=3.9,
        throat_radius=11 / 1000,
        coordinate_system_orientation="nozzle_to_combustion_chamber",
    )
