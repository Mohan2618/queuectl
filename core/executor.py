import subprocess


def execute(command):
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True
        )

        return {
            "success": result.returncode == 0,
            "stdout": result.stdout.strip(),
            "stderr": result.stderr.strip(),
            "exit_code": result.returncode
        }

    except Exception as e:
        return {
            "success": False,
            "stdout": "",
            "stderr": str(e),
            "exit_code": -1
        }