# MIT License

# Copyright (c) 2023 Juan L. Gamella

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import causalchamber.datasets.utils as utils
from pathlib import Path
import pandas as pd
import yaml
from PIL import Image
import numpy as np
import os


# Maybe have this as a downloadable YAML file
directory_path = Path(Path(__file__).parents[0], "directory.yaml")
with open(directory_path, "r") as f:
    directory = yaml.load(f, Loader=yaml.Loader)
    f.close()

# --------------------------------------------------------------------
# Base Dataset and Experiment classes

citation = """
@article{gamella2024chamber,
  title={The Causal Chambers: Real Physical Systems as a Testbed for AI Methodology},
  author={Gamella, Juan L. and B\"uhlmann, Peter and Peters, Jonas},
  journal={(work in progress)},
  year={2023}
}
"""

print(f"If you use our datasets for your work please consider citing:\n{citation}")


class Dataset:
    def __init__(self, name, root, download=True):
        available_datasets = directory["datasets"].keys()
        if name not in available_datasets:
            string = ""
            for d in available_datasets:
                string += '  "' + d + '"\n'
            raise ValueError(
                f'Dataset "{name}" is not available. Available datasets:\n{string}'
            )
        # Store attributes
        self.name = name
        self.root = root
        self.image = directory["datasets"][name]["image"]
        # Check if dataset has already been downloaded to root
        dataset_dir = Path(self.root, self.name)
        if os.path.isdir(dataset_dir):
            print(f'Dataset {self.name} found in "{dataset_dir}".')
        else:
            if download:
                # Download, verify and extract
                self.url = directory["datasets"][name]["url"]
                self.checksum = directory["datasets"][name]["md5"]
                utils.download_and_extract(self.url, self.root, self.checksum)
            else:
                raise FileNotFoundError(
                    f'Could not find dataset directory "{dataset_dir}". Set download=True or choose another root directory (root).'
                )
        # Load available experiments
        #   If not an image dataset, experiments are just .csv files in the dataset directory
        #   If an image dataset, each experiment is a folder
        #   containing the .csv file with measurements and a subfolder
        #   with the images

        if self.image:
            experiment_names = [p.name for p in Path(self.root).glob(f"{self.name}/*")]
            csv_paths = [
                Path(self.root, self.name, e, f"{e}.csv") for e in experiment_names
            ]
            experiments = [ImageExperiment(self.name, path) for path in csv_paths]
        else:
            csv_paths = [p for p in Path(self.root).glob(f"{self.name}/*.csv")]
            experiments = [Experiment(self.name, path) for path in csv_paths]
        # Store experiment dictionary
        assert len(experiments) > 0
        self.__experiments = dict((e.name, e) for e in experiments)

    def available_experiments(self):
        return list(self.__experiments.keys())

    def get_experiment(self, name):
        return self.__experiments[name]


class Experiment:
    def __init__(self, dataset_name, csv_path):
        self.dataset = dataset_name
        self.csv_path = csv_path
        self.name = csv_path.stem
        self.columns = pd.read_csv(self.csv_path, nrows=0).columns.tolist()

    def as_pandas_dataframe(self):
        """Returns a pandas dataframe with the experiment data (excl. images)"""
        return pd.read_csv(self.csv_path)

    def as_image_array(self):
        raise NotImplementedError("This is not an image dataset!")


class ImageExperiment(Experiment):
    def __init__(self, dataset_name, csv_path):
        super().__init__(dataset_name, csv_path)
        self.image_folders = {}
        for path in [p for p in Path(csv_path.parents[0]).glob("images_*")]:
            size = path.stem.split("_")[1]
            self.image_folders[size] = path

    def available_sizes(self):
        return list(self.image_folders.keys())

    def as_image_array(self, size):
        """Returns a numpy array with all the images along the first dimension (axis-0)"""
        if size not in self.image_folders.keys():
            raise ValueError(
                f" Size {size} not available; available image sizes: {list(self.image_folders.keys())}."
            )
        image_filenames = pd.read_csv(self.csv_path).image_file
        image_folder = self.image_folders[size]
        image_paths = [Path(image_folder, f) for f in image_filenames]
        return np.array([np.array(Image.open(f)) for f in image_paths])


