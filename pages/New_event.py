import streamlit as st
import polars as pl

st.set_page_config(page_title="New event", page_icon="📆")
st.logo("assets/BioDataPT_H.svg", link="https://biodata.pt")
st.title("New event")
st.sidebar.write("**BioData.pt Training Metrics Database Parser**")

def generate_csv(df):
    st.session_state.output_csv = df.write_csv()
    st.success('File generated successfully!', icon=":material/check_circle:")
    st.download_button(
        label="Download event declaration",
        data=st.session_state.output_csv,
        file_name="event.csv",
        mime="text/csv",
        icon=":material/download:"
    )

# Initialize the list of institutions in session state if it doesn't exist
if 'institutions' not in st.session_state:
    st.session_state.institutions = []

# Create a callback to handle adding institutions
def add_institution():
    if st.session_state.new_institution and st.session_state.new_institution not in st.session_state.institutions:
        st.session_state.institutions.append(st.session_state.new_institution)

with st.form("event"):

    title = st.text_input("Event title", key="title")

    start_date = st.date_input("Start date", format="YYYY-MM-DD", key="start_date")

    end_date = st.date_input("End date", format="YYYY-MM-DD", key="end_date")

    event_type = st.selectbox("Event type", [
        "Training - face to face",
        "Training - elearning",
        "Training - blended",
        "Knowledge exchange workshop",
        "Hackathon",
    ], key="event_type")

    funding = st.multiselect("Funding", [
        "EXCELERATE",
        "ELIXIR Implementation Study",
        "ELIXIR Community / Use Case",
        "ELIXIR Node",
        "ELIXIR Hub",
        "ELIXIR Platform",
        "Non-ELIXIR/ Non-EXCELERATE funds"
    ], key="funding")

    # Display existing institutions
    if st.session_state.institutions:
        st.write("Organising institutions")
        for i, inst in enumerate(st.session_state.institutions):
            st.write(f"- {inst}")

    # Add new institution input and button in a container for better alignment
    container = st.container()
    with container:
        col1, col2 = st.columns([4, 1])
        with col1:
            new_institution = st.text_input("Organising Institution ROR ID", key="new_institution", placeholder='Press "Add" after typing to confirm')
        with col2:
            st.write("")  # This creates vertical space
            if st.form_submit_button("Add", on_click=add_institution):
                pass

    location = st.text_input("Location (city, country)", key="location")

    excelerate_wp = st.text_input("EXCELERATE WP", key="excelerate_wp")

    target_audience = st.multiselect("Target audience", [
        "Academia/ Research Institution",
        "Industry",
        "Non-Profit Organisation",
        "Healthcare"
    ], key="target_audience")

    platforms = st.multiselect("Additional ELIXIR Platforms involved", [
        "Tools",
        "Interoperability",
        "Compute",
        "Data",
        "NA"
    ], key="platforms")

    communities = st.multiselect("ELIXIR Communities involved", [
        "Human Data",
        "Marine Metagenomics",
        "Rare Diseases",
        "Plant Sciences",
        "Proteomics",
        "Galaxy",
        "NA"
    ], key="communities")

    nodes = st.multiselect("ELIXIR Nodes", [
        "ELIXIR-NL",
        "ELIXIR-IT",
        "ELIXIR-PT",
        "ELIXIR-UK",
        "ELIXIR-EMBL-EBI",
        "ELIXIR-BE",
        "ELIXIR-FR",
        "ELIXIR-EE",
        "ELIXIR-CZ",
        "ELIXIR-CH",
        "ELIXIR-DE",
        "ELIXIR-LU",
        "ELIXIR-DK",
        "ELIXIR-FI",
        "ELIXIR-NO",
        "ELIXIR-SI",
        "ELIXIR-ES",
        "ELIXIR-GR",
        "ELIXIR-HU",
        "ELIXIR-SE",
        "ELIXIR-IL",
        "ELIXIR-IE",
        "ELIXIR-Hub"
    ])

    participants = st.number_input("Number of participants", step=1, min_value=0, value=None, key="participants")
    trainers = st.number_input("Number of trainers/facilitators", step=1, min_value=0, value=None, key="trainers")
    url = st.text_input("URL to event page/agenda", key="url")
    
    submitted = st.form_submit_button("Submit", type="primary")

if submitted:
    data = pl.DataFrame(
        {
            "Title": title,
            "ELIXIR Node": str(nodes).replace("[","").replace("]","").replace("'","").replace(", ",","),
            "Start Date": start_date,
            "End Date": end_date,
            "Event type": event_type,
            "Funding": str(funding).replace("[","").replace("]","").replace("'","").replace(", ",""),
            "Organising Institution/s": str(st.session_state.institutions).replace("[","").replace("]","").replace("'","").replace(", ",","),
            "Location (city, country)": location,
            "EXCELERATE WP": excelerate_wp,
            "Target audience": str(target_audience).replace("[","").replace("]","").replace("'","").replace(", ",","),
            "Additional ELIXIR Platforms involved": str(platforms).replace("[","").replace("]","").replace("'","").replace(", ",","),
            "ELIXIR Communities involved": str(communities).replace("[","").replace("]","").replace("'","").replace(", ",","),
            "No. of participants": participants,
            "No. of trainers/ facilitators": trainers,
            "Url to event page/ agenda": url
        }
    )

    generate_csv(data)
