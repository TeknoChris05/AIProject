"""
phishing_detector.py  —  Core LLM engine using local Ollama.
No API key, no internet required. Runs 100% offline.

Prerequisites:
    ollama serve          (keep running in a terminal)
    ollama pull llama3.2  (one-time ~2GB download)
"""

import json, re, time, requests

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL      = "llama3.2"   # swap to "mistral" or "llama3.1" if preferred
STRATEGIES = ["zero_shot", "few_shot", "chain_of_thought"]


def _build_prompt(email_text: str, strategy: str) -> str:
    if strategy == "zero_shot":
        return (
            'You are a cybersecurity expert. Classify the following email '
            'as either "phishing" or "legitimate".\n\n'
            f"Email:\n{email_text}\n\n"
            "Respond with ONLY a valid JSON object, nothing else:\n"
            '{"classification": "phishing", "confidence": 0.95}'
        )

    elif strategy == "few_shot":
        examples = """
EXAMPLE 1:
Email: "URGENT: Your account has been compromised! Click here: http://secure-bank-verify.xyz"
Answer: {"classification": "phishing", "confidence": 0.98}

EXAMPLE 2:
Email: "Hi John, confirming our meeting tomorrow at 3pm. See attached agenda. - Sarah"
Answer: {"classification": "legitimate", "confidence": 0.97}

EXAMPLE 3:
Email: "You won $1,000,000! Send bank details to lottery.prize99@gmail.com to claim."
Answer: {"classification": "phishing", "confidence": 0.99}

EXAMPLE 4:
Email: "Your Lisinopril 10mg prescription is ready for pickup at CVS. Hours: 9am-9pm."
Answer: {"classification": "legitimate", "confidence": 0.96}
"""
        return (
            'You are a cybersecurity expert. Classify emails as "phishing" or "legitimate".\n'
            + examples
            + f"\nNow classify this email:\n{email_text}\n\n"
            'Respond with ONLY a valid JSON object:\n{"classification": "...", "confidence": 0.0}'
        )

    elif strategy == "chain_of_thought":
        return (
            "You are a cybersecurity expert. Analyze this email step-by-step:\n\n"
            "Step 1 - Sender legitimacy: Does the sender look authentic?\n"
            "Step 2 - Urgency/fear tactics: Does it create artificial urgency?\n"
            "Step 3 - Suspicious URLs: Are there spoofed or unusual links?\n"
            "Step 4 - Sensitive data requests: Passwords, SSN, credit cards?\n"
            "Step 5 - Grammar/professionalism: Is the writing professional?\n\n"
            f"Email:\n{email_text}\n\n"
            "After your analysis, end with ONLY this JSON on the last line:\n"
            '{"classification": "phishing", "confidence": 0.95, "reasoning": "one sentence"}'
        )
    else:
        raise ValueError(f"Unknown strategy: {strategy!r}. Choose from {STRATEGIES}")


def classify_email(email_text: str, strategy: str, retries: int = 3) -> dict:
    prompt = _build_prompt(email_text, strategy)
    payload = {
        "model":    MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "stream":   False,
        "format":   "json",          # ← ADD THIS LINE — forces Ollama to output valid JSON
        "options":  {"temperature": 0.1, "num_predict": 400},
    }

    for attempt in range(retries):
        try:
            resp = requests.post(OLLAMA_URL, json=payload, timeout=120)
            resp.raise_for_status()
            raw = resp.json()["message"]["content"].strip()

            json_match = re.search(r'\{[^{}]+\}', raw, re.DOTALL)
            if not json_match:
                raise ValueError(f"No JSON found in response:\n{raw[:200]}")

            result = json.loads(json_match.group())
            classification = result.get("classification", "").lower().strip()
            if classification not in ("phishing", "legitimate"):
                raise ValueError(f"Unexpected label: {classification!r}")

            return {
                "classification": classification,
                "confidence":     float(result.get("confidence", 0.5)),
                "reasoning":      result.get("reasoning", ""),
                "strategy":       strategy,
                "raw_response":   raw,
            }

        except requests.ConnectionError:
            print("\n  [ERROR] Cannot connect to Ollama. Run: ollama serve\n")
            raise
        except Exception as e:
            if attempt < retries - 1:
                wait = 2 ** attempt
                print(f"  [Retry {attempt+1}] {e}. Waiting {wait}s...")
                time.sleep(wait)
            else:
                return {"classification": "error", "confidence": 0.0,
                        "reasoning": str(e), "strategy": strategy, "raw_response": ""}