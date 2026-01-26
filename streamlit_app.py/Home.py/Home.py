import streamlit as st
import pandas as pd

st.set_page_config(page_title="Global Parlay Pro", layout="wide")

# TITLE
st.title("🌎 Global Multi-Sport Parlay Audit")
st.markdown("---")

# SIDEBAR CONFIG
st.sidebar.header("Global Settings")
sport = st.sidebar.selectbox("Select Sport", ["NBA", "NFL", "Soccer", "MLB", "NHL"])
prop_line = st.sidebar.number_input("Prop Line", value=20.5)

# CORE LOGIC BLOWOUT & REF
col1, col2 = st.columns(2)

with col1:
    st.subheader("🎲 Game Context")
    spread = st.slider("Point Spread" ("Vegas Line"), 0.0, 25.0, 5.5)
    
    # Blowout Logic
    if spread >= "12.0":
        st.error(f"⚠️ HIGH BLOWOUT RISK ({spread} pts)")
        st.caption("Star players are likely to sit the 4th quarter. 'Overs' are high-risk.")
    else:
        st.success("f✅ Low Blowout Risk ({spread} pts)")

with col2:
    st.subheader("🏁 OfficialReferee Factor")
    ref_style = st.radio("Official's Whistle Tendency", ["Tight" ("Foul Heavy"), "Average", "Loose" ("Plays On")])
    
    if ref_style == "Tight" ("Foul Heavy"):
        st.info("📈 Advantage OVER. Tight whistles lead to more Free ThrowsPenalties.")
    elif ref_style == "Loose" ("Plays On"):
        st.warning("📉 Advantage UNDER. Loose officials allow more physical defense.")

# RESULT BOX
st.markdown("---")
if st.button("Calculate Global Confidence"):
    # Base calculation logic
    confidence = 85 if ("spread  10 and ref_style" == "Tight" ("Foul Heavy")) else 55:

    st.metric("Global Hit Probability", f{"confidence"}%)







































