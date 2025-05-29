[![Tests](https://github.com/mupaistudio/ckanext-mtcui/workflows/Tests/badge.svg?branch=main)](https://github.com/mupaistudio/ckanext-mtcui/actions)

# CKAN Extension: ckanext-mtcui

CKAN의 사용자 인터페이스를 개선하기 위한 확장 모듈입니다.

## 기능

### 현재 구현된 기능
1. 기본 Blueprint 페이지 (`/mtcui/page`)
2. 간단한 액션 함수 (`mtcui_get_sum`)
   - 두 숫자의 합을 계산하는 API 엔드포인트

### 구현 예정 기능
1. 사용자 인터페이스 개선
   - 메인 페이지 커스터마이징
   - 데이터셋 페이지 개선
   - 네비게이션 메뉴 추가
   - 테마 적용

## 설치 방법

1. 확장 모듈 설치:
```bash
cd /usr/lib/ckan/default/src
git clone https://github.com/your-org/ckanext-mtcui.git
cd ckanext-mtcui
pip install -e .
```

2. CKAN 설정 파일(`/etc/ckan/default/ckan.ini`)에 플러그인 추가:
```ini
ckan.plugins = mtcui
```

3. CKAN 서비스 재시작:
```bash
sudo systemctl restart apache2
```

## 개발

### 테스트 실행
```bash
cd /usr/lib/ckan/default/src/ckanext-mtcui
source /usr/lib/ckan/default/bin/activate
pytest ckanext/mtcui/tests/
```

### 프로젝트 구조
```
ckanext-mtcui/
├── ckanext/
│   └── mtcui/
│       ├── logic/
│       │   ├── action.py    # API 액션 함수
│       │   ├── auth.py      # 인증 함수
│       │   └── validators.py # 데이터 검증
│       ├── templates/       # 템플릿 파일
│       ├── tests/          # 테스트 코드
│       ├── views.py        # Blueprint 정의
│       └── plugin.py       # 플러그인 설정
├── setup.py
└── README.md
```

## CKAN 버전 호환성

| CKAN 버전 | 호환성 |
|-----------|--------|
| 2.11.x    | yes    |
| 2.10.x    | not tested |
| 2.9.x     | not tested |
| 2.8.x     | not tested |
| 2.7.x     | not tested |
| 2.6.x     | not tested |

## 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다.


## Requirements

**TODO:** For example, you might want to mention here which versions of CKAN this
extension works with.

If your extension works across different versions you can add the following table:

Compatibility with core CKAN versions:

| CKAN version    | Compatible?   |
| --------------- | ------------- |
| 2.6 and earlier | not tested    |
| 2.7             | not tested    |
| 2.8             | not tested    |
| 2.9             | not tested    |

Suggested values:

* "yes"
* "not tested" - I can't think of a reason why it wouldn't work
* "not yet" - there is an intention to get it working
* "no"


## Config settings

None at present

**TODO:** Document any optional config settings here. For example:

	# The minimum number of hours to wait before re-checking a resource
	# (optional, default: 24).
	ckanext.mtcui.some_setting = some_default_value


## Developer installation

To install ckanext-mtcui for development, activate your CKAN virtualenv and
do:

    git clone https://github.com/mupaistudio/ckanext-mtcui.git
    cd ckanext-mtcui
    pip install -e .
    pip install -r dev-requirements.txt


## Tests

To run the tests, do:

    pytest --ckan-ini=test.ini


## Releasing a new version of ckanext-mtcui

If ckanext-mtcui should be available on PyPI you can follow these steps to publish a new version:

1. Update the version number in the `pyproject.toml` file. See [PEP 440](http://legacy.python.org/dev/peps/pep-0440/#public-version-identifiers) for how to choose version numbers.

2. Make sure you have the latest version of necessary packages:

    pip install --upgrade setuptools wheel twine

3. Create a source and binary distributions of the new version:

       python -m build && twine check dist/*

   Fix any errors you get.

4. Upload the source distribution to PyPI:

       twine upload dist/*

5. Commit any outstanding changes:

       git commit -a
       git push

6. Tag the new release of the project on GitHub with the version number from
   the `setup.py` file. For example if the version number in `setup.py` is
   0.0.1 then do:

       git tag 0.0.1
       git push --tags

## License

[AGPL](https://www.gnu.org/licenses/agpl-3.0.en.html)
