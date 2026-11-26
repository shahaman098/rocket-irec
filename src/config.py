"""Airframe configurations.

BASELINE is a validated reference configuration: a 127mm (5in) minimum-diameter
airframe flying the Cesaroni M1670, with drag curves derived from real
wind-tunnel/CFD data for this exact shape. It's the known-good starting
point — the kind of design a team would already have flight history on.

RECORD_ATTEMPT starts from that same validated airframe and pushes it for
altitude: lower structural mass (14.43 kg -> 12.6 kg) and a re-sized
three-fin set, cutting both weight and drag versus the baseline four-fin
set. Because shrinking the fins changes the true drag curve and no CFD
tool is wired in here, DRAG_SCALE below approximates the effect by
scaling the baseline curve in proportion to the change in fin planform
area (assuming fins account for ~30% of total vehicle drag, a typical
fraction for a finned minimum-diameter airframe). Replace this with a
real recomputed drag curve (OpenRocket, Missile DATCOM, or CFD) before
trusting the record-attempt numbers for an actual build.

IMPORTANT, learned by simulating it: naively shrinking the fins to the
"minimum stable area" using the baseline's stability numbers is wrong
once you also lighten the airframe. A lighter dry structure means the
motor (unchanged mass) is a bigger fraction of loaded mass, which pulls
the loaded center of gravity aft and *hurts* stability. A first attempt
at n=3 fins scaled down ~30% by area came out with a *negative* static
margin (unstable, would tumble in flight) despite a naive pre-flight
altitude estimate looking like a win. The geometry below was found by a
static-margin sweep that re-grows the fins until margin is positive and
in the 1.5-2.5 cal band from ignition through burnout — it targets that
stability band, not minimum drag in isolation.
"""
from dataclasses import dataclass


@dataclass
class FinSet:
    n: int
    root_chord: float
    tip_chord: float
    span: float
    position: float
    cant_angle: float = 0.0

    @property
    def planform_area(self) -> float:
        return self.n * 0.5 * (self.root_chord + self.tip_chord) * self.span


@dataclass
class RocketConfig:
    name: str
    radius: float
    mass: float  # dry mass without motor, kg
    inertia: tuple
    nose_length: float
    nose_kind: str
    nose_position: float
    fins: FinSet
    tail_top_radius: float
    tail_bottom_radius: float
    tail_length: float
    tail_position: float
    motor_position: float
    rail_button_upper: float
    rail_button_lower: float
    power_off_drag: str
    power_on_drag: str
    drag_scale: float = 1.0


BASELINE = RocketConfig(
    name="Baseline",
    radius=127 / 2000,
    mass=14.426,
    inertia=(6.321, 6.321, 0.034),
    nose_length=0.55829,
    nose_kind="vonKarman",
    nose_position=1.278,
    fins=FinSet(n=4, root_chord=0.120, tip_chord=0.060, span=0.110, position=-1.04956),
    tail_top_radius=0.0635,
    tail_bottom_radius=0.0435,
    tail_length=0.060,
    tail_position=-1.194656,
    motor_position=-1.255,
    rail_button_upper=0.0818,
    rail_button_lower=-0.618,
    power_off_drag="data/rockets/calisto/powerOffDragCurve.csv",
    power_on_drag="data/rockets/calisto/powerOnDragCurve.csv",
    drag_scale=1.0,
)

_baseline_fin_area = BASELINE.fins.planform_area
# Found via static-margin sweep (scale 1.10 on the original 4-fin baseline
# dimensions, but with 3 fins): margin@ignition=1.57 cal, margin@burnout=2.56 cal.
_record_fins = FinSet(n=3, root_chord=0.132, tip_chord=0.066, span=0.121, position=-1.04956)
_fin_area_ratio = _record_fins.planform_area / _baseline_fin_area
_FIN_DRAG_FRACTION = 0.30
_record_drag_scale = (1 - _FIN_DRAG_FRACTION) + _FIN_DRAG_FRACTION * _fin_area_ratio

RECORD_ATTEMPT = RocketConfig(
    name="Record Attempt",
    radius=127 / 2000,
    mass=12.6,
    # Inertia scaled from baseline by mass ratio as a first-order approximation
    # (airframe length/radius unchanged, mass removed roughly uniformly).
    inertia=tuple(round(v * 12.6 / 14.426, 3) for v in (6.321, 6.321, 0.034)),
    nose_length=0.55829,
    nose_kind="vonKarman",
    nose_position=1.278,
    fins=_record_fins,
    tail_top_radius=0.0635,
    tail_bottom_radius=0.0435,
    tail_length=0.060,
    tail_position=-1.194656,
    motor_position=-1.255,
    rail_button_upper=0.0818,
    rail_button_lower=-0.618,
    power_off_drag="data/rockets/calisto/powerOffDragCurve.csv",
    power_on_drag="data/rockets/calisto/powerOnDragCurve.csv",
    drag_scale=round(_record_drag_scale, 4),
)
