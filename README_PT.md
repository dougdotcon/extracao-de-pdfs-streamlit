# Extrator de Dados de PDF

Uma aplicação robusta baseada em Streamlit, projetada para simplificar a extração e o processamento de dados de arquivos PDF de vários formatos. A ferramenta converte dados não estruturados ou semi-estruturados em planilhas Excel organizadas, utilizando Optical Character Recognition (OCR) para documentos digitalizados ou extração direta de tabelas para arquivos estruturados.

## 📋 Funcionalidades

- **Processamento Multi-Modelo:**
  - **Modelos 1, 3 e 4 (OCR):** Converte PDFs em imagens, extrai texto usando Tesseract OCR e aplica padrões regex para estruturar os dados. Ideal para documentos digitalizados.
  - **Modelo 2 (Tabula):** Extrai tabelas diretamente de PDFs usando a biblioteca Tabula. Realiza limpeza dos dados e consolidação antes de gerar o arquivo Excel final.

- **Interface Amigável:**
  - Upload simples de arquivos via dashboard do Streamlit.
  - Botões interativos para processar e baixar os relatórios gerados.

## 📂 Estrutura do Projeto

bash
/pdf_data_extractor
├── app.py                  # Código principal da aplicação Streamlit
├── README.md               # Documentação do projeto
├── requirements.txt        # Dependências do projeto
├── uploads/                # Armazenamento temporário para PDFs enviados
├── outputs/                # Arquivos Excel (.xlsx) gerados
└── extracted_texts/        # Arquivos de texto brutos extraídos via OCR


## 🚀 Começando

### Pré-requisitos
- Python 3.8 ou superior.
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) instalado no seu sistema (necessário para os Modelos 1, 3 e 4).

### Instalação
1. **Clonar o repositório:**
   bash
   git clone https://github.com/seu-usuario/pdf_data_extractor.git
   cd pdf_data_extractor
   

2. **Instalar as dependências Python:**
   bash
   pip install -r requirements.txt
   

### Executando a Aplicação

Inicie o servidor Streamlit:
bash
streamlit run app.py


Navegue até a URL local fornecida no seu terminal para utilizar a aplicação.

## 🛠️ Stack Tecnológica

- **Streamlit:** Para desenvolvimento rápido de aplicações web e UI.
- **Pytesseract & pdf2image:** Para processamento OCR de PDFs digitalizados.
- **Tabula-py:** Para extrair tabelas de PDFs estruturados.
- **Pandas:** Para manipulação e limpeza de dados.
- **OpenPyXL:** Para escrita de arquivos Excel.

## 📦 Dependências

Certifique-se de que todos os pacotes necessários estão instalados:

bash
streamlit
pytesseract
pandas
tabula-py
openpyxl
Pillow
pdf2image


## ⚠️ Notas Importantes

- **Instalação do Tesseract:** A aplicação depende do binário do Tesseract estar instalado e acessível via PATH do sistema. Certifique-se de que está corretamente instalado no seu OS.
- **Dependência Java do Tabula:** O Tabula requer um Java Runtime Environment (JRE) para funcionar. Certifique-se de que o Java está instalado.
- **Manipulação de Arquivos:** Os diretórios `uploads` e `outputs` são usados para armazenamento temporário. Certifique-se de que a aplicação tem permissões de escrita para essas pastas.