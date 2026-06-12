#!/usr/bin/env python3
import json
import re
from pathlib import Path

BASE = Path(__file__).resolve().parent
JSONDIR = (BASE / "../JSON").resolve()
OUTDIR = BASE / "generated"

FILES = {
    "papers": JSONDIR / "papers.json",
    "pres_int": JSONDIR / "pres_int.json",
    "pres_pos": JSONDIR / "pres_pos.json",
    "pres_jap": JSONDIR / "pres_jap.json",
    "seminars": JSONDIR / "seminars.json",
}


MONTHS = {
    "jan": 1, "january": 1,
    "feb": 2, "february": 2,
    "mar": 3, "march": 3,
    "apr": 4, "april": 4,
    "may": 5,
    "jun": 6, "june": 6,
    "jul": 7, "july": 7,
    "aug": 8, "august": 8,
    "sep": 9, "sept": 9, "september": 9,
    "oct": 10, "october": 10,
    "nov": 11, "november": 11,
    "dec": 12, "december": 12,
}


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def ensure_outdir():
    OUTDIR.mkdir(parents=True, exist_ok=True)


def tex_escape(text):
    if text is None:
        return ""
    text = str(text)

    replacements = {
        "\\": r"\textbackslash{}",
        "&": r"\&",
        "%": r"\%",
        "$": r"\$",
        "#": r"\#",
        "_": r"\_",
        "{": r"\{",
        "}": r"\}",
        "~": r"\textasciitilde{}",
        "^": r"\textasciicircum{}",
    }
    for k, v in replacements.items():
        text = text.replace(k, v)

    text = text.replace("–", "--")
    text = text.replace("—", "---")
    text = text.replace("’", "'")
    text = text.replace("“", "``")
    text = text.replace("”", "''")
    text = text.replace("Jožef", r"Jo\v{z}ef")

    return text


def title_to_tex(text):
    if text is None:
        return ""
    text = text.strip()

    text = text.replace("UV Compeletions", "UV Completions")
    text = text.replace("Tmumu", r"$T^{\mu}_{~\mu}$")
    text = text.replace("η", r"$\eta$")
    text = text.replace("with A Dark Photon Portal", "with a Dark Photon Portal")

    return tex_escape(text)


def normalize_space(text):
    return re.sub(r"\s+", " ", text or "").strip()


def extract_year(text):
    if not text:
        return 0
    m = re.search(r"(20\d{2}|19\d{2})", text)
    return int(m.group(1)) if m else 0


def parse_date_key(text):
    """
    Rough parser for many date formats in the JSON.
    Returns tuple sortable newest-first by reverse sort.
    """
    if not text:
        return (0, 0, 0)

    s = text.strip().lower()
    s = s.replace(".", "")
    s = s.replace("–", "-")
    s = s.replace("—", "-")

    year = extract_year(s)

    month = 1
    day = 1

    for token in re.split(r"[,\s\-]+", s):
        if token in MONTHS:
            month = MONTHS[token]
            break

    nums = re.findall(r"\b(\d{1,2})\b", s)
    if nums:
        try:
            first_num = int(nums[0])
            if 1 <= first_num <= 31:
                day = first_num
        except ValueError:
            pass

    if re.match(r"^\d{1,2}\s", s):
        try:
            day = int(re.match(r"^(\d{1,2})\s", s).group(1))
        except Exception:
            pass

    return (year, month, day)


def infer_invited(conference):
    if not conference:
        return False
    return "invited" in conference.lower()


def infer_selected_talk(talk):
    year = extract_year(talk.get("date", ""))
    conf = talk.get("conference", "")
    if infer_invited(conf):
        return True
    return year >= 2023


def infer_selected_paper(paper):
    year = extract_year(paper.get("journal", "") or paper.get("arxiv", ""))
    title = (paper.get("title") or "").lower()

    if year >= 2022:
        return True

    if "threshold corrections to baryon number violating operators" in title:
        return True

    if paper.get("inspire") == "1705053":
        return True

    return False


