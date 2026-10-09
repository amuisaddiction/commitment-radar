from app.commitments import extract_commitments, detect_conflicts

def test_extracts_commitment():
    items = extract_commitments("I will send the invoice by Friday.")
    assert len(items) == 1
    assert "invoice" in items[0].task.lower()
    assert items[0].due_date is not None

def test_fallback_keeps_unmatched_transcript():
    items = extract_commitments("The weather is nice today.")
    assert len(items) == 1
    assert items[0].confidence < 0.5

def test_detects_possible_conflict():
    old = extract_commitments("I will send the invoice by Friday.")[0]
    new = extract_commitments("I will send the invoice by Monday.")[0]
    assert detect_conflicts(new, [old])