latex_names = {
    # Light tunnel variables
    "red": r"R",
    "green": r"G",
    "blue": r"B",
    "osr_c": r"O_C",
    "v_c": r"R_C",
    "current": r"\tilde{C}",
    "pol_1": r"\theta_1",
    "pol_2": r"\theta_2",
    "osr_angle_1": r"O_1",
    "osr_angle_2": r"O_2",
    "v_angle_1": r"R_1",
    "v_angle_2": r"R_2",
    "angle_1": r"\tilde{\theta}_1",
    "angle_2": r"\tilde{\theta}_2",
    "ir_1": r"\tilde{I}_1",
    "vis_1": r"\tilde{V}_1",
    "ir_2": r"\tilde{I}_2",
    "vis_2": r"\tilde{V}_2",
    "ir_3": r"\tilde{I}_3",
    "vis_3": r"\tilde{V}_3",
    "l_11": r"L_{11}",
    "l_12": r"L_{12}",
    "l_21": r"L_{21}",
    "l_22": r"L_{22}",
    "l_31": r"L_{31}",
    "l_32": r"L_{32}",
    "diode_ir_1": r"D^I_1",
    "diode_vis_1": r"D^V_1",
    "diode_ir_2": r"D^I_2",
    "diode_vis_2": r"D^V_2",
    "diode_ir_3": r"D^I_3",
    "diode_vis_3": r"D^V_3",
    "t_ir_1": r"T^I_1",
    "t_vis_1": r"T^V_1",
    "t_ir_2": r"T^I_2",
    "t_vis_2": r"T^V_2",
    "t_ir_3": r"T^I_3",
    "t_vis_3": r"T^V_3",
    "im": r"\tilde{\text{I}}\text{m}",
    "shutter_speed": r"T_\text{Im}",
    "aperture": r"\text{Ap}",
    "iso": r"\text{ISO}",
    # Wind tunnel variables
    "hatch": r"H",
    "pot_1": r"A_1",
    "pot_2": r"A_2",
    "osr_1": r"O_1",
    "osr_2": r"O_2",
    "osr_mic": r"O_M",
    "osr_in": r"O_\text{in}",
    "osr_out": r"O_\text{out}",
    "osr_upwind": r"O_\text{up}",
    "osr_downwind": r"O_\text{dw}",
    "osr_ambient": r"O_\text{amb}",
    "osr_intake": r"O_\text{int}",
    "v_1": r"R_1",
    "v_2": r"R_2",
    "v_mic": r"R_M",
    "v_in": r"R_\text{in}",
    "v_out": r"R_\text{out}",
    "load_in": r"L_\text{in}",
    "load_out": r"L_\text{out}",
    "current_in": r"\tilde{C}_\text{in}",
    "current_out": r"\tilde{C}_\text{out}",
    "res_in": r"T_\text{in}",
    "res_out": r"T_\text{out}",
    "rpm_in": r"\tilde{\omega}_\text{in}",
    "rpm_out": r"\tilde{\omega}_\text{out}",
    "pressure_upwind": r"\tilde{P}_\text{up}",
    "pressure_downwind": r"\tilde{P}_\text{dw}",
    "pressure_ambient": r"\tilde{P}_\text{amb}",
    "pressure_intake": r"\tilde{P}_\text{int}",
    "mic": r"\tilde{M}",
    "signal_1": r"\tilde{S}_1",
    "signal_2": r"\tilde{S}_2",
}


def latex_name(var, enclose=True):
    """Translate from machine variable name to latex name."""
    if var not in latex_names:
        return var
    else:
        name = latex_names[var]
        return "$" + name + "$" if enclose else name


