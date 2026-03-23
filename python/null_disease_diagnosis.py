import argparse
import json


args = argparse.ArgumentParser(description="Filter disease diagnosis to null for all patients in the input MiAIRR metadata JSON file.")
args.add_argument("infile", type=str, help="Path to the input file")
args.add_argument("outfile", type=str, help="Path to the output file")
args = args.parse_args()

with open(args.infile, "r") as f:
    data = json.load(f)

    for repertoire in data["Repertoire"]:
        for study_group in repertoire["subject"]["diagnosis"]:
            study_group["disease_diagnosis"] = {"label": None, "id": None}

with open(args.outfile, "w") as f:
    json.dump(data, f, indent=4)
