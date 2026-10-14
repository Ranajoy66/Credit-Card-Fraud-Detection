import streamlit as st
import pandas as pd
import joblib
import random
from textwrap import dedent


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="FraudGuard | Credit Card Fraud Detection",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# HELPER FUNCTION FOR HTML
# ============================================================

def render_html(html):
    """
    Render custom HTML using Streamlit's native HTML renderer.
    """
    st.html(dedent(html))


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

        /* ---------- Global ---------- */

        .stApp {
            background:
                radial-gradient(
                    circle at 10% 10%,
                    rgba(59, 130, 246, 0.08),
                    transparent 30%
                ),
                radial-gradient(
                    circle at 90% 20%,
                    rgba(139, 92, 246, 0.07),
                    transparent 30%
                ),
                #0b1120;
            color: #e5e7eb;
        }

        .block-container {
            padding-top: 2rem;
            padding-bottom: 3rem;
            max-width: 1400px;
        }


        /* ---------- Sidebar ---------- */

        section[data-testid="stSidebar"] {
            background: #080d1a;
            border-right: 1px solid rgba(148, 163, 184, 0.12);
        }

        .sidebar-logo {
            font-size: 25px;
            font-weight: 800;
            color: #f8fafc;
            margin-bottom: 3px;
        }

        .sidebar-subtitle {
            color: #64748b;
            font-size: 13px;
            margin-bottom: 30px;
        }

        .sidebar-section {
            color: #64748b;
            font-size: 11px;
            font-weight: 700;
            letter-spacing: 1.5px;
            text-transform: uppercase;
            margin-top: 25px;
            margin-bottom: 10px;
        }


        /* ---------- Header ---------- */

        .top-badge {
            display: inline-block;
            padding: 6px 12px;
            border-radius: 999px;
            background: rgba(34, 197, 94, 0.10);
            border: 1px solid rgba(34, 197, 94, 0.25);
            color: #4ade80;
            font-size: 12px;
            font-weight: 700;
            margin-bottom: 14px;
        }

        .main-title {
            font-size: 42px;
            font-weight: 800;
            letter-spacing: -1.5px;
            color: #f8fafc;
            margin-bottom: 5px;
        }

        .main-subtitle {
            color: #94a3b8;
            font-size: 16px;
            margin-bottom: 25px;
        }


        /* ---------- Cards ---------- */

        .glass-card {
            background: rgba(15, 23, 42, 0.72);
            border: 1px solid rgba(148, 163, 184, 0.12);
            border-radius: 18px;
            padding: 22px;
            box-shadow: 0 12px 35px rgba(0, 0, 0, 0.20);
        }

        .metric-card {
            background: linear-gradient(
                135deg,
                rgba(30, 41, 59, 0.85),
                rgba(15, 23, 42, 0.85)
            );
            border: 1px solid rgba(148, 163, 184, 0.12);
            border-radius: 16px;
            padding: 20px;
            min-height: 115px;
        }

        .metric-label {
            color: #94a3b8;
            font-size: 13px;
            margin-bottom: 7px;
            letter-spacing: 0.4px;
        }

        .metric-value {
            color: #f8fafc;
            font-size: 27px;
            font-weight: 750;
        }

        .metric-description {
            color: #64748b;
            font-size: 12px;
            margin-top: 5px;
        }


        /* ---------- Section Titles ---------- */

        .section-title {
            color: #f8fafc;
            font-size: 21px;
            font-weight: 700;
            margin-top: 10px;
            margin-bottom: 5px;
        }

        .section-description {
            color: #64748b;
            font-size: 13px;
            margin-bottom: 18px;
        }


        /* ---------- Result ---------- */

        .result-card {
            border-radius: 20px;
            padding: 30px;
            text-align: center;
            margin-top: 15px;
        }

        .result-safe {
            background:
                linear-gradient(
                    135deg,
                    rgba(22, 101, 52, 0.35),
                    rgba(6, 78, 59, 0.18)
                );
            border: 1px solid rgba(74, 222, 128, 0.30);
        }

        .result-danger {
            background:
                linear-gradient(
                    135deg,
                    rgba(127, 29, 29, 0.40),
                    rgba(88, 28, 135, 0.15)
                );
            border: 1px solid rgba(248, 113, 113, 0.35);
        }

        .result-icon {
            font-size: 45px;
            margin-bottom: 10px;
        }

        .result-title {
            font-size: 28px;
            font-weight: 800;
            color: #f8fafc;
        }

        .result-description {
            color: #cbd5e1;
            margin-top: 8px;
            font-size: 14px;
        }

        .probability-value {
            font-size: 38px;
            font-weight: 800;
            color: #f8fafc;
            margin-top: 15px;
        }


        /* ---------- Risk Badge ---------- */

        .risk-low {
            display: inline-block;
            padding: 7px 16px;
            border-radius: 999px;
            background: rgba(34, 197, 94, 0.12);
            color: #4ade80;
            border: 1px solid rgba(34, 197, 94, 0.25);
            font-weight: 700;
            font-size: 13px;
        }

        .risk-medium {
            display: inline-block;
            padding: 7px 16px;
            border-radius: 999px;
            background: rgba(234, 179, 8, 0.12);
            color: #facc15;
            border: 1px solid rgba(234, 179, 8, 0.25);
            font-weight: 700;
            font-size: 13px;
        }

        .risk-high {
            display: inline-block;
            padding: 7px 16px;
            border-radius: 999px;
            background: rgba(239, 68, 68, 0.12);
            color: #f87171;
            border: 1px solid rgba(239, 68, 68, 0.25);
            font-weight: 700;
            font-size: 13px;
        }


        /* ---------- Info ---------- */

        .info-box {
            background: rgba(30, 41, 59, 0.45);
            border: 1px solid rgba(96, 165, 250, 0.15);
            border-radius: 14px;
            padding: 15px;
            color: #94a3b8;
            font-size: 13px;
            line-height: 1.6;
        }


        /* ---------- Footer ---------- */

        .footer {
            text-align: center;
            color: #475569;
            font-size: 12px;
            padding-top: 35px;
            padding-bottom: 10px;
        }


        /* ---------- Buttons ---------- */

        .stButton > button {
            border-radius: 10px;
            font-weight: 700;
            min-height: 45px;
            transition: all 0.2s ease;
        }

        .stButton > button:hover {
            transform: translateY(-1px);
        }


        /* ---------- Inputs ---------- */

        div[data-baseweb="input"] {
            border-radius: 9px;
        }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# LOAD MODEL / SCALER / DATASET
