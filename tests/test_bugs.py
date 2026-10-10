import pytest
from app.commitments import extract_commitments, detect_conflicts
from app.models import Commitment

def test_extract_multiple_commitments():
    transcript = "I promised Rahul that I will send him the project report by Friday. I also promised Priya that I will finish her presentation by Thursday. I will be travelling all day Friday, so I may not be able to send Rahul the report on time."
    commitments = extract_commitments(transcript)
    
    assert len(commitments) == 3
    tasks = [c.task.lower() for c in commitments]
    
    assert "i promised rahul that i will send him the project report by friday" in tasks[0]
    assert "i also promised priya that i will finish her presentation by thursday" in tasks[1]
    assert "i will be travelling all day friday" in tasks[2]

def test_conflict_travel_overlap():
    c1 = Commitment(id="1", task="I promised Rahul that I will send him the project report by Friday.", due_date="2023-12-01", source_text="test")
    c2 = Commitment(id="2", task="I also promised Priya that I will finish her presentation by Thursday.", due_date="2023-11-30", source_text="test")
    c3 = Commitment(id="3", task="I will be travelling all day Friday.", due_date="2023-12-01", source_text="test")
    
    # Check c3 vs c1 and c2
    conflicts_c3 = detect_conflicts(c3, [c1, c2])
    
    # Should flag c3 and c1 because dates match and one is travel
    assert len(conflicts_c3) == 1
    assert conflicts_c3[0].severity == "high"
    assert conflicts_c3[0].title == "Possible schedule risk"
    assert conflicts_c3[0].related_commitment_id == "1"

def test_no_deadline_commitment():
    # If no deadline, date_clash or availability_clash shouldn't trigger improperly
    c1 = Commitment(id="1", task="I will send the report eventually.", due_date=None, source_text="test")
    c2 = Commitment(id="2", task="I will be travelling today.", due_date="2023-11-30", source_text="test")
    conflicts = detect_conflicts(c2, [c1])
    assert len(conflicts) == 0

def test_malformed_input():
    commitments = extract_commitments("   !?.  \n")
    assert len(commitments) == 0
