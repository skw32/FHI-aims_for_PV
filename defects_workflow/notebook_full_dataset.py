
import types
import sys
import io
from IPython import get_ipython
from nbformat import read
from IPython.core.interactiveshell import InteractiveShell
import os

class NotebookLoader(object):
    """Module Loader for Jupyter Notebooks"""
    def __init__(self):
        self.shell = InteractiveShell.instance()
    def run_notebook(self, module_identity, path_to_notebook, initial_ns={}):
        """import a notebook as a module"""

        # load the notebook object
        with io.open(path_to_notebook, 'r', encoding='utf-8') as f:
            nb = read(f, 4)

        # create the module and add it to sys.modules
        # if name in sys.modules:
        #    return sys.modules[name]
        mod = types.ModuleType(module_identity)
        mod.__file__ = path_to_notebook
        mod.__loader__ = self
        mod.__dict__['get_ipython'] = get_ipython
        sys.modules[module_identity] = mod

        # extra work to ensure that magics that would affect the user_ns
        # actually affect the notebook module's ns
        save_user_ns = self.shell.user_ns
        self.shell.user_ns = mod.__dict__

        # inject provided values into the module namespace prior to running any cells
        mod.__dict__.update(initial_ns)

        try:
            for i, cell in enumerate(nb.cells):
                # loop over the code cells
                if cell.cell_type == 'code':
                    # skip cells which contain 'skip_cell_when_run_as_script' metadata
                    if 'metadata' in cell and 'skip_cell_when_run_as_script' in cell.metadata and cell.metadata['skip_cell_when_run_as_script'] == True:
                        print("Cell {0} of notebook is skipped when running for full dataset".format(i))
                        continue
                    else:
                        # transform the input to executable Python
                        code = self.shell.input_transformer_manager.transform_cell(
                            cell.source)
                        # run the code in themodule
                        exec(code, mod.__dict__)
        finally:
            self.shell.user_ns = save_user_ns
        return mod

base_dir = "/Users/suzy/Desktop/DefectAnalysis/EnargiteDefects/fromLandau/Results/data/final_one_shots/"

