import streamlit as st
from deepeval.test_case import LLMTestCase
from deepeval.metrics import HallucinationMetric
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="AI Fact-Checker", page_icon="⚖️", layout="wide")

st.title("⚖️ The AI Fact-Checker")
st.markdown("""
This tool uses a 'Judge LLM' to verify if an AI's response is actually supported by the facts provided. 
Perfect for checking if your AI is making things up (**Hallucinating**).
""")

st.divider()
col_input, col_context = st.columns(2)

with col_input:
    st.subheader("1. The AI's Answer")
    actual_output = st.text_area(
        "Paste the response you want to check:",
        placeholder="e.g., The capital of France is Lyon.",
        height=150
    )

with col_context:
    st.subheader("2. The Source Truth")
    context_input = st.text_area(
        "Paste the facts/documents the AI should have used:",
        placeholder="e.g., Paris is the capital and largest city of France.",
        height=150
    )

with st.sidebar:
    st.header("Settings")
    # Sensitivity: 0.1 is very strict, 0.9 is very loose
    threshold = st.slider("Sensitivity (Lower is stricter)", 0.0, 1.0, 0.5)
    run_eval = st.button("🚀 Run Fact-Check", use_container_width=True)

if run_eval:
    if not actual_output or not context_input:
        st.warning("Please provide both an AI answer and a source truth to begin.")
    else:
        with st.spinner("The Judge is analyzing the facts..."):
            # Setup Metric
            metric = HallucinationMetric(threshold=threshold)
            
            test_case = LLMTestCase(
                input="Manual Fact-Check", # placeholder
                actual_output=actual_output,
                context=[context_input]
            )
            
            metric.measure(test_case)
            
            st.divider()
            
            res_col1, res_col2 = st.columns([1, 2])
            
            with res_col1:
                st.metric("Hallucination Score", f"{metric.score:.2f}", help="0.00 = No Hallucinations, 1.00 = Total Hallucination")
                if metric.score <= threshold:
                    st.success("✅ VERIFIED: Accurate")
                else:
                    st.error("❌ REJECTED: Inaccurate")
            
            with res_col2:
                st.markdown("### Judge's Reasoning")
                st.info(metric.reason)

st.sidebar.markdown("---")
st.sidebar.caption("Powered by DeepEval & OpenAI")