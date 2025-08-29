import gradio as gr
import pandas as pd
import json
from src.ocr_extract import extract_from_file

def process(file):
    if file is None:
        return "No file", None, None
    with open(file.name, "rb") as f:
        data = f.read()
    result = extract_from_file(data, file.name)
    df = pd.DataFrame([result["fields"]])
    return json.dumps(result["fields"], indent=2), df, json.dumps(result, indent=2)

with gr.Blocks(title="Invoice OCR") as demo:
    gr.Markdown("# 🧾 Invoice OCR Extractor")
    inp = gr.File(label="Upload PDF/Image")
    fields = gr.Code(label="Extracted Fields (JSON)")
    table = gr.Dataframe(label="Fields Table")
    full = gr.Code(label="Full Result JSON")
    inp.change(process, inputs=inp, outputs=[fields, table, full])

if __name__ == "__main__":
    demo.launch()
