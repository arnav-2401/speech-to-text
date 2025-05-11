from llama_cpp import Llama

# ── model ──────────────────────────────────────────────────────────────────────
model = Llama.from_pretrained(
    repo_id  = "bartowski/gemma-2-2b-it-GGUF",
    filename = "gemma-2-2b-it-IQ4_XS.gguf",
    n_threads = 4,
    n_ctx     = 8192,   # one-pass window
    verbose   = False,
)

SENTINEL      = "<|END|>"
MAX_SUMMARY_T = 1024
PROMPT_PREFIX = "Please summarize the following lecture transcription:\n\n"


# ── single-pass summariser ─────────────────────────────────────────────────────
def summarize_text(text: str) -> str:
    prompt = f"{PROMPT_PREFIX}{text}\n\n{SENTINEL}"
    out = model.create_completion(
        prompt      = prompt,
        max_tokens  = MAX_SUMMARY_T,
        temperature = 0.7,
        stop        = [SENTINEL],
    )
    return out["choices"][0]["text"].strip()


def summarize(input_path: str, output_path: str) -> str:
    with open(input_path, encoding="utf-8") as f:
        transcript = f.read()

    summary = summarize_text(transcript)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(summary)

    return summary


# ── cli ────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    input_file  = "transcriptions/test1.txt"
    output_file = "summary.txt"
    summarize(input_file, output_file)