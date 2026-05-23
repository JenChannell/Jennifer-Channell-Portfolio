from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(__file__).resolve().parent
OUT = ROOT / "assets" / "Jennifer-Channell-Resume.pdf"


def draw_header_footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(colors.HexColor("#d9d5ca"))
    canvas.setLineWidth(0.5)
    canvas.line(0.6 * inch, 0.55 * inch, 7.9 * inch, 0.55 * inch)
    canvas.setFillColor(colors.HexColor("#686b63"))
    canvas.setFont("Helvetica", 8)
    canvas.drawRightString(7.9 * inch, 0.38 * inch, f"Jennifer Channell | Page {doc.page}")
    canvas.restoreState()


def paragraph(text, style):
    return Paragraph(text, style)


def bullets(items, style):
    story = []
    for item in items:
        story.append(Paragraph(f"&bull; {item}", style))
    return story


def job(title, org, date, items, styles):
    story = [
        Spacer(1, 4),
        Paragraph(f"<b>{title}</b>", styles["JobTitle"]),
        Paragraph(f"{org} | {date}", styles["Meta"]),
    ]
    story.extend(bullets(items, styles["Bullet"]))
    return story


def section(title, styles):
    return [
        Spacer(1, 9),
        Paragraph(title, styles["Section"]),
        Spacer(1, 4),
    ]


