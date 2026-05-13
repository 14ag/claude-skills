"""
AI Text Detector — followsci/bert-ai-text-detector + stylometric supplementary metrics.

Exit codes:
  0 = LIKELY HUMAN (AI probability <= 50%)
  1 = ERROR
  2 = LIKELY AI (AI probability > 50%)

Supplementary metrics (rule-based, no model required):
  - Burstiness: standard deviation of sentence word counts. Low (<4.0) = AI signal.
  - Nominal loading: noun+adjective share of content words. High (>60%) = AI signal.
  - Overt conjunctive framing: count of SHAP-flagged transition phrases.
  - Contraction density: fraction of sentences with at least one contraction.

These do not affect the exit code or the primary AI/human verdict. They appear in the
output as actionable guidance for the iteration step. Use --no-model to run only the
stylometric metrics without loading the BERT model.
"""
import sys
import re
import argparse
import warnings
import statistics

OVERT_CONJUNCTIVES = [
    "in conclusion",
    "to summarize",
    "to wrap up",
    "it is important to note",
    "it is worth noting",
    "it is worth mentioning",
    "furthermore,",
    "moreover,",
    "this highlights the importance of",
    "it should be noted that",
    "this underscores the need for",
    "this underscores the importance of",
    "needless to say",
    "last but not least",
    "this is a testament to",
    "at the end of the day",
    "moving forward,",
    "in this section, we will",
    "in summary,",
]

CONTRACTIONS = [
    "don't", "doesn't", "didn't", "won't", "wouldn't", "can't", "couldn't",
    "isn't", "aren't", "wasn't", "weren't", "it's", "that's", "there's",
    "we're", "they're", "you're", "he's", "she's", "i've", "we've",
    "they've", "you've", "i'd", "we'd", "they'd", "you'd", "i'll", "we'll",
    "they'll", "you'll", "shouldn't", "mustn't", "hadn't", "haven't",
    "i'm", "let's",
]

DETERMINERS = {"the", "a", "an", "this", "that", "these", "those", "my", "your",
               "his", "her", "its", "our", "their"}
PRONOUNS = {"i", "me", "we", "us", "you", "he", "him", "she", "her", "it",
            "they", "them", "who", "whom", "which", "that"}
AUXILIARIES = {"is", "are", "was", "were", "be", "been", "being", "have", "has",
               "had", "do", "does", "did", "will", "would", "shall", "should",
               "may", "might", "must", "can", "could", "ought"}
PREPOSITIONS = {"in", "on", "at", "for", "to", "of", "with", "from", "by",
                "about", "as", "into", "through", "during", "before", "after",
                "above", "below", "between", "among", "under", "over"}
CONJUNCTIONS = {"and", "or", "but", "so", "yet", "nor", "for", "although",
                "because", "since", "while", "if", "unless", "until", "when",
                "where", "though", "after", "before", "as"}
ALL_FUNCTION = DETERMINERS | PRONOUNS | AUXILIARIES | PREPOSITIONS | CONJUNCTIONS

KNOWN_ADJECTIVES = {"new", "old", "good", "bad", "large", "small", "high", "low",
                    "long", "short", "important", "different", "early", "late",
                    "great", "little", "own", "right", "big", "real", "best",
                    "free", "last", "next", "open", "public", "strong", "true",
                    "full", "clear", "hard", "easy", "specific", "certain",
                    "key", "main", "major", "significant", "critical", "central",
                    "robust", "effective", "efficient", "complex", "simple",
                    "multiple", "various", "several", "current", "recent",
                    "crucial", "pivotal", "vibrant", "intricate", "valuable",
                    "meticulous", "comprehensive", "seamless", "innovative",
                    "advanced", "enhanced", "improved", "integrated", "dynamic",
                    "strategic", "unique", "diverse", "global", "local"}


def split_sentences(text):
    text = text.strip()
    sentences = re.split(r'(?<=[.!?])\s+', text)
    return [s.strip() for s in sentences if s.strip()]


def word_count(sentence):
    return len(sentence.split())


def compute_burstiness(sentences):
    if len(sentences) < 3:
        return -1.0
    lengths = [word_count(s) for s in sentences]
    return round(statistics.stdev(lengths), 2)


def compute_nominal_loading(text):
    words = re.findall(r"[a-z']+", text.lower())
    content_words = [w for w in words if w not in ALL_FUNCTION and len(w) > 2]
    if not content_words:
        return -1.0
    noun_adj_count = 0
    for w in content_words:
        if w in KNOWN_ADJECTIVES:
            noun_adj_count += 1
        elif (w.endswith(("tion", "sion", "ment", "ness", "ity", "ism", "ist",
                          "ance", "ence", "ship", "hood", "ure", "age"))
              and len(w) > 5):
            noun_adj_count += 1
    return round(noun_adj_count / len(content_words), 3)


def count_overt_conjunctives(text):
    lower = text.lower()
    return [phrase for phrase in OVERT_CONJUNCTIVES if phrase in lower]


def compute_contraction_density(sentences):
    if not sentences:
        return 0.0
    hits = sum(1 for s in sentences if any(c in s.lower() for c in CONTRACTIONS))
    return round(hits / len(sentences), 3)


