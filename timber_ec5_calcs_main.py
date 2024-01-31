# Schraubenbemessungsprogramm: Webapp mit Streamlit - Axial- und Schertragfähigkeit von Würth Vollgewindeschrauben
# Bibliotheken
from math import pi, sqrt, cos, sin
import pandas as pd
import streamlit as st
import plotly.graph_objects as go
# from würth_screws_functions import get_length, ec5_87_tragfähigkeit_vg, get_min_distances_axial, get_min_distances_shear

# HTML Einstellungen
st.set_page_config(layout="wide")
st.markdown("""<style>
[data-testid="stSidebar"][aria-expanded="false"] > div:first-child {width: 500px;}
[data-testid="stSidebar"][aria-expanded="false"] > div:first-child {width: 500px;margin-left: -500px;}
footer:after{
    content:"Berliner Hochschule für Technik (BHT) | Konstruktiver Hoch- und Ingenieurbau (M.Eng.) | \
    Ingenieurholzbau | Prof. Dr. Jens Kickler | Cal Mense 914553";
    display:block;
    position:relative;
    color:grey;
}
</style>""",unsafe_allow_html=True)

st.markdown('''
<style>
.katex-html {
    text-align: left;
}
</style>''',
unsafe_allow_html=True
)

# Eingangsparameter
# Listen
L_kled = ['permanent', 'long-term', 'medium-term', 'short-term', 'instantaneous']
L_kmod = [[0.6, 0.7, 0.8, 0.9, 1.1], [
    0.6, 0.7, 0.8, 0.9, 1.1], [0.5, 0.55, 0.65, 0.7, 0.9]]
L_timber = ["Glulam", "Solid Wood"]
L_rho_k = [[380, 350, 410, 380, 430, 410, 450, 430], 
           [310, 350, 380, 400, 420]]
L_grade = [['GL24h', 'GL24c', 'GL28h','GL28c', 'GL32h', 'GL32c', 'GL36h', 'GL36c'],
          ['C16', 'C24', 'C30','C35', 'C40']]
L_di_axial = [[], [], [], []]
L_di_scher = [[], [], [], []]
L_no = [[], [], [], []]
L_d = [6, 8, 10, 12]
L_f_c0k = [[24, 21,26.5,24,29,26.5,31,29],[17,21,23,25,26]]
L_f_c90k = [[2.7,2.2,3,2.7,3.3,3,3.6,3.3],[2.2,2.5,2.7,2.8,2.9]]

original_title = '<p style="font-family:Times; color:rgb(230, 30, 40); font-size: 60px;">Timber EC5 Calculations</p>'
st.markdown(original_title, unsafe_allow_html=True)

header = '<p style="font-family:Arial; color:rgb(0,0,0); font-size: 25px; font-weight: bold; ">Section 6: Ultimate Limit State</p>'
st.markdown(header, unsafe_allow_html=True)
st.caption('DIN EN 1995-1-1 Ch. 6')
st.write('This program determines the load-bearing capacities of fully threaded screws with regard to axial and shear loads. \
         The manufacturer-specific characteristic values refer to a Würth ASSY plus VG as a countersunk head version. \
         The program bears no responsibility for any errors. It is advised to verify the results according to the Würth tables.')

with st.sidebar:
    a = 1


#__________________________________________________
#__________Main___________________________________
#__________________________________________________
    
st.write("")
st.write("")
st.write("")
header = '<p style="font-family:Arial; color:rgb(0,0,0); font-size: 25px; font-weight: bold; ">Input Parameters</p>'
st.markdown(header, unsafe_allow_html=True)
st.latex(r"\textbf{Load Parameters}")
st.caption("DIN EN 1995-1-1: Ch. 2.4.1 Design value of material property ")

col1, col2, col3, col4 = st.columns(4)
with col1:
    nkl = st.selectbox('Service Class', [1, 2, 3])
with col2:
    kled = st.selectbox('Load-Duration Class ', L_kled)
    index = L_kled.index(kled)

    k_mod = L_kmod[nkl][index]
    gamma = 1.3
    chi = k_mod/gamma
    hersteller = 'Würth'
