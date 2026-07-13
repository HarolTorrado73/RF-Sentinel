import subprocess
import json
from datetime import datetime, timezone
from typing import Any

import nmap
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.scan import Scan
from app.models.target import Target
from app.schemas.scan import ScanCreate


class ScanService:
    @staticmethod
    async def get(db: AsyncSession, scan_id: int) -> Scan | None:
        result = await db.execute(select(Scan).where(Scan.id == scan_id))
        return result.scalar_one_or_none()

    @staticmethod
    async def get_multi(db: AsyncSession) -> list[Scan]:
        result = await db.execute(select(Scan))
        return result.scalars().all()

    @staticmethod
    async def create(db: AsyncSession, scan_in: ScanCreate, user_id: int) -> Scan:
        scan = Scan(
            target_id=scan_in.target_id,
            scan_type=scan_in.scan_type,
            created_by_id=user_id,
            status="pending",
        )
        db.add(scan)
        await db.commit()
        await db.refresh(scan)
        return scan

    @staticmethod
    async def execute(db: AsyncSession, scan_id: int) -> Scan:
        scan = await ScanService.get(db, scan_id)
        if not scan:
            raise ValueError("Scan not found")
        
        scan.status = "running"
        await db.commit()
        
        nm = nmap.PortScanner()
        target = await db.execute(select(Target).where(Target.id == scan.target_id))
        target_obj = target.scalar_one_or_none()
        
        if not target_obj:
            scan.status = "failed"
            scan.error_message = "Target not found"
            await db.commit()
            return scan
        
        try:
            scan_args = ScanService._get_scan_args(scan.scan_type)
            nm.scan(hosts=target_obj.value, arguments=scan_args)
            
            scan.results = ScanService._parse_nmap_results(nm, target_obj.value)
            scan.status = "completed"
            scan.completed_at = datetime.now(timezone.utc)
        except Exception as e:
            scan.status = "failed"
            scan.error_message = str(e)
        
        db.add(scan)
        await db.commit()
        await db.refresh(scan)
        return scan

    @staticmethod
    def _get_scan_args(scan_type: str) -> str:
        scan_args = {
            "ping": "-sn",
            "tcp": "-sT -p- --open",
            "udp": "-sU --top-ports 1000",
            "service": "-sV -sC",
            "os": "-O",
        }
        return scan_args.get(scan_type, "-sn")

    @staticmethod
    def _parse_nmap_results(nm: nmap.PortScanner, target: str) -> dict[str, Any]:
        results: dict[str, Any] = {"hosts": []}
        
        for host in nm.all_hosts():
            host_data = {
                "ip": host,
                "status": nm[host].state(),
                "ports": [],
                "services": [],
            }
            
            for proto in nm[host].all_protocols():
                ports = nm[host][proto].keys()
                for port in ports:
                    port_info = nm[host][proto][port]
                    host_data["ports"].append({
                        "port": port,
                        "protocol": proto,
                        "state": port_info.get("state", ""),
                    })
                    if "name" in port_info:
                        host_data["services"].append({
                            "port": port,
                            "name": port_info["name"],
                            "product": port_info.get("product", ""),
                            "version": port_info.get("version", ""),
                        })
            
            results["hosts"].append(host_data)
        
        return results

    @staticmethod
    async def delete(db: AsyncSession, scan_id: int) -> None:
        scan = await ScanService.get(db, scan_id)
        if scan:
            await db.delete(scan)
            await db.commit()