import os
import time
from tkinter import Tk, filedialog, messagebox

def get_mod_filenames(folder_path):
    mod_filenames = []
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path) and filename.endswith(".jar"):
            mod_filenames.append(filename.lower())  # Convert to lowercase for case-insensitive comparison
    return mod_filenames

def save_mod_filenames_to_file(mod_filenames, file_path):
    with open(file_path, "w") as file:
        num_mods = len(mod_filenames)
        file.write(f"Total number of mods: {num_mods}\n\n")
        if num_mods > 0:
            file.write("Mod Filenames:\n\n")
            for mod_filename in mod_filenames:
                file.write(f"{mod_filename}\n")
        else:
            file.write("No mods found in the folder.")

def save_missing_mods_to_file(missing_mods, file_path, missing_on_server=False):
    with open(file_path, "w") as file:
        num_missing_mods = len(missing_mods)
        file.write(f"Total number of missing mods: {num_missing_mods}\n\n")
        if num_missing_mods > 0:
            file.write("Missing Mods:\n\n")
            for mod_name in missing_mods:
                location = "Server" if missing_on_server else "Locally"
                file.write(f"{mod_name} (Missing on {location})\n")
        else:
            file.write("No missing mods found.")

def process_mod_list(mod_list):
    processed_mod_list = []
    for line in mod_list:
        if not line.strip().endswith("kB") and not line.strip().endswith("MB"):
            processed_mod_list.append(line.strip().lower())  # Convert to lowercase for case-insensitive comparison
    return processed_mod_list


def main():
    root = Tk()
    root.withdraw()

    print("Welcome to the Minecraft Mod List Extractor!")
    print("Please follow the prompts to select the mods folder and output files.")
    input("Press Enter to continue...")
    print("Select Minecraft mods folder")

    mods_folder = filedialog.askdirectory(title="Select Minecraft mods folder")
    if not mods_folder:
        print("No mods folder selected. Program will exit.")
        input("Press Enter to exit...")
        return

    print("Save mod filenames list as... (You can give it a name here too)")
    output_file = filedialog.asksaveasfilename(
        title="Save mod filenames list as",
        defaultextension=".txt",
        filetypes=[("Text Files", "*.txt")]
    )
    if not output_file:
        print("No output file selected. Program will exit.")
        input("Press Enter to exit...")
        return

    mod_filenames = get_mod_filenames(mods_folder)

    save_mod_filenames_to_file(mod_filenames, output_file)
    directory = os.path.dirname(os.path.abspath(output_file))
    os.chdir(directory)
    print(f"Mod filenames list extracted! List saved at: {output_file}")

    # Prompt the user to paste the server mod list (with file sizes)
    print("Paste the server mod list (with file sizes) and press Enter twice to finish:")
    server_mod_list = []
    while True:
        line = input()
        if not line:
            break
            if not server_mod_list:
                break
        server_mod_list.append(line)

    # Process both server and local mod lists
    processed_server_mod_list = process_mod_list(server_mod_list)
    processed_local_mod_list = process_mod_list(mod_filenames)

    # Compare processed server mod list with processed local mod list
    missing_mods_on_server = [mod_name for mod_name in processed_server_mod_list if mod_name not in processed_local_mod_list]
    missing_mods_locally = [mod_name for mod_name in processed_local_mod_list if mod_name not in processed_server_mod_list]

    # Save missing mods to separate files indicating the location
    missing_mods_server_output_file = os.path.join(directory, "missing_mods_server.txt")
    missing_mods_locally_output_file = os.path.join(directory, "missing_mods_locally.txt")

    save_missing_mods_to_file(missing_mods_on_server, missing_mods_server_output_file, missing_on_server=True)
    save_missing_mods_to_file(missing_mods_locally, missing_mods_locally_output_file, missing_on_server=False)

    print(f"Missing mods that are on server (that you don't have) list saved at: {missing_mods_server_output_file}")
    print(f"Missing mods that you have locally (that the server doesn't have) list saved at: {missing_mods_locally_output_file}")
    print("Keep in mind that some mods may have different versions, so they may appear as missing due to that, this should help you keep your mods on the same version too!")

    input("Press Enter to exit...")

if __name__ == "__main__":
    main()