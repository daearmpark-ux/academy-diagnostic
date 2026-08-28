"""Validated middle-school grade 2 mathematics question set."""

M2_MATH_TEST_VERSION = "M2_MATH_2022R_2026_v1.0"
M2_MATH_ANSWER_KEY = [3, 4, 2, 5, 1, 4, 2, 3, 4, 2, 4, 2, 3, 5, 2]
M2_MATH_CORE_AREAS = {
    "수와 식": [1, 2, 3],
    "부등식·연립방정식": [4, 5],
    "일차함수": [6, 7],
    "도형": [8, 9, 10, 11],
    "경우의 수·확률": [12, 13],
}


def _m2_question(
    qid,
    stem,
    options,
    correct_number,
    correct_text,
    recommended_seconds,
    official_domain,
    unit,
    skill,
    solution,
    diagnostic_if_wrong,
    area,
    is_advance_probe=False,
):
    return {
        "id": qid,
        "text": stem,
        "choices": options,
        "answer": correct_text,
        "correct_option_number": correct_number,
        "correct_option_text": correct_text,
        "recommended_sec": recommended_seconds,
        "recommended_seconds": recommended_seconds,
        "official_domain": official_domain,
        "unit": unit,
        "skill": skill,
        "solution": solution,
        "diagnostic_if_wrong": diagnostic_if_wrong,
        "area": area,
        "is_advance_probe": is_advance_probe,
        "score_in_core": not is_advance_probe,
    }


