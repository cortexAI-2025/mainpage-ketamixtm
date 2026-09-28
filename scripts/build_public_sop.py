"""Build the public cooperative documentation guide from the reviewed SOP outline."""
from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, KeepTogether
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "documents" / "KETAMIX-guide-public-cooperatives-v1.pdf"
OUT.parent.mkdir(exist_ok=True)
pdfmetrics.registerFont(TTFont("DejaVu", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"))
pdfmetrics.registerFont(TTFont("DejaVu-Bold", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"))
navy, teal = colors.HexColor("#082F45"), colors.HexColor("#007D7A")
styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name="KTitle", fontName="DejaVu-Bold", fontSize=18, leading=24, textColor=navy, spaceAfter=14))
styles.add(ParagraphStyle(name="KHead", fontName="DejaVu-Bold", fontSize=11, leading=16, textColor=navy, spaceBefore=15, spaceAfter=7, keepWithNext=True))
styles.add(ParagraphStyle(name="KBody", fontName="DejaVu", fontSize=9, leading=14, textColor=colors.HexColor("#284653"), spaceAfter=8))
styles.add(ParagraphStyle(name="KSmall", fontName="DejaVu", fontSize=7.5, leading=11, textColor=colors.HexColor("#526773"), spaceAfter=8))

story = []
def p(text, style="KBody"):
    story.append(Paragraph(text, styles[style]))
def section(title, steps):
    story.append(Paragraph(title, styles["KHead"]))
    for step in steps:
        p("• " + step)

p("KETAMIX | Guide public pour les coopératives", "KTitle")
p("Préparation documentaire d'une biomasse destinée à une filière d'extraction autorisée | Édition publique 1.0 | 28 septembre 2026", "KSmall")
p("Ce guide présente la séquence de travail et les enregistrements à prévoir de la réception à l'expédition. Il est issu de la structure de KTMX-SOP-001 rév. 1.1, sans ses paramètres techniques internes. Il ne constitue ni une procédure approuvée pour un site, ni une certification, ni une autorisation réglementaire.")
p("Champ d'application : coopératives et unités disposant des autorisations pertinentes. Avant usage, le responsable qualité adapte les critères, les méthodes, les équipements, les contrôles et les décisions de libération aux exigences applicables au site, au produit et au marché de destination.")
section("1. Réception et identification du lot", [
    "Vérifier l'origine, les autorisations, la parcelle, la campagne et les documents de transport.",
    "Attribuer un identifiant unique au lot dès sa réception; enregistrer la date, la masse, le fournisseur et l'opérateur.",
    "Consigner l'état visuel et isoler toute matière suspecte avant transformation."
])
section("2. Séparation et stabilisation", [
    "Identifier séparément les fractions graines, matière destinée à l'extraction et matière ligneuse; conserver la filiation avec le lot d'origine.",
    "Effectuer le séchage sous une méthode validée par le site; enregistrer les conditions, contrôles et écarts.",
    "Mesurer l'humidité et l'activité de l'eau selon un plan approuvé, puis documenter la décision de poursuite ou de mise en quarantaine."
])
section("3. Préparation d'un lot homogène", [
    "Contrôler les équipements avant usage et enregistrer nettoyage, étalonnage et identité de l'opérateur.",
    "Définir la granulométrie et les règles d'homogénéisation dans la spécification approuvée du lot.",
    "Conserver la traçabilité de chaque sous-lot et de toute opération de mélange."
])
section("4. Échantillonnage et analyses", [
    "Appliquer un plan d'échantillonnage représentatif, avec chaîne de possession et identification des échantillons.",
    "Faire réaliser les analyses prévues par la spécification approuvée : profil cannabinoïde, contaminants pertinents et paramètres de stabilité.",
    "Rattacher les résultats et le certificat d'analyse au lot; une analyse manquante ou hors spécification bloque la libération."
])
section("5. Écarts et décision qualité", [
    "Placer en quarantaine tout lot non conforme, documenter l'écart et déclencher une investigation.",
    "Toute reprise éventuelle exige une méthode préalablement validée, une évaluation de risque, une autorisation qualité et des contrôles de vérification.",
    "La libération, le rejet ou la destruction sont décidés et signés par la fonction qualité habilitée; aucun traitement n'est automatiquement autorisé par ce guide."
])
section("6. Conditionnement, stockage et transfert", [
    "Utiliser un emballage adapté et identifié avec référence de lot, statut et destination autorisée.",
    "Enregistrer les conditions de stockage, les inspections et tout changement de statut.",
    "Avant transfert, vérifier les autorisations du destinataire et la concordance entre lot, quantité et documents."
])
p("Enregistrements minimaux à prévoir", "KHead")
data = [
    ["Étape", "Preuve à conserver"],
    ["Réception", "Identifiant, origine, parcelle, masse, contrôle initial"],
    ["Préparation", "Fractions, équipements, nettoyage, paramètres suivis, opérateur"],
    ["Qualité", "Plan et résultats d'analyses, COA, écarts, décision signée"],
    ["Sortie", "Étiquette, stock, destinataire, documents de transfert"],
]
table = Table([[Paragraph(x, styles["KSmall"]) for x in row] for row in data], colWidths=[34*mm, 135*mm], repeatRows=1)
table.setStyle(TableStyle([("BACKGROUND", (0,0), (-1,0), colors.HexColor("#EAF4F4")), ("GRID", (0,0), (-1,-1), .4, colors.HexColor("#C9D8DC")), ("VALIGN", (0,0), (-1,-1), "TOP"), ("LEFTPADDING", (0,0), (-1,-1), 8), ("RIGHTPADDING", (0,0), (-1,-1), 8), ("TOPPADDING", (0,0), (-1,-1), 7), ("BOTTOMPADDING", (0,0), (-1,-1), 7)]))
story.append(table)
story.append(Spacer(1, 12))
p("Document public d'orientation. Les seuils analytiques, méthodes de remédiation et critères de libération relèvent des procédures contrôlées de chaque opérateur et du marché concerné. Contact technique : technical@ketamixtm.com", "KSmall")

def footer(canvas, doc):
    canvas.setStrokeColor(teal)
    canvas.line(20*mm, 18*mm, 190*mm, 18*mm)
    canvas.setFont("DejaVu", 7)
    canvas.setFillColor(navy)
    canvas.drawString(20*mm, 13*mm, "KETAMIX | Guide public coopératives | v1.0")
    canvas.drawRightString(190*mm, 13*mm, str(doc.page))

SimpleDocTemplate(str(OUT), pagesize=A4, rightMargin=20*mm, leftMargin=20*mm, topMargin=20*mm, bottomMargin=24*mm, title="KETAMIX Guide public pour les coopératives", author="KETAMIX").build(story, onFirstPage=footer, onLaterPages=footer)
print(OUT)