def paper_status(paper):
    journal = (paper.get("journal") or "").strip()
    if journal:
        return "published"
    return "preprint"


def authors_display_to_tex(authors_display):
    if not authors_display:
        return r"\textbf{Takumi Kuwahara}"

    s = authors_display.strip()
    if s.lower().startswith("with "):
        s = s[5:].strip()

    s = tex_escape(s)
    return r"\textbf{Takumi Kuwahara} with " + s


def render_publication_item(paper):
    authors = authors_display_to_tex(paper.get("authors", ""))
    title = title_to_tex(paper.get("title", ""))
    journal = tex_escape((paper.get("journal") or "").strip())
    arxiv = (paper.get("arxiv") or "").strip()
    inspire = (paper.get("inspire") or "").strip()

    venue = journal if journal else "Preprint"

    links = []
    if arxiv:
        links.append(r"\arXiv{" + tex_escape(arxiv) + "}")
    if inspire:
        links.append(
            r"\href{https://inspirehep.net/literature/" + tex_escape(inspire) + r"}{INSPIRE}"
        )

    links_str = "; ".join(links)

    return (
        "\\pubentry\n"
        f"  {{{authors}}}\n"
        f"  {{{title}}}\n"
        f"  {{{venue}}}\n"
        f"  {{{links_str}}}\n"
    )


def render_talk_item(item, note_override=None):
    title = title_to_tex(item.get("title", ""))
    conference = normalize_space(item.get("conference", ""))
    place = normalize_space(item.get("place", ""))
    date = normalize_space(item.get("date", ""))

    note = note_override or ""
    if infer_invited(conference):
        note = "Invited talk" if not note else note

    conference = re.sub(r"\s*\(invited\)\s*", "", conference, flags=re.I).strip()

    return (
        "\\talkentry\n"
        f"  {{{title}}}\n"
        f"  {{{tex_escape(conference)}}}\n"
        f"  {{{tex_escape(place)}}}\n"
        f"  {{{tex_escape(date)}}}\n"
        f"  {{{tex_escape(note)}}}\n"
    )


def render_seminar_item(item):
    title = title_to_tex(item.get("title", ""))
    place = normalize_space(item.get("place", ""))
    date = normalize_space(item.get("date", ""))
    sem_type = normalize_space(item.get("type", ""))

    note = sem_type if sem_type and sem_type.lower() != "seminar" else ""

    return (
        "\\talkentry\n"
        f"  {{{title}}}\n"
        f"  {{{tex_escape(place)}}}\n"
        f"  {{{tex_escape(place)}}}\n"
        f"  {{{tex_escape(date)}}}\n"
        f"  {{{tex_escape(note)}}}\n"
    )


def write_selected_publications(papers):
    selected = [p for p in papers if infer_selected_paper(p)]
    selected.sort(
        key=lambda p: extract_year((p.get("journal") or "") + " " + (p.get("arxiv") or "")),
        reverse=True,
    )

    content = ["\\begin{publist}", ""]
    for p in selected:
        content.append(render_publication_item(p).rstrip())
        content.append("")
    content.append("\\end{publist}")

    (OUTDIR / "selected_publications.tex").write_text(
        "\n".join(content) + "\n", encoding="utf-8"
    )


def write_full_publications(papers):
    published = [p for p in papers if paper_status(p) == "published"]
    preprints = [p for p in papers if paper_status(p) != "published"]

    published.sort(
        key=lambda p: extract_year((p.get("journal") or "") + " " + (p.get("arxiv") or "")),
        reverse=True,
    )
    preprints.sort(
        key=lambda p: extract_year((p.get("journal") or "") + " " + (p.get("arxiv") or "")),
        reverse=True,
    )

    content = []

    if preprints:
        content.append(r"\cvsubsection{Preprints}")
        content.append("")
        content.append(r"\begin{publist}")
        content.append("")
        for p in preprints:
            content.append(render_publication_item(p).rstrip())
            content.append("")
        content.append(r"\end{publist}")
        content.append("")

    if published:
        content.append(r"\cvsubsection{Peer-Reviewed Publications}")
        content.append("")
        content.append(r"\begin{publist}")
        content.append("")
        for p in published:
            content.append(render_publication_item(p).rstrip())
            content.append("")
        content.append(r"\end{publist}")
        content.append("")

    (OUTDIR / "full_publications.tex").write_text(
        "\n".join(content).rstrip() + "\n", encoding="utf-8"
    )


