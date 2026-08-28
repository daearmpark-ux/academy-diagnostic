"""초1 기초영어 진단 세트."""
from ._common import make_question, validate_elementary_questions
LEVEL, SUBJECT = "초1", "영어"
KEY = [4,1,2,1,3,3,2,1,4,2,3,1,2,3,4]
def q(n, area, skill, text, options, correct, seconds, advance=False):
    answer = options[correct - 1]
    return make_question(f"E1E-{n:02d}", LEVEL, SUBJECT, area, skill, text, options, correct, seconds, f"{answer}는 이 낱말 또는 표현의 알맞은 뜻입니다.", f"{skill} 경험을 다시 확인할 필요가 있음.", advance)
QUESTIONS = [
 q(1,"알파벳·글자","알파벳 순서","A, B, C 다음에 오는 알파벳은 무엇인가요?",["A","B","C","D","E"],4,20),
 q(2,"알파벳·글자","대소문자 대응","대문자 A와 짝이 되는 소문자는 무엇인가요?",["a","b","c","d","e"],1,20),
 q(3,"알파벳·글자","첫 글자 인식","B로 시작하는 영어 낱말을 고르세요.",["cat","book","dog","fish","apple"],2,25),
 q(4,"알파벳·글자","같은 낱말 구별","보기와 똑같이 쓰인 영어 낱말을 고르세요. CAT",["CAT","CAP","CAR","ACT","BAT"],1,25),
 q(5,"기초 어휘","색깔 어휘","red의 뜻은 무엇인가요?",["파란색","노란색","빨간색","초록색","검은색"],3,25),
 q(6,"기초 어휘","수 어휘","three는 몇인가요?",["1","2","3","4","5"],3,20),
 q(7,"기초 어휘","학교 물건 어휘","pencil의 뜻은 무엇인가요?",["책","연필","의자","가방","지우개"],2,25),
 q(8,"기본 표현","인사","A: Hello!  B: ___",["Hi!","Good night.","Thank you.","Sorry.","No."],1,25),
 q(9,"기본 표현","감사 응답","A: Thank you.  B: ___",["Hello.","I'm seven.","Goodbye.","You're welcome.","Sit down."],4,25),
 q(10,"기본 표현","교실 표현","Sit down.의 뜻은 무엇인가요?",["일어나세요.","앉으세요.","문을 여세요.","책을 펴세요.","손을 드세요."],2,25),
 q(11,"짧은 문장 이해","자기소개 이해","I am Mina.에서 사람의 이름은 무엇인가요?",["Tom","Jisu","Mina","Minho","Jane"],3,30),
 q(12,"짧은 문장 이해","안부 묻고 답하기","A: How are you?  B: ___",["I'm fine, thank you.","My name is Tom.","I'm eight.","It's a cat.","Good night."],1,30),
 q(13,"짧은 문장 이해","가족 어휘","mother의 뜻은 무엇인가요?",["아빠","엄마","형제","친구","선생님"],2,25),
 q(14,"다음 단계 진입 탐색","사물 묻고 답하기","A: What is this?  B: It is a cat. 무엇이라고 답했나요?",["dog","book","cat","apple","bag"],3,35,True),
 q(15,"다음 단계 진입 탐색","좋아하는 것 표현 이해","I like apples.에서 좋아하는 것은 무엇인가요?",["milk","dogs","books","apples","soccer"],4,35,True),
]
validate_elementary_questions(QUESTIONS, KEY, 320, 70)
QUESTION_SET = {"level": LEVEL, "subject": SUBJECT, "curriculum": "학원 기초영어 진단 · 초3 영어 진입 참고", "curriculum_year": 2026, "test_version": "E1_ENG_FOUNDATION_2026_v1.0", "core_count": 13, "advance_count": 2, "display_name": "초1 기초영어 진단", "questions": QUESTIONS}
