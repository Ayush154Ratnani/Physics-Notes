from pathlib import Path
import textwrap

PAGE_WIDTH = 595
PAGE_HEIGHT = 842
MARGIN_X = 50
MARGIN_Y = 50
FONT_SIZE = 12
LINE_HEIGHT = 16
MAX_CHARS = 90


def escape_pdf_text(s: str) -> str:
    return s.replace('\\', '\\\\').replace('(', '\\(').replace(')', '\\)')


def wrap_lines(text: str):
    wrapped = []
    for raw in text.splitlines():
        if not raw.strip():
            wrapped.append('')
            continue
        leading = len(raw) - len(raw.lstrip(' '))
        prefix = ' ' * leading
        content = raw.strip()
        lines = textwrap.wrap(content, width=MAX_CHARS - leading) or ['']
        wrapped.extend(prefix + ln for ln in lines)
    return wrapped


def paginate(lines):
    lines_per_page = (PAGE_HEIGHT - 2 * MARGIN_Y) // LINE_HEIGHT
    pages = []
    for i in range(0, len(lines), lines_per_page):
        pages.append(lines[i:i + lines_per_page])
    return pages


def page_stream(lines):
    y_start = PAGE_HEIGHT - MARGIN_Y - FONT_SIZE
    chunks = ["BT", f"/F1 {FONT_SIZE} Tf", f"{MARGIN_X} {y_start} Td"]
    first = True
    for line in lines:
        if first:
            chunks.append(f"({escape_pdf_text(line)}) Tj")
            first = False
        else:
            chunks.append("T*")
            chunks.append(f"({escape_pdf_text(line)}) Tj")
    chunks.append("ET")
    return '\n'.join(chunks).encode('latin-1', errors='replace')


def build_pdf(input_path: Path, output_path: Path):
    lines = wrap_lines(input_path.read_text(encoding='utf-8'))
    pages = paginate(lines)

    objects = []

    # 1: catalog (placeholder)
    objects.append(b"")
    # 2: pages root (placeholder)
    objects.append(b"")
    # 3: font
    objects.append(b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>")

    page_ids = []
    content_ids = []

    for page_lines in pages:
        content = page_stream(page_lines)
        content_obj_id = len(objects) + 1
        objects.append(f"<< /Length {len(content)} >>\nstream\n".encode('latin-1') + content + b"\nendstream")
        content_ids.append(content_obj_id)

        page_obj_id = len(objects) + 1
        page_ids.append(page_obj_id)
        objects.append(b"")  # placeholder for page dictionary

    kids = ' '.join(f"{pid} 0 R" for pid in page_ids)
    objects[1] = f"<< /Type /Pages /Count {len(page_ids)} /Kids [{kids}] >>".encode('latin-1')
    objects[0] = b"<< /Type /Catalog /Pages 2 0 R >>"

    for pid, cid in zip(page_ids, content_ids):
        objects[pid - 1] = (
            f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 {PAGE_WIDTH} {PAGE_HEIGHT}] "
            f"/Resources << /Font << /F1 3 0 R >> >> /Contents {cid} 0 R >>"
        ).encode('latin-1')

    xref_positions = []
    pdf = bytearray(b"%PDF-1.4\n")

    for i, obj in enumerate(objects, start=1):
        xref_positions.append(len(pdf))
        pdf.extend(f"{i} 0 obj\n".encode('latin-1'))
        pdf.extend(obj)
        pdf.extend(b"\nendobj\n")

    xref_start = len(pdf)
    pdf.extend(f"xref\n0 {len(objects) + 1}\n".encode('latin-1'))
    pdf.extend(b"0000000000 65535 f \n")
    for pos in xref_positions:
        pdf.extend(f"{pos:010d} 00000 n \n".encode('latin-1'))

    pdf.extend(
        f"trailer\n<< /Size {len(objects) + 1} /Root 1 0 R >>\nstartxref\n{xref_start}\n%%EOF\n".encode('latin-1')
    )

    output_path.write_bytes(pdf)


if __name__ == "__main__":
    build_pdf(Path("electrostatics_notes.md"), Path("electrostatics_notes.pdf"))
    print("Created electrostatics_notes.pdf")
