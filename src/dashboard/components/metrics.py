"""Metric display components."""

import streamlit as st


def display_metric_card(label: str, value: str, delta: str = None):
    """Display metric card."""
    st.metric(label=label, value=value, delta=delta)


def display_kpi_row(kpis: dict):
    """Display a row of KPIs."""
    cols = st.columns(4)

    with cols[0]:
        st.metric(
            "Total Revenue",
            f"${kpis.get('total_revenue', 0):,.0f}",
            delta=kpis.get('revenue_delta')
        )

    with cols[1]:
        st.metric(
            "Units Sold",
            f"{kpis.get('total_units_sold', 0):,}",
            delta=kpis.get('units_delta')
        )

    with cols[2]:
        st.metric(
            "Avg Transaction",
            f"${kpis.get('avg_transaction_value', 0):,.2f}"
        )

    with cols[3]:
        st.metric(
            "Inventory Value",
            f"${kpis.get('total_inventory_value', 0):,.0f}"
        )

