# 데이터 목록 및 수집 방법

> 핵심 지표: 인구당 보유율(등록대수 ÷ 인구 × 1,000) · 충전소 비율(충전기 수 ÷ 등록대수) · 보조금 합계(국비 + 지방비)

---

## 수집 우선순위 요약

| 우선순위 | 데이터 | 공개 여부 | 방법 | 난이도 |
|---|---|---|---|---|
| 1 | 시도별 전기차 등록대수 | ✅ 공개 | 국토교통부 공공데이터포털 CSV / API | 하 |
| 2 | 시도별 인구수 | ✅ 공개 | 행정안전부 주민등록인구 / KOSIS API | 하 |
| 3 | 시도별 충전소 수 | ✅ 공개 | 한국전력공사 / 한국환경공단 공공데이터포털 API | 하 |
| 4 | 차종별 전기차 보조금 | ✅ 공개 | 무공해차 통합누리집(ev.or.kr) 크롤링 | 중 |
| 5 | 자동차 기업 FAQ | ⚠️ 크롤링 | 제조사 홈페이지 BeautifulSoup | 중 |
| 6 | 정비소 위치 | ⚠️ 크롤링 | 현대·기아 홈페이지 크롤링 | 중 |
| 7 | 차종별 차량 가격 (선택) | ⚠️ 크롤링 | 다나와 자동차 크롤링 | 중 |

---

## 1. 시도별 전기차 등록대수

**용도**: 지역별 전기차 현황 조회 및 인구당 보유율·충전소 비율 계산 기준값