M2_MATH_QUESTIONS = [
    _m2_question("M2M-01", "0.363636…처럼 36이 계속 반복되는 순환소수를 기약분수로 나타낸 것은?", ["3/11", "4/9", "4/11", "9/25", "2/5"], 3, "4/11", 55, "수와 연산", "유리수와 순환소수", "순환소수를 분수로 나타내기", "x = 0.363636…이라 하면 100x - x = 36이므로 99x = 36, 따라서 x = 36/99 = 4/11.", "순환소수와 분수의 관계 및 순환소수를 분수로 변환하는 원리를 점검할 필요가 있음.", "수와 식"),
    _m2_question("M2M-02", "2a³b × (-3a²b²)을 간단히 한 것은?", ["-6a⁶b²", "6a⁵b³", "-5a⁵b³", "-6a⁵b³", "-6a⁶b³"], 4, "-6a⁵b³", 45, "변화와 관계", "식의 계산", "지수법칙과 단항식의 곱셈", "계수는 2×(-3)=-6. 같은 문자의 지수는 더하므로 a³×a²=a⁵, b×b²=b³. 따라서 -6a⁵b³.", "부호 계산, 계수의 곱셈 또는 같은 밑의 지수법칙을 점검할 필요가 있음.", "수와 식"),
    _m2_question("M2M-03", "(4x² - 3x + 2) - (x² + 5x - 4)를 간단히 한 것은?", ["3x² + 2x - 2", "3x² - 8x + 6", "5x² + 2x - 2", "3x² + 8x - 2", "5x² - 8x + 6"], 2, "3x² - 8x + 6", 50, "변화와 관계", "식의 계산", "다항식의 덧셈과 뺄셈", "두 번째 괄호 앞의 -를 분배하면 4x² - 3x + 2 - x² - 5x + 4. 동류항을 정리하면 3x² - 8x + 6.", "괄호 앞 음수의 분배와 동류항 정리를 점검할 필요가 있음.", "수와 식"),
    _m2_question("M2M-04", "-2x + 3 > 7의 해는?", ["x > 2", "x < 2", "x > -2", "x ≤ -2", "x < -2"], 5, "x < -2", 45, "변화와 관계", "일차부등식", "일차부등식 풀이와 부등호 방향", "-2x + 3 > 7 → -2x > 4. 양변을 -2로 나누면 부등호 방향이 바뀌므로 x < -2.", "음수로 곱하거나 나눌 때 부등호 방향이 바뀌는 성질을 점검할 필요가 있음.", "부등식·연립방정식"),
    _m2_question("M2M-05", "2x + y = 11, x - y = 1을 동시에 만족하는 (x, y)는?", ["(4, 3)", "(3, 4)", "(5, 1)", "(2, 7)", "(6, -1)"], 1, "(4, 3)", 70, "변화와 관계", "연립일차방정식", "연립일차방정식의 해", "두 식을 더하면 3x=12이므로 x=4. x-y=1에 대입하면 4-y=1이므로 y=3. 따라서 (4,3).", "연립방정식의 가감법 또는 구한 값을 다시 대입하는 과정을 점검할 필요가 있음.", "부등식·연립방정식"),
    _m2_question("M2M-06", "두 점 (0, -2), (3, 4)를 지나는 일차함수의 식은?", ["y = x + 2", "y = 2x + 2", "y = -2x + 2", "y = 2x - 2", "y = -x - 2"], 4, "y = 2x - 2", 60, "변화와 관계", "일차함수", "두 점을 지나는 일차함수의 식", "기울기 = (4-(-2))/(3-0)=6/3=2. x=0일 때 y=-2이므로 y절편은 -2. 따라서 y=2x-2.", "두 점에서 기울기를 구하고 y절편을 결정하는 과정을 점검할 필요가 있음.", "일차함수"),
    _m2_question("M2M-07", "두 직선 y = 2x + 1, y = -x + 7의 교점은?", ["(1, 3)", "(2, 5)", "(3, 7)", "(5, 2)", "(-2, -3)"], 2, "(2, 5)", 60, "변화와 관계", "일차함수와 일차방정식의 관계", "두 직선의 교점", "교점에서는 두 y값이 같으므로 2x+1=-x+7. 3x=6이므로 x=2. y=2×2+1=5. 따라서 (2,5).", "두 일차함수의 교점과 연립일차방정식의 해의 관계를 점검할 필요가 있음.", "일차함수"),
    _m2_question("M2M-08", "삼각형의 내심에 대한 설명으로 옳은 것은?", ["세 변의 수직이등분선의 교점", "세 중선의 교점", "세 내각의 이등분선의 교점", "세 높이의 교점", "세 변의 중점"], 3, "세 내각의 이등분선의 교점", 45, "도형과 측정", "삼각형의 성질", "삼각형의 내심", "삼각형의 세 내각의 이등분선은 한 점에서 만나며 그 점이 내심이다.", "삼각형의 내심과 다른 중심의 정의를 구분하는 개념을 점검할 필요가 있음.", "도형"),
    _m2_question("M2M-09", "모든 평행사변형에서 항상 성립하는 것은?", ["두 대각선의 길이가 같다", "두 대각선이 서로 수직이다", "네 각의 크기가 모두 같다", "두 대각선은 서로를 이등분한다", "두 대각선은 각각 두 내각을 이등분한다"], 4, "두 대각선은 서로를 이등분한다", 45, "도형과 측정", "사각형의 성질", "평행사변형의 성질", "평행사변형에서는 두 대각선이 서로를 이등분한다. 나머지 성질은 특정한 경우에만 성립할 수 있다.", "평행사변형과 직사각형·마름모·정사각형의 성질을 구분할 필요가 있음.", "도형"),
    _m2_question("M2M-10", "△ABC ∽ △DEF이고 AB = 6, DE = 9, BC = 10일 때 EF의 길이는?", ["12", "15", "18", "20", "24"], 2, "15", 50, "도형과 측정", "도형의 닮음", "닮은 도형의 대응변과 닮음비", "AB와 DE가 대응하므로 확대비는 9/6=3/2. BC와 EF가 대응하므로 EF=10×3/2=15.", "닮은 도형의 대응 관계와 닮음비 적용을 점검할 필요가 있음.", "도형"),
    _m2_question("M2M-11", "직각삼각형의 두 직각변의 길이가 5와 12일 때 빗변의 길이는?", ["7", "10", "12", "13", "17"], 4, "13", 50, "도형과 측정", "피타고라스 정리", "피타고라스 정리의 기본 적용", "빗변을 c라 하면 c²=5²+12²=25+144=169. 길이는 양수이므로 c=13.", "피타고라스 정리에서 직각변과 빗변을 구분하고 제곱 관계를 적용하는 능력을 점검할 필요가 있음.", "도형"),
    _m2_question("M2M-12", "서로 다른 상의 3가지와 서로 다른 하의 2가지 중 각각 하나씩 고르는 방법은 모두 몇 가지인가?", ["5", "6", "7", "8", "9"], 2, "6", 40, "자료와 가능성", "경우의 수", "곱의 법칙", "상의 한 가지를 고르는 각 경우마다 하의를 2가지 방법으로 고를 수 있으므로 3×2=6가지.", "독립된 선택 과정에서 경우의 수를 곱하는 원리를 점검할 필요가 있음.", "경우의 수·확률"),
    _m2_question("M2M-13", "1부터 6까지의 숫자가 하나씩 적힌 크기와 모양이 같은 카드 6장 중 한 장을 무작위로 뽑는다. 나온 수가 '짝수 또는 3의 배수'일 확률은?", ["1/3", "1/2", "2/3", "5/6", "1"], 3, "2/3", 55, "자료와 가능성", "확률", "사건의 확률", "짝수는 {2,4,6}, 3의 배수는 {3,6}. '또는'은 {2,3,4,6}으로 4가지. 전체 6가지 중 4/6=2/3.", "'또는' 사건에서 중복되는 경우를 한 번만 세는 개념을 점검할 필요가 있음.", "경우의 수·확률"),
    _m2_question("M2M-14", "x² = 49를 만족하는 모든 x를 고른 것은?", ["7만", "-7만", "49", "-49", "-7과 7"], 5, "-7과 7", 35, "수와 연산", "상위학년 진입 탐색", "제곱근 개념 진입", "7²=49이고 (-7)²=49이므로 x=-7 또는 x=7.", "제곱과 제곱근 사이의 관계에 대한 상위 과정 진입 개념을 추가 확인할 필요가 있음.", "상위 과정 진입 탐색", True),
    _m2_question("M2M-15", "x² + 5x + 6과 같은 식은?", ["(x + 1)(x + 6)", "(x + 2)(x + 3)", "(x - 2)(x - 3)", "(x + 2)(x - 3)", "(x - 2)(x + 3)"], 2, "(x + 2)(x + 3)", 45, "변화와 관계", "상위학년 진입 탐색", "인수분해 개념 진입", "(x+2)(x+3)=x²+3x+2x+6=x²+5x+6.", "다항식의 곱셈을 역으로 보고 곱의 형태를 인식하는 상위 과정 진입 개념을 추가 확인할 필요가 있음.", "상위 과정 진입 탐색", True),
]


