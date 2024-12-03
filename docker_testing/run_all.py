import subprocess

# scripts in order that they need to run in order to prevent conflicts
# starts by clearing out all tables
scripts = [
    "./docker_testing/clear_all_data.py", 
    "./docker_testing/users_data.py",
    "./docker_testing/activeusers_data.py",
    "./docker_testing/competitions_data.py",
    "./docker_testing/usercompetitions_data.py",
    "./docker_testing/songs_data.py",
    "./docker_testing/playlists_data.py",
    "./docker_testing/votes_data.py"
]

def execute_scripts():
    for script in scripts:
        try:
            print(f"Running {script}...")
            subprocess.run(["python3", script], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error occurred while running {script}: {e}")
            break

def main():
    execute_scripts()

if __name__ == "__main__":
    main()