def print_stylometric_report(text, sentences):
    burstiness = compute_burstiness(sentences)
    nominal = compute_nominal_loading(text)
    conjunctives = count_overt_conjunctives(text)
    contraction_density = compute_contraction_density(sentences)

    print()
    print("STYLOMETRIC SUPPLEMENTARY METRICS")
    print("-" * 30)

    if burstiness < 0:
        burst_note = "insufficient sentences to measure"
    elif burstiness < 4.0:
        burst_note = "LOW — add more sentence length variation (short 5-8 word sentences)"
    elif burstiness < 7.0:
        burst_note = "MODERATE — acceptable; aim higher for longer documents"
    else:
        burst_note = "HIGH — good human-like variance"
    bval = f"{burstiness:.2f}" if burstiness >= 0 else "N/A"
    print(f"Burstiness (sentence length stdev): {bval}")
    print(f"  -> {burst_note}")

    if nominal < 0:
        nom_note = "insufficient content words"
    elif nominal > 0.60:
        nom_note = "HIGH — add pronouns (it, they, this), auxiliary verbs, contractions"
    elif nominal > 0.45:
        nom_note = "MODERATE — watch for further accumulation"
    else:
        nom_note = "OK — good function/content word balance"
    nval = f"{nominal:.1%}" if nominal >= 0 else "N/A"
    print(f"Nominal loading (noun+adj ratio):   {nval}")
    print(f"  -> {nom_note}")

    if conjunctives:
        print(f"Overt conjunctives found ({len(conjunctives)}): {', '.join(repr(p) for p in conjunctives)}")
        print("  -> HIGH classifier signal: remove or restructure these phrases")
    else:
        print("Overt conjunctives found: none")
        print("  -> OK")

    if len(sentences) >= 5:
        if contraction_density < 0.10:
            cont_note = "LOW — add contractions for informal/moderate registers"
        else:
            cont_note = "OK"
        print(f"Contraction density: {contraction_density:.1%} of sentences")
        print(f"  -> {cont_note}")
    else:
        print("Contraction density: insufficient sentences to evaluate")

    print("-" * 30)


def main():
    """
    Evaluate text for AI vs human authorship using followsci/bert-ai-text-detector.
    Exits with code 0 (human), 1 (error), or 2 (AI).
    NOTE: The model accepts a maximum of 512 tokens. Long inputs are truncated silently
    by the tokenizer; this function emits a warning to stderr when that happens.
    """
    warnings.filterwarnings("ignore")

    parser = argparse.ArgumentParser(
        description="AI Text Detector with stylometric supplementary metrics"
    )
    parser.add_argument("--file", type=str, help="Path to text file to evaluate")
    parser.add_argument("--text", type=str, help="Text string to evaluate directly")
    parser.add_argument(
        "--no-model", action="store_true",
        help="Skip BERT model; run stylometric metrics only (always exits 0)"
    )
    args = parser.parse_args()

    if args.file:
        try:
            with open(args.file, "r", encoding="utf-8") as f:
                text = f.read()
        except FileNotFoundError:
            print(f"Error: File '{args.file}' not found.")
            sys.exit(1)
    elif args.text:
        text = args.text
    else:
        print("Error: Must provide --file or --text argument.")
        sys.exit(1)

    if not text.strip():
        print("Error: Empty text provided.")
        sys.exit(1)

    sentences = split_sentences(text)

    if args.no_model:
        print("Mode: stylometric metrics only (--no-model)")
        print_stylometric_report(text, sentences)
        sys.exit(0)

    try:
        import torch
        from transformers import BertTokenizer, BertForSequenceClassification
    except ImportError:
        print("Error: torch and transformers are required for model inference.")
        print("Install: pip install torch transformers")
        print("Or use --no-model for stylometric metrics only.")
        sys.exit(1)

    print("Loading followsci/bert-ai-text-detector model...", file=sys.stderr)
    model_name = "followsci/bert-ai-text-detector"
    try:
        tokenizer = BertTokenizer.from_pretrained(model_name)
        model = BertForSequenceClassification.from_pretrained(model_name)
    except Exception as e:
        print(f"Error loading model: {e}", file=sys.stderr)
        print("Ensure transformers and torch are installed: pip install transformers torch",
              file=sys.stderr)
        sys.exit(1)

    model.eval()

    token_count = len(tokenizer.encode(text, add_special_tokens=True))
    if token_count > 512:
        print(
            f"WARNING: Input is {token_count} tokens. The model truncates at 512 tokens. "
            "Results reflect only the first ~380 words. "
            "For long documents, run on representative excerpts.",
            file=sys.stderr,
        )

    inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=512)

    with torch.no_grad():
        outputs = model(**inputs)
        probs = torch.nn.functional.softmax(outputs.logits, dim=-1)
        ai_prob = probs[0][1].item() * 100
        human_prob = probs[0][0].item() * 100

    print("-" * 30)
    print("AI PROBABILITY SCORE")
    print("-" * 30)
    print(f"AI-Generated:  {ai_prob:.2f}%")
    print(f"Human-Written: {human_prob:.2f}%")
    print("-" * 30)

    if ai_prob > 50:
        print("STATUS: LIKELY AI-GENERATED")
    else:
        print("STATUS: LIKELY HUMAN-WRITTEN")

    print_stylometric_report(text, sentences)

    sys.exit(2 if ai_prob > 50 else 0)


if __name__ == "__main__":
    main()
