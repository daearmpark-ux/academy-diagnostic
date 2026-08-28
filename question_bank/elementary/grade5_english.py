"""초5 영어 진단 세트."""
from ._common import make_question, validate_elementary_questions
LEVEL,SUBJECT="초5","영어"; KEY=[2,3,3,3,1,3,3,2,1,3,1,1,2,1,3]; TIMES=[30,30,30,30,30,30,35,35,35,35,35,35,40,40,40]
def q(n,a,s,t,o,c,adv=False): return make_question(f"E5ENG-{n:02d}",LEVEL,SUBJECT,a,s,t,o,c,TIMES[n-1],f"{o[c-1]}가 문맥에 맞는 표현입니다.",f"{s}를 다시 확인할 필요가 있음.",adv)
D=[
("기본 의사소통","출신지 표현","A: Where are you from? B: I'm from Australia. 어디에서 왔다고 했나요?",["Canada","Australia","Korea","India","France"],2),
("소유·사람","소유자 묻고 답하기","A: Whose phone is this? B: It's Jisu's. 누구의 전화기인가요?",["Mina의","Tom의","Jisu의","선생님의","내 것"],3),
("학교생활","좋아하는 교과","My favorite subject is science. 가장 좋아하는 과목은 무엇인가요?",["English","Math","Science","Music","Art"],3),
("일과·시간","일과 시각 이해","I go home at four o'clock. 몇 시에 집에 가나요?",["2시","3시","4시","5시","6시"],3),
("음식·주문","음식 주문 표현","식당에서 스테이크를 주문할 때 가장 알맞은 말은?",["I'd like a steak, please.","I am a steak.","Where is steak?","I can steak.","This steak is twelve."],1),
("집·장소","장소 어휘 이해","The refrigerator is in the kitchen. 냉장고는 어디에 있나요?",["침실","거실","부엌","욕실","정원"],3),
("과거 경험","과거 경험 이해","I went to Dokdo last summer. 지난여름에 어디에 갔나요?",["Jeju","Seoul","Dokdo","Busan","Incheon"],3),
("사람 묘사","외모 묘사 이해","She has short hair and wears glasses. 알맞은 설명은?",["긴 머리이고 모자를 썼어요.","짧은 머리이고 안경을 썼어요.","짧은 머리이고 모자를 썼어요.","긴 머리이고 안경이 없어요.","머리가 없고 안경을 썼어요."],2),
("길 안내","방향 표현 이해","Go straight and turn left at the bank. 알맞은 뜻은?",["곧장 가다가 은행에서 왼쪽으로 도세요.","은행에서 오른쪽으로 도세요.","은행 앞에서 멈추세요.","은행까지 뒤로 가세요.","은행에서 길을 건너세요."],1),
("가격·쇼핑","가격 표현 이해","These socks are twelve dollars. 양말 가격은 얼마인가요?",["10달러","11달러","12달러","13달러","20달러"],3),
("집·장소","There is 표현 이해","There is a table in the kitchen. 알맞은 뜻은?",["부엌에 탁자가 있어요.","거실에 탁자가 있어요.","부엌에 의자가 두 개 있어요.","탁자가 부엌 밖에 있어요.","부엌에는 아무것도 없어요."],1),
("희망·활동","하고 싶은 일 표현","I want to ride a bike. 무엇을 하고 싶어 하나요?",["자전거 타기","수영하기","책 읽기","축구하기","요리하기"],1),
("짧은 글 이해","직접 정보 찾기","Jina went to the market and bought apples. Jina가 산 것은 무엇인가요?",["bananas","apples","milk","bread","books"],2),
("다음 단계 진입 탐색","건강 조언 이해","I have a headache. What should I do? 가장 알맞은 조언은?",["You should get some rest.","You should run faster.","You should eat five pizzas.","You should shout loudly.","You should stay up all night."],1,True),
("다음 단계 진입 탐색","빈도 표현 이해","I exercise three times a week. 일주일에 몇 번 운동하나요?",["한 번","두 번","세 번","네 번","다섯 번"],3,True)]
QUESTIONS=[q(i+1,*x) for i,x in enumerate(D)]; validate_elementary_questions(QUESTIONS,KEY,430,80)
QUESTION_SET={"level":LEVEL,"subject":SUBJECT,"curriculum":"2022 개정 교육과정 영어 5~6학년군 참고","curriculum_year":2026,"test_version":"E5_ENG_2022R_2026_v1.0","core_count":13,"advance_count":2,"display_name":"초5 영어 진단","questions":QUESTIONS}
