"""Execute the setup notebook with the project's own Python kernel."""

from __future__ import annotations

import json
import os
from pathlib import Path
import platform
import site
import subprocess
import sys
from datetime import datetime, timezone
from importlib.metadata import version


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    venv = root / ".venv"
    expected_python = venv / "Scripts" / "python.exe"
    if sys.version_info < (3, 11):
        raise RuntimeError("Python 3.11 or newer is required.")
    if Path(sys.executable).resolve() != expected_python.resolve():
        raise RuntimeError(r"Run with .\.venv\Scripts\python.exe scripts\verify_environment.py")
    if sys.prefix == sys.base_prefix or site.ENABLE_USER_SITE:
        raise RuntimeError("Python must run in an isolated virtual environment.")

    # Keep Jupyter configuration and runtime files within this project.
    local_paths = {
        "JUPYTER_CONFIG_DIR": root / ".jupyter" / "config",
        "JUPYTER_DATA_DIR": root / ".jupyter" / "data",
        "JUPYTER_RUNTIME_DIR": root / ".jupyter" / "runtime",
        "IPYTHONDIR": root / ".ipython",
        "MPLCONFIGDIR": root / ".matplotlib",
    }
    for name, path in local_paths.items():
        path.mkdir(parents=True, exist_ok=True)
        os.environ[name] = str(path)
    os.environ["ML_ACADEMY_EXPECTED_PYTHON"] = str(expected_python)
    os.environ["PYTHONNOUSERSITE"] = "1"

    import nbformat
    from jupyter_client import KernelManager
    from jupyter_client.kernelspec import KernelSpecManager
    from nbclient import NotebookClient

    artifacts = root / "artifacts"
    artifacts.mkdir(exist_ok=True)
    report_path = artifacts / "environment-check.json"
    report = {
        "status": "running",
        "checked_at_utc": datetime.now(timezone.utc).isoformat(),
        "python": platform.python_version(),
        "executable": sys.executable,
        "platform": platform.platform(),
    }
    report_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")

    try:
        subprocess.run([sys.executable, "-m", "pip", "check"], check=True)
        kernel_name = "ml-academy"
        subprocess.run(
            [sys.executable, "-m", "ipykernel", "install", "--prefix", str(venv),
             "--name", kernel_name, "--display-name", "Python (ML Academy .venv)"],
            check=True,
        )
        # Restrict discovery to this environment; never fall back to a global kernel.
        specs = KernelSpecManager(
            kernel_dirs=[str(venv / "share" / "jupyter" / "kernels")],
            ensure_native_kernel=False,
        )
        spec = specs.get_kernel_spec(kernel_name)
        if Path(spec.argv[0]).resolve() != expected_python.resolve():
            raise RuntimeError("The Jupyter kernel points outside the project's .venv.")
        manager = KernelManager(kernel_name=kernel_name, kernel_spec_manager=specs)
        notebook = nbformat.read(root / "notebooks" / "environment_smoke_test.ipynb", as_version=4)
        nbformat.validate(notebook)
        client = NotebookClient(
            notebook, km=manager, timeout=120, startup_timeout=60,
            allow_errors=False, resources={"metadata": {"path": str(root)}},
        )
        executed = client.execute(cleanup_kc=True)
        code_cells = [cell for cell in executed.cells if cell.cell_type == "code"]
        if not code_cells or any(cell.execution_count is None for cell in code_cells):
            raise RuntimeError("Not all notebook cells executed.")
        outputs = [output for cell in code_cells for output in cell.outputs]
        if any(output.output_type == "error" for output in outputs):
            raise RuntimeError("A notebook cell failed.")
        if not any("image/png" in output.get("data", {}) for output in outputs):
            raise RuntimeError("Matplotlib did not produce an embedded PNG.")
        if not any("Environment smoke test passed." in output.get("text", "") for output in outputs):
            raise RuntimeError("The notebook did not reach its success marker.")
        nbformat.validate(executed)
        output_path = artifacts / "environment_smoke_test.executed.ipynb"
        nbformat.write(executed, output_path)
        packages = ["pip", "notebook", "ipykernel", "nbclient", "nbformat",
                    "numpy", "pandas", "matplotlib", "scikit-learn"]
        report.update(
            status="passed", code_cells_executed=len(code_cells),
            packages={name: version(name) for name in packages},
            kernel=kernel_name, kernel_executable=spec.argv[0],
            executed_notebook=str(output_path),
        )
    except Exception as exc:
        report.update(status="failed", error=str(exc))
        raise
    finally:
        report_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")

    print(f"PASS: {len(code_cells)} notebook code cells executed in {sys.executable}")
    print(f"Executed notebook: {output_path}")
    print(f"Verification report: {report_path}")


if __name__ == "__main__":
    main()
