"""Human-readable flight summary + design checks."""

M_TO_FT = 3.28084
MS_TO_MPH = 2.23694


def print_flight_report(name, rocket, motor, flight, env):
    apogee_agl_m = flight.apogee - env.elevation
    print(f"\n{'=' * 60}")
    print(f"  {name}")
    print(f"{'=' * 60}")
    print(f"  Static margin @ ignition   : {rocket.static_margin(0):6.2f} cal")
    print(f"  Static margin @ rail exit  : {flight.out_of_rail_stability_margin:6.2f} cal")
    print(f"  Static margin @ burnout    : {rocket.static_margin(motor.burn_out_time):6.2f} cal")
    print(f"  Rail exit velocity         : {flight.out_of_rail_velocity:6.1f} m/s  ({flight.out_of_rail_velocity * MS_TO_MPH:6.1f} mph)")
    print(f"  Apogee (AGL)               : {apogee_agl_m:6.1f} m      ({apogee_agl_m * M_TO_FT:8.0f} ft)")
    print(f"  Time to apogee             : {flight.apogee_time:6.1f} s")
    print(f"  Max velocity               : {flight.max_speed:6.1f} m/s  ({flight.max_speed * MS_TO_MPH:6.1f} mph)")
    print(f"  Max Mach number            : {flight.max_mach_number:6.3f}")
    print(f"  Max acceleration           : {flight.max_acceleration:6.1f} m/s^2 ({flight.max_acceleration / 9.81:5.1f} g)")
    print(f"  Impact velocity (under chute): {abs(flight.impact_velocity):6.1f} m/s")
    print(f"  Dry mass (no motor)        : {rocket.mass:6.2f} kg")
    print(f"  Liftoff mass (with motor)  : {rocket.mass + motor.propellant_initial_mass + motor.dry_mass:6.2f} kg")

    return {
        "name": name,
        "apogee_agl_m": apogee_agl_m,
        "apogee_agl_ft": apogee_agl_m * M_TO_FT,
        "max_speed": flight.max_speed,
        "max_mach": flight.max_mach_number,
        "max_accel_g": flight.max_acceleration / 9.81,
        "rail_exit_v": flight.out_of_rail_velocity,
        "margin_ignition": rocket.static_margin(0),
        "margin_rail_exit": flight.out_of_rail_stability_margin,
        "margin_burnout": rocket.static_margin(motor.burn_out_time),
    }


def print_comparison(results):
    print(f"\n{'=' * 60}")
    print("  COMPARISON")
    print(f"{'=' * 60}")
    header = f"  {'Config':<18}{'Apogee (ft)':>14}{'Max Mach':>11}{'Max g':>9}{'Margin (rail)':>15}"
    print(header)
    print(f"  {'-' * 58}")
    for r in results:
        print(
            f"  {r['name']:<18}{r['apogee_agl_ft']:>14,.0f}{r['max_mach']:>11.3f}"
            f"{r['max_accel_g']:>9.1f}{r['margin_rail_exit']:>15.2f}"
        )
    if len(results) == 2:
        gain_ft = results[1]["apogee_agl_ft"] - results[0]["apogee_agl_ft"]
        gain_pct = 100 * gain_ft / results[0]["apogee_agl_ft"]
        print(f"\n  Record attempt gains {gain_ft:,.0f} ft ({gain_pct:+.1f}%) over baseline.")
