# PLUG 자료실

우리아이와 세상의 연결, **PLUG**. 부모님이 아이의 감각·움직임·발달을 이해하는 데 도움이 되도록 강의·교육 자료를 주제별로 정리한 사이트입니다.

- PC와 모바일 모두 지원, 밝은/어두운 화면 자동 대응
- 왼쪽 메뉴: 큰 카테고리 7개 (감각과 지각 · 심리운동 · 심리운동 현장적용 · 아동 발달 · 뇌 발달의 기초 · 뇌의 구조와 네트워크 · 몸속 환경과 뇌)
- 검색, 확인 퀴즈(객관식·단답형), 접고 펼치는 '자세히 읽기'

## 폴더 구성

| 경로 | 내용 |
|---|---|
| `data/site-data.json` | 사이트의 모든 내용(사이트 문구, 로고, 색상, 카테고리, 자료). **내용 수정은 이 파일에서 합니다.** |
| `src/template.html` | 화면 디자인과 동작 코드 (`__SITE_DATA__` 자리에 데이터가 들어갑니다) |
| `build_site.py` | 위 두 파일을 합쳐 `index.html`을 만드는 스크립트 |
| `index.html` | 완성된 사이트 파일 (브라우저에서 바로 열 수 있음) |
| `.github/workflows/pages.yml` | `main`에 올리면 자동으로 사이트를 다시 만들어 GitHub Pages에 게시 |
| `tools/` | 원본 HWP·HWPX·PDF에서 내용을 뽑아낸 변환 스크립트 (참고용) |

## 인터넷에 공개하기 (GitHub Pages)

1. 이 저장소의 **Settings → Pages**로 이동합니다.
2. **Build and deployment → Source**를 **GitHub Actions**로 선택합니다.
3. `main` 브랜치에 커밋이 올라가면 **Actions** 탭에서 배포가 진행되고, 끝나면 `https://<계정이름>.github.io/<저장소이름>/` 주소로 누구나 볼 수 있습니다.

> 무료 계정에서 GitHub Pages는 **공개(Public) 저장소**에서만 쓸 수 있습니다. 공개 저장소는 코드와 `data/site-data.json`의 내용이 모두 공개된다는 점을 확인하고 사용하세요.

## 내용 고치기

### GitHub 웹에서 바로 고치기
1. `data/site-data.json`을 열고 연필(✏️) 아이콘을 눌러 수정합니다.
2. **Commit changes**를 누르면 몇 분 뒤 사이트에 반영됩니다.

데이터 구조 요약:

```text
site        사이트 이름, 한 줄 소개(tagline), 첫 화면 제목(heading)·안내문(intro), 로고(logo / logoDark, data URI)
theme       brand(메인색), accent(강조색), header(머리글 배경색)
categories  id, name(이름), group(큰 카테고리 이름), color, desc(설명)  ← 배열 순서 = 메뉴 순서
posts       id, cat(카테고리 id), title, intro(도입 글), sections[...]   ← 배열 순서 = 카테고리 안 순서
  sections  title, objectives, contents, easy, key, caution, terms, tip,
            detail(자세히 읽기), summary / summaryOutline / summaryTable, quiz[...]
  quiz      q(문제), options(보기), answer(정답 번호 또는 단답형 정답 글자), explain(해설), passage(제시문)
```

- 큰 카테고리는 카테고리의 `group` 값이 같은 것끼리 묶입니다. 새 이름을 쓰면 새 큰 카테고리가 생깁니다.
- `caution`, `summary`에서 `## `로 시작하는 줄은 소제목이 됩니다.
- `detail`에서 `1. `로 시작하면 큰 제목, `1) `은 작은 제목, `- `는 항목입니다.

### 내 컴퓨터에서 고치기
```bash
python build_site.py      # index.html 다시 만들기 (Python 3, 추가 설치 없음)
```
`index.html`을 브라우저로 열면 바로 확인할 수 있습니다. 파일로 열었을 때는 화면 오른쪽 위에 **편집 모드** 버튼이 보여 화면에서 미리 고쳐 볼 수 있지만, 여기서 바꾼 내용은 저장되지 않으므로 최종 수정은 `data/site-data.json`에 반영해야 합니다.

## 원본 자료

원본 HWP·PDF 파일은 저장소에 포함하지 않습니다(`.gitignore`). 교육자료(뇌 발달의 기초 / 뇌의 구조와 네트워크 / 몸속 환경과 뇌)는 원본에 '사내 직원 교육 교재'로 표기되어 있으니, 공개 전에 외부 공개가 가능한 자료인지 확인하세요.

이 사이트의 내용은 교육용 정보이며 아이의 진단이나 치료를 대신하지 않습니다.
