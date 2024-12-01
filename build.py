"""
Скрипт для сборки финального документа.
"""

import os
import subprocess
import yaml


def combine_markdown_to_odt(md_files, output_file, template):
    combined_md = "combined.md"
    with open(combined_md, "w") as outfile:
        for fname in md_files:
            with open(fname) as infile:
                outfile.write(infile.read() + "\n\n")

    subprocess.run([
        "pandoc", combined_md, "-o", output_file, "--reference-doc", template, "--toc"
    ])
    os.remove(combined_md)

def build_document(structure_file, output_dir, template_file):
    with open(structure_file, "r") as file:
        structure = yaml.safe_load(file)

    output_files = []
    for part in structure["parts"]:
        if part["type"] == "text":
            md_files = part["files"]
            odt_file = os.path.join(output_dir, f"{part['name']}.odt")
            combine_markdown_to_odt(md_files, odt_file, template_file)
            output_files.append(odt_file)
        elif part["type"] == "cover":
            output_files.append(part["file"])
        elif part["type"] == "image":
            output_files.append(part["file"])

    # Объединяем части
    final_odt = os.path.join(output_dir, "final_document.odt")
    subprocess.run(["libreoffice", "--headless", "--convert-to", "odt"] + output_files + [final_odt])

    # Конвертируем ODT в PDF
    final_pdf = os.path.join(output_dir, "final_document.pdf")
    subprocess.run(["libreoffice", "--headless", "--convert-to", "pdf", final_odt])

    print(f"Documents generated: {final_odt}, {final_pdf}")

if __name__ == "__main__":
    STRUCTURE_FILE = "structure.yml"
    OUTPUT_DIR = "/output"
    TEMPLATE_FILE = "template.ott"

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    build_document(STRUCTURE_FILE, OUTPUT_DIR, TEMPLATE_FILE)
