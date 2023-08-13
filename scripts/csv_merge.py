import os


def csv_merge():
    merged_file_path = '../metabolites/hmdb_metabolites/merged_gcms.csv'

    # Check if merged file already exists
    header_included = os.path.exists(merged_file_path)

    for filename in os.listdir('../metabolites/hmdb_metabolites/csv_converted'):
        if filename.endswith(".csv"):
            full_path = os.path.join('../metabolites/hmdb_metabolites/csv_converted', filename)
            with open(full_path, 'r') as f1:
                lines = f1.readlines()

                # If header hasn't been added yet, include it
                if not header_included:
                    header_included = True
                else:
                    lines = lines[1:]  # skip the header for subsequent files

                with open(merged_file_path, 'a') as f2:
                    f2.writelines(lines)


csv_merge()
