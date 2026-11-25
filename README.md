깃랩 저장소 링크
https://kdt-gitlab.elice.io/aba_track/class_04/aba4_project1/team2/jhk-project1

당뇨 건강지표 기반 위험도 예측 및 대시보드 링크
https://jhk-project1-fw3nxuzab3usne5bnurjtw.streamlit.app/

# 당뇨 건강지표 기반 위험도 예측 및 대시보드

## 📁 데이터 출처 및 폴더별 산출물 구성

* **원본 데이터 (`data/raw/` — GitLab 및 제출용 ZIP 제외)**

  * `diabetes_binary_health_indicators_BRFSS2015.csv`: CDC BRFSS 2015 당뇨 건강지표 원본 설문 데이터(253,680행 × 22열)로, 로컬 환경에서만 읽기 전용으로 보관하고 `.gitignore` 및 `git rm --cached`로 제출 압축 파일에서는 제외함.

* **중간 분석 및 단계별 산출물 (`data/interim/`)**

  * **루트 공통 요약 및 레지스트리 (`data/interim/`)**

    * `diabetes_interim.csv`: 초기 결측치·기본 분포 점검을 거친 중간 저장 데이터.

    * `diabetes_target_distribution.csv`: 타겟 변수(`Diabetes_binary`) 정상(0) vs 당뇨(1) 클래스 불균형 비율 요약 테이블.

    * `diabetes_by_age.csv`: 연령대(`Age` 1~13단계)별 당뇨 유병률 집계 테이블.

    * `diabetes_correlation_summary.csv`: 주요 수치형·서열형·이진 변수 간 상관계수 요약 테이블.

    * `feature_registry.json`: 원본 변수와 구간화(`*_Group`)·통합(`CardioDisease`) 변수 공존 시 다중공선성과 중복 투입을 막기 위한 분석·모델링용 피처 셋 정의 파일.

  * **Part 1 — 심층 EDA 및 인구통계·사회경제·다중위험 분석 (`data/interim/part1EDA1/`)**

    * `sec1_demographics/age_sex_diabetes_rate.csv`: 성별(`Sex`) 및 연령대(`Age`) 교차 집단별 표본 수와 당뇨 발병률 집계표.

    * `sec2_metabolic_interaction/metabolic_synergy_rate.csv`: 고혈압·고콜레스테롤·비만 등 대사 위험 요인 중첩에 따른 시너지 발병률 요약표.

    * `sec3_lifestyle_cluster/lifestyle_cluster_rate.csv`: 신체활동·흡연·과일·채소 섭취 등 생활습관 군집별 당뇨 발병률 요약표.

    * `sec4_socioeconomic/income_education_health_matrix.csv`: 소득 수준(`Income`) × 교육 수준(`Education`) × 건강 상태 교차 행렬 집계표.

    * `sec5_super_risk/logistic_odds_ratio_super_risk.csv`: 주요 위험 요인 및 고위험 조합의 단변량·다변량 로지스틱 회귀 오즈비(Odds Ratio) 산출 결과.

  * **Part 2 — 변수 유형별 시각화 및 인사이트 리포트 (`data/interim/part2/`, `data/interim/Part2EDA2/`)**

    * `01_binary_14_features_diabetes_relation.png`: 이진형 변수 14종의 0 vs 1 당뇨 발병률 비교 및 상관계수 차트.

    * `02_ordinal_4_features_diabetes_relation.png`: 서열형(등급) 변수 4종(`GenHlth`, `Age`, `Education`, `Income`)의 단계별 당뇨 발병률 추이 차트.

    * `03_continuous_3_features_diabetes_relation.png`: 연속형 수치 변수 3종(`BMI`, `MentHlth`, `PhysHlth`)의 분포 비교 및 구간별 발병률 차트.

    * `sec1` ~ `sec6` 하위 산출물: 섹션별 분포·박스플롯·상관관계 히트맵 차트 및 `eda_insights_report.md` 요약 리포트.

  * **Part 3 — 파생변수 생성 및 통계적 유효성 검증 (`data/interim/Part3Features/`)**

    * `diabetes_with_interactions.csv`: 대사 위험 누적(`Metabolic_Risk_Count`), 삼중 대사 위험(`Triple_Metabolic_Risk`), 연령·고혈압 교호작용(`Age_HighBP_Inter`), 고령·건강악화(`Aged_Poor_Health`), 심혈관·보행장애(`Cardio_DiffWalk_Inter`), 건강체감·BMI(`GenHlth_BMI_Inter`), 비건강 생활습관 점수(`Unhealthy_Lifestyle_Score`) 등 상호작용 파생변수를 결합한 중간 데이터.

    * `interaction_features_eval.csv`: 개별 파생변수 추가 전후 성능 및 통계적 기여도 비교 평가표.

    * `odds_ratio_univariate.csv`: 전체 원본·파생 변수별 단변량 오즈비(OR) 및 신뢰구간 검증 결과표.

  * **Part 4 — 모델 비교·교차검증 및 운영 임계값 산출물 (`data/interim/Part4Modeling/`)**

    * 로지스틱 회귀, 랜덤 포레스트, LightGBM 등 후보 모델의 K-Fold 교차검증 성능 비교 결과 및 운영 목적별 최종 임계값(1차 스크리닝 `0.42` / 정밀 타겟팅 `0.65`) 검증 산출물.