def write_selected_talks(pres_int):
    selected = [t for t in pres_int if infer_selected_talk(t)]
    selected.sort(key=lambda t: parse_date_key(t.get("date", "")), reverse=True)
    selected = selected[:8]

    content = ["\\begin{talklist}", ""]
    for t in selected:
        content.append(render_talk_item(t).rstrip())
        content.append("")
    content.append("\\end{talklist}")

    (OUTDIR / "selected_talks.tex").write_text(
        "\n".join(content) + "\n", encoding="utf-8"
    )


def write_full_talks(pres_int):
    pres_int = sorted(pres_int, key=lambda t: parse_date_key(t.get("date", "")), reverse=True)

    content = ["\\begin{talklist}", ""]
    for t in pres_int:
        content.append(render_talk_item(t).rstrip())
        content.append("")
    content.append("\\end{talklist}")

    (OUTDIR / "full_talks.tex").write_text(
        "\n".join(content) + "\n", encoding="utf-8"
    )


def write_poster_presentations(pres_pos):
    pres_pos = sorted(pres_pos, key=lambda t: parse_date_key(t.get("date", "")), reverse=True)

    content = ["\\begin{talklist}", ""]
    for t in pres_pos:
        content.append(render_talk_item(t, note_override="Poster").rstrip())
        content.append("")
    content.append("\\end{talklist}")

    (OUTDIR / "poster_presentations.tex").write_text(
        "\n".join(content) + "\n", encoding="utf-8"
    )


def write_domestic_presentations_japan(pres_jap):
    pres_jap = sorted(pres_jap, key=lambda t: parse_date_key(t.get("date", "")), reverse=True)

    content = ["\\begin{talklist}", ""]
    for t in pres_jap:
        content.append(render_talk_item(t).rstrip())
        content.append("")
    content.append("\\end{talklist}")

    (OUTDIR / "domestic_presentations_japan.tex").write_text(
        "\n".join(content) + "\n", encoding="utf-8"
    )


def write_seminars(seminars):
    seminars = sorted(seminars, key=lambda t: parse_date_key(t.get("date", "")), reverse=True)

    content = ["\\begin{talklist}", ""]
    for s in seminars:
        content.append(render_seminar_item(s).rstrip())
        content.append("")
    content.append("\\end{talklist}")

    (OUTDIR / "seminars.tex").write_text(
        "\n".join(content) + "\n", encoding="utf-8"
    )


def main():
    ensure_outdir()

    missing = [str(path) for path in FILES.values() if not path.exists()]
    if missing:
        raise FileNotFoundError(
            "Missing required input file(s):\n  " + "\n  ".join(missing)
        )

    papers = load_json(FILES["papers"])
    pres_int = load_json(FILES["pres_int"])
    pres_pos = load_json(FILES["pres_pos"])
    pres_jap = load_json(FILES["pres_jap"])
    seminars = load_json(FILES["seminars"])

    write_selected_publications(papers)
    write_full_publications(papers)
    write_selected_talks(pres_int)
    write_full_talks(pres_int)
    write_poster_presentations(pres_pos)
    write_domestic_presentations_japan(pres_jap)
    write_seminars(seminars)

    print(f"Loaded JSON from: {JSONDIR}")
    print(f"Generated TeX snippets in: {OUTDIR}")


if __name__ == "__main__":
    main()