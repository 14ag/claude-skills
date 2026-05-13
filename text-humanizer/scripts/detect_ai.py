import sys
import argparse
import torch
import warnings
from transformers import BertTokenizer, BertForSequenceClassification

def main():
    """
    Evaluate text for AI vs human authorship using followsci/bert-ai-text-detector.
    Exits with code 0 (human), 1 (error), or 2 (AI).
    NOTE: The model accepts a maximum of 512 tokens. Long inputs are truncated silently
    by the tokenizer; this function emits a warning to stderr when that happens.
    """
    # Suppress warnings for cleaner CLI output
    warnings.filterwarnings('ignore')
    
    parser = argparse.ArgumentParser(description="AI Text Detector")
    parser.add_argument("--file", type=str, help="Path to text file to evaluate")
    parser.add_argument("--text", type=str, help="Text string to evaluate directly")
    args = parser.parse_args()

    if args.file:
        try:
            with open(args.file, 'r', encoding='utf-8') as f:
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

    # Use sys.stderr for loading messages so they don't pollute pipelined scripts
    print("Loading followsci/bert-ai-text-detector model...", file=sys.stderr)
    model_name = "followsci/bert-ai-text-detector"
    try:
        tokenizer = BertTokenizer.from_pretrained(model_name)
        model = BertForSequenceClassification.from_pretrained(model_name)
    except Exception as e:
        print(f"Error loading model: {e}", file=sys.stderr)
        print("Please ensure transformers and torch are installed: pip install transformers torch", file=sys.stderr)
        sys.exit(1)
        
    model.eval()

    # Warn when input exceeds the model's 512-token limit. Longer texts are truncated
    # to the first ~380 words, so results only reflect the opening of the document.
    token_count = len(tokenizer.encode(text, add_special_tokens=True))
    if token_count > 512:
        print(
            f"WARNING: Input is {token_count} tokens. The model truncates at 512 tokens. "
            "Results reflect only the first ~380 words of your text. "
            "For long documents, run the script on representative excerpts.",
            file=sys.stderr,
        )

    # The BERT model has a max length of 512 tokens.
    inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=512)


    with torch.no_grad():
        outputs = model(**inputs)
        probs = torch.nn.functional.softmax(outputs.logits, dim=-1)
        # Class 1 = AI, Class 0 = Human
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
        # Exit with code 2 if it's likely AI, so scripts can catch it easily
        sys.exit(2)
    else:
        print("STATUS: LIKELY HUMAN-WRITTEN")
        sys.exit(0)

if __name__ == "__main__":
    main()
