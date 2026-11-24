from pathlib import Path
import joblib
import pandas as pd
import streamlit as st

st.set_page_config(page_title="당뇨 건강지표 예측 대시보드", layout="wide")


def age_to_brfss_code(real_age: int) -> int:
    """만 나이(세)를 BRFSS 기준 연령 코드(1~13)로 변환"""
    if real_age < 25:
        return 1
    elif real_age < 30:
        return 2
    elif real_age < 35:
        return 3
    elif real_age < 40:
        return 4
    elif real_age < 45:
        return 5
    elif real_age < 50:
        return 6
    elif real_age < 55:
        return 7
    elif real_age < 60:
        return 8
    elif real_age < 65:
        return 9
    elif real_age < 70:
        return 10
    elif real_age < 75:
        return 11
    elif real_age < 80:
        return 12
    else:
        return 13


def add_interaction_features(data: pd.DataFrame) -> pd.DataFrame:
    d = data.copy()

    is_obese = (d["BMI"] >= 30).astype(int) if "BMI" in d.columns else None
    age_60plus = (d["Age"] >= 9).astype(int) if "Age" in d.columns else None
    genhlth_risk = (d["GenHlth"] >= 3).astype(int) if "GenHlth" in d.columns else None

    metabolic_parts = []
    if "HighBP" in d.columns:
        metabolic_parts.append(d["HighBP"])
    if "HighChol" in d.columns:
        metabolic_parts.append(d["HighChol"])
    if is_obese is not None:
        metabolic_parts.append(is_obese)

    if metabolic_parts:
        d["Metabolic_Risk_Count"] = sum(metabolic_parts)
        if len(metabolic_parts) == 3:
            d["Triple_Metabolic_Risk"] = (d["Metabolic_Risk_Count"] == 3).astype(int)

    if {"Age", "HighBP"}.issubset(d.columns):
        d["Age_HighBP_Inter"] = d["Age"] * d["HighBP"]
    if age_60plus is not None and genhlth_risk is not None:
        d["Aged_Poor_Health"] = age_60plus * genhlth_risk

    cardio_col = (
        "CardioDisease"
        if "CardioDisease" in d.columns
        else ("HeartDiseaseorAttack" if "HeartDiseaseorAttack" in d.columns else None)
    )
    if cardio_col and "DiffWalk" in d.columns:
        d["Cardio_DiffWalk_Inter"] = d[cardio_col] * d["DiffWalk"]
    if {"GenHlth", "BMI"}.issubset(d.columns):
        d["GenHlth_BMI_Inter"] = d["GenHlth"] * d["BMI"]

    life_parts = []
    if "PhysActivity" in d.columns:
        life_parts.append(1 - d["PhysActivity"])
    if "Smoker" in d.columns:
        life_parts.append(d["Smoker"])
    if "Fruits" in d.columns:
        life_parts.append(1 - d["Fruits"])
    if "Veggies" in d.columns:
        life_parts.append(1 - d["Veggies"])

    if life_parts:
        d["Unhealthy_Lifestyle_Score"] = sum(life_parts)
        if "Metabolic_Risk_Count" in d.columns:
            d["Metabolic_BadLife_Inter"] = (
                (d["Metabolic_Risk_Count"] >= 2) & (d["Unhealthy_Lifestyle_Score"] >= 3)
            ).astype(int)

    return d


def summarize_risk_factors(raw_input: dict, real_age: int) -> tuple[list[str], list[str], int, int]:
    """현재 입력값 기준 위험 요인 목록과 관리 포인트 반환"""
    factors = []
    tips = []

    if raw_input["HighBP"] == 1:
        factors.append("고혈압 진단 이력 (HighBP = 1)")
        tips.append("혈압 수치 주기적 측정 및 나트륨 섭취 관리")
    if raw_input["HighChol"] == 1:
        factors.append("고콜레스테롤 진단 이력 (HighChol = 1)")
        tips.append("포화지방·트랜스지방 섭취 줄이기 및 지질 검사 확인")
    if raw_input["BMI"] >= 30:
        factors.append(f"비만 범위 BMI ({raw_input['BMI']:.1f} ≥ 30.0)")
        tips.append("체중 감량 및 식단·유산소 운동 병행")
    elif raw_input["BMI"] >= 25:
        factors.append(f"과체중 범위 BMI ({raw_input['BMI']:.1f} ≥ 25.0)")
    if raw_input["GenHlth"] >= 4:
        factors.append(f"주관적 건강 상태 저하 (GenHlth = {raw_input['GenHlth']}/5, 나쁨~매우나쁨)")
        tips.append("전반적 컨디션 저하 원인 확인 및 정기 건강검진 권장")
    elif raw_input["GenHlth"] == 3:
        factors.append("주관적 건강 상태 보통 이하 (GenHlth = 3/5)")
    if real_age >= 60:
        factors.append(f"만 60세 이상 연령대 (만 {real_age}세, Age ≥ 9)")
        tips.append("연령대 고려 정기 혈당·대사 지표 모니터링")
    if raw_input["HeartDiseaseorAttack"] == 1:
        factors.append("심혈관 질환 이력 (HeartDiseaseorAttack = 1)")
        tips.append("심혈관·대사 동반 위험 관리 및 전문의 상담")
    if raw_input["DiffWalk"] == 1:
        factors.append("보행 어려움 (DiffWalk = 1)")
        tips.append("관절·보행 부담을 줄인 안전한 신체 활동 선택")
    if raw_input["PhysActivity"] == 0:
        factors.append("신체 활동 부족 (PhysActivity = 0)")
        tips.append("주 150분 내외 가벼운 걷기 등 규칙적 활동 습관화")
    if raw_input["Smoker"] == 1:
        factors.append("흡연 중 (Smoker = 1)")
        tips.append("금연 실천 및 금연 지원 프로그램 활용")
    if raw_input["Fruits"] == 0:
        factors.append("과일 섭취 부족 (Fruits = 0)")
    if raw_input["Veggies"] == 0:
        factors.append("채소 섭취 부족 (Veggies = 0)")

    if (raw_input["Fruits"] == 0 or raw_input["Veggies"] == 0):
        tips.append("식이섬유가 풍부한 채소·과일 섭취 늘리기")

    metabolic_score = (
        int(raw_input["HighBP"] == 1)
        + int(raw_input["HighChol"] == 1)
        + int(raw_input["BMI"] >= 30)
    )
    lifestyle_score = (
        int(raw_input["PhysActivity"] == 0)
        + int(raw_input["Smoker"] == 1)
        + int(raw_input["Fruits"] == 0)
        + int(raw_input["Veggies"] == 0)
    )

    # 중복 제거 순서 유지
    unique_tips = list(dict.fromkeys(tips))
    return factors, unique_tips, metabolic_score, lifestyle_score


