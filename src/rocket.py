"""Assemble a RocketPy Rocket from a RocketConfig."""
import csv
from pathlib import Path

from rocketpy import Rocket

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"


def _scaled_drag_csv(source_rel_path: str, scale: float, out_path: Path) -> str:
    """Write a copy of a (mach, cd) CSV with cd scaled by `scale`."""
    src = PROJECT_ROOT / source_rel_path
    rows = []
    with open(src, newline="") as f:
        for mach, cd in csv.reader(f):
            rows.append((float(mach), float(cd) * scale))
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", newline="") as f:
        csv.writer(f).writerows(rows)
    return str(out_path)


def build_rocket(config, motor):
    if config.drag_scale != 1.0:
        tag = config.name.lower().replace(" ", "_")
        off = _scaled_drag_csv(
            config.power_off_drag, config.drag_scale,
            DATA_DIR / "rockets" / "generated" / f"{tag}_power_off.csv",
        )
        on = _scaled_drag_csv(
            config.power_on_drag, config.drag_scale,
            DATA_DIR / "rockets" / "generated" / f"{tag}_power_on.csv",
        )
    else:
        off = str(PROJECT_ROOT / config.power_off_drag)
        on = str(PROJECT_ROOT / config.power_on_drag)

    rocket = Rocket(
        radius=config.radius,
        mass=config.mass,
        inertia=config.inertia,
        power_off_drag=off,
        power_on_drag=on,
        center_of_mass_without_motor=0,
        coordinate_system_orientation="tail_to_nose",
    )

    rocket.set_rail_buttons(
        upper_button_position=config.rail_button_upper,
        lower_button_position=config.rail_button_lower,
        angular_position=45,
    )

    rocket.add_motor(motor, position=config.motor_position)

    rocket.add_nose(length=config.nose_length, kind=config.nose_kind, position=config.nose_position)

    rocket.add_trapezoidal_fins(
        n=config.fins.n,
        root_chord=config.fins.root_chord,
        tip_chord=config.fins.tip_chord,
        span=config.fins.span,
        position=config.fins.position,
        cant_angle=config.fins.cant_angle,
        airfoil=(str(DATA_DIR / "airfoils" / "NACA0012-radians.txt"), "radians"),
    )

    rocket.add_tail(
        top_radius=config.tail_top_radius,
        bottom_radius=config.tail_bottom_radius,
        length=config.tail_length,
        position=config.tail_position,
    )

    rocket.add_parachute(
        "Main",
        cd_s=10.0,
        trigger=800,  # deploy at 800 m AGL on descent
        sampling_rate=105,
        lag=1.5,
        noise=(0, 8.3, 0.5),
    )

    rocket.add_parachute(
        "Drogue",
        cd_s=1.0,
        trigger="apogee",
        sampling_rate=105,
        lag=1.5,
        noise=(0, 8.3, 0.5),
    )

    return rocket
