from datetime import datetime
from math import atan2, cos, sin
from pathlib import Path
from textwrap import fill

from PIL import Image, ImageDraw, ImageFont
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN
from pptx.util import Inches, Pt


ROOT = Path(__file__).parent
ASSETS_DIR = ROOT / "presentation_assets"
OUTPUT_FILE = ROOT / "Solution_Assessment_Cursor_AI_Capabilities_Integration_Review.pptx"


def load_font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    ]
    for candidate in candidates:
        if Path(candidate).exists():
            return ImageFont.truetype(candidate, size)
    return ImageFont.load_default()


def draw_header(draw: ImageDraw.ImageDraw, title: str, width: int, accent=(35, 94, 179)) -> None:
    draw.rectangle((0, 0, width, 104), fill=accent)
    draw.text((34, 24), title, font=load_font(44, bold=True), fill=(255, 255, 255))


def draw_box(
    draw: ImageDraw.ImageDraw,
    xy,
    title: str,
    lines,
    fill_color=(246, 250, 255),
    border=(132, 163, 210),
) -> None:
    x1, y1, x2, y2 = xy
    draw.rounded_rectangle(xy, radius=20, fill=fill_color, outline=border, width=3)
    draw.text((x1 + 18, y1 + 16), title, font=load_font(34, bold=True), fill=(24, 41, 70))
    y = y1 + 72
    for line in lines:
        wrapped = fill(line, width=25)
        draw.text((x1 + 20, y), f"- {wrapped}", font=load_font(25), fill=(40, 57, 84))
        y += 54 + (wrapped.count("\n") * 18)


def draw_arrow(draw: ImageDraw.ImageDraw, start, end, color=(68, 107, 173), width=6) -> None:
    draw.line([start, end], fill=color, width=width)
    angle = atan2(end[1] - start[1], end[0] - start[0])
    arrow_len = 20
    arrow_width = 10
    p1 = end
    p2 = (
        end[0] - arrow_len * cos(angle) + arrow_width * sin(angle),
        end[1] - arrow_len * sin(angle) - arrow_width * cos(angle),
    )
    p3 = (
        end[0] - arrow_len * cos(angle) - arrow_width * sin(angle),
        end[1] - arrow_len * sin(angle) + arrow_width * cos(angle),
    )
    draw.polygon([p1, p2, p3], fill=color)


def save_image(image: Image.Image, path: Path) -> None:
    image.save(path, format="PNG", dpi=(300, 300))


def create_title_visual(path: Path) -> None:
    width, height = 1800, 1012
    image = Image.new("RGB", (width, height), (243, 247, 253))
    draw = ImageDraw.Draw(image)
    draw_header(draw, "Cursor AI + MCP integration view", width)

    center = (890, 500)
    r = 190
    draw.ellipse((center[0] - r, center[1] - r, center[0] + r, center[1] + r), fill=(29, 78, 156), outline=(18, 56, 120), width=4)
    draw.text((center[0] - 128, center[1] - 34), "Cursor\nAgents", font=load_font(54, bold=True), fill=(255, 255, 255), align="center")

    node_specs = [
        ((260, 220, 620, 360), "Jira MCP", (255, 245, 232)),
        ((1180, 220, 1540, 360), "Figma MCP", (236, 250, 243)),
        ((260, 670, 620, 810), "Bitbucket MCP", (237, 244, 255)),
        ((1180, 670, 1540, 810), "Policy + Audit", (250, 240, 250)),
    ]

    for box, label, color in node_specs:
        draw.rounded_rectangle(box, radius=24, fill=color, outline=(137, 164, 206), width=3)
        tw, th = draw.textbbox((0, 0), label, font=load_font(46, bold=True))[2:]
        draw.text(((box[0] + box[2] - tw) / 2, (box[1] + box[3] - th) / 2), label, font=load_font(46, bold=True), fill=(26, 48, 83))

    draw_arrow(draw, (620, 290), (700, 390))
    draw_arrow(draw, (1180, 290), (1080, 390))
    draw_arrow(draw, (620, 740), (700, 620))
    draw_arrow(draw, (1180, 740), (1080, 620))

    draw.text((36, 920), "Assessment focus: capability maturity, integration design, operating model, and skill governance", font=load_font(32), fill=(46, 66, 99))
    save_image(image, path)


