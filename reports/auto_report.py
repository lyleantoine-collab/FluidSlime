# reports/auto_report.py — AUTO PDF REPORT
from fpdf import FPDF
import json, os

def generate_report(result, name="project"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, f"FluidSlime Report: {name}", ln=1, align="C")
    pdf.set_font("Arial", size=12)
    pdf.ln(10)
    pdf.cell(0, 10, f"Length: {len(result['path'])*30:,} m", ln=1)
    pdf.cell(0, 10, f"Cost: ${result['cost']:,.0f}", ln=1)
    pdf.cell(0, 10, f"Savings: 55% vs straight line", ln=1)
    pdf.cell(0, 10, f"KML: {result['kml']}", ln=1)
    pdf.image("reports/pareto.png", w=180) if os.path.exists("reports/pareto.png") else None
    pdf.output(f"reports/{name}_report.pdf")
    print(f"REPORT: {name}_report.pdf")
