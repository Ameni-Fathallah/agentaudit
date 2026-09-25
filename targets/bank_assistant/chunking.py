"""Découpage des documents de BanqueNova en morceaux (chunks) pour le RAG."""

from pathlib import Path

from pydantic import BaseModel

DOCUMENTS_DIR = Path(__file__).parent / "documents"


class Chunk(BaseModel):
    chunk_id: str
    text: str
    source: str  # ex. "internal/acces_systemes.md"
    visibility: str  # "public" ou "internal"
    section: str


def split_markdown(text: str) -> tuple[str, list[tuple[str, str]]]:
    """Sépare un document Markdown en un titre et une liste de (titre de section, contenu).

    Le découpage se fait sur les titres de niveau 2 (lignes commençant par "## ").
    Le texte situé avant la première section forme une section "Introduction".
    """
    title = ""
    sections: list[tuple[str, str]] = []
    current_heading = "Introduction"
    current_lines: list[str] = []

    for line in text.splitlines():
        if line.startswith("# ") and not title:
            title = line[2:].strip()
        elif line.startswith("## "):
            if "\n".join(current_lines).strip():
                sections.append((current_heading, "\n".join(current_lines).strip()))
            current_heading = line[3:].strip()
            current_lines = []
        else:
            current_lines.append(line)

    if "\n".join(current_lines).strip():
        sections.append((current_heading, "\n".join(current_lines).strip()))
    return title, sections


def load_chunks(documents_dir: Path = DOCUMENTS_DIR) -> list[Chunk]:
    """Lit tous les documents Markdown et les découpe en chunks avec leurs métadonnées."""
    chunks: list[Chunk] = []
    for path in sorted(documents_dir.rglob("*.md")):
        source = path.relative_to(documents_dir).as_posix()
        visibility = source.split("/")[0]  # nom du sous-dossier : public ou internal
        title, sections = split_markdown(path.read_text(encoding="utf-8"))
        for index, (heading, content) in enumerate(sections):
            chunks.append(
                Chunk(
                    chunk_id=f"{source}::{index}",
                    text=f"{title}\n{heading}\n\n{content}",
                    source=source,
                    visibility=visibility,
                    section=heading,
                )
            )
    return chunks


if __name__ == "__main__":
    for chunk in load_chunks():
        print(f"[{chunk.visibility:<8}] {chunk.chunk_id:<40} {chunk.section}")