# ============================================================

@st.cache_resource
def load_model():

    model = joblib.load(
        "models/fraud_detection_model.pkl"
    )

    scaler = joblib.load(
        "models/scaler.pkl"
    )

    return model, scaler


@st.cache_data
def load_dataset():

    return pd.read_csv(
        "dataset/creditcard.csv"
    )


model, scaler = load_model()
dataset = load_dataset()


# ============================================================
# SESSION STATE
# ============================================================

if "transaction" not in st.session_state:
    st.session_state.transaction = None

if "prediction" not in st.session_state:
    st.session_state.prediction = None

if "probability" not in st.session_state:
    st.session_state.probability = None


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    render_html(
        """
        <div class="sidebar-logo">
            🛡️ FraudGuard
        </div>

        <div class="sidebar-subtitle">
            AI-powered transaction monitoring
        </div>
        """
    )

    render_html(
        """
        <div class="sidebar-section">
            System
        </div>
        """
    )

    st.success("● Model Online")

    # render_html(
    #     """
    #     <div class="sidebar-section">
    #         Model Information
    #     </div>
    #     """
    # )

    # st.write("**Algorithm**")
    # st.caption("Logistic Regression")

    # st.write("**Detection Type**")
    # st.caption("Binary Classification")

    # st.write("**Dataset**")
    # st.caption("Credit Card Fraud Detection")

    # st.write("**Features**")
    # st.caption("30 transaction features")

    # render_html(
    #     """
    #     <div class="sidebar-section">
    #         Detection Logic
    #     </div>
    #     """
    # )

    # st.caption(
    #     "The trained model estimates the probability "
    #     "that a transaction belongs to the fraudulent class."
    # )


