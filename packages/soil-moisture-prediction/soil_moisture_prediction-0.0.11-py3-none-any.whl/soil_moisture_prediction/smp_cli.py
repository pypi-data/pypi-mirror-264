"""Command line module for soil moisture prediction."""

import argparse
import json
import logging
import os
import sys
import warnings

from soil_moisture_prediction.random_forest_model import RFoModel

# TODO catch warnings
warnings.filterwarnings("ignore")

parser = argparse.ArgumentParser()
parser.add_argument("-w", "--work_dir", type=str, required=True)
parser.add_argument(
    "-v",
    "--verbosity",
    choices=["quiet", "verbose", "debug"],
    default="verbose",
    help="Verbosity level (quiet, verbose [default], debug)",
)
# Test class passes its own arguments, this is to avoid conflict
if sys.argv[0] == "soil_moisture_prediction.py":
    args = parser.parse_args()


def main(verbosity, work_dir):
    """Run the soil moisture prediction module."""
    # Convert string choice to corresponding numeric level
    verbosity_levels = {"quiet": 30, "verbose": 20, "debug": 10}
    selected_verbosity = verbosity_levels[verbosity]
    logging.basicConfig(format="%(asctime)s - %(message)s", level=selected_verbosity)

    with open(os.path.join(work_dir, "parameters.json"), "r") as f_handle:
        input_data = json.loads(f_handle.read())

    logging.debug("Input data:")
    logging.debug(json.dumps(input_data, indent=4))

    rfo_model = RFoModel(**input_data, work_dir=work_dir)
    rfo_model.compute()
    rfo_model.plot_figure_selection()

    return rfo_model


if __name__ == "__main__":
    # TODO args.verbosity() did not work
    main(parser.parse_args().verbosity, parser.parse_args().work_dir)
