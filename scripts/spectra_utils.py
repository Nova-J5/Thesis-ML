import ast
import os
import xml.etree.ElementTree as ET


def min_max_values():
    metabolite_counter = 0
    max_peak_count = 0
    min_peak_count = float('inf')
    max_peak_intensity = 0
    min_peak_intensity = float('inf')
    max_mass_charge = 0
    min_mass_charge = float('inf')
    max_collision_energy_voltage = 0
    min_collision_energy_voltage = float('inf')
    unique_ids = set()

    for filename in os.listdir('../metabolites/hmdb_metabolites/parsed_gcms'):
        if filename.endswith(".xml"):
            full_path = os.path.join('../metabolites/hmdb_metabolites/parsed_gcms', filename)
            try:
                tree = ET.parse(full_path)
                root = tree.getroot()
                for metabolite in root.findall('metabolite'):
                    metabolite_counter += 1
                    unique_ids.add(metabolite.find('id').text)

                    for spectrum in metabolite.findall('spectrum'):

                        peak_count = int(spectrum.find('peak_counter').text)
                        if peak_count > max_peak_count:
                            max_peak_count = peak_count
                        if peak_count < min_peak_count:
                            min_peak_count = peak_count

                        # find max and min peak intensity in format [['15.0234751', '0.0215998644'], ['16.01872406',
                        # '1.891453219'], ...]
                        peaks_element = spectrum.find('peaks')
                        if peaks_element is not None:
                            # parse the text of the peaks element as a Python object
                            peaks_list = ast.literal_eval(peaks_element.text)
                            for peak in peaks_list:
                                mass_charge = float(peak[0])
                                if mass_charge > max_mass_charge:
                                    max_mass_charge = mass_charge
                                if mass_charge < min_mass_charge:
                                    min_mass_charge = mass_charge

                                intensity = float(peak[1])
                                if intensity > max_peak_intensity:
                                    max_peak_intensity = intensity
                                if intensity < min_peak_intensity:
                                    min_peak_intensity = intensity

            except Exception as e:
                print(f"Error parsing {filename}: {e}")

    print(f"Metabolites: {metabolite_counter}")
    print(f"Unique IDs: {len(unique_ids)}")
    print(f"Max peak count: {max_peak_count}")
    print(f"Min peak count: {min_peak_count}")
    print(f"Max peak intensity: {max_peak_intensity}")
    print(f"Min peak intensity: {min_peak_intensity}")
    print(f"Max charge: {max_mass_charge}")
    print(f"Min charge: {min_mass_charge}")
    print(f"Max collision energy voltage: {max_collision_energy_voltage}")
    print(f"Min collision energy voltage: {min_collision_energy_voltage}")


def peaks_similarity_on_single_spectrum(mode="intensity", distance=0.1, print_similar=False):
    metabolite_counter = 0
    intensity_counter = 0
    mass_charge_counter = 0
    for filename in os.listdir('../metabolites/hmdb_metabolites/parsed_gcms'):
        if filename.endswith(".xml"):
            full_path = os.path.join('../metabolites/hmdb_metabolites/parsed_gcms', filename)
            try:
                tree = ET.parse(full_path)
                root = tree.getroot()
                for metabolite in root.findall('metabolite'):
                    metabolite_counter += 1
                    found = False

                    for spectrum in metabolite.findall('spectrum'):
                        peaks_element = spectrum.find('peaks')
                        if peaks_element is not None:
                            # parse the text of the peaks element as a Python object
                            peaks_list_str = ast.literal_eval(peaks_element.text)
                            peaks_list = [(float(pair[0]), float(pair[1])) for pair in peaks_list_str]

                            for i, peak1 in enumerate(peaks_list):
                                for peak2 in peaks_list[i + 1:]:
                                    if mode == "intensity":
                                        if abs(peak1[1] - peak2[1]) <= distance:
                                            found = True
                                            if print_similar:
                                                print(f"Similar peaks: {peak1} and {peak2}")
                                    elif mode == "mass_charge":
                                        if abs(peak1[0] - peak2[0]) <= distance:
                                            found = True
                                            if print_similar:
                                                print(f"Similar peaks: {peak1} and {peak2}")

                    if found:
                        if mode == "intensity":
                            intensity_counter += 1
                            if print_similar:
                                print(
                                    f"metabolite: {metabolite.find('id').text}" + " spectrum: " + spectrum.find(
                                        'id').text)
                        elif mode == "mass_charge":
                            mass_charge_counter += 1
                            if print_similar:
                                print(
                                    f"metabolite: {metabolite.find('id').text} " + " spectrum: " + spectrum.find(
                                        'id').text)

            except Exception as e:
                print(f"Error parsing {filename}: {e}")

    if mode == "intensity":
        print(f"Similar (intensity) at distance {distance}: {intensity_counter}")
        print(intensity_counter / metabolite_counter * 100, "%")
    else:
        print(f"Similar (mass charge) at distance {distance}: {mass_charge_counter}")
        print(mass_charge_counter / metabolite_counter * 100, "%")


# min_max_values()

peaks_similarity_on_single_spectrum(mode="mass_charge", distance=0.5)
peaks_similarity_on_single_spectrum(mode="mass_charge", distance=0.1)
peaks_similarity_on_single_spectrum(mode="mass_charge", distance=0.05)
peaks_similarity_on_single_spectrum(mode="mass_charge", distance=0.01)

#%%