| 항목 | 내용 |
|---|---|
| 추천 방법 | **국토교통부 자동차 등록현황** 공공데이터포털 CSV 다운로드 또는 API 조회 |
| 출처 | [국토교통부 자동차 등록 현황 (공공데이터포털)](https://www.data.go.kr/data/15109006/fileData.do) |
| 필요 항목 | 연도, 시도명, 차종(전기차), 누적 등록대수 |
| 수집 주기 | 연 1회 (분석 대상 연도 범위 확정 후 일괄 수집) |
| 주의 | 개인·법인 등록 합산 여부 및 차종 분류 코드 확인 필요 |

---

## 2. 시도별 인구수

**용도**: 인구당 전기차 보유율 계산 기준값 (참고 지표)

| 항목 | 내용 |
|---|---|
| 추천 방법 | **행정안전부 주민등록인구 현황** 또는 **통계청 KOSIS** CSV 다운로드 / API |
| 출처 | [행정안전부 주민등록 인구통계](https://jumin.mois.go.kr) · [통계청 KOSIS](https://kosis.kr) |
| 필요 항목 | 연도, 시도명, 주민등록인구 |
| 수집 주기 | 연 1회 (전기차 등록 데이터와 동일 연도 기준) |
| 주의 | 전기차 등록 데이터와 연도·지역 단위(17개 시/도) 일치 여부 확인 필요 |

---

## 3. 시도별 충전소 수

**용도**: 지역별 전기차 대비 충전소 비율 계산 (전기차 1대당 충전기 수)

| 항목 | 내용 |
|---|---|
| 추천 방법 | **한국전력공사** 또는 **한국환경공단** 공공데이터포털 API<br>→ 시도별 충전기 설치 현황 제공 |
| 출처 | [한국환경공단 전기차 충전소 현황 (공공데이터포털)](https://www.data.go.kr/data/15076352/openapi.do)<br>[한국전력공사 EV 충전인프라 통계](https://home.kepco.co.kr) |
| 필요 항목 | 연도, 시도명, 충전기 수 (급속·완속 구분 가능 시 포함) |
| 수집 주기 | 연 1회 (전기차 등록 데이터와 동일 연도 기준) |
| 주의 | 한국전력공사·환경공단 출처가 복수 → 단일 출처로 통일 후 기준 명시 필요 |

---

## 4. 차종별 전기차 보조금

**용도**: 지역별·차종별 보조금(국비+지방비) 비교

| 항목 | 내용 |
|---|---|
| 추천 방법 | **무공해차 통합누리집(ev.or.kr)** 보조금 조회 페이지 BeautifulSoup 크롤링<br>→ 지역·차종별 국비·지방비 금액 수록 |
| 출처 | [무공해차 통합누리집 보조금 조회](https://www.ev.or.kr/evInfo/searchSubsidy) (환경부) |
| 필요 항목 | 연도, 시도명, 차종명, 국비 보조금, 지방비 보조금, 합계 |
| 수집 주기 | 연 1회 (보조금은 매년 초 갱신됨) |
| 주의 | 보조금은 예산 소진 시 중단 → 수집 시점 및 기준 연도 명시 필수. 차종 명칭이 제조사와 다를 수 있어 매핑 처리 필요 |

---

## 5. 자동차 기업 FAQ

**용도**: 기업별 전기차 A/S 관련 FAQ 검색 및 조회

---

### 5-1. 수집

#### 수집 완료 — `data/faq/all_faq.csv` (총 1653건, 2026-06-28 기준)

| 기업 | 건수 | 출처 URL | 수집 스크립트 | 수집 방법 |
|---|---|---|---|---|
| 현대자동차 | 283건 | `www.hyundai.com` | `collect_faq.py` | Selenium 쿠키 획득 → 내부 GW API POST (`/faq/category`, `/faq/list`) |
| 제네시스 | 232건 | `www.genesis.com` | `collect_faq.py` | 정적 HTML `requests` 직접 요청 → `.cp-faq__accordion-item` DOM 파싱 |
| 기아자동차 | 41건 | `www.kia.com/kr/customer-service/faq` | `collect_faq.py` | Selenium 카테고리 탭 클릭 + `.cmp-accordion__item` DOM 파싱 |
| 볼보 | 53건 | `www.volvocars.com/kr/support/` | `collect_bmw_volvo.py` | Selenium topic→subtopic 순차 방문, body 텍스트 title+ingress 쌍 추출 |
| BMW | 908건 | `www.bmw.co.kr/kr/s/` | `collect_bmw_volvo.py` | Selenium Salesforce 포털, '도움말 더 보기' 반복 클릭(176회)으로 전체 수집 |
| 메르세데스-벤츠 | 19건 | `www.mercedes-benz.co.kr/passengercars/buy/mbmk/help/help-faq.html` | `collect_bmw_volvo.py` | Selenium `innerText` 파싱, WB7-ACCORDION shadow DOM 구조, Q1 노이즈 제거 |
| KGM | 117건 | `www.kg-mobility.com/sr/online-center/faq/detail?searchWord=&categoryCd=300` | `collect_kgm.py` | REST API 직접 호출 (`getFaqContentList.do` → `getFaqContentDetail.do?bbNo=`) |

#### 수집 불가 — 접근 차단 또는 FAQ 부재

| 기업 | 사유 |
|---|---|
| 르노코리아 | FAQ 전용 페이지 없음 (전화·카카오 상담만 제공) |
| 테슬라 | Cloudflare WAF 차단 (403) — headless 브라우저도 차단됨 |
| BYD | 한국 공식 FAQ 페이지 없음 |
| 아우디코리아 | FAQ URL 404. 차량 Q&A 페이지(`/ko/owners/audi_qa/`)는 존재하나 답변이 YouTube 영상 링크뿐 |

#### 수집 방법 상세

**현대자동차**
- Selenium으로 FAQ 페이지 방문 후 세션 쿠키 획득
- `GET /faq/category` → 카테고리 코드 목록 수집 (`faqCategoryCode=Z019` 필수 파라미터)
- `POST /faq/list` (JSON body: `pageSize=100`, `pageNo` 반복) → 페이지 단위 전체 수집
- 필수 헤더: `ep-channel: homepage`, `Content-Type: application/json`

**제네시스**
- `requests`로 정적 HTML 직접 요청 (Selenium 불필요)
- `.cp-faq__accordion-item` → `.accordion-label`(카테고리) + `.accordion-title`(질문) + `.accordion-panel-inner`(답변) 구조 파싱

**기아자동차**
- Selenium으로 FAQ 페이지 로드 후 카테고리 탭(`.cmp-faq-search-tab button`) 순차 클릭
- 탭당 "더보기" 버튼 반복 클릭으로 전체 항목 전개
- `.cmp-accordion__item` → `button[aria-controls]`(질문) + `#panel-id`(답변) 구조 파싱
- `TOP 10` 탭 제외, 전역 중복 제거 적용

**볼보**
- Selenium으로 `/kr/support/` 메인에서 topic 링크 수집
- topic → subtopic → body 텍스트 추출, 홀수줄=제목·짝수줄=설명 패턴으로 Q/A 쌍 구성
- 쿠키 배너 이후 텍스트 제외, breadcrumb·카테고리명과 동일한 항목 필터링

**BMW**
- Salesforce 포털(`bmw.co.kr/kr/s/`) 로드 20초 대기
- `//button[contains(text(),'도움말 더 보기')]` XPath로 버튼 반복 클릭 (총 176회, 5건씩 추가 로드)
- 전체 로드 완료 후 `document.body.innerText` 추출
- `[조회수]\n[질문]\n[답변]\n전체 도움말 보기` 패턴으로 파싱 → 908건 수집

**메르세데스-벤츠**
- MBMK(모빌리티 코리아) FAQ 페이지 로드 20초 대기
- 페이지 구조: `WB7-ACCORDION` / `WB7-ACCORDION-ITEM` Shadow DOM 컴포넌트
- Shadow DOM 특성으로 `document.body.innerText`에 Q1(첫 번째 질문)이 모든 항목 직전에 반복 삽입
- Q1을 구분자로 활용: Q1 직전 줄 = 질문, Q1 이후 줄 = 답변
- 로마 숫자(I., Ⅱ., Ⅲ., Ⅳ.) 카테고리 헤더 감지, 종료 마커("회원 가입하고 소식 받기") 기준 수집 중단 → 19건

**KGM**
- REST API 직접 호출 (Selenium 불필요)
- `getFaqContentList.do?pageIdx=1&rowsPerPage=300&categoryCd=` → 전체 117건의 `bbNo`(게시물 ID) + `title`(질문) + `categoryNm`(카테고리) 수집
- 각 항목에 대해 `getFaqContentDetail.do?bbNo=<bbNo>` → `content` 필드(HTML 답변) 수집
- BeautifulSoup으로 HTML 태그 제거 후 텍스트 추출 → 117건

#### 참고: 유사 프로젝트 수집 방식 (SKN23-1ST-2TEAM)

출처: [SKN23-1ST-2TEAM GitHub](https://github.com/SKNETWORKS-FAMILY-AICAMP/SKN23-1ST-2TEAM)

해당 팀은 현대자동차 FAQ를 Selenium DOM 파싱 방식으로 수집함.

| 항목 | 내용 |
|---|---|
| 수집 대상 | `www.hyundai.com/kr/ko/digital-customer-support/helpdesk/faq` |
| DOM 구조 | `.ui_accordion.acc_01 dl` → `dt`(질문) / `dd`(답변) |
| 동적 처리 | JS로 아코디언 항목에 `on` 클래스 추가 → 접힌 답변 강제 전개 |
| 페이지네이션 | `button.navi.next` 클릭, 비활성화 감지 시 종료 |
| 후처리 | SQL로 `[대분류 > 소분류]` 패턴 → `major_category` / `minor_category` 분리 |

본 프로젝트는 내부 GW API를 직접 호출해 283건을 수집. DOM 파싱 방식 대비 더 많은 데이터를 안정적으로 수집함.

---

### 5-2. 전처리

**스크립트**: `crawling/preprocess_faq.py`
**입력**: `data/faq/all_faq.csv` (1653건)
**출력**: `data/faq/preprocessing_faq.csv` (1595건)

#### 전처리 단계

| 단계 | 처리 내용 | 제거 건수 |
|---|---|---|
| 1. 짧은 Q/A 제거 | 볼보: 답변 30자 미만 제거 (카테고리명이 파싱 오류로 답변에 들어간 케이스) / 기타: 질문·답변 10자 미만 제거 | 23건 |
| 2. 볼보 Q/A 뒤바뀜 제거 | 질문 80자 초과 + 답변 40자 미만인 경우 파싱 오류로 판단해 제거 | 0건 (1단계에서 처리됨) |
| 3. 중복 질문 제거 | `question` 컬럼 기준 중복 제거, 첫 번째 항목 유지 (현대·제네시스 간 동일 FAQ 내용 중복 수록) | 35건 |
| 4. 줄바꿈 정규화 | `question`, `answer` 필드 내 `\n` → 공백 치환 (파일 줄 수 = 데이터 행 수 일치) | - |

#### 전처리 후 최종 현황

| 기업 | 원본 | 전처리 후 |
|---|---|---|
| 현대자동차 | 283건 | 283건 |
| 제네시스 | 232건 | 203건 (-29, 현대와 중복 제거) |
| 기아자동차 | 41건 | 40건 |
| 볼보 | 53건 | 30건 (-23, 파싱 오류 제거) |
| BMW | 908건 | 908건 |
| 메르세데스-벤츠 | 19건 | 17건 (-2, 짧은 Q/A 제거) |
| KGM | 117건 | 114건 (-3, 짧은 Q/A 제거) |
| **합계** | **1653건** | **1595건** |

---

### 5-3. CSV 스키마

| 컬럼 | 설명 | 예시 |
|---|---|---|
| `company` | 제조사명 | `현대자동차`, `볼보`, `BMW` |
| `category` | 대분류 | `전동화`, `FAQ`, `차량 정보` |
| `sub_category` | 소분류 (없으면 빈 값) | `배터리`, `충전`, `시작하기` |
| `question` | FAQ 질문 또는 아티클 제목 | `충전 시간 및 속도 이해` |
| `answer` | FAQ 답변 또는 아티클 요약 | `충전 시간과 속도는 다양한 요인의...` |
| `collected_at` | 수집 일자 | `2026-06-28` |
| `source_url` | 원본 URL (마지막 컬럼) | `https://www.volvocars.com/kr/...` |

> `sub_category`는 현대자동차만 채워짐 (나머지 기업은 빈 값). `source_url`은 클릭 오류 방지를 위해 마지막 컬럼으로 배치.

---

### 5-4. 파일 구조

```
crawling/
├── collect_faq.py           # 현대/기아/제네시스 수집 (FIELDS 고정 순서로 저장)
├── collect_bmw_volvo.py     # 볼보/BMW/메르세데스-벤츠 수집
├── collect_kgm.py           # KGM 수집 (REST API)
└── preprocess_faq.py        # 전처리 (all_faq → preprocessing_faq)

data/faq/                    # 수집 원본 및 중간 산출물
                             # ※ hyundai/kia/genesis 원본은 source_url↔collected_at 순서가
                             #   다른 파일과 다름 (collect_faq.py 수정 전 수집분, 재수집 시 정상화)
├── all_faq.csv              # 수집 원본 통합 (1653건)
├── preprocessing_faq.csv    # 전처리 완료본 (1595건)
├── hyundai_faq.csv          # 현대자동차 원본 (283건)
├── kia_faq.csv              # 기아자동차 원본 (41건)
├── genesis_faq.csv          # 제네시스 원본 (232건)
├── volvo_faq.csv            # 볼보 원본 (53건)
├── bmw_faq.csv              # BMW 원본 (908건)
├── mbenz_faq.csv            # 메르세데스-벤츠 원본 (19건)
└── kgm_faq.csv              # KGM 원본 (117건)

db/data/                     # 최종 정제 CSV ← 실사용 파일
├── hyundai_kia_faq.csv      # 현대(283) + 기아(40) = 323건
├── genesis_faq.csv          # 제네시스 203건
├── volvo_faq.csv            # 볼보 30건
├── bmw_faq.csv              # BMW 908건
├── mbenz_faq.csv            # 메르세데스-벤츠 17건
└── kgm_faq.csv              # KGM 114건
```

---

## 6. 정비소 위치

**용도**: 기업별 전기차 정비소(서비스센터) 위치 조회

| 항목 | 내용 |
|---|---|
| 추천 방법 | 현대·기아 공식 홈페이지 서비스센터 찾기 페이지 크롤링 |
| 출처 | [현대 서비스센터 찾기](https://www.hyundai.com/kr/ko/e/service-center) · [기아 서비스센터 찾기](https://www.kia.com/kr/service/center) |
| 필요 항목 | 기업명, 지점명, 시도, 주소, 전화번호, 전기차 전담 여부 |
| 수집 주기 | 최초 1회 수집 |
| 주의 | 지점 수가 많아 페이지 네이션 처리 필요. 전기차 전담 여부는 별도 표기되지 않을 수 있음 |

---

## 7. 차종별 차량 가격 (선택)

**용도**: 현대·기아 전기차 차종별 가격 비교

| 항목 | 내용 |
|---|---|
| 추천 방법 | **다나와 자동차** BeautifulSoup + Selenium 크롤링<br>→ 트림별 가격이 정리돼 있어 공식 SPA보다 파싱 용이 |
| 출처 | [다나와 자동차 신차견적](https://auto.danawa.com/newcar/) |
| 필요 항목 | 제조사, 차종명, 트림명, 가격, 연료 유형(전기) |
| 수집 주기 | 최초 1회 수집 (가격 변동 시 재수집) |
| 주의 | 시간 여유가 있을 경우에만 구현. 크롤링 전 robots.txt 확인 필요 |