@st.cache_resource
def load_model_bundle(model_path: str):
    return joblib.load(model_path)


st.title("당뇨 건강지표 기반 위험도 예측 대시보드")
st.caption("학습된 LightGBM 모델과 확정 임계값(0.42 / 0.65)을 연동한 예측 화면입니다.")

model_file = Path(__file__).resolve().parent / "models" / "lgbm_diabetes_model.joblib"

# 사이드바 건강지표 입력
st.sidebar.header("건강지표 입력")
real_age = st.sidebar.number_input("만 나이 (세)", min_value=18, max_value=110, value=52, step=1)
age_code = age_to_brfss_code(int(real_age))
st.sidebar.caption(f"자동 변환된 연령 코드 (Age): **{age_code}** / 13")

gen_hlth = st.sidebar.slider("일반 건강 상태 (GenHlth, 1=매우좋음 ~ 5=매우나쁨)", 1, 5, 3)
high_bp = st.sidebar.selectbox("고혈압 여부 (HighBP)", options=[0, 1], format_func=lambda x: "예 (1)" if x == 1 else "아니오 (0)")
high_chol = st.sidebar.selectbox("고콜레스테롤 여부 (HighChol)", options=[0, 1], format_func=lambda x: "예 (1)" if x == 1 else "아니오 (0)")
bmi = st.sidebar.number_input("BMI", min_value=12.0, max_value=60.0, value=28.0, step=0.5)
diff_walk = st.sidebar.selectbox("보행 어려움 (DiffWalk)", options=[0, 1], format_func=lambda x: "예 (1)" if x == 1 else "아니오 (0)")
heart_disease = st.sidebar.selectbox("심혈관 질환 (HeartDiseaseorAttack)", options=[0, 1], format_func=lambda x: "예 (1)" if x == 1 else "아니오 (0)")
phys_activity = st.sidebar.selectbox("신체 활동 (PhysActivity)", options=[0, 1], format_func=lambda x: "예 (1)" if x == 1 else "아니오 (0)")
smoker = st.sidebar.selectbox("흡연 여부 (Smoker)", options=[0, 1], format_func=lambda x: "예 (1)" if x == 1 else "아니오 (0)")
fruits = st.sidebar.selectbox("과일 섭취 (Fruits)", options=[0, 1], format_func=lambda x: "예 (1)" if x == 1 else "아니오 (0)")
veggies = st.sidebar.selectbox("채소 섭취 (Veggies)", options=[0, 1], format_func=lambda x: "예 (1)" if x == 1 else "아니오 (0)")

if not model_file.exists():
    st.warning(f"모델 파일이 아직 없습니다: `{model_file}`")
    st.stop()

bundle = load_model_bundle(str(model_file))
model = bundle["model"]
feature_columns = bundle["feature_columns"]
raw_columns = bundle.get("raw_columns", [])
thresholds = bundle.get("thresholds", {"screening": 0.42, "baseline": 0.50, "targeting": 0.65})

raw_input = {
    "HighBP": high_bp,
    "HighChol": high_chol,
    "BMI": bmi,
    "Smoker": smoker,
    "HeartDiseaseorAttack": heart_disease,
    "PhysActivity": phys_activity,
    "Fruits": fruits,
    "Veggies": veggies,
    "GenHlth": gen_hlth,
    "DiffWalk": diff_walk,
    "Age": age_code,
}

