import os
import re
import subprocess

import pytest


# NOTE: The docker xdist group is so that these tests
# are not run in parralel and two docker instances contend
# for the same port
@pytest.mark.xdist_group(name="docker")
@pytest.mark.parametrize(
    "requirement",
    [
        "nx-cugraph-cu11",
        "nvidia-cuda-runtime-cu12==12.4.99",
    ],
)
def test_wheel_install(
    requirement, install_in_pypi, venv_python, pypi_server, nvidia_pypi_server
):
    assert install_in_pypi, "nvidia-stub wheel addition failed"
    env = os.environ.copy()
    env["NVIDIA_PIP_INDEX_URL"] = nvidia_pypi_server
    proc = subprocess.run(
        [
            venv_python,
            "-m",
            "pip",
            "install",
            "--no-deps",
            requirement,
            f"--index-url={pypi_server}",
        ],
        check=True,
        env=env,
        text=True,
        capture_output=True,
    )
    assert re.search(
        rf"Successfully installed {requirement.replace('==', '-')}", proc.stdout
    )