with col3:
    st.write("")
    st.latex('k_{mod} / \gamma = ' + str("{:.2f}".format(chi)) )

st.latex(r"\textbf{Material Parameters}")
st.caption("DIN EN 14080:2013 and DIN 1052:2008")

col1, col2, col3, col4 = st.columns(4)
with col1:
    timber = st.selectbox('Timber', L_timber)
    indexTimber = L_timber.index(timber)
with col2:
    grade = st.selectbox('Grade', L_grade[indexTimber])

    index = L_grade[indexTimber].index(grade) 
    rho_k = L_rho_k[indexTimber][index]  

st.latex(r"\textbf{Language}")
language = st.radio("Choose Language", ["English", "German"])


st.latex(r"\textbf{}")
header = '<p style="font-family:Arial; color:rgb(0,0,0); font-size: 25px; font-weight: bold; ">6.1 DESIGN OF CROSS-SECTIONS SUBJECTED TO STRESS IN ONE PRINCIPAL DIRECTION</p>'
st.markdown(header, unsafe_allow_html=True)


tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs(["6.1.1 General", "6.1.2 Tension parallel to the grain", "6.1.3 Tension perpendicular to the grain", 
                      "6.1.4 Compression parallel to the grain", "6.1.5 Compression perpendicular to the grain",
                      "6.1.6 Bending    ", "6.1.7 Shear    ", "6.1.8 Torsion    "])


#__________________________________________________
#_________________________TAB4_____________________
#__________________________________________________
with tab1:
    header = '<p style="font-family:Arial; color:rgb(0,0,0); font-size: 25px; font-weight: bold; ">6.1.1 General</p>'
    st.markdown(header, unsafe_allow_html=True)
    st.write("Clause 6.1 applies to straight solid timber, glued laminated timber or wood·based structural products of constant cross-section, whose grain runs essentially parallel to the length of the member.")
    st.write("The member is assumed to be subjected to stresses in the direction of only one of its principal axes.")
    st.image("image_general.png")
    st.caption("Member Axes")



with tab4: 
    header = '<p style="font-family:Arial; color:rgb(0,0,0); font-size: 25px; font-weight: bold; ">6.1.4 Compression parallel to the grain</p>'
    st.markdown(header, unsafe_allow_html=True)

    st.latex(r"\textbf{Input}")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        F_c0d = int(st.text_input('Compressive Design Load [kN]', 700))
    with col2:
        width = int(st.text_input('Support Width b [mm] ', 300))
    with col3:
        length = int(st.text_input('Support Length l [mm] ', 300))
        area = width*length

    st.latex(r"\textbf{Geometry}")    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.latex(r'''b = ''' + str(width) + r''' mm''') 
    with col2:
        st.latex(r'''l = ''' + str(length) + r''' mm''')
    with col3:
        st.latex(r'''A = ''' + str(area) + r''' mm^2 ''') 

    st.latex(r"\textbf{Stress}")
    st.caption("Design compressive stress along the grain")
    sigma_c0d = round(F_c0d*1000/area,2)
    st.latex(r'''\sigma_{c0d} = \frac{F_{c0d}}{A} = ''' + str(sigma_c0d) + r''' N/mm^2 ''') 

    st.latex(r"\textbf{Resistance}")
    st.caption("Design compressive strength along the grain")
    f_c0k = L_f_c0k[indexTimber][index]
    f_c0d = round(f_c0k*chi,2)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.latex(r"\text{Service Class: }" + str(nkl)) 
    with col2:
         st.latex(r"\text{Load Duration Class: }" + str(kled)) 
    with col3:
         st.latex('k_{mod} / \gamma = ' + str("{:.2f}".format(chi)) )

    st.latex(r'''f_{c0d} = \frac{f_{c0k}*k_{mod}}{\gamma} = ''' + str(f_c0d) + r''' N/mm^2 ''') 

    st.latex(r"\textbf{Check}")
    st.caption("DIN EN 1995-1-1: Chapter 6.1.4 Compression parallel to the grain")
    eta = round(sigma_c0d/f_c0d,2)
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.latex(r'''\eta_{c0d} = \frac{\sigma_{c0d}}{f_{c0d}} = ''' + str(eta))
    with col2:
        if eta < 1:
            st.write("")
            st.write(":heavy_check_mark:")
        else:
            st.write("")
            st.write(":x:")

