"""Natural language query service."""

import re
import json
from typing import Dict, Any, Optional
from sqlalchemy import text
from sqlalchemy.orm import Session

from src.llm.core.client import client
from src.llm.core.prompts import SQL_GENERATOR_SYSTEM, get_nl_query_prompt, get_data_explanation_prompt
from src.utils.logger import get_logger
from src.utils.exceptions import LLMServiceError

logger = get_logger(__name__)


class NLQueryService:
    """Natural language to SQL query service."""

    def __init__(self, db: Session):
        """Initialize with database session."""
        self.db = db
        self.client = client

    def process_query(self, question: str) -> Dict[str, Any]:
        """Process natural language query and return results."""
        try:
            logger.info(f"Processing NL query: {question}")

            # Generate SQL
            sql_query = self._generate_sql(question)

            if not sql_query:
                return {
                    "success": False,
                    "error": "Could not generate SQL query",
                    "question": question,
                }

            # Validate SQL (basic security check)
            if not self._is_safe_query(sql_query):
                return {
                    "success": False,
                    "error": "Query validation failed - only SELECT queries are allowed",
                    "question": question,
                }

            # Execute query
            results = self._execute_query(sql_query)

            if results is None:
                return {
                    "success": False,
                    "error": "Query execution failed",
                    "question": question,
                    "sql": sql_query,
                }

            # Format results
            formatted_results = self._format_results(results)

            # Generate explanation
            explanation = self._generate_explanation(question, formatted_results)

            response = {
                "success": True,
                "question": question,
                "sql": sql_query,
                "results": formatted_results,
                "explanation": explanation,
                "row_count": len(results) if results else 0,
            }

            logger.info(f"NL query processed successfully: {len(results)} rows")
            return response

        except LLMServiceError as e:
            logger.error(f"LLM service error processing NL query: {e}")
            return {
                "success": False,
                "error": f"AI service error: {str(e)}. Please verify your OpenAI API key is valid and has sufficient credits.",
                "question": question,
            }
        except Exception as e:
            logger.error(f"Error processing NL query: {e}")
            return {
                "success": False,
                "error": f"Query processing error: {str(e)}",
                "question": question,
            }

    def _generate_sql(self, question: str) -> Optional[str]:
        """Generate SQL from natural language question."""
        try:
            schema_context = """
Tables:
- vehicles: id, vin, make, model, year, category, trim, msrp
- inventory: id, vehicle_id, warehouse_location, region, quantity_available, status
- sales: id, vehicle_id, sale_date, quantity, unit_price, total_amount, customer_segment, region

Common queries:
- Top selling vehicles: JOIN sales with vehicles, GROUP BY vehicle_id, ORDER BY SUM(quantity)
- Sales by region: GROUP BY region FROM sales
- Inventory status: SELECT from inventory WHERE status='low'
"""

            prompt = get_nl_query_prompt(question, schema_context)
            response = self.client.structured_completion(
                SQL_GENERATOR_SYSTEM, prompt, temperature=0.3
            )

            # Extract SQL from response (handle markdown code blocks)
            sql = self._extract_sql(response)

            logger.debug(f"Generated SQL: {sql}")
            return sql

        except LLMServiceError as e:
            logger.error(f"OpenAI API error in SQL generation: {e}")
            raise LLMServiceError(f"Unable to connect to AI service. Please check your OpenAI API key and account status. Error: {str(e)}")
        except Exception as e:
            logger.error(f"Error generating SQL: {e}")
            raise LLMServiceError(f"Error generating SQL query: {str(e)}")

    def _extract_sql(self, response: str) -> str:
        """Extract SQL query from LLM response."""
        # Remove markdown code blocks
        response = re.sub(r"```sql\n", "", response)
        response = re.sub(r"```\n", "", response)
        response = re.sub(r"```", "", response)

        # Find SELECT statement
        lines = response.split("\n")
        sql_lines = []
        in_query = False

        for line in lines:
            line = line.strip()
            if line.upper().startswith("SELECT"):
                in_query = True
            if in_query:
                sql_lines.append(line)
                if line.endswith(";"):
                    break

        sql = " ".join(sql_lines).strip()
        return sql

    def _is_safe_query(self, sql: str) -> bool:
        """Validate that SQL is safe (read-only)."""
        sql_upper = sql.upper()

        # Must start with SELECT
        if not sql_upper.strip().startswith("SELECT"):
            return False

        # Blacklist dangerous keywords
        dangerous_keywords = [
            "INSERT",
            "UPDATE",
            "DELETE",
            "DROP",
            "CREATE",
            "ALTER",
            "TRUNCATE",
            "EXEC",
            "EXECUTE",
        ]

        for keyword in dangerous_keywords:
            if keyword in sql_upper:
                return False

        return True

    def _execute_query(self, sql: str) -> Optional[list]:
        """Execute SQL query safely."""
        try:
            result = self.db.execute(text(sql))
            rows = result.fetchall()

            # Convert to list of dicts
            if rows:
                columns = result.keys()
                return [dict(zip(columns, row)) for row in rows]
            return []

        except Exception as e:
            logger.error(f"Error executing query: {e}")
            return None

    def _format_results(self, results: list) -> Any:
        """Format query results."""
        if not results:
            return []

        # Convert decimals and dates to strings for JSON serialization
        formatted = []
        for row in results:
            formatted_row = {}
            for key, value in row.items():
                if hasattr(value, "isoformat"):  # datetime/date
                    formatted_row[key] = value.isoformat()
                elif hasattr(value, "__float__"):  # Decimal
                    formatted_row[key] = float(value)
                else:
                    formatted_row[key] = value
            formatted.append(formatted_row)

        return formatted

    def _generate_explanation(self, question: str, results: Any) -> str:
        """Generate natural language explanation of results."""
        try:
            # Limit results for LLM context
            results_preview = results[:10] if len(results) > 10 else results
            results_str = json.dumps(results_preview, indent=2)

            if len(results) > 10:
                results_str += f"\n... and {len(results) - 10} more rows"

            prompt = get_data_explanation_prompt(results_str, question)
            explanation = self.client.structured_completion(
                SQL_GENERATOR_SYSTEM, prompt, temperature=0.7
            )

            return explanation

        except Exception as e:
            logger.error(f"Error generating explanation: {e}")
            return "Results retrieved successfully."

