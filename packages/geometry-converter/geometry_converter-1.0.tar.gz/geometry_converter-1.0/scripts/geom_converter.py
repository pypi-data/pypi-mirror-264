#!/usr/bin/env python3
import argparse
from shapely.wkb import loads as wkb_loads
from shapely.wkt import loads as wkt_loads
from shapely.geometry import mapping
import json


def parse_cli_args(description: str) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("--conversion_type", "-ct", type=str, default="wkb2wkt",
                        help="Type of conversion to be performed. "
                             "Options: wkb2wkt, wkb2geojson, wkt2wkb, wkt2geojson, geojson2wkb, geojson2wkt."
                             "Default: wkb2wkt")
    parser.add_argument("--input_type", "-it", type=str, default="text",
                        help="Type of input. Options: file or text. Default: text")
    parser.add_argument('--wkb', "-wkb", type=str, required=False,
                        help="wkb value or path to the file")
    parser.add_argument('--wkt', "-wkt", type=str, required=False,
                        help="wkt value or path to the file")
    parser.add_argument('--geo_json', "-gj", type=str, required=False,
                        help="geojson value or path to the file")
    return parser


def convert(conversion_type: str, input_type: str, wkb: str, wkt: str, geo_json: str):
    conversion_type = conversion_type.lower().strip()
    input_type = input_type.lower().strip()
    conversion_src_type, conversion_tgt_type = conversion_type.split("2")
    if input_type not in ["file", "text"]:
        raise ValueError("Invalid input type")

    if conversion_src_type == "wkb":
        if wkb is None:
            raise ValueError("WKB value is required for this conversion type")
        if input_type == "file":
            with open(wkb, "r") as f:
                wkb = f.read()
        if conversion_tgt_type == "wkt":
            geom = wkb_loads(bytes.fromhex(wkb))
            print(geom.wkt)
        elif conversion_tgt_type == "geojson":
            geom = wkb_loads(bytes.fromhex(wkb))
            print(json.dumps(mapping(geom)))
        else:
            raise ValueError("Invalid conversion type")
    elif conversion_src_type == "wkt":
        if wkt is None:
            raise ValueError("WKT value is required for this conversion type")
        if input_type == "file":
            with open(wkt, "r") as f:
                wkt = f.read()
        if conversion_tgt_type == "wkb":
            geom = wkt_loads(wkt)
            print(geom.wkb_hex)
        elif conversion_tgt_type == "geojson":
            geom = wkt_loads(wkt)
            print(json.dumps(mapping(geom)))
        else:
            raise ValueError("Invalid conversion type")
    elif conversion_src_type == "geojson":
        if geo_json is None:
            raise ValueError("GeoJson value is required for this conversion type")
        if input_type == "file":
            with open(geo_json, "r") as f:
                geo_json = f.read()
        if conversion_tgt_type == "wkb":
            geom = wkb_loads(json.loads(geo_json))
            print(geom.wkb_hex)
        elif conversion_tgt_type == "wkt":
            geom = wkb_loads(json.loads(geo_json))
            print(geom.wkt)
        else:
            raise ValueError("Invalid conversion type")
    else:
        raise ValueError("Invalid conversion type")


def main():
    args = parse_cli_args("Convert between different geometry formats").parse_args()
    convert(args.conversion_type, args.input_type, args.wkb, args.wkt, args.geo_json)


if __name__ == "__main__":
    main()
