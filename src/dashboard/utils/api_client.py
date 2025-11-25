"""API client for dashboard."""

import requests
from typing import Optional, Dict, Any
from datetime import date


class APIClient:
    """Client for communicating with FastAPI backend."""

    def __init__(self, base_url: str = None):
        """Initialize API client."""
        # Use hardcoded default or passed URL to avoid config import issues
        self.base_url = base_url or "http://localhost:8000"

    def _make_request(self, method: str, endpoint: str, **kwargs) -> Optional[Dict]:
        """Make HTTP request."""
        url = f"{self.base_url}{endpoint}"
        try:
            response = requests.request(method, url, **kwargs)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error making request to {url}: {e}")
            return None

    # Analytics endpoints
    def get_sales_summary(self, start_date: Optional[date] = None, end_date: Optional[date] = None):
        """Get sales summary."""
        params = {}
        if start_date:
            params["start_date"] = str(start_date)
        if end_date:
            params["end_date"] = str(end_date)
        return self._make_request("GET", "/api/v1/analytics/sales/summary", params=params)

    def get_sales_trends(self, start_date: Optional[date] = None, end_date: Optional[date] = None, period: str = "D"):
        """Get sales trends."""
        params = {"period": period}
        if start_date:
            params["start_date"] = str(start_date)
        if end_date:
            params["end_date"] = str(end_date)
        result = self._make_request("GET", "/api/v1/analytics/sales/trends", params=params)
        # Handle API response that may be wrapped in {"value": [...]} format
        if result and isinstance(result, dict) and "value" in result:
            return result["value"]
        return result

    def get_top_vehicles(self, n: int = 10, start_date: Optional[date] = None, end_date: Optional[date] = None):
        """Get top selling vehicles."""
        params = {"n": n}
        if start_date:
            params["start_date"] = str(start_date)
        if end_date:
            params["end_date"] = str(end_date)
        result = self._make_request("GET", "/api/v1/analytics/sales/top-vehicles", params=params)
        # Handle API response that may be wrapped in {"value": [...]} format
        if result and isinstance(result, dict) and "value" in result:
            return result["value"]
        return result

    def get_regional_performance(self, start_date: Optional[date] = None, end_date: Optional[date] = None):
        """Get regional performance."""
        params = {}
        if start_date:
            params["start_date"] = str(start_date)
        if end_date:
            params["end_date"] = str(end_date)
        result = self._make_request("GET", "/api/v1/analytics/sales/regional", params=params)
        # Handle API response that may be wrapped in {"value": [...]} format
        if result and isinstance(result, dict) and "value" in result:
            return result["value"]
        return result

    def get_category_breakdown(self, start_date: Optional[date] = None, end_date: Optional[date] = None):
        """Get category breakdown."""
        params = {}
        if start_date:
            params["start_date"] = str(start_date)
        if end_date:
            params["end_date"] = str(end_date)
        result = self._make_request("GET", "/api/v1/analytics/sales/categories", params=params)
        # Handle API response that may be wrapped in {"value": [...]} format
        if result and isinstance(result, dict) and "value" in result:
            return result["value"]
        return result

    def get_customer_segments(self, start_date: Optional[date] = None, end_date: Optional[date] = None):
        """Get customer segment analysis."""
        params = {}
        if start_date:
            params["start_date"] = str(start_date)
        if end_date:
            params["end_date"] = str(end_date)
        result = self._make_request("GET", "/api/v1/analytics/sales/segments", params=params)
        # Handle API response that may be wrapped in {"value": [...]} format
        if result and isinstance(result, dict) and "value" in result:
            return result["value"]
        return result

    def get_kpis(self, start_date: Optional[date] = None, end_date: Optional[date] = None):
        """Get KPIs."""
        params = {}
        if start_date:
            params["start_date"] = str(start_date)
        if end_date:
            params["end_date"] = str(end_date)
        return self._make_request("GET", "/api/v1/analytics/kpis", params=params)

    def get_inventory_summary(self):
        """Get inventory summary."""
        return self._make_request("GET", "/api/v1/analytics/inventory/summary")

    def get_inventory_status(self):
        """Get inventory status."""
        return self._make_request("GET", "/api/v1/analytics/inventory/status")

    def get_inventory_by_status(self):
        """Get inventory breakdown by status (for charts)."""
        result = self._make_request("GET", "/api/v1/analytics/inventory/by-status")
        # Handle API response that may be wrapped in {"value": [...]} format
        if result and isinstance(result, dict) and "value" in result:
            return result["value"]
        return result

    def get_low_stock(self):
        """Get low stock alerts."""
        result = self._make_request("GET", "/api/v1/analytics/inventory/low-stock")
        # Handle API response that may be wrapped in {"value": [...]} format
        if result and isinstance(result, dict) and "value" in result:
            return result["value"]
        return result

    # Insights endpoints
    def generate_insights(self, focus_area: str = "sales", start_date: Optional[date] = None, end_date: Optional[date] = None):
        """Generate insights."""
        data = {"focus_area": focus_area}
        if start_date:
            data["start_date"] = str(start_date)
        if end_date:
            data["end_date"] = str(end_date)
        return self._make_request("POST", "/api/v1/insights/generate", json=data)

    def get_insight_history(self, limit: int = 50):
        """Get insight history."""
        result = self._make_request("GET", "/api/v1/insights/history", params={"limit": limit})
        # Handle API response that may be wrapped in {"value": [...]} format
        if result and isinstance(result, dict) and "value" in result:
            return result["value"]
        return result

    # Query endpoints
    def nl_query(self, question: str):
        """Natural language query."""
        return self._make_request("POST", "/api/v1/query", json={"question": question})

    def rag_query(self, question: str, context_limit: int = 3):
        """RAG query."""
        return self._make_request("POST", "/api/v1/query/rag", json={"question": question, "context_limit": context_limit})

    # Reports endpoints
    def generate_report(self, report_type: str, start_date: Optional[date] = None, end_date: Optional[date] = None):
        """Generate report."""
        data = {"report_type": report_type}
        if start_date:
            data["start_date"] = str(start_date)
        if end_date:
            data["end_date"] = str(end_date)
        return self._make_request("POST", "/api/v1/reports/generate", json=data)

