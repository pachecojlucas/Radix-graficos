import pandas as pd
import numpy as np
import plotly.express as px
import streamlit as st

#famoso back

def app():
    #pegando os data frames
    normal = pd.read_excel('radix.xlsx')

    seca = pd.read_excel('radix.xlsx',sheet_name="sede")

    #calculando a media das variaveis quantitativas
    normal_media = normal.groupby('Espécie')['Peso seco g','N.Raizes','Comprimento CM'].median().reset_index()
    normal_media.columns = ['Material genético', 'Peso seco medio','N.Raizes medio', 'Comprimento CM medio']
    seca_media = seca.groupby('Espécie')['Peso seco g','N.Raizes','Comprimento CM'].median().reset_index()
    seca_media.columns = ['Material genético', 'Peso seco medio','N.Raizes medio', 'Comprimento CM medio']
    normal_media['Irrigado'] = 'comum'
    seca_media['Irrigado'] = 'deficit'
    ambientes = pd.concat([normal_media,seca_media])

    #calculando o coeficiente de variação
    cv = lambda x: np.std(x, ddof=1) / np.mean(x) * 100 
    normal_cv = normal.groupby(['Espécie'])['Peso seco g','N.Raizes','Comprimento CM'].apply(cv).round().reset_index()
    normal_cv.columns = ['Material genético', 'Peso seco (CV%)','N.Raizes (CV%)', 'Comprimento CM (CV%)']
    seca_cv = seca.groupby(['Espécie'])['Peso seco g','N.Raizes','Comprimento CM'].apply(cv).round().reset_index()
    seca_cv.columns = ['Material genético', 'Peso seco (CV%)','N.Raizes (CV%)', 'Comprimento CM (CV%)']
    normal_cv['Irrigado'] = 'comum'
    seca_cv['Irrigado'] = 'deficit'
    CV_Radix = pd.concat([normal_cv,seca_cv])

    #unindo as duas bases com media e com CV%
    tabela_resumo = ambientes.merge(CV_Radix, how='inner', on=['Material genético','Irrigado'])
    
    #O front:

    coluna = st.selectbox('Selecione entre as variaveis para o bar plot', ('Peso seco medio', 
    'N.Raizes medio', 'Comprimento CM medio'))
                #setando labels
    label = coluna


    #Gráfico de barras
    st.write("Gráfico de barras - " , label, "dentro de cada material genético")
    barra_Matgen = px.bar(tabela_resumo, x= "Material genético",y =coluna, 
    color='Irrigado',barmode='group')
    barra_Matgen.update_layout(xaxis={'categoryorder': 'total ascending'})

    st.plotly_chart(barra_Matgen, use_container_width=True)

    #scatter de numero de raizes

    test = px.scatter(tabela_resumo, x='N.Raizes medio', y="Peso seco medio",  color='Material genético', hover_name='Irrigado', trendline="ols", 
                 trendline_scope="overall",opacity=0.65, title="Gráfico de dispersão - Peso seco x N.Raizes", 
                 size=tabela_resumo['N.Raizes medio'].replace(np.nan,0)           
        )
    st.plotly_chart(test)

    #irrigação comum
    if st.checkbox('Visualizar dados de irrigação comum'):
        coluna2 = st.selectbox('Selecione entre as variaveis para o Box Plot', ('Comprimento CM', 
    'N.Raizes', 'Peso seco g'))
        label = coluna2
        tabela_resumo = tabela_resumo[tabela_resumo['Irrigado']== 'comum']
        normal = normal[normal[coluna2]>0]

        st.write("Box plot - " , label, "por material genético")

        Boxplot_Matgen = px.box(data_frame=normal, x='Espécie', y=coluna2, color='Espécie', 
        hover_name='Codigo L1',
        points='all', width=None, height=None, labels={
        coluna2: label,
        'Espécie': 'Material genético'                   
        })

        st.plotly_chart(Boxplot_Matgen)

        #grafico de barras pintado
        coluna_normal = st.selectbox('Selecione entre as variaveis para as Bar plot', ('Peso seco medio', 
        'N.Raizes medio', 'Comprimento CM medio'))
        if coluna_normal == "Peso seco medio":
            cv = 'Peso seco (CV%)'
        elif coluna_normal == "N.Raizes medio":
            cv = 'N.Raizes (CV%)'
        else:
            cv = 'Comprimento CM (CV%)' 

        resumo_normal = tabela_resumo[tabela_resumo["Irrigado"]=='comum']
        st.write("Gráfico de barras - " , coluna_normal, "pintado pelo coeficiente de variação")
        fig = px.bar(resumo_normal, x='Material genético', y= coluna_normal, barmode='group', width=1000,color = cv,
             hover_data=["Irrigado"],
            labels={
            'y': coluna_normal})
                
                
        fig.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)

        fig.update_layout( xaxis={'categoryorder':'total descending'})

        st.plotly_chart(fig)

    #irrigação limitada

    if st.checkbox('Visualizar dados de irrigação limitada'):
        coluna2 = st.selectbox('Selecione entre as variaveis para o Box Plot', ('Comprimento CM', 
    'N.Raizes', 'Peso seco g'))
        label = coluna2
        tabela_resumo = tabela_resumo[tabela_resumo['Irrigado']== 'deficit']
        seca = seca[seca["Peso seco g"]>0]

        st.write("Box plot - " , label, "por material genético")

        Boxplot_Matgen = px.box(data_frame=seca, x='Espécie', y=coluna2, color='Espécie', 
        hover_name='Codigo L2',
        points='all', width=None, height=None, labels={
        coluna2: label,
        'Espécie': 'Material genético'                   
        })

        st.plotly_chart(Boxplot_Matgen)

        #grafico de barras pintado
        coluna_deficit = st.selectbox('Selecione entre as variaveis para as Bar plot', ('Peso seco medio', 
        'N.Raizes medio', 'Comprimento CM medio'))
        if coluna_deficit == "Peso seco medio":
            cv = 'Peso seco (CV%)'
        elif coluna_deficit == "N.Raizes medio":
            cv = 'N.Raizes (CV%)'
        else:
            cv = 'Comprimento CM (CV%)' 

        resumo_deficit = tabela_resumo[tabela_resumo["Irrigado"]=='deficit']
        st.write("Gráfico de barras - " , coluna_deficit, "pintado pelo coeficiente de variação")
        fig = px.bar(resumo_deficit, x='Material genético', y= coluna_deficit, barmode='group', width=1000,color = cv,
             hover_data=["Irrigado"],
            labels={
            'y': coluna_deficit})
                
                
        fig.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)

        fig.update_layout( xaxis={'categoryorder':'total descending'})

        st.plotly_chart(fig)

    

if __name__ == '__main__':
        app()
