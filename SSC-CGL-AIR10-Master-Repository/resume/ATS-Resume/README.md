# ATS Resume Package

Polished, single-page, ATS-friendly resume for **Priyadharshini Arumugam**
(Full Stack Developer — Laravel / PHP).

## Files

- `Priyadharshini_Arumugam_Resume.pdf` — final PDF (single page, ATS-safe)
- `Priyadharshini_Arumugam_Resume.docx` — editable Word version (same content)
- `generate_resume_docs.py` — source of truth; edit the content constants at the
  top, then re-run to regenerate **both** the PDF and DOCX.

## Regenerate

```bash
python generate_resume_docs.py
```

Requires `python-docx` and `reportlab`.

## Design notes

- Single column, standard headings, real selectable text — parses cleanly in ATS.
- Deep-blue accent (#1F4E79) headings with thin rules; Calibri (DOCX) / Helvetica (PDF).
- Bullets emphasize end-to-end ownership, rapid startup-speed delivery, and team
  collaboration, while keeping the whole resume to one page.