def validate_m2_math_questions(questions=M2_MATH_QUESTIONS):
    required = {
        "id", "text", "choices", "correct_option_number",
        "correct_option_text", "recommended_seconds", "official_domain",
        "unit", "skill", "is_advance_probe", "score_in_core", "solution",
        "diagnostic_if_wrong",
    }
    if len(questions) != 15:
        raise ValueError("중2 수학 문항은 정확히 15개여야 합니다.")
    if len({question["id"] for question in questions}) != 15:
        raise ValueError("중2 수학 문항 ID가 중복되었습니다.")
    if sum(question["score_in_core"] for question in questions) != 13:
        raise ValueError("CORE 문항은 정확히 13개여야 합니다.")
    if sum(question["is_advance_probe"] for question in questions) != 2:
        raise ValueError("ADVANCE_PROBE 문항은 정확히 2개여야 합니다.")
    if [question["is_advance_probe"] for question in questions] != [False] * 13 + [True, True]:
        raise ValueError("ADVANCE_PROBE는 Q14와 Q15만이어야 합니다.")
    for question in questions:
        if not required.issubset(question):
            raise ValueError(f"필수 metadata가 없는 문항: {question['id']}")
        if len(question["choices"]) != 5 or len(set(question["choices"])) != 5:
            raise ValueError(f"선택지는 중복 없이 5개여야 합니다: {question['id']}")
        number = question["correct_option_number"]
        if number not in range(1, 6):
            raise ValueError(f"정답 번호가 범위를 벗어났습니다: {question['id']}")
        if question["choices"][number - 1] != question["correct_option_text"]:
            raise ValueError(f"정답 번호와 정답 문자열이 다릅니다: {question['id']}")
        if question["recommended_seconds"] <= 0:
            raise ValueError(f"권장시간은 양수여야 합니다: {question['id']}")
        if question["score_in_core"] == question["is_advance_probe"]:
            raise ValueError(f"CORE/ADVANCE 구분이 충돌합니다: {question['id']}")
    if [question["correct_option_number"] for question in questions] != M2_MATH_ANSWER_KEY:
        raise ValueError("중2 수학 정답키가 canonical 정답키와 다릅니다.")
    if sum(question["recommended_seconds"] for question in questions) != 750:
        raise ValueError("전체 권장시간은 750초여야 합니다.")
    if sum(question["recommended_seconds"] for question in questions if question["score_in_core"]) != 670:
        raise ValueError("CORE 권장시간은 670초여야 합니다.")
    return True


validate_m2_math_questions()

QUESTION_SET = {
    "level": "중2",
    "subject": "수학",
    "curriculum": "2022 개정 교육과정",
    "curriculum_year": 2026,
    "test_version": M2_MATH_TEST_VERSION,
    "core_count": 13,
    "advance_count": 2,
    "display_name": "중2 수학 진단",
    "questions": M2_MATH_QUESTIONS,
}
