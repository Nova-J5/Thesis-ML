import os
import xml.etree.ElementTree as ET

xml_spectra_path = "../spectra/hmdb_predicted_msms_spectra"


def find_element(node, element):
    result = node.find(element)
    if result is None:
        return ''
    else:
        text = result.text if result.text else ''
        if text.lower() == 'yes':
            return '1'
        elif text.lower() == 'no':
            return '0'
        else:
            return text


def get_spectrum(metabolite_id, spectrum_id):
    xml_spectrum_file = os.path.join(xml_spectra_path,
                                     '{}_ms_ms_spectrum_{}_predicted.xml'.format(metabolite_id, spectrum_id))

    if os.path.exists(xml_spectrum_file):
        tree = ET.parse(xml_spectrum_file)
        root = tree.getroot()

        # select only some specific information from the spectrum file
        spectrum = {
            'id': spectrum_id,
            'peak_counter': find_element(root, 'peak-counter'),
            'ionization_mode': find_element(root, 'ionization-mode'),
            'collision_energy_voltage': find_element(root, 'collision-energy-voltage'),
            'collision_energy_level': find_element(root, 'collision-energy-level'),
        }

        # get the peaks
        peaks = []
        for peak in root.findall('ms-ms-peaks/ms-ms-peak'):
            peaks.append([find_element(peak, 'mass-charge'), find_element(peak, 'intensity')])

        spectrum['peaks'] = peaks

        return spectrum
    else:
        return None


def parser(input_file, output_file):
    tree = ET.parse(input_file)
    root = tree.getroot()

    with open(output_file, 'w', newline='') as xmlfile:
        xmlfile.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        xmlfile.write('<hmdb>\n')

        for metabolite in root.findall('metabolite'):

            spectra = []
            for s in metabolite.findall('spectra/spectrum'):

                if find_element(s, 'type') is None:
                    continue

                if find_element(s, 'type') != 'Specdb::MsMs':
                    continue

                result_spectrum = get_spectrum(find_element(metabolite, 'accession'), find_element(s, 'spectrum_id'))

                if result_spectrum:
                    spectra.append(result_spectrum)

            # Scrivi le informazioni del metabolita solo se esiste uno spettro valido
            if len(spectra) == 0:
                continue

            for spectrum in spectra:
                xmlfile.write('  <metabolite>\n')

                xmlfile.write('    <id>' + find_element(metabolite, 'accession') + '</id>\n')
                xmlfile.write('    <status>' + find_element(metabolite, 'status') + '</status>\n')
                xmlfile.write('    <name>' + find_element(metabolite, 'name') + '</name>\n')
                xmlfile.write('    <average_molecular_weight>' + find_element(metabolite,
                                                                              'average_molecular_weight') + '</average_molecular_weight>\n')
                xmlfile.write('    <monisotopic_molecular_weight>' + find_element(metabolite,
                                                                                  'monisotopic_molecular_weight') + '</monisotopic_molecular_weight>\n')
                xmlfile.write('    <kingdom>' + find_element(metabolite, 'taxonomy/kingdom') + '</kingdom>\n')
                xmlfile.write(
                    '    <super_class>' + find_element(metabolite, 'taxonomy/super_class') + '</super_class>\n')
                xmlfile.write('    <class>' + find_element(metabolite, 'taxonomy/class') + '</class>\n')
                xmlfile.write('    <state>' + find_element(metabolite, 'state') + '</state>\n')

                for p in metabolite.findall('predicted_properties/property'):
                    if find_element(p, 'kind') == 'logp':
                        xmlfile.write('    <logp>' + find_element(p, 'value') + '</logp>\n')
                    elif find_element(p, 'kind') == 'logs':
                        xmlfile.write('    <logs>' + find_element(p, 'value') + '</logs>\n')
                    elif find_element(p, 'kind') == 'solubility':
                        xmlfile.write('    <solubility>' + find_element(p, 'value') + '</solubility>\n')
                    elif find_element(p, 'kind') == 'pka_strongest_acidic':
                        xmlfile.write(
                            '    <pka_strongest_acidic>' + find_element(p, 'value') + '</pka_strongest_acidic>\n')
                    elif find_element(p, 'kind') == 'pka_strongest_basic':
                        xmlfile.write(
                            '    <pka_strongest_basic>' + find_element(p, 'value') + '</pka_strongest_basic>\n')
                    elif find_element(p, 'kind') == 'average_mass':
                        xmlfile.write('    <average_mass>' + find_element(p, 'value') + '</average_mass>\n')
                    elif find_element(p, 'kind') == 'mono_mass':
                        xmlfile.write('    <mono_mass>' + find_element(p, 'value') + '</mono_mass>\n')
                    elif find_element(p, 'kind') == 'polar_surface_area':
                        xmlfile.write('    <polar_surface_area>' + find_element(p, 'value') + '</polar_surface_area>\n')
                    elif find_element(p, 'kind') == 'refractivity':
                        xmlfile.write('    <refractivity>' + find_element(p, 'value') + '</refractivity>\n')
                    elif find_element(p, 'kind') == 'polarizability':
                        xmlfile.write('    <polarizability>' + find_element(p, 'value') + '</polarizability>\n')
                    elif find_element(p, 'kind') == 'rotatable_bond_count':
                        xmlfile.write(
                            '    <rotatable_bond_count>' + find_element(p, 'value') + '</rotatable_bond_count>\n')
                    elif find_element(p, 'kind') == 'acceptor_count':
                        xmlfile.write('    <acceptor_count>' + find_element(p, 'value') + '</acceptor_count>\n')
                    elif find_element(p, 'kind') == 'donor_count':
                        xmlfile.write('    <donor_count>' + find_element(p, 'value') + '</donor_count>\n')
                    elif find_element(p, 'kind') == 'physiological_charge':
                        xmlfile.write(
                            '    <physiological_charge>' + find_element(p, 'value') + '</physiological_charge>\n')
                    elif find_element(p, 'kind') == 'formal_charge':
                        xmlfile.write('    <formal_charge>' + find_element(p, 'value') + '</formal_charge>\n')
                    elif find_element(p, 'kind') == 'number_of_rings':
                        xmlfile.write('    <number_of_rings>' + find_element(p, 'value') + '</number_of_rings>\n')
                    elif find_element(p, 'kind') == 'bioavailability':
                        xmlfile.write('    <bioavailability>' + find_element(p, 'value') + '</bioavailability>\n')
                    elif find_element(p, 'kind') == 'rule_of_five':
                        xmlfile.write('    <rule_of_five>' + find_element(p, 'value') + '</rule_of_five>\n')
                    elif find_element(p, 'kind') == 'ghose_filter':
                        xmlfile.write('    <ghose_filter>' + find_element(p, 'value') + '</ghose_filter>\n')
                    elif find_element(p, 'kind') == 'veber_rule':
                        xmlfile.write('    <veber_rule>' + find_element(p, 'value') + '</veber_rule>\n')
                    elif find_element(p, 'kind') == 'mddr_like_rule':
                        xmlfile.write('    <mddr_like_rule>' + find_element(p, 'value') + '</mddr_like_rule>\n')

                xmlfile.write('    <spectrum>\n')
                for key, value in spectrum.items():
                    xmlfile.write('      <{}>{}</{}>\n'.format(key, value, key))
                xmlfile.write('    </spectrum>\n')

                xmlfile.write('  </metabolite>\n')

        xmlfile.write('</hmdb>')


