"""Prompt templates for LLM interactions."""

# System prompts
AUTOMOTIVE_ANALYST_SYSTEM = """You are an expert automotive industry data analyst specializing in sales and inventory analytics for Product teams. Your role is to:
- Analyze automotive sales and inventory data
- Generate actionable insights from data patterns
- Explain trends, anomalies, and correlations
- Provide strategic recommendations
- Communicate findings clearly in business language

Always be specific, data-driven, and actionable in your responses."""

SQL_GENERATOR_SYSTEM = """You are an expert SQL query generator for an automotive analytics database. The database has the following tables:

1. vehicles (id, vin, make, model, year, category, trim, msrp, specifications, created_at)
2. inventory (id, vehicle_id, warehouse_location, region, quantity_available, quantity_reserved, reorder_point, last_restocked, status, created_at, updated_at)
3. sales (id, vehicle_id, sale_date, quantity, unit_price, total_amount, customer_segment, region, salesperson_id, discount_applied, created_at)

Categories include: sedan, suv, truck, sports, offroad, compact
Regions include: West, Midwest, South, Northeast, Southeast
Customer segments: individual, fleet, dealer

Generate safe, read-only SQL queries (SELECT only). Always include appropriate JOINs when needed."""

REPORT_GENERATOR_SYSTEM = """You are an expert at creating professional business reports for automotive analytics. Your reports should:
- Start with an executive summary
- Include key metrics and findings
- Provide visual descriptions where helpful
- Offer actionable recommendations
- Be well-structured with clear sections
- Use business-appropriate language"""

# Prompt templates
def get_insights_generation_prompt(data_summary: str, focus_area: str = "general") -> str:
    """Generate prompt for insights generation."""
    return f"""Analyze the following automotive {focus_area} data and generate 3-5 key insights:

{data_summary}

For each insight, provide a concise bullet point (maximum 20 words) that:
1. Highlights the main finding with specific numbers
2. Focuses on actionable insights
3. Uses storytelling to make it memorable

Format as numbered list (1., 2., 3., etc.) with crisp, impactful statements.
Focus on trends, anomalies, opportunities, and risks."""


def get_nl_query_prompt(question: str, schema_context: str) -> str:
    """Generate prompt for natural language to SQL conversion."""
    return f"""Convert the following natural language question into a SQL query:

Question: {question}

Database Schema:
{schema_context}

Generate a safe, read-only SELECT query that answers the question. If the question cannot be answered with the available data, explain why."""


def get_report_generation_prompt(report_type: str, data: str, period: str) -> str:
    """Generate prompt for report creation."""
    if report_type == "executive":
        return f"""Create an executive summary report for automotive {period} performance:

Data:
{data}

The report should include:
1. Executive Summary (2-3 paragraphs)
2. Key Performance Indicators
3. Top 3 Achievements
4. Top 3 Challenges
5. Strategic Recommendations (3-5 items)

Keep it concise and executive-level."""

    elif report_type == "detailed":
        return f"""Create a detailed performance report for automotive {period}:

Data:
{data}

The report should include:
1. Overview
2. Sales Performance Analysis
3. Inventory Status Analysis
4. Regional Performance Breakdown
5. Product Category Analysis
6. Trends and Patterns
7. Recommendations
8. Conclusion

Provide comprehensive analysis with specific numbers."""

    else:
        return f"""Create a {report_type} report for automotive {period}:

Data:
{data}

Provide a comprehensive analysis appropriate for this report type."""


def get_data_explanation_prompt(data: str, question: str) -> str:
    """Generate prompt for explaining data results."""
    return f"""A user asked: "{question}"

Here is the data result:
{data}

Provide 3-5 concise bullet points (maximum 20 words each) that tell the story of this data. 
Use storytelling techniques: highlight key findings, include specific numbers, and make it memorable.
Focus on the most important insights that answer the user's question."""


def get_anomaly_explanation_prompt(anomaly_data: str) -> str:
    """Generate prompt for explaining anomalies."""
    return f"""The following anomalies were detected in automotive sales data:

{anomaly_data}

Analyze these anomalies and provide:
1. Possible explanations for each anomaly
2. Whether it's concerning or expected
3. Recommended actions if any"""


def get_trend_analysis_prompt(trend_data: str) -> str:
    """Generate prompt for trend analysis."""
    return f"""Analyze the following sales trend data:

{trend_data}

Provide:
1. Key trend observations
2. Growth patterns (positive/negative)
3. Inflection points or significant changes
4. Forecast implications
5. Strategic recommendations"""