full_raw = {col: raw_input.get(col, 0) for col in raw_columns} if raw_columns else raw_input
raw_df = pd.DataFrame([full_raw])
fe_df = add_interaction_features(raw_df)
X_infer = fe_df.reindex(columns=feature_columns, fill_value=0)

prob = float(model.predict_proba(X_infer)[0][1])
prob_pct = prob * 100.0

th_screen = float(thresholds.get("screening", 0.42))
th_target = float(thresholds.get("targeting", 0.65))

# 상단 핵심 지표
col1, col2, col3 = st.columns(3)
col1.metric("예상 당뇨 위험 확률", f"{prob_pct:.1f}%")
col2.metric(
    f"1차 스크리닝 (≥ {th_screen:.2f})",
    "고위험군 선별" if prob >= th_screen else "일반 관찰",
)
col3.metric(
    f"정밀 타겟팅 (≥ {th_target:.2f})",
    "집중 개입 대상" if prob >= th_target else "비대상",
)

# 위험도 게이지(진행바 + 구간 표시)
st.subheader("위험도 게이지 및 운영 구간")
progress_val = min(max(prob, 0.0), 1.0)
st.progress(progress_val, text=f"현재 예측 위험도: {prob_pct:.1f}% (1차 스크리닝 기준 {th_screen*100:.0f}% / 정밀 타겟팅 기준 {th_target*100:.0f}%)")

if prob >= th_target:
    st.error(f"현재 구간: **정밀 타겟팅 구간 (≥ {th_target:.2f})** — 오탐을 줄이고 집중 개입이 필요한 고위험군입니다.")
elif prob >= th_screen:
    st.warning(f"현재 구간: **1차 스크리닝 구간 ({th_screen:.2f} ~ {th_target:.2f} 미만)** — 미탐을 줄이기 위해 폭넓게 선별하는 1차 관찰·상담 대상입니다.")
else:
    st.info(f"현재 구간: **일반 관찰 구간 (< {th_screen:.2f})** — 두 운영 임계값 기준선 아래로 일반 건강관리 흐름에 해당합니다.")

# 현재 입력값 기준 위험 요인 요약
st.subheader("현재 입력값 기준 위험 요인 요약")
factors, tips, metabolic_score, lifestyle_score = summarize_risk_factors(raw_input, int(real_age))

rf_col1, rf_col2, rf_col3 = st.columns(3)
rf_col1.metric("감지된 위험 요인 수", f"{len(factors)}개")
rf_col2.metric("대사 위험 요인 점수", f"{metabolic_score} / 3")
rf_col3.metric("불건강 생활습관 점수", f"{lifestyle_score} / 4")

detail_col1, detail_col2 = st.columns(2)
with detail_col1:
    with st.container(border=True):
        st.markdown("#### 감지된 주요 위험 요인")
        if factors:
            for item in factors:
                st.markdown(f"- {item}")
        else:
            st.markdown("- 현재 입력 기준 뚜렷한 위험 요인이 감지되지 않았습니다.")

with detail_col2:
    with st.container(border=True):
        st.markdown("#### 참고 관리 포인트")
        if tips:
            for tip in tips:
                st.markdown(f"- {tip}")
        else:
            st.markdown("- 현재 건강 습관과 지표를 꾸준히 유지해 보세요.")

# 운영 기준선(0.42, 0.65) 설명 카드
st.subheader("운영 임계값 기준선 안내")
guide_col1, guide_col2 = st.columns(2)

with guide_col1:
    with st.container(border=True):
        st.markdown(f"### 1차 스크리닝 · 임계값 `{th_screen:.2f}`")
        st.markdown("- **목적:** 실제 당뇨 위험군을 놓치지 않도록 **미탐(FN) 최소화(High Recall)**")
        st.markdown("- **테스트셋 참고:** 약 **42.6%** 선별, **Recall 0.8580** 수준")
        st.markdown("- **활용:** 폭넓은 사전 안내, 생활습관 점검 및 1차 선별")

with guide_col2:
    with st.container(border=True):
        st.markdown(f"### 정밀 타겟팅 · 임계값 `{th_target:.2f}`")
        st.markdown("- **목적:** **오탐(FP) 및 개입 비용 절감**, 정밀 개입 대상 압축")
        st.markdown("- **테스트셋 참고:** 약 **22.6%** 선별, **Precision 0.3818 / F1 0.4724** 수준")
        st.markdown("- **활용:** 자원이 제한된 심화 상담·집중 관리 대상 선정")

st.subheader("입력 지표 요약 (만 나이 및 변환 연령 코드 포함)")
summary_df = pd.DataFrame([{"Age_Years": int(real_age), **raw_input}])
st.dataframe(summary_df, width="stretch")

if hasattr(model, "feature_importances_"):
    st.subheader("모델 주요 변수 중요도 (Top 10)")
    imp_df = (
        pd.DataFrame({
            "변수명": feature_columns,
            "중요도": model.feature_importances_,
        })
        .sort_values("중요도", ascending=False)
        .head(10)
    )
    st.dataframe(imp_df, width="stretch")
