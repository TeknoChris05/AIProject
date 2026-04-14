# PhishSense - An AI-Powered Phishing Detector

# Overview
Phishing emails are the #1 cause of cybersecurity breaches - over 80% of attacks start with one. Traditional spam filters use keyword matching, which attackers can easily bypass. Using an AI-Powered Model helps our phishing mitigation strategies work more intelligently, and you more secure.

PhishSense understands **intent**, not just keywords. This pushes the limit of what can be understood about not only the emails themselves,but also the attackers behind them.

# Our Model
PhishSense utilizes Llama 3.2 via Ollama. This runs completely offline on the user's machine, so that data is unable to leave and cause potential security violations.

Our model is tested with 3 different prompting strategies, each giving a varying amount of prior information for the model to work with.

**Zero-Shot** - Ask the model to classify without hints

**Few-Shot** - Give the model 4 examples before testing

**Chain-of-Thought** - Make the model reason step-by-step through 5 indicators before answering

This not only tests our model's ability to detect phishing emails, but also showcases which strategy works best.

Our model evaluates its results through 4 measured classifcation metrics.

**Accuracy** - What percentage did it get right overall

**Precision** - Of the ones it called phishing, how many actually were

**Recall** - Of all the actual phishing emails, how many did it catch

**F1 Score** - A combined score that balances precision and recall.

# How to Run
### 1. Install Ollama
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

### 2. Pull the Llama 3.2 model (one-time, ~2GB)
```bash
ollama pull llama3.2
```

### 3. Start Ollama (keep this terminal open)
```bash
ollama serve
```

### 4. Create a Python virtual environment
```bash
cd "/home/christopher/Documents/Artifical Intelligence Class/AIProject"
python3 -m venv venv
source venv/bin/activate
```

### 5. Install dependencies
```bash
pip install -r requirements.txt
```

### 6. Generate the dataset
```bash
python3 create_dataset.py
```

---

## Running the Project

### Full evaluation — all 3 strategies on 30 emails
```bash
python3 evaluate.py
```
Results saved to `results/`:
- `summary_metrics.csv` — accuracy, precision, recall, F1 per strategy
- `evaluation_results.png` — bar charts and confusion matrices
- `*_results.csv` — per-email predictions for each strategy

### Interactive live demo
```bash
python3 demo.py
```
Paste any email text, press Enter twice, and the model classifies it using
all three strategies in real time.

---

## Dataset

`data/sample_emails.csv` — 30 hand-curated labeled emails:

- **15 phishing**: bank fraud, credential harvesting, prize scams, fake IT alerts,
  spoofed delivery notices, IRS impersonation, crypto scams
- **15 legitimate**: meeting reminders, order confirmations, appointment reminders,
  GitHub notifications, course announcements, pharmacy notifications