# ============================================================
# HEADER
# ============================================================

render_html(
    """
    <div class="top-badge">
        ● LIVE DETECTION SYSTEM
    </div>

    <div class="main-title">
        Credit Card Fraud Detection
    </div>

    <div class="main-subtitle">
        Analyze transaction patterns using a trained
        machine learning classification model.
    </div>
    """
)


# ============================================================
# TOP METRICS
# ============================================================

total_transactions = len(dataset)

fraud_transactions = int(
    dataset["Class"].sum()
)

legitimate_transactions = (
    total_transactions - fraud_transactions
)

fraud_rate = (
    fraud_transactions /
    total_transactions
) * 100


col1, col2, col3, col4 = st.columns(4)


# with col1:

#     render_html(
#         f"""
#         <div class="metric-card">

#             <div class="metric-label">
#                 TOTAL TRANSACTIONS
#             </div>

#             <div class="metric-value">
#                 {total_transactions:,}
#             </div>

#             <div class="metric-description">
#                 Dataset records
#             </div>

#         </div>
#         """
#     )


# with col2:

#     render_html(
#         f"""
#         <div class="metric-card">

#             <div class="metric-label">
#                 FRAUD CASES
#             </div>

#             <div class="metric-value">
#                 {fraud_transactions:,}
#             </div>

#             <div class="metric-description">
#                 Detected in dataset
#             </div>

#         </div>
#         """
#     )


# with col3:

#     render_html(
#         f"""
#         <div class="metric-card">

#             <div class="metric-label">
#                 FRAUD RATE
#             </div>

#             <div class="metric-value">
#                 {fraud_rate:.3f}%
#             </div>

#             <div class="metric-description">
#                 Dataset fraud ratio
#             </div>

#         </div>
#         """
#     )


# with col4:

#     render_html(
#         """
#         <div class="metric-card">

#             <div class="metric-label">
#                 MODEL STATUS
#             </div>

#             <div class="metric-value">
#                 Online
#             </div>

#             <div class="metric-description">
#                 Logistic Regression
#             </div>

#         </div>
#         """
#     )


st.write("")
st.divider()


# ============================================================
# TRANSACTION ANALYSIS
# ============================================================

render_html(
    """
    <div class="section-title">
        Transaction Analysis
    </div>

    <div class="section-description">
        Enter a transaction manually or load a real transaction
        from the dataset for demonstration.
    </div>
    """
)


# ============================================================
# RANDOM TRANSACTION
# ============================================================

random_col, clear_col = st.columns([3, 1])


with random_col:

    if st.button(
        "🎲 Load Random Transaction",
        use_container_width=True
    ):

        random_index = random.randint(
            0,
            len(dataset) - 1
        )

        random_transaction = dataset.iloc[
            random_index
        ].copy()

        st.session_state.transaction = (
            random_transaction
        )

        st.session_state.prediction = None
        st.session_state.probability = None

        st.rerun()


with clear_col:

    if st.button(
        "↻ Clear",
        use_container_width=True
    ):

        st.session_state.transaction = None
        st.session_state.prediction = None
        st.session_state.probability = None

        st.rerun()


# ============================================================
# TRANSACTION INPUT
# ============================================================

transaction = st.session_state.transaction


if transaction is None:

    st.info(
        "💡 Click **Load Random Transaction** to automatically "
        "load an actual transaction from the Kaggle dataset, "
        "or enter the transaction values manually below."
    )

    default_time = 0.0
    default_amount = 100.0

