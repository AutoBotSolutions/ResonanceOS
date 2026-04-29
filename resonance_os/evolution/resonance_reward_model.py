def compute_hr_resonance_reward(hrv_vector, hrv_feedback, alpha=0.6):
    """
    Compute reward combining target HRV alignment and HRF feedback.
    """
    alignment = sum(hrv_vector) / len(hrv_vector)  # placeholder for real cosine alignment
    reward = alpha * alignment + (1 - alpha) * hrv_feedback
    return reward
