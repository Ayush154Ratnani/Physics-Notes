from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch

# File name
file_name = "Electrostatics_Class_11_Handwritten_Notes.pdf"

# Create PDF
doc = SimpleDocTemplate(
    file_name,
    pagesize=A4,
    rightMargin=40,
    leftMargin=40,
    topMargin=40,
    bottomMargin=40,
)

styles = getSampleStyleSheet()

# Custom handwritten-like style
hand_style = ParagraphStyle(name="Handwritten", fontSize=12, leading=18, spaceAfter=10)

story = []

content = [
    "<b>ELECTROSTATICS – CLASS 11</b>",
    " ",
    "<b>1. Charge Densities</b>",
    "Linear charge density (λ) is charge per unit length.",
    "λ = dq/dl  (SI unit: C m⁻¹)",
    "Surface charge density (σ) is charge per unit area.",
    "σ = dq/dA  (SI unit: C m⁻²)",
    "Volume charge density (ρ) is charge per unit volume.",
    "ρ = dq/dV  (SI unit: C m⁻³)",
    " ",
    "<b>2. Gauss’s Law</b>",
    "The total electric flux through a closed surface is equal to Q/ε₀.",
    "∮ E · dS = Q / ε₀",
    " ",
    "<b>3. Electric Field Lines</b>",
    "• Originate from positive charge and end on negative charge",
    "• Never intersect each other",
    "• Density shows strength of electric field",
    " ",
    "<b>4. Electric Field Intensity</b>",
    "Electric field intensity is force per unit positive charge.",
    "E = F / q",
    "SI unit: N C⁻¹ or V m⁻¹",
    " ",
    "<b>5. Coulomb’s Law</b>",
    "Force between two point charges is:",
    "F = (1 / 4πε₀) × (q₁q₂ / r²)",
    " ",
    "<b>6. Electric Dipole</b>",
    "An electric dipole consists of two equal and opposite charges.",
    "Dipole moment p = q × 2a",
    "Torque acting on dipole: τ = pE sinθ",
    " ",
    "<b>7. Electric Field on Axial Line of Dipole</b>",
    "E = (1 / 4πε₀) × (2p / r³)",
    " ",
    "<b>8. Coulomb’s Law (Vector Form)</b>",
    "F⃗₁₂ = (1 / 4πε₀) × (q₁q₂ / r²) r̂₁₂",
]

for line in content:
    story.append(Paragraph(line, hand_style))
    story.append(Spacer(1, 0.15 * inch))

doc.build(story)

print("PDF created successfully!")