else:

    default_time = float(
        transaction["Time"]
    )

    default_amount = float(
        transaction["Amount"]
    )


# ============================================================
# MAIN TRANSACTION FIELDS
# ============================================================

input_col1, input_col2 = st.columns(2)


with input_col1:

    time = st.number_input(
        "Transaction Time",
        min_value=0.0,
        value=default_time,
        format="%.2f"
    )


with input_col2:

    amount = st.number_input(
        "Transaction Amount",
        min_value=0.0,
        value=default_amount,
        format="%.2f"
    )


# ============================================================
# ANONYMIZED FEATURES
# ============================================================

with st.expander(
    "⚙️ Advanced Transaction Features (V1 – V28)",
    expanded=False
):

    st.caption(
        "These are anonymized numerical features from the "
        "original credit-card fraud dataset."
    )

    features = {}

    feature_columns_ui = st.columns(4)

    for i in range(1, 29):

        default_value = 0.0

        if transaction is not None:

            default_value = float(
                transaction[f"V{i}"]
            )

        with feature_columns_ui[(i - 1) % 4]:

            features[f"V{i}"] = st.number_input(
                f"V{i}",
                value=default_value,
                format="%.6f",
                key=f"feature_{i}"
            )


# ============================================================
# ANALYZE BUTTON
# ============================================================

st.write("")


if st.button(
    "🔍 Analyze Transaction",
    type="primary",
    use_container_width=True
):

    # --------------------------------------------------------
    # Create transaction
    # --------------------------------------------------------

    transaction_data = {
        "Time": time,
        **features,
        "Amount": amount
    }

    transaction_df = pd.DataFrame(
        [transaction_data]
    )


    # --------------------------------------------------------
    # Correct feature order
    # --------------------------------------------------------

    feature_columns = [
        "Time"
    ]

    feature_columns += [
        f"V{i}"
        for i in range(1, 29)
    ]

    feature_columns.append(
        "Amount"
    )


    transaction_df = transaction_df[
        feature_columns
    ]


    # --------------------------------------------------------
    # Scale
    # --------------------------------------------------------

    transaction_scaled = scaler.transform(
        transaction_df
    )


    # --------------------------------------------------------
    # Prediction
    # --------------------------------------------------------

    prediction = model.predict(
        transaction_scaled
    )[0]

    probability = model.predict_proba(
        transaction_scaled
    )[0][1]


    # --------------------------------------------------------
    # Save result
    # --------------------------------------------------------

    st.session_state.prediction = int(
        prediction
    )

    st.session_state.probability = float(
        probability
    )

    st.rerun()


# ============================================================
# RESULT
# ============================================================

prediction = st.session_state.prediction
probability = st.session_state.probability


