from pathlib import Path
def load_demo_files():
    demo_dir = Path("sample_data/resumes")
    resumes = []
    for f in demo_dir.glob("*"):
        try:
            text = f.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            text = ""
        resumes.append({"filename": f.name, "text": text})
    return resumes
