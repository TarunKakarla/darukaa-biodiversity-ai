from app.graph.reasoning_graph import relevant_chains

def test_example_returns_three_chains():
    m = {"soil_organic_carbon":0.3,"rainfall":"low","crop":"monoculture wheat","land_use_type":"monoculture","region":"semi-arid"}
    chains = relevant_chains(m)
    assert len(chains) == 3
    assert any("soil carbon" in c["name"] for c in chains)
    assert any("rainfall" in c["name"] for c in chains)
    assert any("land use" in c["name"] for c in chains)