# parse all the xml file in the folder "export" and write the result in the folder "parsed"
def parse_all_xml_files():
    # Crea la directory 'parsed/' se non esiste
    if not os.path.exists('../metabolites/hmdb_metabolites/parsed'):
        os.makedirs('../metabolites/hmdb_metabolites/parsed')

    for filename in os.listdir('../metabolites/hmdb_metabolites/split'):
        if filename.endswith(".xml"):
            full_path = os.path.join('../metabolites/hmdb_metabolites/split', filename)
            try:
                parser(full_path, '../metabolites/hmdb_metabolites/parsed/' + filename)
                print(f"Parsed {filename} successfully!")
            except Exception as e:
                print(f"Error parsing {filename}: {e}")


def parse_first_n_xml_files(n):
    # Create the directory 'parsed/' if it doesn't exist
    if not os.path.exists('../metabolites/hmdb_metabolites/parsed'):
        os.makedirs('../metabolites/hmdb_metabolites/parsed')

    i = 0
    for filename in os.listdir('../metabolites/hmdb_metabolites/split'):
        if filename.endswith(".xml"):
            full_path = os.path.join('../metabolites/hmdb_metabolites/split', filename)
            try:
                parser(full_path, '../metabolites/hmdb_metabolites/parsed/' + filename)
                print(f"Parsed {filename} successfully!")
            except Exception as e:
                print(f"        ---Error parsing {filename}: {e}")

            i += 1
            if i == n:
                break


parse_all_xml_files()
