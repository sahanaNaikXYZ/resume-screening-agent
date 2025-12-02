import os
import streamlit as st
from parsers import extract_text_from_file
from embeddings_client import get_embedding, demo_embed
from scorer import rank_resumes
from utils import load_demo_files

st.set_page_config(page_title="Resume Screening Agent", layout="wide")
st.title("Resume Screening Agent — Demo (VS Code)")

# Sidebar: API key
OPENAI_KEY = st.sidebar.text_input("OpenAI API Key (leave empty for demo)", type="password")
use_demo = not bool(OPENAI_KEY)
if OPENAI_KEY:
    os.environ["OPENAI_API_KEY"] = OPENAI_KEY

st.sidebar.markdown("Upload resumes (pdf/docx/txt) or use demo files.")
uploaded = st.file_uploader("Upload resumes (multiple)", accept_multiple_files=True)
jd_text = st.text_area("Paste Job Description (JD) here", height=200)
if st.button("Run Screening"):
    if use_demo:
        st.info("Running in DEMO mode (no OpenAI key). Using simple heuristics.")
        resumes = load_demo_files()
    else:
        resumes = []
        if not uploaded:
            st.error("Please upload resumes or run in demo mode.")
            st.stop()
        for f in uploaded:
            text = extract_text_from_file(f)
            resumes.append({"filename": f.name, "text": text})

    if not jd_text.strip():
        st.error("Please paste a job description.")
        st.stop()

    # Embed JD
    if use_demo:
        jd_emb = demo_embed(jd_text)
    else:
        jd_emb = get_embedding(jd_text)

    results = rank_resumes(jd_emb, resumes, use_demo=use_demo)
    st.success(f"Ranked {len(results)} resumes.")
    for r in results:
        st.header(f"{r['filename']} — Score: {r['score']:.1f}")
        st.write("**Top matched snippet:**")
        st.write(r["snippet"])
        st.write("**Rationale (short):**")
        st.write(r.get("rationale","(demo)"))
        st.markdown("---")
