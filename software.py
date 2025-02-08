import streamlit as st
import os
import re
import pytesseract
import shutil
import pandas as pd
import tabula
from pdf2image import convert_from_path
from PIL import Image
from io import BytesIO

# Configurar o caminho do Tesseract (ajuste se necessário)
pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'

def salvar_arquivo_no_sistema(uploaded_file, pasta_destino):
    if not os.path.exists(pasta_destino):
        os.makedirs(pasta_destino)
    caminho_arquivo = os.path.join(pasta_destino, uploaded_file.name)
    with open(caminho_arquivo, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return caminho_arquivo

def remover_arquivos_temporarios(caminhos):
    for caminho in caminhos:
        if os.path.exists(caminho):
            if os.path.isfile(caminho):
                os.remove(caminho)
            else:
                shutil.rmtree(caminho)

# =============================================================================
# Funções para modelos 1, 3 e 4 (OCR + filtragem + extração com regex)
def extrair_texto_com_pagina(img_path, pagina):
    # A partir da página 21 utiliza --psm 4; caso contrário, usa a configuração padrão
    psm_config = "--psm 4" if pagina >= 21 else None
    imagem = Image.open(img_path)
    if psm_config:
        return pytesseract.image_to_string(imagem, lang='por', config=psm_config)
    return pytesseract.image_to_string(imagem, lang='por')

def tratar_prov_desc(nome):
    nome_tratado = nome.replace('...', '').replace('..', '').replace('.......', '').replace(',', '').strip()
    while '  ' in nome_tratado:
        nome_tratado = nome_tratado.replace('  ', ' ')
    if nome_tratado.endswith('.'):
        nome_tratado = nome_tratado[:-1]
    nome_tratado = nome_tratado.upper()
    nome_tratado = nome_tratado.replace('GRAT.DIFICIL ACESS', 'GRATIFICACAO DIFICIL ACESSO')
    nome_tratado = nome_tratado.replace('GRATDIFICIL ACESS', 'GRATIFICACAO DIFICIL ACESSO')
    nome_tratado = nome_tratado.replace('QUENQUENIO', 'QUINQUENIO')
    nome_tratado = nome_tratado.replace('QUINQUENTO', 'QUINQUENIO')
    nome_tratado = nome_tratado.replace('VENCIMENTO.', 'VENCIMENTO')
    return nome_tratado

def processar_pdf_ocr_avancado(pdf_caminho, nome_arquivo_original, modelo):
    """
    Fluxo para modelos 1, 3 e 4:
      1) Converte o PDF em imagens.
      2) Extrai o texto de cada página (utilizando --psm 4 a partir da página 21).
      3) Salva o texto completo em um arquivo temporário.
      4) Filtra as linhas contendo palavras-chave.
      5) Extrai os dados via regex.
      6) Trata a coluna PROV/DESC.
      7) Salva o DataFrame final em Excel.
    """
    nome_base = os.path.splitext(nome_arquivo_original)[0]
    pasta_imagens = f"imagens_ocr_{nome_base}"
    if not os.path.exists(pasta_imagens):
        os.makedirs(pasta_imagens)
    
    txt_extraido = os.path.join(pasta_imagens, f"{nome_base}_texto_extraido.txt")
    
    # Converter cada página do PDF em imagem e extrair o texto
    pages = convert_from_path(pdf_caminho)
    image_files = []
    with open(txt_extraido, "w", encoding="utf-8") as arquivo:
        for i, page in enumerate(pages, start=1):
            img_path = os.path.join(pasta_imagens, f"page_{i}.jpg")
            page.save(img_path, "JPEG")
            image_files.append(img_path)
            texto = extrair_texto_com_pagina(img_path, i)
            arquivo.write(f"=== Página {i} ===\n")
            arquivo.write(texto + "\n")
            arquivo.write("-" * 80 + "\n")
    
    # Filtrar linhas com base em palavras-chave
    palavras_chave = ['MES', 'QUANT', 'PROV/DESC', 'ACRESCIMO', 'QUINQUENIO.', 'VENCIMENTO.', 'GRAT.TITULARIDADE.', 'FICHA FINANCEIRA']
    txt_filtrado = os.path.join(pasta_imagens, f"{nome_base}_texto_filtrado.txt")
    with open(txt_extraido, "r", encoding="utf-8") as fin:
        linhas = fin.readlines()
    linhas_filtradas = [linha for linha in linhas if any(chave in linha for chave in palavras_chave)]
    with open(txt_filtrado, "w", encoding="utf-8") as fout:
        fout.writelines(linhas_filtradas)
    
    # Extração dos dados via expressões regulares
    with open(txt_filtrado, "r", encoding="utf-8") as f:
        conteudo = f.read()
    
    padrao = re.compile(
        r"(?P<MES>\b(?:0[1-9]|1[0-2])\b)\s+"
        r"(?P<PROV_DESC>[A-ZÀ-Ž0-9\.,\-/\s]+?)\s+"
        r"(?P<QUANT>\d{1,6})\s+"
        r"(?P<VALOR>\d{1,3},\d{2})"
    )
    padrao_ano = re.compile(r"FICHA FINANCEIRA INDIVIDUAL.*?(\d{4})")
    
    dados = []
    ano_atual = None
    for linha in conteudo.splitlines():
        match_ano = padrao_ano.search(linha)
        if match_ano:
            ano_atual = match_ano.group(1)
        for match in padrao.finditer(linha):
            mes = match.group("MES")
            prov_desc = match.group("PROV_DESC").strip()
            quant = match.group("QUANT")
            valor = match.group("VALOR")
            dados.append({
                "ANO": ano_atual,
                "MES": mes,
                "PROV/DESC": prov_desc,
                "QUANT": quant,
                "VALOR": valor
            })
    
    df = pd.DataFrame(dados)
    if not df.empty:
        df["PROV/DESC"] = df["PROV/DESC"].apply(tratar_prov_desc)
    
    # Salvar DataFrame final em Excel
    pasta_saida = "arquivos_xlsx"
    if not os.path.exists(pasta_saida):
        os.makedirs(pasta_saida)
    xlsx_final = os.path.join(pasta_saida, f"{nome_base}.xlsx")
    df.to_excel(xlsx_final, index=False)
    
    # Remover arquivos temporários (imagens e txt)
    remover_arquivos_temporarios([pasta_imagens])
    
    return xlsx_final, txt_filtrado

# =============================================================================
# Funções para modelo 2 (Extração via Tabula e processamento das abas)
def converter_pdf_para_excel(pdf_caminho, excel_saida):
    dfs = tabula.read_pdf(pdf_caminho, pages="all", multiple_tables=True, lattice=True)
    if not dfs:
        raise ValueError("Nenhuma tabela foi encontrada no PDF.")
    with pd.ExcelWriter(excel_saida, engine='openpyxl') as writer:
        for i, df in enumerate(dfs, start=1):
            df.to_excel(writer, sheet_name=f"Tabela_{i}", index=False)
    return excel_saida

def processar_aba(sheet_name, excel_data):
    df = pd.read_excel(excel_data, sheet_name=sheet_name, header=None)
    # Identificar linhas onde aparece "Proventos"
    inicio_tabelas = df[df.apply(lambda x: x.dropna().astype(str).str.contains("Proventos").any(), axis=1)].index.tolist()
    tabelas = []
    for i, start in enumerate(inicio_tabelas):
        end = inicio_tabelas[i + 1] if i + 1 < len(inicio_tabelas) else len(df)
        tabela = df.iloc[start:end].copy()
        tabela.columns = tabela.iloc[0]
        tabela = tabela[1:]
        tabela.dropna(how="all", axis=0, inplace=True)
        tabela.dropna(how="all", axis=1, inplace=True)
        regex = r'Proventos|Janeiro|Fevereiro|Março|Abril|Maio|Junho|Julho|Agosto|Setembro|Outubro|Novembro|Dezembro'
        tabela = tabela.loc[:, tabela.columns.astype(str).str.contains(regex, na=False)]
        tabela = tabela[~tabela.apply(lambda x: any(isinstance(cell, str) and ("Orgão" in cell or "Servidor" in cell) for cell in x), axis=1)]
        tabelas.append(tabela)
    return pd.concat(tabelas, ignore_index=True)

def limpar_valores(valor):
    if isinstance(valor, str):
        valor = valor.replace("R$", "").replace(".", "").replace(",", ".").strip()
        try:
            return float(valor)
        except:
            return valor
    return valor

def limpar_nome(nome):
    if isinstance(nome, str):
        nome_limpo = nome.replace("\r", " ").replace("...", "").replace(".", "").strip()
        nome_limpo = " ".join(nome_limpo.split())
        return nome_limpo
    return nome

def processar_pdf_tabula_avancado(pdf_caminho, nome_arquivo_original):
    """
    Fluxo para o modelo 2:
      1) Converte o PDF em um Excel intermediário usando Tabula.
      2) Processa cada aba para identificar e extrair a tabela.
      3) Realiza a limpeza dos dados.
      4) Salva o resultado final em um arquivo Excel.
    """
    nome_base = os.path.splitext(nome_arquivo_original)[0]
    pasta_saida = "arquivos_xlsx"
    if not os.path.exists(pasta_saida):
        os.makedirs(pasta_saida)
    excel_intermediario = os.path.join(pasta_saida, f"{nome_base}_intermediario.xlsx")
    converter_pdf_para_excel(pdf_caminho, excel_intermediario)
    
    excel_data = pd.ExcelFile(excel_intermediario)
    try:
        resultado = pd.concat([processar_aba(sheet, excel_intermediario) for sheet in excel_data.sheet_names])
    except Exception as e:
        os.remove(excel_intermediario)
        raise e
    
    if "Proventos / Descontos" in resultado.columns:
        resultado["Proventos / Descontos"] = resultado["Proventos / Descontos"].apply(limpar_nome)
    for col in resultado.columns:
        if resultado[col].dtype == object and col != "Proventos / Descontos":
            resultado[col] = resultado[col].apply(limpar_valores)
    
    nome_excel_final = os.path.join(pasta_saida, f"{nome_base}.xlsx")
    resultado.to_excel(nome_excel_final, index=False)
    
    if os.path.exists(excel_intermediario):
        os.remove(excel_intermediario)
    
    return nome_excel_final

# =============================================================================
# Fluxo principal do Streamlit
def main():
    st.title("Conversor de PDF para XLSX")
    
    st.write("Escolha o tipo de PDF que deseja extrair:")
    opcoes_modelos = {
        "Extrato de pagamento Scaneado? (MODELO1)": "modelo1",
        "Dados de Servidor por Ano de Referencia (MODELO2)": "modelo2",
        "DEMONSTRATIVO DE PAGAMENTO - SMR (MODELO3)": "modelo3",
        "DEMONSTRATIVO DE PAGAMENTO - SRH (MODELO4)": "modelo4",
    }
    modelo_escolhido = st.selectbox("Selecione o modelo:", list(opcoes_modelos.keys()))
    
    pdf_file = st.file_uploader("Envie seu PDF:", type=["pdf"])
    
    if pdf_file is not None:
        st.write(f"Arquivo carregado: {pdf_file.name}")
        pasta_upload = "uploads"
        caminho_pdf_salvo = salvar_arquivo_no_sistema(pdf_file, pasta_upload)
        
        if st.button("Processar"):
            try:
                if opcoes_modelos[modelo_escolhido] == "modelo2":
                    # Processamento via Tabula avançado para modelo2
                    xlsx_final = processar_pdf_tabula_avancado(caminho_pdf_salvo, pdf_file.name)
                    st.success("Conversão concluída (Modelo2 - Tabula).")
                    with open(xlsx_final, "rb") as f:
                        st.download_button(
                            label="Baixar XLSX Convertido",
                            data=f,
                            file_name=os.path.basename(xlsx_final),
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                        )
                else:
                    # Processamento via OCR avançado para modelos 1, 3 e 4
                    xlsx_final, txt_filtrado = processar_pdf_ocr_avancado(caminho_pdf_salvo, pdf_file.name, opcoes_modelos[modelo_escolhido])
                    st.success(f"Conversão concluída ({opcoes_modelos[modelo_escolhido]} - OCR).")
                    with open(xlsx_final, "rb") as f:
                        st.download_button(
                            label="Baixar XLSX Convertido",
                            data=f,
                            file_name=os.path.basename(xlsx_final),
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                        )
                    st.write(f"Arquivo de texto filtrado gerado em: {txt_filtrado}")
            except Exception as e:
                st.error(f"Ocorreu um erro: {e}")
            
            # Remover o PDF original após o processamento
            if os.path.exists(caminho_pdf_salvo):
                os.remove(caminho_pdf_salvo)

if __name__ == "__main__":
    main()
