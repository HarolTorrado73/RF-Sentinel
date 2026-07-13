import os
from datetime import datetime, timezone
from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
import json
import csv

from app.models.report import Report
from app.models.scan import Scan
from app.schemas.report import ReportCreate


class ReportService:
    REPORTS_DIR = "/tmp/reports"

    @staticmethod
    async def get(db: AsyncSession, report_id: int) -> Report | None:
        result = await db.execute(select(Report).where(Report.id == report_id))
        return result.scalar_one_or_none()

    @staticmethod
    async def get_multi(db: AsyncSession) -> list[Report]:
        result = await db.execute(select(Report))
        return result.scalars().all()

    @staticmethod
    async def create(
        db: AsyncSession, report_in: ReportCreate, user_id: int
    ) -> Report:
        report = Report(
            scan_id=report_in.scan_id,
            title=report_in.title,
            report_type=report_in.report_type,
            created_by_id=user_id,
        )
        db.add(report)
        await db.commit()
        await db.refresh(report)
        return report

    @staticmethod
    async def generate_report(db: AsyncSession, report: Report) -> dict[str, Any]:
        if not os.path.exists(ReportService.REPORTS_DIR):
            os.makedirs(ReportService.REPORTS_DIR)

        scan_result = await db.execute(
            select(Scan).where(Scan.id == report.scan_id)
        )
        scan = scan_result.scalar_one_or_none()

        if report.report_type == "pdf":
            return await ReportService._generate_pdf(report, scan)
        elif report.report_type == "csv":
            return await ReportService._generate_csv(report, scan)
        else:
            return await ReportService._generate_json(report, scan)

    @staticmethod
    async def _generate_pdf(report: Report, scan: Scan | None) -> dict[str, Any]:
        filename = f"report_{report.id}_{int(datetime.now().timestamp())}.pdf"
        filepath = os.path.join(ReportService.REPORTS_DIR, filename)
        
        doc = SimpleDocTemplate(filepath, pagesize=letter)
        styles = getSampleStyleSheet()
        elements = []

        elements.append(Paragraph(f"Report: {report.title}", styles["Title"]))
        elements.append(Spacer(1, 12))
        
        if scan and scan.results:
            hosts = scan.results.get("hosts", [])
            elements.append(Paragraph(f"Hosts Discovered: {len(hosts)}", styles["Heading2"]))
            
            for host in hosts:
                elements.append(Paragraph(f"Host: {host['ip']}", styles["Heading3"]))
                elements.append(Paragraph(f"Status: {host['status']}", styles["Normal"]))
        
        doc.build(elements)
        return {"file_path": filepath, "type": "pdf"}

    @staticmethod
    async def _generate_csv(report: Report, scan: Scan | None) -> dict[str, Any]:
        filename = f"report_{report.id}_{int(datetime.now().timestamp())}.csv"
        filepath = os.path.join(ReportService.REPORTS_DIR, filename)
        
        with open(filepath, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Target", "Protocol", "Port", "State", "Service"])
            
            if scan and scan.results:
                for host in scan.results.get("hosts", []):
                    for port in host.get("ports", []):
                        writer.writerow([
                            host["ip"],
                            port["protocol"],
                            port["port"],
                            port["state"],
                            "",
                        ])
        
        return {"file_path": filepath, "type": "csv"}

    @staticmethod
    async def _generate_json(report: Report, scan: Scan | None) -> dict[str, Any]:
        filename = f"report_{report.id}_{int(datetime.now().timestamp())}.json"
        filepath = os.path.join(ReportService.REPORTS_DIR, filename)
        
        with open(filepath, "w") as f:
            json.dump({
                "title": report.title,
                "scan_id": report.scan_id,
                "results": scan.results if scan else None,
                "generated_at": datetime.now(timezone.utc).isoformat(),
            }, f, indent=2)
        
        return {"file_path": filepath, "type": "json"}

    @staticmethod
    async def delete(db: AsyncSession, report_id: int) -> None:
        report = await ReportService.get(db, report_id)
        if report and report.file_path and os.path.exists(report.file_path):
            os.remove(report.file_path)
        if report:
            await db.delete(report)
            await db.commit()