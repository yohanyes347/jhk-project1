# 당뇨 건강지표 예측 대시보드 (Diabetes Health Indicators Dashboard)

## 프로젝트 개요
- Streamlit 기반 당뇨병 위험도 예측 대시보드(`app.py`)
- 학습된 LightGBM 모델(`models/lgbm_diabetes_model.joblib`)과 확정 운영 임계값(`0.42` / `0.65`) 연동
- 만 나이의 BRFSS 연령 코드(`1~13`) 자동 변환, 키(`cm`)·몸무게(`kg`) 기반 BMI 자동 계산 및 WHO 구간 안내 제공

## 핵심 지표 및 기능
- **입력 지표:** `Age`(만 나이 변환 코드), `GenHlth`(1~5점 선택지 및 기준표), `HighBP`, `HighChol`, `BMI`(자동 계산 및 WHO 구간), `DiffWalk`, `HeartDiseaseorAttack`, `PhysActivity`, `Smoker`, `Fruits`, `Veggies`
- **파생변수(`add_interaction_features`):** `Metabolic_Risk_Count`, `Triple_Metabolic_Risk`, `Age_HighBP_Inter`, `Aged_Poor_Health`, `Cardio_DiffWalk_Inter`, `GenHlth_BMI_Inter`, `Unhealthy_Lifestyle_Score`, `Metabolic_BadLife_Inter`
- **운영 임계값:** `0.42`(1차 스크리닝, 고위험군 선별/일반 관찰), `0.65`(정밀 타겟팅, 집중 개입 대상/비대상)
- **화면 구성:** 예상 당뇨 위험 확률, 위험도 게이지, 현재 입력값 기준 위험 요인 및 관리 포인트 요약, `GenHlth`·`PhysActivity`·`Fruits`·`Veggies` 설명, 입력 지표 요약, 모델 주요 변수 중요도(Top 10)

## 작업 규칙 및 관례
1. 원본 데이터셋 및 저장된 모델 파일(`models/lgbm_diabetes_model.joblib`)은 임의로 수정하거나 삭제하지 않는다.
2. 모델 입력 피처 순서·개수 및 `add_interaction_features` 파생변수 정합성을 유지한다.
3. 기능 수정이나 추가는 한 번에 한 가지씩 구체적으로 반영한다.
4. `app.py` 수정 요청 시 기존 기능을 유지한 수정본 전체 코드를 제공한다.
5. 산출물과 문서는 프로젝트 폴더 기준으로 관리한다.
