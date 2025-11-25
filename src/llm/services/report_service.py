"""Report generation service."""

import json
from typing import Dict, Any, Optional
from datetime import date, datetime, timedelta
from sqlalchemy.orm import Session

from src.llm.core.client import client
from src.llm.core.prompts import REPORT_GENERATOR_SYSTEM, get_report_generation_prompt
from src.analytics.sales_analytics import SalesAnalytics
from src.analytics.inventory_analytics import InventoryAnalytics
from src.analytics.kpi_calculator import KPICalculator
from src.utils.logger import get_logger
from src.utils.exceptions import LLMServiceError

logger = get_logger(__name__)


class ReportService:
    """Generate automated reports using LLM."""

    def __init__(self, db: Session):
        """Initialize with database session."""
        self.db = db
        self.client = client
        self.sales_analytics = SalesAnalytics(db)
        self.inventory_analytics = InventoryAnalytics(db)
        self.kpi_calculator = KPICalculator(db)

    def generate_executive_report(
        self, start_date: Optional[date] = None, end_date: Optional[date] = None
    ) -> Dict[str, Any]:
        """Generate executive summary report."""
        try:
            logger.info("Generating executive report...")

            # Gather high-level data
            kpis = self.kpi_calculator.calculate_all_kpis(start_date, end_date)
            top_vehicles = self.sales_analytics.get_top_selling_vehicles(5, start_date, end_date)
            regional = self.sales_analytics.get_regional_performance(start_date, end_date)

            # Format data
            data_summary = f"""
Key Performance Indicators:
- Total Revenue: ${kpis['total_revenue']:,.2f}
- Total Units Sold: {kpis['total_units_sold']:,}
- Average Transaction Value: ${kpis['avg_transaction_value']:,.2f}
- Inventory Value: ${kpis['total_inventory_value']:,.2f}
- Inventory Turnover Rate: {kpis['inventory_turnover_rate']:.2f}

Top 5 Selling Vehicles:
{json.dumps(top_vehicles, indent=2)}

Regional Performance:
{json.dumps(regional[:3], indent=2)}

Period: {kpis['period_start']} to {kpis['period_end']} ({kpis['period_days']} days)
"""

            period = f"{kpis['period_start']} to {kpis['period_end']}"
            prompt = get_report_generation_prompt("executive", data_summary, period)

            report_content = self.client.structured_completion(
                REPORT_GENERATOR_SYSTEM, prompt, temperature=0.5
            )

            report = {
                "report_type": "executive",
                "report_title": f"Executive Summary - {period}",
                "generated_at": datetime.now().isoformat(),
                "period_start": str(start_date) if start_date else None,
                "period_end": str(end_date) if end_date else None,
                "content": report_content,
                "kpis": kpis,
            }

            logger.info("Executive report generated successfully")
            return report

        except LLMServiceError as e:
            logger.error(f"OpenAI API error in report generation: {e}")
            raise LLMServiceError(f"Unable to generate report. Please check your OpenAI API key and account status. Error: {str(e)}")
        except Exception as e:
            logger.error(f"Error generating executive report: {e}")
            raise Exception(f"Error generating executive report: {str(e)}")

    def generate_detailed_report(
        self, start_date: Optional[date] = None, end_date: Optional[date] = None
    ) -> Dict[str, Any]:
        """Generate detailed performance report."""
        try:
            logger.info("Generating detailed report...")

            # Gather comprehensive data
            kpis = self.kpi_calculator.calculate_all_kpis(start_date, end_date)
            sales_summary = self.sales_analytics.get_sales_summary(start_date, end_date)
            inventory_summary = self.inventory_analytics.get_inventory_summary()
            regional = self.sales_analytics.get_regional_performance(start_date, end_date)
            categories = self.sales_analytics.get_category_breakdown(start_date, end_date)
            segments = self.sales_analytics.get_customer_segment_analysis(start_date, end_date)
            top_vehicles = self.sales_analytics.get_top_selling_vehicles(10, start_date, end_date)

            data_summary = f"""
Complete Performance Data:

Sales Performance:
{json.dumps(sales_summary, indent=2)}

Inventory Status:
{json.dumps(inventory_summary, indent=2)}

Regional Performance:
{json.dumps(regional, indent=2)}

Category Breakdown:
{json.dumps(categories, indent=2)}

Customer Segment Analysis:
{json.dumps(segments, indent=2)}

Top 10 Vehicles:
{json.dumps(top_vehicles, indent=2)}

Key Performance Indicators:
{json.dumps(kpis, indent=2)}
"""

            period = f"{kpis['period_start']} to {kpis['period_end']}"
            prompt = get_report_generation_prompt("detailed", data_summary, period)

            report_content = self.client.structured_completion(
                REPORT_GENERATOR_SYSTEM, prompt, model=self.client.primary_model, temperature=0.5
            )

            report = {
                "report_type": "detailed",
                "report_title": f"Detailed Performance Report - {period}",
                "generated_at": datetime.now().isoformat(),
                "period_start": str(start_date) if start_date else None,
                "period_end": str(end_date) if end_date else None,
                "content": report_content,
                "data": {
                    "kpis": kpis,
                    "sales": sales_summary,
                    "inventory": inventory_summary,
                },
            }

            logger.info("Detailed report generated successfully")
            return report

        except LLMServiceError as e:
            logger.error(f"OpenAI API error in detailed report: {e}")
            raise LLMServiceError(f"Unable to generate report. Please check your OpenAI API key and account status. Error: {str(e)}")
        except Exception as e:
            logger.error(f"Error generating detailed report: {e}")
            raise Exception(f"Error generating detailed report: {str(e)}")

    def generate_product_report(
        self, vehicle_id: int, start_date: Optional[date] = None, end_date: Optional[date] = None
    ) -> Dict[str, Any]:
        """Generate product-specific report."""
        try:
            logger.info(f"Generating product report for vehicle {vehicle_id}...")

            from src.database.repositories.vehicle_repo import VehicleRepository
            from src.database.repositories.sales_repo import SalesRepository

            vehicle_repo = VehicleRepository(self.db)
            sales_repo = SalesRepository(self.db)

            # Get vehicle info
            vehicle = vehicle_repo.get_by_id(vehicle_id)
            if not vehicle:
                raise ValueError(f"Vehicle {vehicle_id} not found")

            # Get sales data
            sales = sales_repo.get_by_vehicle_id(vehicle_id)

            # Filter by date range if provided
            if start_date or end_date:
                sales = [
                    s
                    for s in sales
                    if (not start_date or s.sale_date >= start_date)
                    and (not end_date or s.sale_date <= end_date)
                ]

            total_units = sum(s.quantity for s in sales)
            total_revenue = sum(float(s.total_amount) for s in sales)

            data_summary = f"""
Product Information:
- Make: {vehicle.make}
- Model: {vehicle.model}
- Year: {vehicle.year}
- Category: {vehicle.category}
- MSRP: ${float(vehicle.msrp):,.2f}

Sales Performance:
- Total Units Sold: {total_units}
- Total Revenue: ${total_revenue:,.2f}
- Number of Transactions: {len(sales)}
- Average Sale Price: ${total_revenue / total_units if total_units > 0 else 0:,.2f}
"""

            period = f"{start_date} to {end_date}" if start_date and end_date else "all time"
            prompt = f"""Create a product performance report for {vehicle.make} {vehicle.model}:

{data_summary}

Analyze the product's performance, market position, and provide recommendations."""

            report_content = self.client.structured_completion(
                REPORT_GENERATOR_SYSTEM, prompt, temperature=0.5
            )

            report = {
                "report_type": "product",
                "report_title": f"Product Report - {vehicle.make} {vehicle.model}",
                "generated_at": datetime.now().isoformat(),
                "vehicle_id": vehicle_id,
                "content": report_content,
            }

            logger.info(f"Product report generated for vehicle {vehicle_id}")
            return report

        except Exception as e:
            logger.error(f"Error generating product report: {e}")
            raise

    def export_report_markdown(self, report: Dict[str, Any]) -> str:
        """Export report as markdown."""
        try:
            md = f"# {report['report_title']}\n\n"
            md += f"**Generated:** {report['generated_at']}\n\n"
            if report.get("period_start"):
                md += f"**Period:** {report['period_start']} to {report['period_end']}\n\n"
            md += "---\n\n"
            md += report['content']
            return md

        except Exception as e:
            logger.error(f"Error exporting report to markdown: {e}")
            raise

    def export_report_html(self, report: Dict[str, Any]) -> str:
        """Export report as HTML."""
        try:
            # Convert markdown-like content to HTML (simple approach)
            content = report['content'].replace("\n\n", "</p><p>").replace("\n", "<br>")

            html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>{report['report_title']}</title>
    <style>
        body {{ font-family: Arial, sans-serif; max-width: 1000px; margin: 40px auto; padding: 20px; }}
        h1 {{ color: #333; }}
        .meta {{ color: #666; font-size: 14px; }}
        p {{ line-height: 1.6; }}
    </style>
</head>
<body>
    <h1>{report['report_title']}</h1>
    <div class="meta">
        <p>Generated: {report['generated_at']}</p>
        {f"<p>Period: {report.get('period_start')} to {report.get('period_end')}</p>" if report.get('period_start') else ''}
    </div>
    <hr>
    <p>{content}</p>
</body>
</html>
"""
            return html

        except Exception as e:
            logger.error(f"Error exporting report to HTML: {e}")
            raise

