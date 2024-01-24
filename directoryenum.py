import subprocess
import re
import sys

def command_exists(command):
    """Check if a command exists"""
    return subprocess.call(["which", command], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) == 0

def run_command(command, output_file):
    """Run a command and write positive results to a file"""
    with open(output_file, "w") as file:
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
        for line in process.stdout:
            if "positive condition" in line:  # Replace with actual condition for positive results
                file.write(line)
                print(line, end='')

def main():
    # Check for required tools
    if not all(command_exists(tool) for tool in ["dirb", "gobuster", "ffuf"]):
        print("Error: Please make sure Dirb, Gobuster, and ffuf are installed.", file=sys.stderr)
        sys.exit(1)

    # Ask for the IP address
    ip_address = input("Enter the IP address: ")

    # Simple IP address format validation
    if not re.match(r"^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+$", ip_address):
        print("Invalid IP address format.")
        sys.exit(1)

    # Ask for the wordlist
    wordlist = input("Enter the path to the wordlist: ")

    # Define a base URL (assuming HTTP protocol)
    base_url = f"http://{ip_address}"

    # Run Dirb
    print("Running Dirb...")
    run_command(["dirb", base_url, wordlist], f"dirb_{ip_address}.txt")

    # Run Gobuster
    print("Running Gobuster...")
    run_command(["gobuster", "dir", "-u", base_url, "-w", wordlist], f"gobuster_{ip_address}.txt")

    # Run ffuf
    print("Running ffuf...")
    run_command(["ffuf", "-u", f"{base_url}/FUZZ", "-w", wordlist, "-o", f"ffuf_{ip_address}.json", "-of", "json"], f"ffuf_{ip_address}.json")

    print("Enumeration complete.")

if __name__ == "__main__":
    main()
