# Import python libraries
import streamlit as st
import matplotlib.pyplot as plt
import lasio
from streamlit_option_menu import option_menu
from PIL import Image
from io import StringIO


# Insert icon of web app
icon = Image.open("recursos/barril.jpg")
# Page Layout
st.set_page_config(page_title="Well Logs App")

# Title of app
st.title("Well Logs Visualization")
st.write("This logs contain information about petrophysical features of any well")
image = Image.open("recursos/petro.jpg")
st.image(image, width=100, use_column_width=True)

# Pages
with st.sidebar:
    options = option_menu(
        menu_title="Main Menu",
        options=["Home", "Data Information", "Logs Visualization","Petrophysics Calculation"],
        icons=["house", "clipboard-data", "tv"],
    )

# Options
if options == "Data Information":
    # number of file to upload
    n_wells = int(st.number_input("Enter the well logs files"))
    files = [
        st.file_uploader(f"Upload the las file of well {n + 1}") for n in range(n_wells)
    ]
    if files is not None:
        for log in files:
            stri=[StringIO(log.getvalue().decode("utf-8"))]
            for log in stri:
                data=lasio.read(log).df()
                well=[st.write(data)]
                val=[st.write(data.columns)]


elif options == "Logs Visualization":
    # number of file to upload
    n_wells = int(st.number_input("Enter the well logs files"))
    files = [
        st.file_uploader(f"Upload the las file of well {n + 1}") for n in range(n_wells)
    ]
    if files is not None:
        stri = [StringIO(log.getvalue().decode("utf-8")) for log in files]
        for log in stri:
            data = lasio.read(log).df()
            fig, axs = plt.subplots(nrows=1, ncols=3, figsize=(5, 10), sharey=True, gridspec_kw={"wspace": 0})
            logs_to_plot = ["KLOGH", "PHIF", "SW"]

            for ax, log in zip(axs, logs_to_plot):
                ax.plot(data[log], data.index)
                ax.set_title(log)
                ax.xaxis.tick_top()

            axs[0].set_ylim(None, None)
            axs[0].invert_yaxis()

            # plt.subplots_adjust(wspace=0)
            graf=plt.show()
            st.pyplot(graf)

elif options== "Petrophysics Calculation":
    n_wells = int(st.number_input("Enter the well logs files"))
    files = [
        st.file_uploader(f"Upload the las file of well {n + 1}") for n in range(n_wells)
    ]
    if files is not None:
        stri = [StringIO(log.getvalue().decode("utf-8")) for log in files]
        for log in stri:
            data = lasio.read(log).df()

            data['VSH'] = (data['GR'].max() - data['GR']) / (data['GR'].max()- data['GR'].min())
            st.write(data['VSH'])