def create_capability_chart(path: Path) -> None:
    width, height = 1800, 1012
    image = Image.new("RGB", (width, height), (247, 250, 255))
    draw = ImageDraw.Draw(image)
    draw_header(draw, "Current capability assessment", width)

    categories = [
        ("Code generation and refactoring", 4.4, (60, 130, 246)),
        ("Developer productivity gains", 4.1, (52, 168, 83)),
        ("MCP integration readiness", 3.7, (235, 135, 49)),
        ("Governance and controls", 3.3, (200, 93, 93)),
        ("Skill reuse and standardization", 3.5, (130, 102, 219)),
    ]

    left = 110
    top = 160
    bar_max = 1080
    row_height = 130

    draw.text((left, 115), "Maturity score (0-5)", font=load_font(30, bold=True), fill=(36, 59, 94))
    for idx, (label, score, color) in enumerate(categories):
        y = top + idx * row_height
        draw.text((left, y + 22), label, font=load_font(29, bold=True), fill=(34, 52, 82))
        track_x1 = 700
        track_x2 = track_x1 + bar_max
        draw.rounded_rectangle((track_x1, y + 20, track_x2, y + 70), radius=18, fill=(225, 234, 248))
        fill_width = int(bar_max * (score / 5.0))
        draw.rounded_rectangle((track_x1, y + 20, track_x1 + fill_width, y + 70), radius=18, fill=color)
        draw.text((track_x2 + 18, y + 22), f"{score:.1f}", font=load_font(31, bold=True), fill=(20, 38, 65))

    draw.rectangle((110, 815, 1490, 865), fill=(234, 242, 255), outline=(159, 179, 214), width=2)
    draw.text((140, 826), "Overall readiness score: 3.8 / 5.0 (strong pilot candidate with governance uplift needed)", font=load_font(25, bold=True), fill=(32, 56, 90))
    save_image(image, path)


def create_architecture(path: Path) -> None:
    width, height = 1800, 1012
    image = Image.new("RGB", (width, height), (244, 248, 254))
    draw = ImageDraw.Draw(image)
    draw_header(draw, "Target integration architecture", width)

    draw_box(
        draw,
        (80, 170, 520, 760),
        "Enterprise tools",
        [
            "Jira projects and workflows",
            "Figma files and design systems",
            "Bitbucket repositories and pull requests",
        ],
        fill_color=(236, 246, 255),
    )
    draw_box(
        draw,
        (590, 170, 1020, 760),
        "MCP server layer",
        [
            "Authentication and token management",
            "Standardized tool schemas",
            "Rate limits, retries, and audit logs",
        ],
        fill_color=(235, 250, 240),
    )
    draw_box(
        draw,
        (1090, 170, 1520, 760),
        "Cursor agents",
        [
            "Workflow prompts and skills",
            "Human approval checkpoints",
            "Outputs: tickets, PRs, implementation notes",
        ],
        fill_color=(248, 239, 255),
    )

    draw_arrow(draw, (520, 320), (590, 320))
    draw_arrow(draw, (520, 520), (590, 520))
    draw_arrow(draw, (1020, 420), (1090, 420))

    draw.rectangle((640, 785, 970, 852), fill=(255, 243, 228), outline=(210, 156, 89), width=3)
    draw.text((665, 806), "Policy + Compliance guardrails", font=load_font(25, bold=True), fill=(115, 71, 24))

    save_image(image, path)


def create_mcp_service_diagram(path: Path, service: str, color: tuple, exposed_data, agent_actions, impact) -> None:
    width, height = 1800, 1012
    image = Image.new("RGB", (width, height), (247, 249, 253))
    draw = ImageDraw.Draw(image)
    draw_header(draw, f"MCP integration pattern: {service}", width, accent=color)

    draw_box(draw, (70, 170, 520, 780), "Data exposed via MCP", exposed_data, fill_color=(241, 247, 255))
    draw_box(draw, (580, 170, 1030, 780), "Agent actions", agent_actions, fill_color=(241, 255, 245))
    draw_box(draw, (1090, 170, 1540, 780), "Business impact", impact, fill_color=(255, 246, 238))

    draw_arrow(draw, (520, 470), (580, 470), color=(92, 123, 176))
    draw_arrow(draw, (1030, 470), (1090, 470), color=(92, 123, 176))

    save_image(image, path)


def create_effectiveness_matrix(path: Path) -> None:
    width, height = 1800, 1012
    image = Image.new("RGB", (width, height), (245, 249, 255))
    draw = ImageDraw.Draw(image)
    draw_header(draw, "How to use Cursor + MCP effectively", width)

    grid = (180, 180, 1420, 780)
    draw.rectangle(grid, outline=(99, 131, 186), width=4, fill=(252, 254, 255))
    mid_x = (grid[0] + grid[2]) // 2
    mid_y = (grid[1] + grid[3]) // 2
    draw.line((mid_x, grid[1], mid_x, grid[3]), fill=(120, 150, 201), width=3)
    draw.line((grid[0], mid_y, grid[2], mid_y), fill=(120, 150, 201), width=3)

    draw.text((210, 140), "Low standardization", font=load_font(24), fill=(36, 58, 92))
    draw.text((1180, 140), "High standardization", font=load_font(24), fill=(36, 58, 92))
    draw.text((40, 480), "High\nautonomy", font=load_font(24), fill=(36, 58, 92))
    draw.text((50, 210), "Low\nautonomy", font=load_font(24), fill=(36, 58, 92))

    draw.text((225, 215), "Ad hoc prompts", font=load_font(26, bold=True), fill=(122, 62, 62))
    draw.text((850, 215), "Reusable task recipes", font=load_font(26, bold=True), fill=(43, 79, 135))
    draw.text((215, 525), "Uncontrolled automation", font=load_font(26, bold=True), fill=(122, 62, 62))
    draw.text((865, 525), "Governed agent workflows", font=load_font(26, bold=True), fill=(38, 107, 72))

    practices = [
        ("Prompt template library", (1080, 330), (51, 112, 187)),
        ("Definition of Done checks", (1140, 380), (31, 130, 73)),
        ("Approval gates for writes", (1020, 610), (31, 130, 73)),
        ("Weekly usage analytics", (1230, 560), (31, 130, 73)),
        ("One-off assistant chats", (370, 350), (175, 90, 90)),
        ("Unreviewed status updates", (420, 630), (175, 90, 90)),
    ]
    for label, center, color in practices:
        x, y = center
        draw.ellipse((x - 14, y - 14, x + 14, y + 14), fill=color)
        draw.text((x + 22, y - 14), label, font=load_font(22), fill=(33, 53, 84))

    save_image(image, path)


