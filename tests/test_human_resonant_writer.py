from resonance_os.generation.human_resonant_writer import HumanResonantWriter

def test_writer_generate():
    writer = HumanResonantWriter()
    article = writer.generate("Write a futuristic AI article")
    assert isinstance(article, str)
    assert len(article) > 0
