import os
import xml.etree.ElementTree as ET
import csv


def get_nested_value(node, keys):
    # Funzione ricorsiva per ottenere il valore di un tag innestato dato un elenco di chiavi
    if len(keys) == 0:
        return node.text if node is not None else ''
    else:
        child = node.find(keys[0])
        return get_nested_value(child, keys[1:]) if child is not None else ''


def xml2csv(input_file, output_file, extracted_header_keys):
    tree = ET.parse(input_file)
    root = tree.getroot()

    # Apriamo un file CSV in modalità di scrittura
    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)

        # Scriviamo l'intestazione delle colonne nel file CSV utilizzando l'elenco di chiavi fornito
        writer.writerow(extracted_header_keys)

        # Cicliamo attraverso tutti i metabolite nel file XML e scriviamo i dati nel file CSV
        for metabolite in root.findall('metabolite'):
            # Costruiamo una riga di dati utilizzando i valori dei tag innestati corrispondenti alle chiavi
            row_data = [get_nested_value(metabolite, key.split('/')) for key in extracted_header_keys]
            writer.writerow(row_data)


# Definiamo l'elenco delle chiavi per l'header del file CSV
header_keys = ['id', 'status', 'name', 'average_molecular_weight', 'monisotopic_molecular_weight', 'kingdom',
               'super_class', 'class', 'state', 'logp', 'logs', 'solubility', 'pka_strongest_acidic',
               'pka_strongest_basic', 'average_mass', 'mono_mass', 'polar_surface_area', 'refractivity',
               'polarizability', 'rotatable_bond_count', 'acceptor_count', 'donor_count',
               'physiological_charge', 'formal_charge', 'number_of_rings', 'bioavailability', 'rule_of_five',
               'ghose_filter', 'veber_rule', 'mddr_like_rule']


def convert_all_file():
    # Crea la directory 'parsed/' se non esiste
    if not os.path.exists('../metabolites/hmdb_metabolites/csv_converted'):
        os.makedirs('../metabolites/hmdb_metabolites/csv_converted')

    for filename in os.listdir('../metabolites/hmdb_metabolites/parsed_gcms'):
        if filename.endswith(".xml"):
            full_path = os.path.join('../metabolites/hmdb_metabolites/parsed_gcms', filename)  # Corrected path
            xml2csv(full_path, '../metabolites/hmdb_metabolites/csv_converted/' + filename.replace(".xml", ".csv"), header_keys)


convert_all_file()