def main():
    OUT.parent.mkdir(exist_ok=True)

    base = getSampleStyleSheet()
    styles = {
        "Name": ParagraphStyle(
            "Name",
            parent=base["Normal"],
            fontName="Helvetica-Bold",
            fontSize=22,
            leading=25,
            alignment=TA_CENTER,
            textColor=colors.HexColor("#252724"),
            spaceAfter=4,
        ),
        "Contact": ParagraphStyle(
            "Contact",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=9,
            leading=12,
            alignment=TA_CENTER,
            textColor=colors.HexColor("#4f5653"),
            spaceAfter=8,
        ),
        "Headline": ParagraphStyle(
            "Headline",
            parent=base["Normal"],
            fontName="Helvetica-Bold",
            fontSize=11,
            leading=14,
            alignment=TA_CENTER,
            textColor=colors.HexColor("#4f604f"),
            spaceAfter=10,
        ),
        "Section": ParagraphStyle(
            "Section",
            parent=base["Normal"],
            fontName="Helvetica-Bold",
            fontSize=10,
            leading=12,
            textColor=colors.HexColor("#4f604f"),
            uppercase=True,
            spaceBefore=4,
        ),
        "Body": ParagraphStyle(
            "Body",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=9,
            leading=12,
            textColor=colors.HexColor("#252724"),
        ),
        "Bullet": ParagraphStyle(
            "Bullet",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=8.7,
            leading=11,
            leftIndent=9,
            firstLineIndent=-7,
            textColor=colors.HexColor("#252724"),
        ),
        "JobTitle": ParagraphStyle(
            "JobTitle",
            parent=base["Normal"],
            fontName="Helvetica-Bold",
            fontSize=9.4,
            leading=12,
            textColor=colors.HexColor("#252724"),
        ),
        "Meta": ParagraphStyle(
            "Meta",
            parent=base["Normal"],
            fontName="Helvetica-Oblique",
            fontSize=8.4,
            leading=11,
            textColor=colors.HexColor("#686b63"),
            spaceAfter=2,
        ),
        "Small": ParagraphStyle(
            "Small",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=8.5,
            leading=11,
            textColor=colors.HexColor("#252724"),
        ),
    }

    doc = BaseDocTemplate(
        str(OUT),
        pagesize=letter,
        rightMargin=0.6 * inch,
        leftMargin=0.6 * inch,
        topMargin=0.55 * inch,
        bottomMargin=0.7 * inch,
    )
    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="normal")
    doc.addPageTemplates([PageTemplate(id="resume", frames=[frame], onPage=draw_header_footer)])

    story = [
        paragraph("Jennifer Channell", styles["Name"]),
        paragraph(
            "Sacramento, CA 95822 | +1 916 728 0478 | jenchannell@yahoo.com | "
            "linkedin.com/in/jennifer-channell-16782a132",
            styles["Contact"],
        ),
        paragraph(
            "Senior Animal Control Officer | Target Role: Shelter Operations Manager / "
            "Animal Services Operations Supervisor",
            styles["Headline"],
        ),
    ]

    story.extend(section("Professional Summary", styles))
    story.append(
        paragraph(
            "Municipal animal welfare professional with 15+ years of progressive experience in "
            "animal care, animal control, shelter operations, humane investigations, team training, "
            "public education, and cross-department collaboration. Known for calm leadership in "
            "complex environments and for developing practical systems that support humane outcomes "
            "and sustainable staff workflows.",
            styles["Body"],
        )
    )

    story.extend(section("Experienced In", styles))
    skills = [
        "Supervising animal control officers",
        "Shelter operations coordination",
        "Humane investigations and compliance",
        "Staff training and development",
        "Community outreach initiatives",
        "Program implementation",
        "SOP and policy development",
        "Cross-department collaboration",
        "Public education and presentations",
    ]
    table_data = [[Paragraph(item, styles["Small"]) for item in skills[i : i + 3]] for i in range(0, len(skills), 3)]
    skill_table = Table(table_data, colWidths=[2.35 * inch, 2.35 * inch, 2.35 * inch])
    skill_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#f6f4ef")),
                ("BOX", (0, 0), (-1, -1), 0.4, colors.HexColor("#d9d5ca")),
                ("INNERGRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#d9d5ca")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 7),
                ("RIGHTPADDING", (0, 0), (-1, -1), 7),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )
    story.append(skill_table)

    story.extend(section("Work Experience", styles))
    jobs = [
        (
            "Senior Animal Control Officer",
            "City of Sacramento, Sacramento, CA",
            "Oct 2023 - Present",
            [
                "Compile, document, and preserve case evidence; prepare reports, affidavits, and case files for administrative or court proceedings.",
                "Testify in court and administrative hearings and serve as a subject-matter expert in animal welfare and enforcement matters.",
                "Plan, assign, and review subordinate work to support consistent enforcement and operational effectiveness.",
                "Develop and update department policies, standard operating procedures, and training materials.",
                "Collaborate with community groups, shelters, veterinarians, and partner agencies to promote compliance and humane outcomes.",
            ],
        ),
        (
            "Animal Control Officer II",
            "City of Sacramento, Sacramento, CA",
            "Feb 2020 - Oct 2023",
            [
                "Investigated animal cruelty, nuisance, and dangerous animal reports while enforcing City and State laws.",
                "Assisted law enforcement and other agencies during emergencies, investigations, animal custody, and transport.",
                "Prepared animal control cases for court, issued citations, provided testimony, and maintained records.",
                "Educated the public on animal laws, licensing, responsible care, and public safety.",
                "Assisted with training other animal control officers.",
            ],
        ),
        (
            "Animal Care Technician",
            "City of Sacramento, Sacramento, CA",
            "Mar 2018 - Feb 2020",
            [
                "Provided humane care, feeding, treatment, health inspections, and behavior monitoring for impounded animals.",
                "Supported behavior modification, enrichment programs, behavioral evaluations, and volunteer training.",
                "Maintained kennel sanitation and assisted with medical treatments and euthanasia procedures.",
            ],
        ),
        (
            "Assistant Manager",
            "Grateful Dog Daycare, Sacramento, CA",
            "Feb 2017 - Mar 2018",
            [
                "Managed scheduling, staff training, customer concerns, inventory, kennel cleanliness, safety regulations, and OSHA compliance.",
            ],
        ),
        (
            "Animal Care Supervisor",
            "Placer SPCA, Roseville, CA",
            "Mar 2016 - Feb 2017",
            [
                "Supervised animal care staff and volunteers; managed schedules, training, performance reviews, shelter resources, and safety compliance.",
            ],
        ),
        (
            "Earlier Animal Care Roles",
            "Napa County Animal Shelter, City of Sacramento, Animal Den, UC Davis, Solano SPCA, Petco",
            "2006 - 2016",
            [
                "Built broad experience in kennel management, animal care, medication administration, adoption and intake support, foster and rescue coordination, temperament testing, staff coaching, and customer service.",
            ],
        ),
    ]
    for item in jobs:
        story.extend(job(*item, styles))

    story.extend(section("Featured Project Experience", styles))
    story.extend(
        bullets(
            [
                "HOAP: Supported unhoused pet owners through veterinary resources, vaccinations, outreach, and coordinated community partnerships.",
                "Volunteer Kennel Enrichment Pilot Program: Structured repeatable enrichment scheduling, volunteer workflow organization, and outcome tracking concepts.",
                "QR Code Animal Behavior Tracking Concept: Proposed a digital workflow to improve documentation consistency, team communication, and behavior tracking efficiency.",
            ],
            styles["Bullet"],
        )
    )

    story.extend(section("Education", styles))
    story.extend(
        bullets(
            [
                "Human Resource Management, Bachelor's degree - Western Governors University, Aug 2025 - Present",
                "Business Management, some college - Solano Community College",
                "PC 832 Search and Seizure / Firearms - American River College, May 2020",
                "High School Diploma - Campolindo High School",
            ],
            styles["Bullet"],
        )
    )

    story.extend(section("Certifications and Licenses", styles))
    story.extend(
        bullets(
            [
                "Humane euthanasia certification",
                "Fear Free handling certified",
                "CLETS Certification, Sep 2022 - Present",
                "Chemical capture, Sep 2022",
                "PC 832 Search and Seizure / Firearms, May 2020",
                "NACA Certified Animal Control Officer I, Jun 2022 - Jun 2025",
                "IAABC Supporting Member, May 2021 - May 2025",
                "Shelter Behavior Affiliate, Nov 2021 - Nov 2023",
            ],
            styles["Bullet"],
        )
    )

    story.extend(section("Skills", styles))
    story.append(
        paragraph(
            "Dog handling | Pet care | Animal control enforcement | Cruelty investigations | Court testimony | "
            "Report writing | Team training | Communication | Microsoft Word | Microsoft Excel | Typing | Sales",
            styles["Body"],
        )
    )

    doc.build(story)


if __name__ == "__main__":
    main()
