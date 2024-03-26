import requests
from tqdm import tqdm
import sys,os



def download(package_name, version):
    # Remove ".py" from package_name if it ends with ".py"
    if package_name.endswith(".py"):
        package_name = package_name[:-3]

    url = f"https://zhrxxgroup.com/slame/spm/packages/{package_name}-{version}.py"
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    block_size = 1024  # 1 Kibibyte

    # Create a progress bar using tqdm
    filename = f"{package_name}.py"
    folder_path = os.path.join(os.getcwd(), "packages")
    file_path = os.path.join(folder_path, filename)

    # Ensure the folder exists, if not, create it
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    progress_bar = tqdm(total=total_size, unit='iB', unit_scale=True)
    with open(file_path, 'wb') as file:
        for data in response.iter_content(block_size):
            progress_bar.update(len(data))
            file.write(data)
    progress_bar.close()

    packages_py = os.path.join(folder_path, "packages_import.py")
    if not os.path.exists(packages_py):
        with open(packages_py, "w") as f:
            f.write(f"\nfrom packages import {package_name}")

    with open(packages_py, "a") as f:
        f.write(f"\nfrom packages import {package_name}")





def main():
    # Check if correct number of arguments is provided
    if len(sys.argv) != 4:
        print("Usage: python script_name.py install PACKAGE_NAME VERSION")
        return

    # Parse command-line arguments
    command = sys.argv[1]
    package_name = sys.argv[2]
    version = sys.argv[3]

    # Check if the command is 'install'
    if command != 'install':
        print("Invalid command")
        return

    download(package_name, version)
if __name__ == "__main__":

    """
    download_file("hello", 1.0)
    print("Download completed!")
    """
    download("hello.py", 1)
