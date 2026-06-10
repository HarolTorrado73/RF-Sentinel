"""Servicio de exportación."""

import json
from datetime import datetime
from typing import Any

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


class ExportService:
    """Servicio para exportación de datos."""

    def export_to_json(self, data: dict[str, Any]) -> str:
        """Exporta captura a JSON."""
        return json.dumps(data, indent=2, default=str)

    def export_to_pdf(self, capture: dict[str, Any]) -> bytes:
        """Exporta captura a PDF."""
        import io

        buffer = io.BytesIO()
        c = canvas.Canvas(buffer, pagesize=letter)

        c.setFont("Helvetica-Bold", 16)
        c.drawString(100, 750, "RF Sentinel - Capture Report")

        c.setFont("Helvetica", 12)
        y = 700
        for key, value in capture.items():
            c.drawString(100, y, f"{key}: {value}")
            y -= 20

        c.save()
        buffer.seek(0)
        return buffer.getvalue()

    def generate_filename(self, prefix: str, extension: str) -> str:
        """Genera nombre de archivo único."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"{prefix}_{timestamp}.{extension}"