lt_standard_edges = [
    ("red", "ir_1"),
    ("green", "ir_1"),
    ("blue", "ir_1"),
    ("red", "ir_2"),
    ("green", "ir_2"),
    ("blue", "ir_2"),
    ("red", "ir_3"),
    ("green", "ir_3"),
    ("blue", "ir_3"),
    ("red", "vis_1"),
    ("green", "vis_1"),
    ("blue", "vis_1"),
    ("red", "vis_2"),
    ("green", "vis_2"),
    ("blue", "vis_2"),
    ("red", "vis_3"),
    ("green", "vis_3"),
    ("blue", "vis_3"),
    ("red", "current"),
    ("green", "current"),
    ("blue", "current"),
    ("pol_1", "ir_3"),
    ("pol_2", "ir_3"),
    ("pol_1", "vis_3"),
    ("pol_2", "vis_3"),
    ("pol_1", "angle_1"),
    ("pol_2", "angle_2"),
    ("v_angle_1", "angle_1"),
    ("osr_angle_1", "angle_1"),
    ("v_angle_2", "angle_2"),
    ("osr_angle_2", "angle_2"),
    ("v_c", "current"),
    ("osr_c", "current"),
    ("l_11", "ir_1"),
    ("l_12", "ir_1"),
    ("l_11", "vis_1"),
    ("l_12", "vis_1"),
    ("t_ir_1", "ir_1"),
    ("diode_ir_1", "ir_1"),
    ("t_vis_1", "vis_1"),
    ("diode_vis_1", "vis_1"),
    ("l_21", "ir_2"),
    ("l_22", "ir_2"),
    ("l_21", "vis_2"),
    ("l_22", "vis_2"),
    ("t_ir_2", "ir_2"),
    ("diode_ir_2", "ir_2"),
    ("t_vis_2", "vis_2"),
    ("diode_vis_2", "vis_2"),
    ("l_31", "ir_3"),
    ("l_32", "ir_3"),
    ("l_31", "vis_3"),
    ("l_32", "vis_3"),
    ("t_ir_3", "ir_3"),
    ("diode_ir_3", "ir_3"),
    ("t_vis_3", "vis_3"),
    ("diode_vis_3", "vis_3"),
    ("pol_1", "im"),
    ("pol_2", "im"),
    ("red", "im"),
    ("green", "im"),
    ("blue", "im"),
    ("shutter_speed", "im"),
    ("aperture", "im"),
    ("iso", "im"),
]

wt_standard_edges = [
    ("load_in", "rpm_in"),
    ("res_in", "rpm_in"),
    ("load_in", "rpm_out"),
    ("load_in", "current_in"),
    ("load_in", "current_out"),
    ("load_out", "rpm_in"),
    ("load_out", "rpm_out"),
    ("res_out", "rpm_out"),
    ("load_out", "current_out"),
    ("load_out", "current_in"),
    ("hatch", "rpm_in"),
    ("hatch", "rpm_out"),
    ("load_in", "pressure_intake"),
    ("hatch", "pressure_intake"),
    ("load_out", "pressure_intake"),
    ("osr_intake", "pressure_intake"),
    ("load_in", "pressure_upwind"),
    ("hatch", "pressure_upwind"),
    ("load_out", "pressure_upwind"),
    ("osr_up", "pressure_upwind"),
    ("load_in", "pressure_downwind"),
    ("hatch", "pressure_downwind"),
    ("load_out", "pressure_downwind"),
    ("osr_downwind", "pressure_downwind"),
    ("osr_ambient", "pressure_ambient"),
    ("osr_in", "current_in"),
    ("v_in", "current_in"),
    ("osr_out", "current_out"),
    ("v_out", "current_out"),
    ("pot_1", "signal_1"),
    ("osr_1", "signal_1"),
    ("v_1", "signal_1"),
    ("pot_1", "signal_2"),
    ("pot_2", "signal_2"),
    ("osr_2", "signal_2"),
    ("v_2", "signal_2"),
    ("pot_1", "mic"),
    ("load_in", "mic"),
    ("load_out", "mic"),
    ("hatch", "mic"),
    ("osr_mic", "mic"),
    ("v_mic", "mic"),
]
