### YAML 생성 플러그인


다음과 TMDB 에 없는 에피소드 정보를 OTT에서 직접 가져오기 위한 플러그인이다.

기본적으로 TMDB에서 메인포스터, 에피소드별 썸네일, 공개날짜, 배우 등 정보는

IMDB에서 TMDB 봇이 잘 등록하므로 놔두고 한국어 에피소드 정보만 OTT에서 직접 가져올 목적이다.

가져온 정보가 한글이 아닐경우 만들지 않는다(티빙 어큐즈드).

추후 FF용 TMDB 쇼 파일처리에서 자동으로 만들게 할 계획이다(언제 만들지는 모른다).


######**<우선순위>**


EBSKIDS 를 제외하고 7개의 OTT 를 원하는 순서대로 넣는다.


원치 않는건 빼면 된다.


수동으로 찾을때만 해당하면 자동화시 파일명 릴정보에 해당하는 OTT만 검색한다.


아마존은 국내 OTT도 검색할 예정


######**<최소 매칭 점수>**


특수문자를 제외하고 매칭된다.


['로앤 오더: 성범죄 전담반', '로앤 오더 성범죄 전담반] 매칭점수는 100점이다.

['로앤 오더 성범죄 전담반', '로 앤 오더 성범죄 전담반'] 매칭점수는 96점이다.

['전생했더니 슬라임이었던 건에 대하여', '전생했더니 슬라임이었던 건에 대하여 OAD'] 매칭점수는 90점이다.


참고해서 취향대로 정한다. 실제 점수는 소수점이다.


######**<통합검색어>**

쇼의 경우는 영화하고 달리 제목이 같은 경우가 거의 없어서 특별한 경우를 제외하면 제목만으로 매칭하는데 큰 문제가 없다. 가십걸 (2007), 가십걸 (2021) 같은 경우를 위해 구분자 | 를 이용하여 연도 정보를 함께 넣을 수 있다.

모든 시즌 탐색은 티빙, 웨이브에만 해당하며 다른 OTT는 기본적으로 모든 시즌을 가져온다.

웨이브 티빙의 경우 **시즌 1, 시즌 2, 1기, 2기 모두 시즌 1 ,2** 로 생성되도록 제작되었다. 특별한 경우 어쩔수 없다.

시즌 2 스페셜 이런건 시즌 0으로 본다.

웨이브 https://www.wavve.com/player/vod?programid=F3501_F35000000015 에서 ***F3501_F35000000015***

티빙 https://www.tving.com/contents/P001565742 에서 ***P001565742***

쿠팡 https://www.coupangplay.com/titles/65c0c0a9-c2eb-4016-ab42-e26f0426fdb6 에서 ***65c0c0a9-c2eb-4016-ab42-e26f0426fdb6***

넷플릭스 https://www.netflix.com/title/81519223 에서 ***81519223***

디즈니플러스 https://www.disneyplus.com/ko-kr/series/big-bet/506cEky88AhL 에서 ***506cEky88AhL***

아마존 https://www.primevideo.com/detail/0N3EDITHIBCK6E9G5PPZZQYOGQ/ref=atv_dl_rdr 에서 ***0N3EDITHIBCK6E9G5PPZZQYOGQ***

애플 tv https://tv.apple.com/kr/show/리에종---liaison/umc.cmc.62t13xacr3mxnit5a40g8tkla 에서 ***umc.cmc.62t13xacr3mxnit5a40g8tkla***

EBSKIDS https://anikids.ebs.co.kr/anikids/program/show/10024440 에서 ***10024440***

