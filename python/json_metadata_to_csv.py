from receptor_utils import simple_bio_seq as simple
import json

json_file = "P37_PRJNA1207082.json"
sample_csv_file = "sample_genomic_metadata.csv"
output_csv_file = "P37_PRJNA1207082_metadata.csv"
correspondence_file = "airr_correspondence.csv"

sample_read = simple.read_csv(sample_csv_file)[0]
required_keys = list(sample_read.keys())

capture_specific_keys = [
    "cells_per_reaction", "cell_storage", "cell_quality", "cell_isolation", 
    "cell_processing_protocol", "template_class", "template_quality", 
    "template_amount", "template_amount_unit", "library_generation_method", 
    "library_generation_protocol", "library_generation_kit_version", 
    "pcr_target_locus", "forward_pcr_primer_target_location", 
    "reverse_pcr_primer_target_location", "complete_sequences", 
    "physical_linkage", "sequencing_run_id", "total_reads_passing_qc_filter", 
    "sequencing_platform", "sequencing_facility", "sequencing_run_date", 
    "sequencing_kit", "sequencing_data_id", "file_type", "filename", 
    "read_direction", "read_length", "paired_filename", "paired_read_direction", 
    "paired_read_length", "primary_annotation", "software_versions", 
    "paired_reads_assembly", "quality_thresholds", "primer_match_cutoffs", 
    "collapsing_method", "data_processing_protocols", "data_processing_files", 
    "germline_database", "analysis_provenance_id"
]

required_keys = [k for k in required_keys if k not in capture_specific_keys]

vdjbase_names = {row['airr_repertoire_id']: row['vdjbase_name'] for row in simple.read_csv(correspondence_file)}

with open(json_file, 'r') as f:
    data = json.load(f)

result = []

for rep in data['Repertoire']:
    row = {}
    # visit every leaf in the json tree. If the key is in the required_keys, add it to the row
    def visit(obj, path):
        if isinstance(obj, dict):
            for key, value in obj.items():
                #if key == 'keywords_study':
                #    breakpoint()
                if key in required_keys:
                    if value:
                        # if value is a dict, render using the json.dumps function
                        if isinstance(value, dict):
                            value = json.dumps(value)
                        # if value is a list, render using the json.dumps function
                        elif isinstance(value, list):
                            value = json.dumps(value)
                        else:
                            value = str(value)
                        row[key] = value
                    else:
                        row[key] = ""
                elif key in capture_specific_keys:
                    row[key] = sample_read[key]
                visit(value, path + [key])
        elif isinstance(obj, list):
            for item in obj:
                visit(item, path)
        else:
            pass

    visit(rep, [])
    row['vdjbase_name'] = vdjbase_names[rep['repertoire_id']]
    row['species'] = sample_read['species']
    # add the row to the result list
    result.append(row)

headers = result[0].keys()

# list any required_keys that are not in the json file
missing_keys = []   
for key in required_keys:
    if key not in headers:
        missing_keys.append(key)    
if missing_keys:
    print("The following keys are missing from the json file:")
    for key in missing_keys:
        print(key)

for row in result:
    # if the key is not in the row, add it with an empty value
    for key in missing_keys:
        if key not in row:
            row[key] = ""

simple.write_csv(output_csv_file, result, scan_all=True)