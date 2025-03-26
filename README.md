# vatrix
![Python](https://img.shields.io/badge/python-3.9-blue)  ![License](https://img.shields.io/badge/license-MIT-green) [![Last Commit](https://img.shields.io/github/last-commit/brianbatesactual/vatrix)](https://github.com/brianbatesactual/vatrix) [![Stars](https://img.shields.io/github/stars/brianbatesactual/vatrix?style=social)](https://github.com/brianbatesactual/vatrix)


# 🧠 Vatrix

**Vatrix** is a command-line tool for processing SAP log data, rendering natural language descriptions using Jinja2 templates, injecting augmented data, and generating training pairs for fine-tuning Sentence Transformers (SBERT).

---

## ✨ Features

- CLI-powered processing of SAP logs
- Modular template system powered by Jinja2
- SBERT data generation and similarity scoring
- Supports file mode, stream mode, and CLI flags
- Exports training pairs to CSV
- Exports highly similar sentence pairs for SBERT fine-tuning
- Flexible and colorful logging with log rotation

---

## 📦 Installation

```bash
pip install vatrix
```
Or install the latest from source:

```bash
git clone https://github.com/brianbatesactual/vatrix.git
cd vatrix
make setup
```
---

## 🛠️ Usage
```bash
vatrix --mode file \
       --render-mode all \
       --input data/input_logs.json \
       --output data/processed_logs.csv \
       --unmatched data/unmatched_logs.json \
       --generate-sbert-data \
       --log-level DEBUG \
       --log-file logs/vatrix_debug.log
```
Makefile Commands
```bash
make setup         # Create venv and install dependencies
make run           # Run log processor on default file
make stream        # Start reading NDJSON from stdin
make retrain       # Export SBERT sentence pairs
make freeze        # Regenerate requirements.txt
make clean         # Clean environment and build artifacts
make nuke          # Full reset of the project environment
```
---

## 🧠 Example

---

## 🧪 Testing
```bash
make test
```
---

## 📁 Logs

All logs are saved to the logs/ directory with daily rotation.

---

## 🧼 Cleanup
```bash
make clean    # Clean temp data
make nuke     # Wipe and rebuild virtualenv
```
---

## 📚 License

MIT © Brian Bates

Built with ❤️ for log intelligibility and NLP adventures.