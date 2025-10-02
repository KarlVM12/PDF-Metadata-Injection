#!/usr/bin/env python3
# add_pdf_metadata.py
# Adds/updates PDF metadata fields (Title, Author, Subject, Keywords) via CLI.

import argparse
from PyPDF2 import PdfReader, PdfWriter
from pathlib import Path
import sys

def load_keywords(args) -> str:
    if args.keywords is not None:
        return args.keywords
    if args.keywords_file is not None:
        text = Path(args.keywords_file).read_text(encoding="utf-8")
        # Accept either comma- or newline-separated keywords
        parts = [p.strip() for p in text.replace("\n", ",").split(",") if p.strip()]
        return ", ".join(parts)
    return None

def main():
    parser = argparse.ArgumentParser(
        description="Add or update PDF metadata (Title, Author, Subject, Keywords)."
    )
    parser.add_argument("input_pdf", help="Path to the source PDF (e.g., resume.pdf)")
    parser.add_argument("output_pdf", help="Path to write the updated PDF")
    parser.add_argument("--title", help="Document Title", default=None)
    parser.add_argument("--author", help="Document Author", default=None)
    parser.add_argument("--subject", help="Document Subject", default=None)
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--keywords", help="Comma-separated keywords", default=None)
    group.add_argument("--keywords-file", help="Text file containing keywords (comma or newline separated)", default=None)
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Allow writing output_pdf even if it already exists"
    )
    args = parser.parse_args()

    out_path = Path(args.output_pdf)
    if out_path.exists() and not args.overwrite:
        print(f"Error: {out_path} already exists. Use --overwrite to replace it.", file=sys.stderr)
        sys.exit(2)

    # Read input
    reader = PdfReader(args.input_pdf)
    writer = PdfWriter()

    for page in reader.pages:
        writer.add_page(page)

    # Start with existing metadata if present
    md = dict(reader.metadata or {})

    # Normalize keys to standard PDF Info keys
    def set_if(value, key):
        if value is not None:
            md[f"/{key}"] = value

    set_if(args.title, "Title")
    set_if(args.author, "Author")
    set_if(args.subject, "Subject")
    kw = load_keywords(args)
    set_if(kw, "Keywords")

    # Apply updated metadata
    writer.add_metadata(md)

    with open(out_path, "wb") as f:
        writer.write(f)

    print("Updated metadata written to:", out_path)
    print("Summary:")
    print("  Title   :", md.get("/Title"))
    print("  Author  :", md.get("/Author"))
    print("  Subject :", md.get("/Subject"))
    print("  Keywords:", md.get("/Keywords"))

if __name__ == "__main__":
    main()

