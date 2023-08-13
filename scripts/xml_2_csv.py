import os
import xml.etree.ElementTree as ET
import csv
import numpy as np

# Costanti
BIN_WIDTH = 0.05  # Larghezza del bin
MZ_MIN = 10  # Valore minimo di m/z
MZ_MAX = 700  # Valore massimo di m/z
NUM_BINS = int((MZ_MAX - MZ_MIN) / BIN_WIDTH) + 1

HEADER_KEYS = ['id', 'status', 'name', 'average_molecular_weight', 'monisotopic_molecular_weight', 'kingdom',
               'super_class', 'class', 'state', 'logp', 'logs', 'solubility', 'pka_strongest_acidic',
               'pka_strongest_basic', 'average_mass', 'mono_mass', 'polar_surface_area', 'refractivity',
               'polarizability', 'rotatable_bond_count', 'acceptor_count', 'donor_count',
               'physiological_charge', 'formal_charge', 'number_of_rings', 'bioavailability', 'rule_of_five',
               'ghose_filter', 'veber_rule', 'mddr_like_rule']


def bin_spectrum(spectrum):
    binned_spectrum = [0] * NUM_BINS
    for peak in spectrum:
        mz, intensity = float(peak[0]), float(peak[1])
        bin_index = int((mz - MZ_MIN) / BIN_WIDTH)
        if 0 <= bin_index < NUM_BINS:
            binned_spectrum[bin_index] += intensity
    return binned_spectrum


def get_nested_value(element, path):
    for key in path:
        element = element.find(key)
        if element is None:
            return None
    return element.text


def xml2csv(input_file, output_file):
    tree = ET.parse(input_file)
    root = tree.getroot()

    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)

        # Aggiungi le colonne per gli spettri binned, la carica iniziale e quella finale
        header_keys_extended = HEADER_KEYS + [
            'spectrum_bin_{:.2f}-{:.2f}'.format(round(MZ_MIN + i * BIN_WIDTH, 2), round(MZ_MIN + (i + 1) * BIN_WIDTH, 2))
            for i in range(NUM_BINS)
        ]

        writer.writerow(header_keys_extended)

        for metabolite in root.findall('metabolite'):

            row_data = [get_nested_value(metabolite, key.split('/')) for key in HEADER_KEYS]

            spectrum_element = metabolite.find('spectrum')
            if spectrum_element is not None:
                peaks_str = get_nested_value(spectrum_element, ['peaks'])
                if peaks_str:
                    spectrum = eval(peaks_str)
                    binned = bin_spectrum(spectrum)
                    row_data.extend(binned)
                else:
                    row_data.extend([0, 0] + [0] * NUM_BINS)  # se lo spettro non è disponibile, riempi di zeri
            else:
                row_data.extend([0, 0] + [0] * NUM_BINS)  # se il tag spectrum non è disponibile, riempi di zeri

            writer.writerow(row_data)


def convert_all_file():
    # Crea la directory 'parsed/' se non esiste
    if not os.path.exists('../metabolites/hmdb_metabolites/csv_converted'):
        os.makedirs('../metabolites/hmdb_metabolites/csv_converted')

    for filename in os.listdir('../metabolites/hmdb_metabolites/parsed_gcms'):
        if filename.endswith(".xml"):
            full_path = os.path.join('../metabolites/hmdb_metabolites/parsed_gcms', filename)  # Corrected path
            xml2csv(full_path, '../metabolites/hmdb_metabolites/csv_converted/' + filename.replace(".xml", ".csv"))


convert_all_file()

# %%
