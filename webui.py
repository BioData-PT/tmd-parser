# SPDX-License-Identifier: BSD-2-Clause

# ELIXIR Training Metrics Database Web UI
# Author: Gil Poiares-Oliveira <gpo@biodata.pt>
# © 2025 Associação BIP4DAB

import streamlit as st
from tmd_parser import tmd_parser

# Initialize session state for storing the parsed data
if 'demographic_csv' not in st.session_state:
    st.session_state.demographic_csv = None
if 'quality_csv' not in st.session_state:
    st.session_state.quality_csv = None

st.logo("assets/BioDataPT_H.svg", link="https://biodata.pt")
st.title("BioData.pt Training Metrics Database feedback parser")
event_id = st.number_input("Event ID", step=1, min_value=0, value=0)

uploaded_file = st.file_uploader(
    "Demographic and quality data file", type="csv"
)

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("Submit", type="primary"):
        if uploaded_file is not None:
            # Run the parser
            data_demographic, data_quality = tmd_parser(event_id, uploaded_file)
            
            # Store CSVs in session state
            st.session_state.demographic_csv = data_demographic.write_csv()
            st.session_state.quality_csv = data_quality.write_csv()
        else:
            st.error("Please upload a CSV file first")

# Show download buttons if data is available
if st.session_state.demographic_csv is not None:
    with col2:
        st.download_button(
            label="Download Demographic Data",
            data=st.session_state.demographic_csv,
            file_name=f"{event_id}_demographic.csv",
            mime="text/csv"
        )
    
    with col3:
        st.download_button(
            label="Download Quality Data",
            data=st.session_state.quality_csv,
            file_name=f"{event_id}_quality.csv",
            mime="text/csv"
        )

# Clear button at the bottom
if st.session_state.demographic_csv is not None:
    if st.button("Clear All"):
        st.session_state.demographic_csv = None
        st.session_state.quality_csv = None
        st.rerun()