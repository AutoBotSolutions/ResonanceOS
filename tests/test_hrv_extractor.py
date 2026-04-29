from resonance_os.profiles.hrv_extractor import HRVExtractor

def test_hrv_extractor():
    extractor = HRVExtractor()
    vec = extractor.extract("This is a test sentence. It should vary in length!")
    assert len(vec) == 8
