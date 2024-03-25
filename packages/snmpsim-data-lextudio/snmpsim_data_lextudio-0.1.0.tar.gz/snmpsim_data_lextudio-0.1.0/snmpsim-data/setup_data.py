# snmpsim_data/setup_data.py

import os
import shutil
import argparse
from pkg_resources import resource_filename

def setup_data(target_directory="."):
    """
    Copies data files from the package to a specified directory.

    Parameters:
    - target_directory (str): The directory where data files will be copied.
      Defaults to the current directory if not specified.
    """
    try:
        source_directory = resource_filename('snmpsim_data', 'data')
    except ImportError:
        print("Error: Could not locate the 'snmpsim_data' package. Is it installed?")
        return

    if not os.path.exists(source_directory):
        print(f"Error: The source data directory '{source_directory}' does not exist.")
        return

    for filename in os.listdir(source_directory):
        source_file = os.path.join(source_directory, filename)
        target_file = os.path.join(target_directory, filename)
        try:
            shutil.copy(source_file, target_file)
            print(f"Copied {source_file} to {target_file}")
        except Exception as e:
            print(f"Error copying {source_file} to {target_file}: {e}")

def main():
    """
    Main function to execute the setup_data script.
    Handles command-line arguments for displaying help and specifying the target directory.
    """
    parser = argparse.ArgumentParser(
        description="Copies SNMP simulation data files to a specified directory. " 
                    "By default, files are copied to the current directory."
    )
    parser.add_argument(
        'target_directory', nargs='?', default=".",
        help="The directory where data files will be copied (default: current directory)."
    )
    
    args = parser.parse_args()
    
    print(f"Copying SNMP simulation data files to '{args.target_directory}'...")
    setup_data(args.target_directory)

if __name__ == "__main__":
    main()
