# Section 8: 전체 22개 피처 종합 상관관계 및 다중공선성 분석 리포트

## 1. 당뇨병(`Diabetes_binary`) 주요 연관 변수
- **최상위 영향 요인:** `GenHlth` (일반 건강 상태, 0.29), `HighBP` (고혈압, 0.26), `BMI` (체질량지수, 0.23), `HighChol` (고콜레스테롤, 0.20), `Age` (연령, 0.18)[cite: 5]
- **사회경제적 역학 관계:** `Income` (-0.16) 및 `Education` (-0.12)은 당뇨 발병률과 뚜렷한 음(-)의 상관관계를 보여 사회경제적 지위(SES)가 건강에 미치는 영향 확인[cite: 5]

## 2. 주요 다중공선성(Multicollinearity) 진단
- **고도 상관 쌍:**
  - `GenHlth` & `PhysHlth` (상관계수 0.52): 체감 일반 건강과 신체 건강 악화 일수 간 강한 중복 정보[cite: 5]
  - `Education` & `Income` (상관계수 0.45): 교육 수준과 소득 간의 뚜렷한 양(+)의 상관관계[cite: 5]
  - `HighBP` & `Age` (0.34) / `HighChol` & `HighBP` (0.30): 연령 증가에 따른 만성질환 동반 상승 패턴[cite: 5]

## 3. 머신러닝 모델링 전략 (Action Plan)
- 선형 분류 모델(로지스틱 회귀 등) 적용 시 공선성으로 인한 계수 왜곡 방지를 위해 **릿지(Ridge) 또는 라스소(Lasso) 규제** 필수 적용
- 다중공선성에 강건한 트리 기반 모델(Random Forest, XGBoost 등)을 함께 도입하여 변수 중요도(`Feature Importance`) 교차 검증 수행
