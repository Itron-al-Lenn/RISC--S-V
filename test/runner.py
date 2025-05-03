from pathlib import Path

from cocotb.runner import get_runner


def runner(feature: str, srcs: list[str]):
    proj_path = Path(__file__).resolve().parent.parent
    sources = [proj_path / "src" / src for src in srcs]
    
    runner = get_runner("icarus")
    runner.build(sources=sources, hdl_toplevel=feature)

    runner.test(hdl_toplevel=feature, test_module=f"test.test_{feature}")

