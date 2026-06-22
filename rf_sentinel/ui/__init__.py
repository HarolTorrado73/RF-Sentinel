"""Interfaces de usuario."""


def __getattr__(name: str):
    if name in ("RFMainUI", "main"):
        from rf_sentinel.ui.desktop.main import RFMainUI, main

        return main if name == "main" else RFMainUI
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


__all__ = ["RFMainUI", "main"]
