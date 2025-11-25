"""Insights generation service."""

import json
from typing import Dict, Any, List, Optional
from datetime import date, datetime
from sqlalchemy.orm import Session

from src.llm.core.client import client
from src.llm.core.prompts import (
    AUTOMOTIVE_ANALYST_SYSTEM,
    get_insights_generation_prompt,
    get_anomaly_explanation_prompt,
    get_trend_analysis_prompt,
)
from src.analytics.sales_analytics import SalesAnalytics
from src.analytics.inventory_analytics import InventoryAnalytics
from src.analytics.trend_analyzer import TrendAnalyzer
from src.database.models import InsightHistory
from src.utils.logger import get_logger
from src.utils.exceptions import LLMServiceError

logger = get_logger(__name__)


class InsightsService:
    """Generate AI-powered insights from analytics data."""

    def __init__(self, db: Session):
        """Initialize with database session."""
        self.db = db
        self.client = client
        self.sales_analytics = SalesAnalytics(db)
        self.inventory_analytics = InventoryAnalytics(db)
        self.trend_analyzer = TrendAnalyzer(db)

    def generate_sales_insights(
        self, start_date: Optional[date] = None, end_date: Optional[date] = None
    ) -> List[Dict[str, Any]]:
        """Generate insights for sales data."""
        try:
            logger.info("Generating sales insights...")

            # Gather sales data
            summary = self.sales_analytics.get_sales_summary(start_date, end_date)
            regional = self.sales_analytics.get_regional_performance(start_date, end_date)
            top_vehicles = self.sales_analytics.get_top_selling_vehicles(5, start_date, end_date)
            categories = self.sales_analytics.get_category_breakdown(start_date, end_date)

            # Format data for LLM
            data_summary = f"""
Sales Summary:
- Total Revenue: ${summary['total_revenue']:,.2f}
- Total Units Sold: {summary['total_units']:,}
- Total Transactions: {summary['total_transactions']:,}
- Average Transaction Value: ${summary['avg_transaction_value']:,.2f}
- Average Discount: {summary['avg_discount']:.2f}%

Regional Performance:
{json.dumps(regional[:5], indent=2)}

Top Selling Vehicles:
{json.dumps(top_vehicles, indent=2)}

Category Breakdown:
{json.dumps(categories, indent=2)}
"""

            # Generate insights using LLM
            prompt = get_insights_generation_prompt(data_summary, "sales")
            response = self.client.structured_completion(
                AUTOMOTIVE_ANALYST_SYSTEM, prompt, temperature=0.7
            )

            # Parse response into structured insights
            insights = self._parse_insights_response(response, "sales")

            # Store insights in database
            for insight in insights:
                self._store_insight(insight["text"], "sales_trend", insight.get("metadata", {}))

            logger.info(f"Generated {len(insights)} sales insights")
            return insights

        except LLMServiceError as e:
            logger.error(f"OpenAI API error in insights generation: {e}")
            raise LLMServiceError(f"Unable to generate insights. Please check your OpenAI API key and account status. Error: {str(e)}")
        except Exception as e:
            logger.error(f"Error generating sales insights: {e}")
            raise Exception(f"Error generating sales insights: {str(e)}")

    def generate_inventory_insights(self) -> List[Dict[str, Any]]:
        """Generate insights for inventory data."""
        try:
            logger.info("Generating inventory insights...")

            # Gather inventory data
            summary = self.inventory_analytics.get_inventory_summary()
            by_region = self.inventory_analytics.get_inventory_by_region()
            by_category = self.inventory_analytics.get_inventory_by_category()
            low_stock = self.inventory_analytics.get_low_stock_alerts()

            data_summary = f"""
Inventory Summary:
- Total Units: {summary['total_units']:,}
- Total Value: ${summary['total_value']:,.2f}
- Unique Vehicles: {summary['unique_vehicles']}
- Low Stock Items: {summary['low_stock_count']}
- Out of Stock Items: {summary['out_of_stock_count']}

Regional Distribution:
{json.dumps(by_region, indent=2)}

Category Distribution:
{json.dumps(by_category, indent=2)}

Low Stock Alerts: {summary['low_stock_count']} items
"""

            prompt = get_insights_generation_prompt(data_summary, "inventory")
            response = self.client.structured_completion(
                AUTOMOTIVE_ANALYST_SYSTEM, prompt, temperature=0.7
            )

            insights = self._parse_insights_response(response, "inventory")

            # Store insights
            for insight in insights:
                self._store_insight(insight["text"], "inventory_status", insight.get("metadata", {}))

            logger.info(f"Generated {len(insights)} inventory insights")
            return insights

        except LLMServiceError as e:
            logger.error(f"OpenAI API error in inventory insights: {e}")
            raise LLMServiceError(f"Unable to generate insights. Please check your OpenAI API key and account status. Error: {str(e)}")
        except Exception as e:
            logger.error(f"Error generating inventory insights: {e}")
            raise Exception(f"Error generating inventory insights: {str(e)}")

    def analyze_anomalies(
        self, start_date: Optional[date] = None, end_date: Optional[date] = None
    ) -> Dict[str, Any]:
        """Analyze and explain anomalies."""
        try:
            logger.info("Analyzing anomalies...")

            anomalies = self.trend_analyzer.detect_sales_anomalies(start_date, end_date)

            if not anomalies:
                return {"anomalies": [], "explanation": "No significant anomalies detected."}

            anomaly_summary = json.dumps(anomalies, indent=2)
            prompt = get_anomaly_explanation_prompt(anomaly_summary)
            explanation = self.client.structured_completion(
                AUTOMOTIVE_ANALYST_SYSTEM, prompt, temperature=0.7
            )

            result = {"anomalies": anomalies, "explanation": explanation}

            # Store as insight
            self._store_insight(explanation, "anomaly", {"anomaly_count": len(anomalies)})

            logger.info(f"Analyzed {len(anomalies)} anomalies")
            return result

        except Exception as e:
            logger.error(f"Error analyzing anomalies: {e}")
            raise

    def analyze_trends(
        self, start_date: Optional[date] = None, end_date: Optional[date] = None
    ) -> Dict[str, Any]:
        """Analyze sales trends."""
        try:
            logger.info("Analyzing trends...")

            trends = self.sales_analytics.get_sales_trends(start_date, end_date, period="W")  # Weekly
            moving_avg = self.trend_analyzer.calculate_moving_average(start_date, end_date, window=7)

            trend_summary = f"""
Weekly Sales Trends:
{json.dumps(trends[:10], indent=2)}

7-Day Moving Average:
{json.dumps(moving_avg[-10:], indent=2)}
"""

            prompt = get_trend_analysis_prompt(trend_summary)
            analysis = self.client.structured_completion(
                AUTOMOTIVE_ANALYST_SYSTEM, prompt, temperature=0.7
            )

            result = {"trends": trends, "moving_average": moving_avg, "analysis": analysis}

            # Store as insight
            self._store_insight(analysis, "trend_analysis", {})

            logger.info("Trend analysis completed")
            return result

        except Exception as e:
            logger.error(f"Error analyzing trends: {e}")
            raise

    def _parse_insights_response(self, response: str, insight_type: str) -> List[Dict[str, Any]]:
        """Parse LLM response into structured insights."""
        # Simple parsing - in production, could use more sophisticated extraction
        insights = []
        lines = response.split("\n")

        current_insight = None
        for line in lines:
            line = line.strip()
            if not line:
                continue

            # Look for numbered items (1., 2., etc.)
            if len(line) > 2 and line[0].isdigit() and line[1] in (".", ")"):
                if current_insight:
                    insights.append(current_insight)
                current_insight = {"text": line[2:].strip(), "type": insight_type, "metadata": {}}
            elif current_insight:
                current_insight["text"] += " " + line

        if current_insight:
            insights.append(current_insight)

        # If parsing didn't work, treat whole response as single insight
        if not insights:
            insights = [{"text": response, "type": insight_type, "metadata": {}}]

        return insights

    def _store_insight(self, insight_text: str, insight_type: str, metadata: Dict[str, Any]):
        """Store insight in database."""
        try:
            insight = InsightHistory(
                insight_text=insight_text, insight_type=insight_type, insight_metadata=metadata
            )
            self.db.add(insight)
            self.db.commit()
            logger.debug(f"Stored insight of type {insight_type}")
        except Exception as e:
            logger.error(f"Error storing insight: {e}")
            self.db.rollback()

