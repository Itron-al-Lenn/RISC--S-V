import os
from pathlib import Path

from cocotb.runner import get_runner

PROJ_PATH = Path(os.path.dirname(__file__)).parent

def runner(feature: str, srcs: list[str], parameters: list[tuple[str, str]] = [], clean = True):
    sources = [PROJ_PATH / "src" / src for src in srcs]
    build_args = []
    for parameter in parameters:
        build_args.append(f"-P{feature}.{parameter[0]}={parameter[1]}")
    
    runner = get_runner("icarus")
    runner.build(sources=sources, hdl_toplevel=feature, clean=clean, build_args=build_args)

    runner.test(hdl_toplevel=feature, test_module=f"test.test_{feature}")
