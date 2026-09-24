import pytest
from app.models import EnvironmentalMetrics
from app.graph.reasoning_graph import relevant_chains, analyze_multi_metric_nexus
from app.memory.session import (
    merge_metrics,
    extract_metrics_from_text,
    add_turn,
    get_conversation_history,
    get_session_summary,
    reset_session,
    missing_groups
)
from app.rag.store import rag_store
from app.pipeline import process


def test_multi_metric_nexus_three_variables():
    """
    Verifies that the multi-metric nexus analyzes at least 3 environmental variables together.
    """
    metrics = {
        "soil_organic_carbon": 0.3,
        "rainfall": "low",
        "crop": "monoculture wheat",
        "land_use_type": "monoculture",
        "region": "semi-arid"
    }
    nexus = analyze_multi_metric_nexus(metrics)
    assert nexus["satisfies_multi_variable_constraint"] is True
    assert nexus["variable_count"] >= 3
    assert len(nexus["coupled_variables"]) >= 3
    assert "Arid-Monoculture" in nexus["nexus_name"] or "Coupled" in nexus["nexus_name"]
    assert len(nexus["recommended_interventions"]) > 0


def test_clarifying_question_on_incomplete_input():
    """
    Verifies that incomplete input triggers a scientific clarifying question.
    """
    session_id = "test_incomplete_session"
    reset_session(session_id)

    # Empty metrics, vague question
    resp = process(session_id, None, "Biodiversity is declining on my land. What should I do?")
    assert resp["type"] == "clarification"
    assert "question" in resp
    assert len(resp["missing_metrics"]) >= 2
    assert "soil" in resp["missing_metrics"] or "land_use" in resp["missing_metrics"]


def test_conversational_parameter_extraction():
    """
    Verifies natural language extraction of soil organic carbon, pH, rainfall, and crops.
    """
    user_msg = "My soil organic carbon is 0.35%, soil pH is 6.5, rainfall is low, and crop is wheat."
    extracted = extract_metrics_from_text(user_msg)

    assert extracted.get("soil_organic_carbon") == 0.35
    assert extracted.get("soil_ph") == 6.5
    assert extracted.get("rainfall") == "low"
    assert extracted.get("crop") == "wheat"


def test_multi_turn_session_memory():
    """
    Verifies that session memory maintains environmental parameters and dialogue turns across turns.
    """
    session_id = "test_multiturn_session"
    reset_session(session_id)

    # Turn 1: Provide baseline metrics and query
    m = EnvironmentalMetrics(
        soil_organic_carbon=0.3,
        rainfall="low",
        crop="monoculture wheat",
        region="semi-arid",
        land_use_type="monoculture"
    )
    resp1 = process(session_id, m, "Suggest agroforestry and intercropping recommendations.")
    assert resp1["type"] == "recommendations"
    assert len(resp1["recommendations"]) >= 2

    # Turn 2: Follow-up question with NO metrics passed
    resp2 = process(session_id, None, "How will this affect soil moisture in year 2?")
    assert resp2["type"] == "recommendations"

    # Verify session summary records both turns
    summary = get_session_summary(session_id)
    assert summary["total_turns"] == 2
    assert summary["environmental_state"].get("soil_organic_carbon") == 0.3
    assert summary["environmental_state"].get("rainfall") == "low"
    assert len(summary["prior_recommendations"]) > 0


def test_hybrid_rag_retrieval_and_citations():
    """
    Verifies that RAG retrieval returns verified citations with page numbers and URLs.
    """
    sources = rag_store.retrieve("semi-arid monoculture wheat agroforestry", k=4)
    assert len(sources) > 0

    found_fao_or_ipcc = False
    for s in sources:
        meta = s.get("metadata", {})
        title = meta.get("source_title", "")
        url = meta.get("source_url", "")
        if "FAO" in title or "Food and Agriculture" in title or "IPCC" in title or "CBD" in title:
            found_fao_or_ipcc = True
            assert url.startswith("http")

    assert found_fao_or_ipcc is True


def test_recommendation_structure_and_actionability():
    """
    Verifies that output recommendations contain what to do, why it works, causal chains,
    time horizons, confidence, and evidence.
    """
    session_id = "test_structure_session"
    reset_session(session_id)

    m = EnvironmentalMetrics(
        soil_organic_carbon=0.3,
        rainfall="low",
        crop="wheat",
        region="semi-arid",
        land_use_type="monoculture"
    )
    result = process(session_id, m, "Recommend biodiversity interventions")
    assert result["type"] == "recommendations"
    assert "summary" in result
    assert "multi_metric_nexus" in result

    for rec in result["recommendations"]:
        assert "what_to_do" in rec and len(rec["what_to_do"]) > 5
        assert "why_it_works" in rec and len(rec["why_it_works"]) > 10
        assert "causal_chain" in rec and len(rec["causal_chain"]) >= 2
        assert "impacted_metrics" in rec and len(rec["impacted_metrics"]) >= 2
        assert rec["time_horizon"] in ["short", "medium", "long"]
        assert rec["confidence"] in ["low", "medium", "high"]
        assert "evidence" in rec and len(rec["evidence"]) > 0
