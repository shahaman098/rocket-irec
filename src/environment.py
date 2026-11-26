"""Launch environment definition.

Site: Spaceport America, Truth or Consequences, NM — the Spaceport America
Cup / IREC competition launch site. Coordinates and elevation are the
site's real published values.
"""
from rocketpy import Environment

LAUNCH_SITE = {
    "name": "Spaceport America, Truth or Consequences, NM",
    "latitude": 32.990254,
    "longitude": -106.974998,
    "elevation": 1400,  # meters ASL
}


def build_environment(date=None):
    """Build the launch-site Environment.

    Uses the standard atmosphere model (deterministic, reproducible) rather
    than a live weather forecast, so simulation results are stable run to
    run. Swap in `env.set_atmospheric_model(type="forecast", file="GFS")`
    for a real weather-day analysis before an actual launch.
    """
    env = Environment(
        latitude=LAUNCH_SITE["latitude"],
        longitude=LAUNCH_SITE["longitude"],
        elevation=LAUNCH_SITE["elevation"],
    )
    if date is not None:
        env.set_date(date)
    env.set_atmospheric_model(type="standard_atmosphere")
    return env