* **전처리 완료 및 모델 학습용 최종 데이터 (`data/processed/`)**

  * `diabetes_binary_health_indicators_cleaned.csv`: 전 컬럼 결측치 점검 및 도메인 정상 범위(BMI `10 < BMI < 60`, 연령 `1~13`, 건강 일수 `0~30`일 등) 이탈 이상치를 정제한 기본 클리닝 데이터(252,812행).

  * `diabetes_binary_with_bmi_group.csv`: 정제 데이터에 WHO 기준 BMI 구간화(`BMI_Group`) 파생 컬럼을 추가한 데이터.

  * `diabetes_binary_with_bmi_and_age_group.csv`: BMI 구간화(`BMI_Group`)와 연령대 구간화(`Age_Group`) 파생 컬럼을 함께 추가한 데이터.

  * `diabetes_binary_with_health_groups.csv`: 신체 건강 악화 일수(`PhysHlth_Group`) 및 정신 건강 악화 일수(`MentHlth_Group`) 구간화 컬럼을 추가한 데이터.

  * `diabetes_binary_edu_merged_age_ordinal_cardio_combined.csv`: 희소 등급인 `Education` 1·2등급 병합, `Age` 13단계 서열 척도 유지, `Stroke`와 `HeartDiseaseorAttack`을 `CardioDisease`로 통합한 전처리 데이터.

  * `diabetes_binary_edu_cardio_bmi_outlier_removed_binned.csv`: BMI 극단 이상치 제거, `Education` 1·2등급 병합(1~5단계), `CardioDisease` 통합, `BMI_Group`·`MentHlth_Group`·`PhysHlth_Group` 3종 범주화를 모두 반영한 핵심 기준 데이터셋(252,812행 × 24열).

  * `diabetes_binary_edu_cardio_bmi5_health3_binned.csv`: BMI 5단계 및 건강 악화 일수 3단계 구간화 기준을 반영해 실험·비교용으로 생성한 데이터셋.

* **학습 모델 및 대시보드 서비스 (`models/`, `app.py`)**

  * `models/lgbm_diabetes_model.joblib`: `data/processed/` 전처리 데이터와 상호작용 파생변수를 기반으로 학습한 최종 LightGBM 모델 번들(피처 목록 및 임계값 포함).

  * `app.py`: 핵심 건강·대사·생활습관 11개 입력 위젯을 통해 예상 당뇨 위험 확률과 운영 구간(일반 관찰 / 1차 스크리닝 `≥ 0.42` / 정밀 타겟팅 `≥ 0.65`)을 안내하는 Streamlit 대시보드.



