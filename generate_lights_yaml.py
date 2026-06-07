#!/usr/bin/env python3
import csv
from pathlib import Path


INPUT_CSV = "LightInZone.csv"
OUTPUT_YAML = "lights.yaml"


def yaml_quote(value: str) -> str:
    value = str(value).replace('"', '\\"')
    return f'"{value}"'


def build_light_block(row: dict) -> str:
    name = (row.get("LightRemark") or "").strip()
    if not name:
        name = f"Light {row['id']}"

    subnet = str(row["SubnetID"]).strip()
    device = str(row["DeviceID"]).strip()
    channel = str(row["ChannelNo"]).strip()
    csv_id = str(row["id"]).strip()

    unique_id = f"smartbus_light_{csv_id}"

    return f"""- light:
    - name: {yaml_quote(name)}
      unique_id: {yaml_quote(unique_id)}
      state: "false"
      turn_on:
        action: shell_command.smartbus_light
        data:
          subnet: {yaml_quote(subnet)}
          device: {yaml_quote(device)}
          channel: {yaml_quote(channel)}
          level: "100"
      turn_off:
        action: shell_command.smartbus_light
        data:
          subnet: {yaml_quote(subnet)}
          device: {yaml_quote(device)}
          channel: {yaml_quote(channel)}
          level: "0"
"""


def main():
    input_path = Path(INPUT_CSV)
    output_path = Path(OUTPUT_YAML)

    blocks = []

    with input_path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            subnet = str(row.get("SubnetID", "")).strip()
            device = str(row.get("DeviceID", "")).strip()
            channel = str(row.get("ChannelNo", "")).strip()
            csv_id = str(row.get("id", "")).strip()

            if not subnet or not device or not channel or not csv_id:
                continue

            blocks.append(build_light_block(row))

    output_path.write_text("\n".join(blocks), encoding="utf-8")
    print(f"Wrote {len(blocks)} lights to {output_path}")


if __name__ == "__main__":
    main()