defect_dataset = {
    "V-S_q=+1_sg=1": [
        # neutral_dir, charge_dir, charge_state
        "VacancySupercells/V-S/neutral/DefectSpacegroup1", "VacancySupercells/V-S/charged/+1/DefectSpacegroup1", 1
    ],
    "V-S_q=+2_sg=1": [
        # neutral_dir, charge_dir, charge_state
        "VacancySupercells/V-S/neutral/DefectSpacegroup1", "VacancySupercells/V-S/charged/+2/DefectSpacegroup1", 2
    ],
    "V-S_q=+1_sg=6_s1": [
        # neutral_dir, charge_dir, charge_state
        "VacancySupercells/V-S/neutral/DefectSpacegroup6/structure1", "VacancySupercells/V-S/charged/+1/DefectSpacegroup6/structure1", 1
    ],
    "V-S_q=+1_sg=6_s2": [
        # neutral_dir, charge_dir, charge_state
        "VacancySupercells/V-S/neutral/DefectSpacegroup6/structure2", "VacancySupercells/V-S/charged/+1/DefectSpacegroup6/structure2", 1
    ],
    "V-S_q=+2_sg=6_s1": [
        # neutral_dir, charge_dir, charge_state
        "VacancySupercells/V-S/neutral/DefectSpacegroup6/structure1", "VacancySupercells/V-S/charged/+2/DefectSpacegroup6/structure1", 2
    ],
    "V-S_q=+2_sg=6_s2": [
        # neutral_dir, charge_dir, charge_state
        "VacancySupercells/V-S/neutral/DefectSpacegroup6/structure2", "VacancySupercells/V-S/charged/+2/DefectSpacegroup6/structure2", 2
    ],
    "V-Cu_q=-1_sg=1": [
        # neutral_dir, charge_dir, charge_state
        "VacancySupercells/V-Cu/neutral/DefectSpacegroup1", "VacancySupercells/V-Cu/charged/-1/DefectSpacegroup1", -1
    ],
    "V-Cu_q=-1_sg=6": [
        # neutral_dir, charge_dir, charge_state
        "VacancySupercells/V-Cu/neutral/DefectSpacegroup6", "VacancySupercells/V-Cu/charged/-1/DefectSpacegroup6", -1
    ],
    "V-As_q=-1_sg=6": [
        # neutral_dir, charge_dir, charge_state
        "VacancySupercells/V-As/neutral/DefectSpacegroup6", "VacancySupercells/V-As/charged/-1/DefectSpacegroup6", -1
    ],
    "V-As_q=-2_sg=6": [
        # neutral_dir, charge_dir, charge_state
        "VacancySupercells/V-As/neutral/DefectSpacegroup6", "VacancySupercells/V-As/charged/-2/DefectSpacegroup6", -2
    ],
    "V-As_q=-3_sg=6": [
        # neutral_dir, charge_dir, charge_state
        "VacancySupercells/V-As/neutral/DefectSpacegroup6", "VacancySupercells/V-As/charged/-3/DefectSpacegroup6", -3
    ],
    "V-As_q=-4_sg=6": [
        # neutral_dir, charge_dir, charge_state
        "VacancySupercells/V-As/neutral/DefectSpacegroup6", "VacancySupercells/V-As/charged/-4/DefectSpacegroup6", -4
    ],
    "V-As_q=-5_sg=6": [
        # neutral_dir, charge_dir, charge_state
        "VacancySupercells/V-As/neutral/DefectSpacegroup6", "VacancySupercells/V-As/charged/-5/DefectSpacegroup6", -5
    ],
    "As_Cu_q=+1_sg=1": [
        # neutral_dir, charge_dir, charge_state
        "AntisiteSupercells/As-Cu/neutral/DefectSpacegroup1", "AntisiteSupercells/As-Cu/charged/+1/DefectSpacegroup1", 1
    ],
    "As_Cu_q=+2_sg=1": [
        # neutral_dir, charge_dir, charge_state
        "AntisiteSupercells/As-Cu/neutral/DefectSpacegroup1", "AntisiteSupercells/As-Cu/charged/+2/DefectSpacegroup1", 2
    ],
    "As_Cu_q=+3_sg=1": [
        # neutral_dir, charge_dir, charge_state
        "AntisiteSupercells/As-Cu/neutral/DefectSpacegroup1", "AntisiteSupercells/As-Cu/charged/+3/DefectSpacegroup1", 3
    ],
    "As_Cu_q=+4_sg=1": [
        # neutral_dir, charge_dir, charge_state
        "AntisiteSupercells/As-Cu/neutral/DefectSpacegroup1", "AntisiteSupercells/As-Cu/charged/+4/DefectSpacegroup1", 4
    ],
    "As_Cu_q=+1_sg=6": [
        # neutral_dir, charge_dir, charge_state
        "AntisiteSupercells/As-Cu/neutral/DefectSpacegroup6", "AntisiteSupercells/As-Cu/charged/+1/DefectSpacegroup6", 1
    ],
    "As_Cu_q=+2_sg=6": [
        # neutral_dir, charge_dir, charge_state
        "AntisiteSupercells/As-Cu/neutral/DefectSpacegroup6", "AntisiteSupercells/As-Cu/charged/+2/DefectSpacegroup6", 2
    ],
    "As_Cu_q=+3_sg=6": [
        # neutral_dir, charge_dir, charge_state
        "AntisiteSupercells/As-Cu/neutral/DefectSpacegroup6", "AntisiteSupercells/As-Cu/charged/+3/DefectSpacegroup6", 3
    ],
    "As_Cu_q=+4_sg=6": [
        # neutral_dir, charge_dir, charge_state
        "AntisiteSupercells/As-Cu/neutral/DefectSpacegroup6", "AntisiteSupercells/As-Cu/charged/+4/DefectSpacegroup6", 4
    ],

    "Cu_As_q=-1_sg=6": [
        # neutral_dir, charge_dir, charge_state
        "AntisiteSupercells/Cu-As/neutral/DefectSpacegroup6", "AntisiteSupercells/Cu-As/charged/-1/DefectSpacegroup6", -1
    ],
    "Cu_As_q=-2_sg=6": [
        # neutral_dir, charge_dir, charge_state
        "AntisiteSupercells/Cu-As/neutral/DefectSpacegroup6", "AntisiteSupercells/Cu-As/charged/-2/DefectSpacegroup6", -2
    ],
    "Cu_As_q=-3_sg=6": [
        # neutral_dir, charge_dir, charge_state
        "AntisiteSupercells/Cu-As/neutral/DefectSpacegroup6", "AntisiteSupercells/Cu-As/charged/-3/DefectSpacegroup6", -3
    ],
    "Cu_As_q=-4_sg=6": [
        # neutral_dir, charge_dir, charge_state
        "AntisiteSupercells/Cu-As/neutral/DefectSpacegroup6", "AntisiteSupercells/Cu-As/charged/-4/DefectSpacegroup6", -4
    ]
}

global_configuration = {
    "dielectric_xx": 7.49,
    "dielectric_yy": 6.92,
    "dielectric_zz": 7.19,
    "path_to_coffee_dir": '/Users/suzy/Desktop/DefectAnalysis/CoFFEE_1.1',
    "path_to_all_defects": '/Users/suzy/Desktop/DefectAnalysis/EnargiteDefects/fromLandau/Results/data/final_one_shots',
    "path_to_host": '/Users/suzy/Desktop/DefectAnalysis/EnargiteDefects/fromLandau/Results/data/final_one_shots/PerfectReference',
    "charge_model_file": 'charge_model.dat',
    "pa_plot_file": 'pa_plot.png',
    "manual_cutoff": None
}

def copy_with_keys(orig_dict, new_values):
    x = {}
    x.update(orig_dict)
    x.update(new_values)
    return x

configurations = []
for name, (neutral_dir, charge_dir, charge_state) in defect_dataset.items():
    # make sure required inputs exists
    path_to_defect = os.path.join(base_dir, charge_dir)
    path_to_neutral = os.path.join(base_dir, neutral_dir)  
    assert os.path.exists(path_to_defect), 'required input directory is missing {0}'.format(path_to_defect)
    assert os.path.exists(path_to_neutral), 'required input directory is missing {0}'.format(path_to_neutral)
    config = copy_with_keys(global_configuration, {
        "defect_outputs_dir": name,
        "path_to_defect": path_to_defect,
        "path_to_neutral": path_to_neutral,
        "defect_charge": charge_state
    })
    configurations.append(config)

#print(configurations)

for config in configurations:
    notebook = NotebookLoader()
    try:
        notebook.run_notebook(
            "test_namespace", "./DefectCorrectionsNotebook.ipynb", config)
    except Exception as err:
        print("Caught error when executing notebook {0} {1}".format(err, config))

print("FINISHED")
print("Outputs for all defects processed can be found in directories: "+ ", ".join(defect_dataset.keys()) )