def create_skill_lifecycle(path: Path) -> None:
    width, height = 1800, 1012
    image = Image.new("RGB", (width, height), (246, 250, 255))
    draw = ImageDraw.Draw(image)
    draw_header(draw, "Agent skill lifecycle", width)

    steps = [
        ("1. Discover", "Find repeatable workflow"),
        ("2. Define", "Write skill metadata and prompt"),
        ("3. Package", "Attach tools and constraints"),
        ("4. Validate", "Run golden-task tests"),
        ("5. Publish", "Version and release notes"),
        ("6. Observe", "Track quality and retire stale"),
    ]

    x = 80
    y = 290
    w = 230
    h = 220
    gap = 25
    colors = [
        (233, 243, 255),
        (232, 247, 240),
        (241, 240, 255),
        (255, 245, 234),
        (236, 249, 249),
        (252, 240, 246),
    ]
    for idx, (title, subtitle) in enumerate(steps):
        box = (x, y, x + w, y + h)
        draw.rounded_rectangle(box, radius=18, fill=colors[idx], outline=(130, 161, 208), width=3)
        draw.text((x + 15, y + 22), title, font=load_font(29, bold=True), fill=(31, 53, 88))
        draw.text((x + 15, y + 88), fill(subtitle, width=18), font=load_font(23), fill=(43, 63, 94))
        if idx < len(steps) - 1:
            draw_arrow(draw, (x + w, y + h // 2), (x + w + gap - 5, y + h // 2), color=(75, 109, 167))
        x += w + gap

    draw.rectangle((115, 620, 1480, 790), fill=(236, 243, 255), outline=(148, 170, 214), width=3)
    code_block = [
        "skills/",
        "  jira-ticket-triage/",
        "    skill.yaml",
        "    prompts.md",
        "    tests.json",
    ]
    draw.text((150, 650), "\n".join(code_block), font=load_font(31), fill=(36, 60, 96))
    draw.text((660, 670), "Version each skill and validate against baseline tasks\nbefore publishing to the team registry.", font=load_font(28), fill=(36, 60, 96))

    save_image(image, path)


def create_roadmap(path: Path) -> None:
    width, height = 1800, 1012
    image = Image.new("RGB", (width, height), (247, 251, 255))
    draw = ImageDraw.Draw(image)
    draw_header(draw, "90-day implementation roadmap", width)

    draw.line((170, 420, 1430, 420), fill=(84, 119, 179), width=8)
    milestones = [
        (280, "0-30 days", ["Stand up MCP connectors", "Define security controls", "Pilot 2 squads"]),
        (800, "31-60 days", ["Publish top 10 skills", "Add CI quality checks", "Enable usage analytics"]),
        (1320, "61-90 days", ["Scale to 6+ squads", "Executive value review", "Production operating model"]),
    ]

    for x, title, bullets in milestones:
        draw.ellipse((x - 26, 394, x + 26, 446), fill=(36, 94, 178))
        draw.rounded_rectangle((x - 220, 170, x + 220, 360), radius=20, fill=(234, 242, 255), outline=(129, 160, 209), width=3)
        draw.text((x - 200, 196), title, font=load_font(33, bold=True), fill=(24, 46, 79))
        y = 250
        for item in bullets:
            draw.text((x - 198, y), f"- {item}", font=load_font(23), fill=(38, 60, 94))
            y += 38

    draw.rectangle((190, 560, 1410, 780), fill=(237, 251, 244), outline=(126, 182, 148), width=3)
    draw.text((230, 600), "Exit criteria: >20% cycle-time improvement, >30% prompt reuse, and zero critical governance incidents.", font=load_font(29, bold=True), fill=(27, 93, 60))
    draw.text((230, 660), "Track KPIs weekly: lead time, review latency, rework rate, automation success rate.", font=load_font(27), fill=(27, 93, 60))

    save_image(image, path)


def create_risk_heatmap(path: Path) -> None:
    width, height = 1800, 1012
    image = Image.new("RGB", (width, height), (248, 250, 255))
    draw = ImageDraw.Draw(image)
    draw_header(draw, "Risk and governance heatmap", width)

    x0, y0 = 220, 170
    cell = 180
    colors = {
        (1, 1): (222, 241, 223),
        (1, 2): (236, 247, 199),
        (1, 3): (255, 234, 179),
        (2, 1): (229, 240, 204),
        (2, 2): (255, 235, 183),
        (2, 3): (255, 209, 169),
        (3, 1): (255, 235, 183),
        (3, 2): (255, 209, 169),
        (3, 3): (248, 176, 170),
    }
    for i in range(1, 4):
        for j in range(1, 4):
            x1 = x0 + (j - 1) * cell
            y1 = y0 + (3 - i) * cell
            draw.rectangle((x1, y1, x1 + cell, y1 + cell), fill=colors[(i, j)], outline=(150, 162, 180), width=2)

    draw.text((x0 + 150, y0 + 560), "Impact  ->", font=load_font(26, bold=True), fill=(43, 63, 98))
    draw.text((90, y0 + 190), "Probability", font=load_font(26, bold=True), fill=(43, 63, 98))
    draw.text((125, y0 + 225), "(Low to High)", font=load_font(23), fill=(43, 63, 98))

    risk_labels = [
        ("Over-permissioned tokens", (x0 + 390, y0 + 80)),
        ("Unreviewed write actions", (x0 + 390, y0 + 260)),
        ("Inconsistent skill quality", (x0 + 210, y0 + 260)),
        ("Prompt drift", (x0 + 210, y0 + 440)),
    ]
    for label, pos in risk_labels:
        draw.text(pos, label, font=load_font(22, bold=True), fill=(54, 58, 79))

    draw_box(
        draw,
        (850, 180, 1530, 760),
        "Top controls",
        [
            "Role-based access and repository allow-lists",
            "Human approvals for all state-changing tool calls",
            "Central audit logs for prompt, action, and output traceability",
            "Golden-task test suite for each published skill",
            "Quarterly access review and token rotation",
        ],
        fill_color=(238, 246, 255),
    )

    save_image(image, path)


def create_tutorial_flow(path: Path) -> None:
    width, height = 1800, 1012
    image = Image.new("RGB", (width, height), (246, 250, 255))
    draw = ImageDraw.Draw(image)
    draw_header(draw, "Hands-on training path (step-by-step)", width, accent=(24, 102, 173))

    stages = [
        ("Step 1", "Prepare environment\nand credentials"),
        ("Step 2", "Configure MCP\nservers in Cursor"),
        ("Step 3", "Run Jira, Figma,\nand Bitbucket labs"),
        ("Step 4", "Create reusable\nagent skills"),
        ("Step 5", "Add approvals,\nlogs, and KPIs"),
    ]

    x = 110
    y = 280
    w = 290
    h = 250
    gap = 42
    for i, (title, subtitle) in enumerate(stages):
        box = (x, y, x + w, y + h)
        draw.rounded_rectangle(box, radius=20, fill=(236, 244, 255), outline=(120, 155, 210), width=3)
        draw.text((x + 28, y + 32), title, font=load_font(38, bold=True), fill=(24, 50, 90))
        draw.text((x + 28, y + 108), subtitle, font=load_font(31), fill=(33, 62, 105))
        if i < len(stages) - 1:
            draw_arrow(draw, (x + w, y + h // 2), (x + w + gap - 8, y + h // 2), color=(74, 112, 178), width=8)
        x += w + gap

    draw.rectangle((150, 640, 1660, 862), fill=(236, 251, 244), outline=(126, 182, 148), width=3)
    draw.text((190, 690), "Delivery model: 20% theory + 80% labs, pair exercises, and weekly office hours.", font=load_font(34, bold=True), fill=(26, 92, 58))
    draw.text((190, 750), "Success check: every developer completes one end-to-end workflow and publishes one skill.", font=load_font(30), fill=(26, 92, 58))

    save_image(image, path)


def generate_images() -> dict:
    ASSETS_DIR.mkdir(exist_ok=True)
    files = {
        "title": ASSETS_DIR / "title_visual.png",
        "capabilities": ASSETS_DIR / "capability_chart.png",
        "architecture": ASSETS_DIR / "architecture.png",
        "jira": ASSETS_DIR / "jira_mcp.png",
        "figma": ASSETS_DIR / "figma_mcp.png",
        "bitbucket": ASSETS_DIR / "bitbucket_mcp.png",
        "effectiveness": ASSETS_DIR / "effectiveness_matrix.png",
        "skills": ASSETS_DIR / "skill_lifecycle.png",
        "risk": ASSETS_DIR / "risk_heatmap.png",
        "roadmap": ASSETS_DIR / "roadmap.png",
        "tutorial": ASSETS_DIR / "tutorial_flow.png",
    }

    create_title_visual(files["title"])
    create_capability_chart(files["capabilities"])
    create_architecture(files["architecture"])
    create_mcp_service_diagram(
        files["jira"],
        "Jira",
        (6, 90, 180),
        ["Issue summaries", "Backlog and sprint state", "Comments and links"],
        ["Draft acceptance criteria", "Generate test scenarios", "Summarize blockers"],
        ["Faster triage", "Higher ticket clarity", "Lower reopen rates"],
    )
    create_mcp_service_diagram(
        files["figma"],
        "Figma",
        (53, 94, 59),
        ["Design tokens", "Components and variants", "Frame comments"],
        ["Generate implementation notes", "Map specs to UI stories", "Flag design-code drift"],
        ["Fewer handoff defects", "Lower UI rework", "Faster design-to-code flow"],
    )
    create_mcp_service_diagram(
        files["bitbucket"],
        "Bitbucket",
        (0, 96, 136),
        ["Repository structure", "Commits and diffs", "Pull request history"],
        ["Draft PR descriptions", "Generate review checklists", "Summarize release deltas"],
        ["Reduced PR lead time", "Better review quality", "Higher delivery confidence"],
    )
    create_effectiveness_matrix(files["effectiveness"])
    create_skill_lifecycle(files["skills"])
    create_risk_heatmap(files["risk"])
    create_roadmap(files["roadmap"])
    create_tutorial_flow(files["tutorial"])

    return files


def style_title(shape, text: str) -> None:
    tf = shape.text_frame
    tf.clear()
    p = tf.paragraphs[0]
    run = p.add_run()
    run.text = text
    run.font.size = Pt(34)
    run.font.bold = True
    run.font.color.rgb = RGBColor(21, 42, 75)
    p.alignment = PP_ALIGN.LEFT


def add_title_block(slide, title: str, subtitle: str | None = None) -> None:
    title_box = slide.shapes.add_textbox(Inches(0.45), Inches(0.16), Inches(12.2), Inches(0.7))
    style_title(title_box, title)
    if subtitle:
        sub_box = slide.shapes.add_textbox(Inches(0.48), Inches(0.82), Inches(12), Inches(0.45))
        tf = sub_box.text_frame
        tf.clear()
        p = tf.paragraphs[0]
        run = p.add_run()
        run.text = subtitle
        run.font.size = Pt(18)
        run.font.color.rgb = RGBColor(70, 88, 118)


def add_bullets(slide, items, x=0.55, y=1.35, w=5.5, h=5.65) -> None:
    text_box = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = text_box.text_frame
    tf.clear()
    tf.word_wrap = True
    for idx, item in enumerate(items):
        if isinstance(item, tuple):
            text, level = item
        else:
            text, level = item, 0
        p = tf.paragraphs[0] if idx == 0 else tf.add_paragraph()
        p.text = text
        p.level = level
        p.font.size = Pt(22 if level == 0 else 18)
        p.font.color.rgb = RGBColor(35, 52, 82)
        p.space_after = Pt(10)
        p.space_before = Pt(2)


def add_image(slide, image_path: Path, x=6.2, y=1.3, w=6.8) -> None:
    slide.shapes.add_picture(str(image_path), Inches(x), Inches(y), width=Inches(w))


def add_code_block(slide, code_lines, x=0.55, y=1.65, w=12.2, h=5.45) -> None:
    block = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h))
    block.fill.solid()
    block.fill.fore_color.rgb = RGBColor(24, 33, 52)
    block.line.color.rgb = RGBColor(24, 33, 52)

    tf = block.text_frame
    tf.clear()
    tf.word_wrap = True
    for idx, line in enumerate(code_lines):
        p = tf.paragraphs[0] if idx == 0 else tf.add_paragraph()
        p.text = line
        p.font.size = Pt(15)
        p.font.name = "DejaVu Sans Mono"
        p.font.color.rgb = RGBColor(232, 238, 252)
        p.space_after = Pt(3)
        p.space_before = Pt(0)


def build_presentation(images: dict) -> None:
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank = prs.slide_layouts[6]

    # Slide 1: Cover
    slide = prs.slides.add_slide(blank)
    add_title_block(
        slide,
        "Solution Assessment: Cursor AI Capabilities and Integration Review",
        "Training edition with step-by-step labs, commands, and adoption model.",
    )
    add_bullets(
        slide,
        [
            "Objective: evaluate technical fit, operating readiness, and governance controls.",
            "Scope: IDE productivity, workflow automation, and enterprise integration design.",
            f"Date: {datetime.now().strftime('%Y-%m-%d')}",
        ],
        x=0.6,
        y=1.55,
        w=5.3,
        h=4.8,
    )
    add_image(slide, images["title"], x=5.95, y=1.2, w=7.15)

    # Slide 2: Agenda
    slide = prs.slides.add_slide(blank)
    add_title_block(slide, "Agenda")
    add_bullets(
        slide,
        [
            "1) Capability assessment and current maturity baseline",
            "2) MCP integration patterns for Jira, Figma, and Bitbucket",
            "3) Effective usage model for developers and team leads",
            "4) Hands-on tutorial with setup and commands",
            "5) How to add and maintain agent skills",
            "6) Governance controls, KPI tracking, and 90-day roadmap",
        ],
        x=0.9,
        y=1.5,
        w=11.5,
        h=5.7,
    )

    # Slide 3: Training approach
    slide = prs.slides.add_slide(blank)
    add_title_block(
        slide,
        "Developer Training Approach (Easy Adoption)",
        "Run this as a 4-week plan: 20% concepts + 80% practical labs.",
    )
    add_bullets(
        slide,
        [
            "Week 1: foundation and MCP setup by each developer.",
            "Week 2: Jira, Figma, and Bitbucket workflow labs.",
            "Week 3: prompt standardization and quality gates.",
            "Week 4: skill creation, versioning, and team rollout.",
        ],
    )
    add_image(slide, images["tutorial"], x=6.05, y=1.25, w=7.0)

    # Slide 4: Capability assessment
    slide = prs.slides.add_slide(blank)
    add_title_block(slide, "Assessment Snapshot: Cursor AI Capability Maturity")
    add_bullets(
        slide,
        [
            "Overall readiness is strong for a controlled pilot: 3.8 / 5.0.",
            "Strongest dimensions: code generation, refactoring, and context-aware assistance.",
            "Main gaps: standardized workflow recipes, governance instrumentation, and skill reuse.",
            "Recommendation: pilot with two squads and centralized enablement support.",
        ],
    )
    add_image(slide, images["capabilities"], x=5.95, y=1.25, w=7.1)

    # Slide 5: Architecture
    slide = prs.slides.add_slide(blank)
    add_title_block(slide, "Target Integration Architecture (MCP + Cursor Agents)")
    add_bullets(
        slide,
        [
            "MCP servers expose enterprise tools using normalized schemas for agents.",
            "Use least-privilege service accounts and repository/project allow-lists.",
            "Require human approval for state-changing actions (status updates, merges).",
            "Log prompts, tool calls, and outputs for audit and compliance traceability.",
        ],
    )
    add_image(slide, images["architecture"], x=5.95, y=1.25, w=7.1)

    # Slide 6: Jira MCP
    slide = prs.slides.add_slide(blank)
    add_title_block(slide, "MCP for Jira: Workflow Automation Opportunities")
    add_bullets(
        slide,
        [
            "Use cases: ticket summarization, acceptance criteria drafting, and test scenario generation.",
            "Setup: Jira token, MCP Jira server configuration, project and issue filters.",
            "Guardrails: no automatic status transitions without explicit user confirmation.",
            "KPIs: grooming time, cycle time, reopen rate, and requirement clarity.",
        ],
    )
    add_image(slide, images["jira"], x=5.95, y=1.25, w=7.1)

    # Slide 7: Figma MCP
    slide = prs.slides.add_slide(blank)
    add_title_block(slide, "MCP for Figma: Design-to-Code Acceleration")
    add_bullets(
        slide,
        [
            "Use cases: extract design tokens, generate implementation notes, map components to stories.",
            "Setup: scoped Figma token, design-system mapping, and project-level permissions.",
            "Guardrails: read-only access in production design files; write only in sandbox.",
            "KPIs: handoff defects, UI rework effort, and design implementation lead time.",
        ],
    )
    add_image(slide, images["figma"], x=5.95, y=1.25, w=7.1)

    # Slide 8: Bitbucket MCP
    slide = prs.slides.add_slide(blank)
    add_title_block(slide, "MCP for Bitbucket: Source Control Intelligence")
    add_bullets(
        slide,
        [
            "Use cases: repository analysis, PR description drafts, and review checklist generation.",
            "Setup: OAuth/app password, branch protections, and repository allow-list.",
            "Guardrails: protected branches, mandatory reviewer, and CI pass before merge.",
            "KPIs: PR lead time, review latency, escaped defect rate, and release quality.",
        ],
    )
    add_image(slide, images["bitbucket"], x=5.95, y=1.25, w=7.1)

    # Slide 9: Effective usage
    slide = prs.slides.add_slide(blank)
    add_title_block(slide, "How to Use Cursor + MCP Effectively")
    add_bullets(
        slide,
        [
            "Standardize prompts as reusable recipes for common engineering tasks.",
            "Start with assistant mode, then scale to agent actions with approval checkpoints.",
            "Attach each workflow to quality gates and a clear Definition of Done.",
            "Review adoption and quality metrics weekly; retire low-value automations quickly.",
        ],
    )
    add_image(slide, images["effectiveness"], x=5.95, y=1.25, w=7.1)

    # Slide 10: Agent skills
    slide = prs.slides.add_slide(blank)
    add_title_block(slide, "How to Add Agent Skills")
    add_bullets(
        slide,
        [
            "A skill package should include metadata, prompts, tools, and validation tests.",
            "Use a versioned registry and changelog for transparent rollout and rollback.",
            "Test each skill on golden tasks before publishing to teams.",
            "Run monthly quality reviews to improve prompts and remove stale skills.",
        ],
    )
    add_image(slide, images["skills"], x=5.95, y=1.25, w=7.1)

    # Slide 11: Tutorial step 1
    slide = prs.slides.add_slide(blank)
    add_title_block(
        slide,
        "Tutorial Step 1: Local Environment Setup",
        "Run these commands once per developer machine.",
    )
    add_code_block(
        slide,
        [
            "# 1) Create training workspace",
            "mkdir -p ~/cursor-mcp-training/{servers,skills,logs} && cd ~/cursor-mcp-training",
            "",
            "# 2) Create Python environment for helper scripts",
            "python3 -m venv .venv",
            "source .venv/bin/activate",
            "python -m pip install --upgrade pip",
            "pip install mcp httpx python-dotenv pyyaml",
            "",
            "# 3) Verify runtime versions",
            "python --version && node --version && npm --version",
            "",
            "# 4) Optional CLI helper",
            "sudo apt-get update && sudo apt-get install -y jq",
        ],
    )

    # Slide 12: Tutorial step 2
    slide = prs.slides.add_slide(blank)
    add_title_block(
        slide,
        "Tutorial Step 2: Configure MCP Servers in Cursor",
        "Use this as a template and replace placeholders with your values.",
    )
    add_code_block(
        slide,
        [
            "# 1) Store credentials",
            "cat > .env <<'EOF'",
            "JIRA_BASE_URL=https://your-company.atlassian.net",
            "JIRA_EMAIL=you@company.com",
            "JIRA_API_TOKEN=<jira_token>",
            "FIGMA_TOKEN=<figma_token>",
            "BITBUCKET_WORKSPACE=<workspace>",
            "BITBUCKET_USERNAME=<username>",
            "BITBUCKET_APP_PASSWORD=<app_password>",
            "EOF",
            "",
            "# 2) Cursor MCP config",
            "mkdir -p .cursor",
            "cat > .cursor/mcp.json <<'JSON'",
            "{\"mcpServers\":{\"jira\":{\"command\":\"python\",\"args\":[\"servers/jira_server.py\"],\"envFile\":\".env\"},\"figma\":{\"command\":\"python\",\"args\":[\"servers/figma_server.py\"],\"envFile\":\".env\"},\"bitbucket\":{\"command\":\"python\",\"args\":[\"servers/bitbucket_server.py\"],\"envFile\":\".env\"}}}",
            "JSON",
        ],
    )

    # Slide 13: Tutorial step 3
    slide = prs.slides.add_slide(blank)
    add_title_block(
        slide,
        "Tutorial Step 3: Jira Lab (Ticket Triage + Acceptance Criteria)",
        "First validate API access, then run the workflow from Cursor chat.",
    )
    add_code_block(
        slide,
        [
            "source .venv/bin/activate && source .env",
            "",
            "# Validate Jira token and user",
            "curl -s -u \"$JIRA_EMAIL:$JIRA_API_TOKEN\" \"$JIRA_BASE_URL/rest/api/3/myself\" | jq '.displayName'",
            "",
            "# Pull latest issues from a project",
            "curl -s -u \"$JIRA_EMAIL:$JIRA_API_TOKEN\" -G \"$JIRA_BASE_URL/rest/api/3/search\" --data-urlencode 'jql=project = PROJ ORDER BY updated DESC' --data-urlencode 'maxResults=5' | jq '.issues[].key'",
            "",
            "# Prompt in Cursor",
            "Prompt: \"Using Jira MCP, summarize PROJ-101, draft acceptance criteria, and produce test cases.\"",
            "Prompt: \"Generate status update with blockers, risks, and next actions for standup.\"",
        ],
    )

    # Slide 14: Tutorial step 4
    slide = prs.slides.add_slide(blank)
    add_title_block(
        slide,
        "Tutorial Step 4: Figma Lab (Design-to-Code Handoff)",
        "Validate token, then generate implementation checklist and tasks.",
    )
    add_code_block(
        slide,
        [
            "source .venv/bin/activate && source .env",
            "export FIGMA_FILE_KEY=<file_key>",
            "",
            "# Validate Figma API access",
            "curl -s -H \"X-Figma-Token: $FIGMA_TOKEN\" \"https://api.figma.com/v1/files/$FIGMA_FILE_KEY\" | jq '.name'",
            "",
            "# Prompts in Cursor",
            "Prompt: \"Using Figma MCP, extract colors, spacing, and typography tokens.\"",
            "Prompt: \"Map components in frame HomePage to frontend stories with acceptance criteria.\"",
            "Prompt: \"Create UI handoff checklist including responsive and accessibility checks.\"",
        ],
    )

    # Slide 15: Tutorial step 5
    slide = prs.slides.add_slide(blank)
    add_title_block(
        slide,
        "Tutorial Step 5: Bitbucket Lab (PR Review and Release Notes)",
        "Use repo metadata + prompts to speed up review quality.",
    )
    add_code_block(
        slide,
        [
            "source .venv/bin/activate && source .env",
            "",
            "# Validate Bitbucket workspace access",
            "curl -s -u \"$BITBUCKET_USERNAME:$BITBUCKET_APP_PASSWORD\" \"https://api.bitbucket.org/2.0/repositories/$BITBUCKET_WORKSPACE\" | jq '.values[0].full_name'",
            "",
            "# Prompts in Cursor",
            "Prompt: \"Using Bitbucket MCP, summarize PR #123 and list functional risk areas.\"",
            "Prompt: \"Generate a reviewer checklist focused on tests, security, and rollback plan.\"",
            "Prompt: \"Create release notes from commits merged since previous release tag.\"",
        ],
    )

    # Slide 16: Tutorial step 6
    slide = prs.slides.add_slide(blank)
    add_title_block(
        slide,
        "Tutorial Step 6: Add Agent Skills (Reusable Team Assets)",
        "Each skill should include metadata, prompt contract, and test cases.",
    )
    add_code_block(
        slide,
        [
            "# Create skill directory",
            "mkdir -p skills/jira-ticket-triage && cd skills/jira-ticket-triage",
            "",
            "cat > skill.yaml <<'YAML'",
            "name: jira-ticket-triage",
            "version: 1.0.0",
            "description: Triage issue and output action plan",
            "tools: [jira.search, jira.get_issue]",
            "YAML",
            "",
            "cat > prompts.md <<'MD'",
            "# Inputs: issue key, team context, definition of done",
            "# Output: summary, acceptance criteria, test cases",
            "MD",
            "",
            "echo '[{\"input\":\"PROJ-101\",\"assert_contains\":[\"Summary\",\"Acceptance Criteria\"]}]' > tests.json",
        ],
    )

    # Slide 17: Tutorial step 7
    slide = prs.slides.add_slide(blank)
    add_title_block(
        slide,
        "Tutorial Step 7: Governance and KPI Operations",
        "Use scheduled scripts and weekly reviews to sustain adoption quality.",
    )
    add_code_block(
        slide,
        [
            "# Example weekly KPI export (replace script names with your internal tooling)",
            "mkdir -p logs metrics",
            "python scripts/export_mcp_logs.py --last-days 7 > logs/mcp_weekly.json",
            "python scripts/calc_kpis.py --input logs/mcp_weekly.json --output metrics/weekly_kpis.csv",
            "",
            "# KPI template",
            "echo 'date,cycle_time,pr_lead_time,reopen_rate,prompt_reuse,automation_success' > metrics/template.csv",
            "",
            "# Weekly review checklist",
            "echo 'Review failed automations, stale skills, and permission scope' > logs/weekly_review.txt",
            "echo 'Approve next sprint improvements based on KPI trends' >> logs/weekly_review.txt",
        ],
    )

    # Slide 18: Risk and governance
    slide = prs.slides.add_slide(blank)
    add_title_block(slide, "Risk Management and Governance Controls")
    add_bullets(
        slide,
        [
            "Top risks: over-permissioned tokens, unreviewed write actions, and prompt drift.",
            "Controls: RBAC, approval checkpoints, central logs, and benchmark test suites.",
            "Security baseline: vault secrets, rotate credentials every 90 days, anomaly alerts.",
            "Ownership: platform team manages MCP; squad leads manage skill effectiveness.",
        ],
    )
    add_image(slide, images["risk"], x=5.95, y=1.25, w=7.1)

    # Slide 19: Roadmap
    slide = prs.slides.add_slide(blank)
    add_title_block(slide, "90-Day Rollout Roadmap")
    add_bullets(
        slide,
        [
            "Days 0-30: establish MCP connectors, security controls, and baseline metrics.",
            "Days 31-60: publish high-value skills, add CI quality gates, and train champions.",
            "Days 61-90: scale to additional squads and report quantified business impact.",
            "Success target: >20% cycle-time improvement without governance incidents.",
        ],
    )
    add_image(slide, images["roadmap"], x=5.95, y=1.25, w=7.1)

    # Slide 20: Close
    slide = prs.slides.add_slide(blank)
    add_title_block(slide, "Recommended Next Steps")
    add_bullets(
        slide,
        [
            "Approve pilot scope and select 2-3 candidate squads.",
            "Assign owners for MCP platform, security controls, and skill registry.",
            "Start weekly steering reviews using KPI dashboard outputs.",
            "Plan executive checkpoint at day 45 and day 90.",
            "",
            "Q&A",
        ],
        x=0.9,
        y=1.6,
        w=5.5,
        h=5.4,
    )
    add_image(slide, images["title"], x=5.95, y=1.25, w=7.1)

    prs.save(OUTPUT_FILE)


def main() -> None:
    images = generate_images()
    build_presentation(images)
    print(f"Created: {OUTPUT_FILE}")
    print(f"Assets directory: {ASSETS_DIR}")


if __name__ == "__main__":
    main()
