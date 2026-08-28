"""초4 영어 진단 세트."""
from ._common import make_question, validate_elementary_questions
LEVEL,SUBJECT="초4","영어"; KEY=[1,1,1,1,2,1,5,3,1,1,3,3,1,2,3]; TIMES=[25,25,25,25,25,25,25,25,30,25,30,25,35,35,35]
def q(n,a,s,t,o,c,adv=False): return make_question(f"E4ENG-{n:02d}",LEVEL,SUBJECT,a,s,t,o,c,TIMES[n-1],f"{o[c-1]}가 문맥에 맞는 정답입니다.",f"{s}를 다시 확인할 필요가 있음.",adv)
D=[
("기본 의사소통","안부 묻고 답하기","A: How are you?  B: ___",["I'm fine, thanks.","I'm ten.","It's a book.","No, I don't.","Good night."],1),
("기본 의사소통","사람 소개","A: Who is she?  B: ___",["She's my sister.","It's my bag.","I'm fine.","He's ten.","Yes, she is."],1),
("기본 의사소통","상태 묻고 답하기","A: Are you okay?  B: ___",["Yes, I am.","It's okay.","I'm a student.","Yes, I do.","I like it."],1),
("기본 의사소통","소유 확인","A: Is this your bag?  B: ___",["Yes, it is.","Yes, I am.","Yes, I do.","It's a bag.","No, I'm not."],1),
("위치·장소","위치 표현 이해","My watch is under the table. 시계는 어디에 있나요?",["탁자 위","탁자 아래","가방 안","의자 옆","문 앞"],2),
("제안·응답","제안에 응답하기","A: Let's play soccer.  B: ___",["Sounds good.","I'm soccer.","It's five.","No, it isn't.","Thank you very much."],1),
("요일·시간","요일 묻고 답하기","A: What day is it today?  B: It's Friday. 오늘은 무슨 요일인가요?",["Monday","Tuesday","Wednesday","Thursday","Friday"],5),
("요일·시간","시각 표현 이해","A: What time is it?  B: It's three o'clock. 몇 시인가요?",["1시","2시","3시","4시","5시"],3),
("일상 활동","현재 활동 이해","I am reading a book. 지금 무엇을 하고 있나요?",["책을 읽고 있어요.","축구를 하고 있어요.","잠을 자고 있어요.","물을 마시고 있어요.","학교에 가고 있어요."],1),
("음식·의사소통","음식 권유에 응답하기","A: Do you want some pizza?  B: ___",["Yes, please.","I'm pizza.","It's Friday.","No, it isn't.","I am ten."],1),
("가격·수","가격 표현 이해","A: How much is it?  B: It's five dollars. 가격은 얼마인가요?",["2달러","3달러","5달러","7달러","10달러"],3),
("직업·자기소개","직업 어휘 이해","I am a pilot. 나의 직업은 무엇인가요?",["의사","교사","조종사","요리사","경찰관"],3),
("짧은 글 이해","직접 정보 찾기","Mina is in the park. She is riding a bike. Mina는 무엇을 하고 있나요?",["자전거를 타고 있어요.","책을 읽고 있어요.","수영하고 있어요.","밥을 먹고 있어요.","축구를 하고 있어요."],1),
("다음 단계 진입 탐색","출신지 묻고 답하기","A: Where are you from?  B: I'm from Canada. 어디에서 왔다고 했나요?",["Korea","Canada","Japan","China","Australia"],2,True),
("다음 단계 진입 탐색","좋아하는 교과 표현 이해","My favorite subject is math. 가장 좋아하는 과목은 무엇인가요?",["English","Science","Math","Music","Art"],3,True)]
QUESTIONS=[q(i+1,*x) for i,x in enumerate(D)]; validate_elementary_questions(QUESTIONS,KEY,345,70)
QUESTION_SET={"level":LEVEL,"subject":SUBJECT,"curriculum":"2022 개정 교육과정 영어 3~4학년군 참고","curriculum_year":2026,"test_version":"E4_ENG_2022R_2026_v1.0","core_count":13,"advance_count":2,"display_name":"초4 영어 진단","questions":QUESTIONS}
