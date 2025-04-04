from io import StringIO

def df_info_to_string(df):

    # To capture the output for avoiding None value from df.info()
    buffer = StringIO()

    # Pass the buffer to df.info() using the 'buf' parameter
    df.info(buf=buffer)

    # Get the string from the buffer
    return buffer.getvalue()