if prediction is not None:

    st.divider()

    render_html(
        """
        <div class="section-title">
            Detection Result
        </div>
        """
    )


    probability_percentage = (
        probability * 100
    )


    # --------------------------------------------------------
    # Determine risk level
    # --------------------------------------------------------

    if probability < 0.30:

        risk = "LOW RISK"
        risk_class = "risk-low"

    elif probability < 0.70:

        risk = "MEDIUM RISK"
        risk_class = "risk-medium"

    else:

        risk = "HIGH RISK"
        risk_class = "risk-high"


    # --------------------------------------------------------
    # Result Card
    # --------------------------------------------------------

    if prediction == 1:

        render_html(
            f"""
            <div class="result-card result-danger">

                <div class="result-icon">
                    🚨
                </div>

                <div class="result-title">
                    Potentially Fraudulent Transaction
                </div>

                <div class="result-description">
                    The trained model classified this transaction
                    as belonging to the fraud class.
                </div>

                <div class="probability-value">
                    {probability_percentage:.2f}%
                </div>

                <div class="result-description">
                    Estimated fraud probability
                </div>

                <br>

                <span class="{risk_class}">
                    {risk}
                </span>

            </div>
            """
        )

    else:

        render_html(
            f"""
            <div class="result-card result-safe">

                <div class="result-icon">
                    ✅
                </div>

                <div class="result-title">
                    Legitimate Transaction
                </div>

                <div class="result-description">
                    The trained model classified this transaction
                    as belonging to the legitimate class.
                </div>

                <div class="probability-value">
                    {probability_percentage:.2f}%
                </div>

                <div class="result-description">
                    Estimated fraud probability
                </div>

                <br>

                <span class="{risk_class}">
                    {risk}
                </span>

            </div>
            """
        )


    # ========================================================
    # PROBABILITY BAR
    # ========================================================

    st.write("")

    st.caption(
        f"Fraud probability: {probability_percentage:.2f}%"
    )

    st.progress(
        probability
    )


    # ========================================================
    # TRANSACTION SUMMARY
    # ========================================================

    st.write("")

    summary1, summary2, summary3 = st.columns(3)


    with summary1:

        render_html(
            f"""
            <div class="metric-card">

                <div class="metric-label">
                    TRANSACTION AMOUNT
                </div>

                <div class="metric-value">
                    ${amount:,.2f}
                </div>

                <div class="metric-description">
                    Transaction value
                </div>

            </div>
            """
        )


    with summary2:

        render_html(
            f"""
            <div class="metric-card">

                <div class="metric-label">
                    FRAUD PROBABILITY
                </div>

                <div class="metric-value">
                    {probability_percentage:.2f}%
                </div>

                <div class="metric-description">
                    Model probability
                </div>

            </div>
            """
        )


    with summary3:

        prediction_text = (
            "FRAUD"
            if prediction == 1
            else "LEGITIMATE"
        )

        render_html(
            f"""
            <div class="metric-card">

                <div class="metric-label">
                    MODEL PREDICTION
                </div>

                <div class="metric-value">
                    {prediction_text}
                </div>

                <div class="metric-description">
                    Classification result
                </div>

            </div>
            """
        )


    # ========================================================
    # ACTUAL DATASET CLASS
    # ========================================================

    if transaction is not None:

        actual_class = int(
            transaction["Class"]
        )

        st.write("")

        if actual_class == 1:

            st.warning(
                "Dataset reference: This transaction is "
                "actually labelled as **fraudulent** in the "
                "original dataset."
            )

        else:

            st.info(
                "Dataset reference: This transaction is "
                "actually labelled as **legitimate** in the "
                "original dataset."
            )


# ============================================================
# INFORMATION SECTION
# ============================================================

st.write("")
st.divider()


info1, info2 = st.columns(2)


# with info1:

#     render_html(
#         """
#         <div class="section-title">
#             How it works
#         </div>

#         <div class="info-box">

#             <b>1. Transaction Input</b><br>
#             Transaction details are collected from the interface.
#             <br><br>

#             <b>2. Preprocessing</b><br>
#             The transaction is transformed using the same scaler
#             used during model training.
#             <br><br>

#             <b>3. Logistic Regression</b><br>
#             The trained classification model analyzes the
#             transaction features.
#             <br><br>

#             <b>4. Probability</b><br>
#             The model produces an estimated probability for the
#             fraud class.

#         </div>
#         """
#     )


# with info2:

#     render_html(
#         """
#         <div class="section-title">
#             About the Dataset
#         </div>

#         <div class="info-box">

#             This project uses the Credit Card Fraud Detection
#             dataset containing anonymized transaction features.

#             <br><br>

#             <b>Target:</b><br>
#             0 = Legitimate transaction<br>
#             1 = Fraudulent transaction

#             <br><br>

#             <b>Features:</b><br>
#             Time, V1–V28 and Amount

#         </div>
#         """
#     )


# ============================================================
# FOOTER
# ============================================================

render_html(
    """
    <div class="footer">

        FraudGuard • Credit Card Fraud Detection System

        <br>

        Machine Learning Project

    </div>
    """
)