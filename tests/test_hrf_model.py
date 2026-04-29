from resonance_os.generation.hrf_model import HRFModel

def test_hrf_predict():
    hrf = HRFModel()
    score = hrf.predict("Test sentence for HRF model")
    assert 0 <= score <= 1
