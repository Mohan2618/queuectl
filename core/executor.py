import subprocess


def execute(command):
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True
        )

        return result.returncode == 0

    except Exception:
        return False