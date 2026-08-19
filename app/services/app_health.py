"""AL-HUDA Step 16 - lightweight application health checks.

This module is intentionally dependency-light and additive. It checks that
the core project structure exists without starting Android-only functionality.
"""

from pathlib import Path


class AppHealth:
    REQUIRED_PATHS = (
        "main.py",
        "buildozer.spec",
        "requirements.txt",
        "app",
        "app/screens",
        "app/services",
        "assets",
        "data",
        "backend",
    )

    @classmethod
    def check_project(cls, project_root=None):
        root = Path(project_root or Path(__file__).resolve().parents[2])
        missing = [item for item in cls.REQUIRED_PATHS if not (root / item).exists()]
        return {"ok": not missing, "missing": missing}

    @classmethod
    def summary(cls, project_root=None):
        result = cls.check_project(project_root)
        if result["ok"]:
            return "AL-HUDA project structure: OK"
        return "AL-HUDA project structure missing: " + ", ".join(result["missing"])
