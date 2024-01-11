import subprocess


def run_script(script_name):
    print(f"Running {script_name}...")

    subprocess.run(["python", script_name])

    print(f"{script_name} completed.\n")


def main():
    run_script("main.py")
    run_script("interpolate_handler.py")
    run_script("visualization_handler.py")

    print("All processes completed!")


if __name__ == "__main__":
    main()
