# 기획

### **주제 : 스팀게임 추천**

## [스겜]

- 스팀 게임 추천
- 스피디한 게임 추천

### **개요**

- 빅데이터 기반 추천 알고리즘 사용한 스팀게임 추천 앱 (Native App)

### **타겟층**

- 스팀을 이용중인 게이머들

### **장점**

- 편의성, 손쉬운 접근성

### 주요 기능

- 인기 게임 추천
- 설문조사를 통한 성향에 맞는 게임 추천

### **고려 가능한 추가 기능**

- 커뮤니티적 기능
- 게임 리뷰

### 팀원 역할

- 김민관 : 안드로이드, CI/CD
- 박성호 : 안드로이드
- 윤혜원 : 안드로이드
- 이윤기 : 데이터셋 구축, 데이터베이스 구축, 백엔드
- 이호형 : 데이터셋 구축, 백엔드, 추천 알고리즘
- 서형준 : 추천 알고리즘, 백엔드

### 프로젝트 구조 / 기술 스택

![2222222222222222222222222222](https://s3.us-west-2.amazonaws.com/secure.notion-static.com/9fd79a8e-86db-4a2f-b41d-80c6582da8a4/Untitled.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=AKIAT73L2G45EIPT3X45%2F20220325%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20220325T022820Z&X-Amz-Expires=86400&X-Amz-Signature=e3af581f893bf184f0f6e2f9110d0e805bf1394ad85f325a0095a2dff45dbb6a&X-Amz-SignedHeaders=host&response-content-disposition=filename%20%3D%22Untitled.png%22&x-id=GetObject)

**임시 디자인**

![1111111111111111111111111111111111111111111](https://user-images.githubusercontent.com/44665707/158924218-36a72329-c350-4e14-b090-2b8c90b7e09b.png)

---

## 개발 규칙

### 코드 통일성

```java
if (b) {
	// 로그인 성공시
	
} else{
	//로그인 실패시

}

	// 전체 유저수만큼 반복
	for (int i = 0; i < user.size() ; i++) {

	}

// 로그인하는 함수 (args : 아이디)
void func(int args){
}
```

- 변수명, 함수명 : steamApi (camelCase 사용)
- 클래스명은 대문자로 시작
- 데이터 형식 맞추기



### Commit Convention

- Feat : 새로운 기능 추가
- Merge : 머지
- Fix : 버그 수정
- UI : 디자인 변경
- Doc : 문서 추가/변경/삭제

```
-- 간결하게 한두문장으로
commit -m "Feat : 로그인 기능 추가 - 김민관"
```



### 그  외

- 각자 맡은 부분 개발 후 노션에 정리하기
- 서로 서로 진행상황에 대한 공유 확실하게 하기

---

## 데이터 수집

### 자세한 사항은 [notion](https://www.notion.so/38b632c393294b729b29e4d3d002b5cb) 참조

### 게임 정보 수집 방법

- API (steam web api)
- Crawling (steam web page)



### 소규모, 독립적인 데이터 수집 완료

- [x]  인기 게임 목록(API & crawling)
- [x]  특정 게임의 상세 정보(API)
- [x]  특정 게임의 평가 목록(혹은 특정 게임에 평가를 남긴 유저 목록 혹은 특정 게임을 구매 또는 플레이한 유저 목록)(crawling)
- [x]  유저의 steam id 확인(API)
- [x]  특정 유저의 게임 목록 및 플레이 시간(API)
- [x]  특정 유저의 평가 목록(crawling)

- 이 외에도 어플 내에서의 설문 조사를 통해 유저에 대한 정보 및 성향(성별, 나이 등) 수집 가능


---
# Android
---
# MVVM + LiveData 모델

### ViewModel

View model을 사용하는 이유 : UI와 로직의 분리

ViewModel을 사용하게 된다면 UI관련 데이터를 액티비티와 프래그먼트로 부터 분리시킬 수 있다.

- 액티비티와 프래그먼트로 부터 데이터가 분리된다.
- 액티비티와 프래그먼트가 데이터 관리를 할 필요가 없으므로 UI 업데이트에만 집중할 수 있다.
- ViewModel에 있는 데이터는 액티비티와 프래그먼트의 수명주기에 영향을 받지 않는다.
- 프래그먼트 사이에서 데이터 공유가 훨씬 쉬워진다.

### LiveData
LiveData는 식별 가능한 데이터 홀더 클래스

- UI와 데이터 상태의 일치 보장
- 메모리 누출이 없음
- 비정상 종료가 없음
- 수명주기를 자동으로 관리
- 최신의 데이터 유지
- 기기회전 등 프래그먼트나 액티비티가 재생성되어도 데이터의 변화가 없음
- 
LiveData는 ViewModel과 함께 사용해야 그 효과가 커지게 됩니다. ViewModel 안에 있는 LiveData 객체를 DataBinding을 통해 UI에서 관찰만 할 수 있도록 만들면 액티비티나 프래그먼트에서 일일히 데이터를 갱신할 필요 없이 알아서 UI에 최신 데이터가 보이게 될 것입니다.

### Gradle Setting

```
apply plugin: 'kotlin-kapt'
android {
	...
    
    buildFeatures{
        dataBinding true
    }
    compileOptions {
        sourceCompatibility JavaVersion.VERSION_1_8
        targetCompatibility JavaVersion.VERSION_1_8
    }
    // For Kotlin projects
    kotlinOptions {
        jvmTarget = "1.8"
    }


}

dependencies{
	...
    
    def lifecycle_version = "2.2.0"
    // ViewModel
    implementation "androidx.lifecycle:lifecycle-viewmodel-ktx:$lifecycle_version"
    // LiveData
    implementation "androidx.lifecycle:lifecycle-livedata-ktx:$lifecycle_version"
    implementation "androidx.activity:activity-ktx:1.1.0"
}
```

---
## Dump data
 - Dump data는 makemigrations/migrate/runserver 시 자동으로 load 됩니다. 다만 초기 1회에 dump data가 load 되는 시간이 몇 분 정도 소요될 수 있습니다.
 - Local DB를 사용하신다면 settings.py에서 DB 설정을 변경하실 수 있습니다.
---

### 참조문서

[노션](https://verdant-smartphone-930.notion.site/A202-2143bd7ab62f486584d54a2ea9e83e26)