#__________________________________________________
#_________________________TAB5_____________________
#__________________________________________________
            
with tab5: 
    st.latex(r"\textbf{Input}")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        F_c90d = int(st.text_input('Compressive Design Load [kN] ', 200))
        type_support = st.radio("Type of support", ["Continuous Support (a)", "Discrete Support (b)"])
    with col2:
        width = int(st.text_input('Width b [mm]', 300))
    with col3:
        length = int(st.text_input('Support Length l [mm]', 300))
        
        if type_support== "Discrete Support (b)":
            extra_length = 30
            k_c90 = 1.75 if timber == "Glulam" and length <= 400 else 1.5 

        else: 
            extra_length = 60
            k_c90 = 1.25 if timber == "Solid Wood" else 1.5
            
        area_eff = width*(length+extra_length)

    header = '<p style="font-family:Arial; color:rgb(0,0,0); font-size: 25px; font-weight: bold; ">6.1.5 Compression perpendicular to the grain</p>'
    st.markdown(header, unsafe_allow_html=True)

    # Loading
    st.latex(r"\textbf{Loading}")
    st.latex(r'''F_{c90d} = ''' + str(F_c90d) + r''' kN''') 

    st.latex(r"\textbf{Geometry}")   
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.latex(r'''b = ''' + str(width) + r''' mm''') 
    with col2:
        st.latex(r'''l = ''' + str(length) + r''' mm''') 
    with col3:
        if type_support== "Discrete Support (b)":
                st.latex(r'''l_{extra} = ''' + str(extra_length) + r''' mm''') 
        else: 
                st.latex(r'''l_{extra} = ''' + str(extra_length) + r''' mm''') 
    with col4:
         st.latex(r'''A_{ef} = ''' + str(area_eff) + r''' mm^2 ''') 

    st.latex(r"\textbf{Stress}")
    st.caption("DIN EN 1995-1-1: Equation 6.4: Design compressive stress in the effective contact area perpendicular to the grain")
    sigma_c90d = round(F_c90d*1000/area_eff,2)
    st.latex(r'''\sigma_{c90d} = \frac{F_{c90d}}{A_{ef}} = ''' + str(sigma_c90d) + r''' N/mm^2 ''') 

    st.latex(r"\textbf{Resistance}")
    st.caption("Design compressive strength perpendicular to the grain")
    st.caption("kc90: factor taking into account the load configuration, the possibility of splitting and the degree of compressive deformation")
    f_c90k = L_f_c90k[indexTimber][index]
    f_c90d = round(f_c90k*chi,2)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.latex(r"\text{Service Class: }" + str(nkl)) 
    with col2:
         st.latex(r"\text{Load Duration Class: }" + str(kled)) 
    with col3:
         st.latex('k_{mod} / \gamma = ' + str("{:.2f}".format(chi)) )
    with col4:
        st.latex(r'''k_{c90} = ''' + str(k_c90)) 

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.latex(r'''f_{c90d} = \frac{f_{c90k}*k_{mod}}{\gamma} = ''' + str(f_c90d) + r''' N/mm^2 ''') 



    st.latex(r"\textbf{Check}")
    st.caption("DIN EN 1995-1-1: Chapter 6.1.5 Compression perpendicular to the grain")
    eta = round(sigma_c90d/(f_c90d*k_c90),2)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.latex(r'''\eta_{c90d} = \frac{\sigma_{c90d}}{f_{c90d}*k_{c90}} = ''' + str(eta)) 

    with col2:
        if eta < 1:
            st.write("")
            st.write(":heavy_check_mark:")
        else:
            st.write("")
            st.write(":x:")
