from __future__ import annotations

import typing

from biscuit.extensions import Extension

if typing.TYPE_CHECKING:
    from biscuit.api import ExtensionsAPI


class Quokka(Extension):
    """Live interactive scratchpad runner with instant expression evaluation."""

    def __init__(self, api: ExtensionsAPI) -> None:
        super().__init__(api)
        self.api = api
        self.api.logger.info("Quokka extension initialised.")

    def evaluate_expression(self, expr: str, context: dict | None = None) -> object:
        ctx = context or {}
        try:
            return eval(expr, {}, ctx)
        except Exception as e:
            return f"Error: {e}"

    def run_lines(self, lines: list[str]) -> list[dict]:
        results = []
        ctx: dict = {}
        for idx, line in enumerate(lines, start=1):
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" in line and not line.startswith("="):
                var, val = line.split("=", 1)
                try:
                    res = eval(val.strip(), {}, ctx)
                    ctx[var.strip()] = res
                    results.append({"line": idx, "output": res})
                except Exception as e:
                    results.append({"line": idx, "error": str(e)})
            else:
                out = self.evaluate_expression(line, ctx)
                results.append({"line": idx, "output": out})
        return results

    def install(self) -> None:
        self.api.logger.info("Quokka extension installed.")
