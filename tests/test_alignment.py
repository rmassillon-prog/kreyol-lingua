from src.core.normalizer import Normalizer

def test_alignment_spans_basic():
    n = Normalizer()
    text = "Mwen renmen zoranj"
    r = n.normalize(text)

    assert r.original_text == text
    assert r.get_normalized_text()

    for tok in r.tokens:
        s, e = tok.source_span
        assert 0 <= s < e <= len(text)
        assert text[s:e].strip() != ""

def test_visualize_alignment_runs():
    n = Normalizer()
    r = n.normalize("Mwen renmen zoranj")
    s = r.visualize_alignment()
    assert "ALIGNMENT VISUALIZATION" in s

def test_segmentation_alignment_map():
    # "map" should segment into ["m", "ap"] and BOTH tokens should point to the same source span
    from src.core.normalizer import Normalizer
    n = Normalizer(enable_segmentation=True)

    text = "map manje"
    r = n.normalize(text)

    # Expect first two tokens from "map"
    assert r.tokens[0].normalized == "m"
    assert r.tokens[1].normalized == "ap"
    assert r.tokens[0].is_segmented is True
    assert r.tokens[1].is_segmented is True
    assert r.tokens[0].original_fused_form.lower() == "map"
    assert r.tokens[0].source_span == r.tokens[1].source_span

def test_unlicensed_clitic_warning():
    from src.core.normalizer import Normalizer
    n = Normalizer(enable_segmentation=False)

    # "sak w" is suspicious: 'sak' ends with consonant 'k', so clitic 'w' is likely unlicensed.
    r = n.normalize("sak w vini")

    assert any("clitic" in w.lower() for w in r.warnings)
