from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.quokka import setup
from src.quokka.extension import Quokka


class TestQuokkaExtension:
    def test_extension_setup(self, app_instance) -> None:
        setup(app_instance.api)
        ext = Quokka(app_instance.api)
        lines = ["a = 10", "b = 20", "a + b"]
        res = ext.run_lines(lines)
        assert len(res) == 3
        assert res[2]["output"] == 30
