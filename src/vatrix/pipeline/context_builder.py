# src/vatrix/pipeline/context_builder.py

from collections import Counter

def build_context(log_entry, config=None):
    fields = [
        'ALGDATE', 
        'ALGTIME', 
        'ALGUSER', 
        'ALGCLIENT', 
        'ALGTEXT', 
        'PARAM1',
        'PARAM2', 
        'PARAM3',
        'PARAM4', 
        'ALGSYSTEM'
    ] 
    
    context = {field: log_entry.get(field, '') for field in fields}
    
    return context

### Prototyping Area ###

def infer_schema(logs, threshold=0.8):
    
    # Infer a field schema based on the presence of keys in a batch of log entries.
    # Fields must appear in at least `threshold` fraction of logs to be included.
    
    key_counts = Counter()
    total_logs = len(logs)

    for log in logs:
        key_counts.update(log.keys())
    # keep only those that appear in >= threshold fraction of logs
    schema = [key for key, count in key_counts.items() if count / total_logs >= threshold]

    return schema

def infer_context(log_entry, schema):
    # Build context dict from log entry, missing filled with empty.
    return {field: log_entry.get(field, '') for field in schema}