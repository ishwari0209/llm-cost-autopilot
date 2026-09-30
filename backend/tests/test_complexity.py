from app.router.complexity import score_prompt


def test_simple_question_is_low():
    result = score_prompt("What is an API?")
    assert result.level == "LOW"


def test_analysis_task_is_high():
    prompt = (
        "Analyze this dataset and explain step by step why the model's "
        "performance dropped after deployment, considering the architecture "
        "and possible root causes."
    )
    result = score_prompt(prompt)
    assert result.level == "HIGH"


def test_coding_bug_bumps_score():
    result = score_prompt("Debug this function, I'm getting a stack trace error.")
    assert result.score >= 4