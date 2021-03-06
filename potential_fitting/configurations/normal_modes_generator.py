from potential_fitting import calculator
from potential_fitting.molecule import xyz_to_molecules
from potential_fitting.utils import SettingsReader

def generate_normal_modes(settings_path, geo_path, normal_modes_path):
    """
    Generates the normal modes based on a given optimized geometry
    """
    
    settings = SettingsReader(settings_path)

    # parse the optimized geometry
    molecule = xyz_to_molecules(geo_path, settings)[0]
    
    # calculate the normal modes
    normal_modes, frequencies, red_masses = calculator.frequencies(settings, molecule, settings.get("config_generator", "method"), settings.get("config_generator", "basis"))

    # calculate dim null
    dim_null = 3 * molecule.get_num_atoms() - len(normal_modes)
    
    # write the normal modes to the output file
    write_normal_modes(normal_modes, frequencies, red_masses, normal_modes_path)

    # return dim null so it can be used as input to configuration_generator
    return dim_null

def write_normal_modes(normal_modes, frequencies, red_masses, normal_modes_path):

    # formatter strings
    norm_formatter = "{:> 12.4f}"
    freq_formatter = "{:.2f}"
    mass_formatter = "{:.6f}"

    normal_out = ""
    
    num_modes = len(frequencies)

    # for each normal mode
    for i in range(1, 1 + num_modes):
        index = i - 1
        
        # get the geometry of this normal mode
        geo = normal_modes[index]
        
        normal_out += "normal mode: " + str(i) + "\n"
        normal_out += freq_formatter.format(frequencies[index]) + "\n"
        normal_out += "red_mass = " + mass_formatter.format(red_masses[index]) + "\n"
        
        # for each atom in the molecule
        for atom in range(len(geo)):
            # write this atom's x, y, and z for this normal mode, setting any values below .000001 to 0.
            normal_out += norm_formatter.format(0.0 if abs(float(geo[atom][0])) < 1e-6 else float(geo[atom][0])) + "\t"
            normal_out += norm_formatter.format(0.0 if abs(float(geo[atom][1])) < 1e-6 else float(geo[atom][1])) + "\t"
            normal_out += norm_formatter.format(0.0 if abs(float(geo[atom][2])) < 1e-6 else float(geo[atom][2])) + "\n"
        
        normal_out += "\n"

    # write the normal modes to the output file
    with open(normal_modes_path, 'w') as norm_file:
        norm_file.write(normal_out)
