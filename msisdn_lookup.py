import streamlit as st
import pandas as pd
import requests
import io

st.title("📡 MSISDN Lookup Runner")

# User inputs
base_url = st.text_input("Base URL (use <msisdn> as placeholder)", value="http://10.27.14.182:8080/ocsapi/msisdnlookup/<msisdn>")
msisdns_input = st.text_area("Enter MSISDNs (one per line)")

if st.button("Run Lookup"):
    if "<msisdn>" not in base_url:
        st.error("Please make sure the URL contains '<msisdn>' placeholder.")
    else:
        msisdns = [line.strip() for line in msisdns_input.splitlines() if line.strip()]
        results = []

        for msisdn in msisdns:
            url = base_url.replace("<msisdn>", msisdn)
            try:
                response = requests.get(url, timeout=10)
                result = response.json() if response.headers.get("Content-Type", "").startswith("application/json") else response.text
                results.append({
                    "MSISDN": msisdn,
                    "Status Code": response.status_code,
                    "Result": result
                })
            except Exception as e:
                results.append({
                    "MSISDN": msisdn,
                    "Status Code": "Error",
                    "Result": str(e)
                })

        # Convert to DataFrame
        df = pd.DataFrame(results)
        st.dataframe(df)

        # CSV download
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📥 Download Results as CSV",
            data=csv,
            file_name="msisdn_results.csv",
            mime="text/csv"
        )
