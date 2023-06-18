import dataclasses
from typing import List

import burst_calc
from io import BytesIO
from matplotlib.figure import Figure
import base64

TARGET_ASCENT_RATE = 5

@dataclasses.dataclass
class LaunchStats():
    balloon_enum: burst_calc.BalloonEnum
    ascent_rate:float
    burst_altitude:int
    time_to_burst:int
    neck_lift:int
    launch_volume_gas:float
    launch_litres_gas:int
    launch_cf:float
    warnings: List


def generate_balloon_data(balloon_enums: List[burst_calc.BalloonEnum], weight, target_ascent_rate=5)-> List[LaunchStats]:
    launch_sats = []
    for balloon_enum in balloon_enums:
        ascent_rate, burst_altitude, time_to_burst, neck_lift, launch_volume, launch_litres, launch_cf, warnings = burst_calc.calc_update(balloon_enum, weight, target_ascent_rate=target_ascent_rate)
        launch = LaunchStats(balloon_enum, float(ascent_rate), int(burst_altitude), int(time_to_burst), int(neck_lift), float(launch_volume), int(launch_litres), launch_cf, warnings)

        launch_sats.append(launch)
    return launch_sats


def create_balloon_gas_graph(target_ascent_rate=5, weights=(500, 1000, 1500, 2000, 2500, 3000)):
    f = Figure()
    fig = f.add_subplot(1, 1, 1)
    balloon_enums = []
    balloon_names = []
    for balloon_enum in burst_calc.BalloonEnum:
        if not balloon_enum.value.name.startswith("H") or balloon_enum.value.standard == False:
            continue
        balloon_enums.append(balloon_enum)
        balloon_names.append(balloon_enum.value.name)

    balloon_datas = []
    for payload_weight in weights:
        balloon_data = generate_balloon_data(balloon_enums, payload_weight, target_ascent_rate=target_ascent_rate)
        fig.plot(balloon_names, [b.launch_volume_gas for b in balloon_data], label=f"{payload_weight}g payload")
        balloon_datas.append(balloon_data)

    fig.set_title(f'Helium required vs balloon sizes ({target_ascent_rate}m/s ascent rate)')
    fig.set_xlabel('Balloon names (g)')
    fig.set_ylabel('Helium needed (m3)')
    # Rotate x-axis labels
    fig.set_xticks(range(len(balloon_names)))
    fig.set_xticklabels(balloon_names, rotation=90)
    # Adjust figure size and layout
    f.tight_layout()
    # Add background grid
    fig.grid(True, axis='y', linestyle='--')
    fig.grid(True, axis='x', linestyle='-')
    fig.set_ylim(0)
    lines, labels = fig.get_legend_handles_labels()
    fig.legend(lines, labels)
    buf = BytesIO()
    f.savefig(buf, format="png")
    # Embed the result in the html output.
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return data


def create_balloon_altitude_graph(target_ascent_rate=5, weights=(500, 1000, 1500, 2000, 2500, 3000)):
    f = Figure()
    fig = f.add_subplot(1, 1, 1)
    balloon_enums = []
    balloon_names = []
    for balloon_enum in burst_calc.BalloonEnum:
        if not balloon_enum.value.name.startswith("H") or balloon_enum.value.standard == False:
            continue
        balloon_enums.append(balloon_enum)
        balloon_names.append(balloon_enum.value.name)

    balloon_datas = []
    for payload_weight in weights:
        balloon_data = generate_balloon_data(balloon_enums, payload_weight, target_ascent_rate=target_ascent_rate)
        fig.plot(balloon_names, [b.burst_altitude for b in balloon_data], label=f"{payload_weight}g payload")
        balloon_datas.append(balloon_data)

    fig.set_title(f'Burst altitudes vs balloon sizes ({target_ascent_rate}m/s ascent rate)')
    fig.set_xlabel('Balloon names (g)')
    fig.set_ylabel('Burst altitude (m)')
    # Rotate x-axis labels
    fig.set_xticks(range(len(balloon_names)))
    fig.set_xticklabels(balloon_names, rotation=90)
    # Adjust figure size and layout
    f.tight_layout()
    # Add background grid
    fig.grid(True, axis='y', linestyle='--')
    fig.grid(True, axis='x', linestyle='-')
    fig.set_ylim(0, 37000)
    lines, labels = fig.get_legend_handles_labels()
    fig.legend(lines, labels)
    buf = BytesIO()
    f.savefig(buf, format="png")
    # Embed the result in the html output.
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return data


def create_single_balloon_altitude_graph(balloon_enum: burst_calc.BalloonEnum, payload_weight=2000, ascent_rates=(2.5, 3, 3.5, 4, 4.5, 5, 5.5, 6)):
    f = Figure()
    fig = f.add_subplot(1, 1, 1)
    balloon_launches = []
    for target_ascent_rate in ascent_rates:
        ascent_rate, burst_altitude, time_to_burst, neck_lift, launch_volume, launch_litres, launch_cf, warnings = burst_calc.calc_update(balloon_enum, weight, target_ascent_rate=target_ascent_rate)
        launch = LaunchStats(balloon_enum, float(ascent_rate), int(burst_altitude), int(time_to_burst), int(neck_lift), float(launch_volume), int(launch_litres), launch_cf, warnings)
        balloon_launches.append(launch)
        fig.plot(ascent_rates, [b.burst_altitude for b in balloon_launches], label=f"{payload_weight}g payload")

    fig.set_title(f'Burst altitudes vs balloon sizes ({target_ascent_rate}m/s ascent rate)')
    fig.set_xlabel('Balloon names (g)')
    fig.set_ylabel('Burst altitude (m)')
    # Rotate x-axis labels
    fig.set_xticks(range(len(balloon_names)))
    fig.set_xticklabels(balloon_names, rotation=90)
    # Adjust figure size and layout
    f.tight_layout()
    # Add background grid
    fig.grid(True, axis='y', linestyle='--')
    fig.grid(True, axis='x', linestyle='-')
    fig.set_ylim(0, 37000)
    lines, labels = fig.get_legend_handles_labels()
    fig.legend(lines, labels)
    buf = BytesIO()
    f.savefig(buf, format="png")
    # Embed the result in the html output.
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return data