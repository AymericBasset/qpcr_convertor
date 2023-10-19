import streamlit as st
import pandas as pd
import base64
import io
# buffer to use for excel writer
buffer = io.BytesIO()

@st.cache_data
def convert_df(df):
   return df.to_csv(index=False)

# Function to convert a given value to numeric
def convert_to_numeric(value):
    try:
        # Try converting from the string format
        return float(str(value).replace("\xa0", "").replace(",", "."))
    except ValueError:
        # If that fails, return the value directly
        return value

# Streamlit app UI
st.title("Excel Western Blot Convertor App")
uploaded_file = st.file_uploader("Upload an Excel file", type=["xlsx"])

processed = False

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    df_raw = df.copy()
    name = df.columns[0].split('.')[0]
    df.columns = df.iloc[0]
    df = df[1:]
    df.reset_index(inplace=True)
    df.rename(columns={'index':name}, inplace=True)
    df = df.applymap(convert_to_numeric)
    
    st.write("Processed DataFrame:")
    st.write(df)
    processed = True
    
    if processed:
        
        csv = convert_df(df)
        st.download_button(
        "Download data as CSV",
        csv,
        name+".csv",
        "text/csv",
        key='download-csv'
        )

   
        # download button 2 to download dataframe as xlsx
        with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
            # Write each dataframe to a different worksheet.
            df.to_excel(writer, sheet_name='Sheet1', index=False)

            download2 = st.download_button(
                label="Download data as Excel",
                data=buffer,
                file_name=name+'.xlsx',
                mime='application/vnd.ms-excel'
        )

    
