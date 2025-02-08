# Conversor de PDFs para Excel (Streamlit)

Este projeto é uma aplicação em **Streamlit** para extrair e processar dados de PDFs de diferentes modelos e convertê-los em arquivos **Excel** (`.xlsx`). A aplicação suporta quatro tipos de modelos de PDFs, cada um com sua própria lógica de extração e processamento.

## 📋 Funcionalidades

- **Modelo 1, 3 e 4 (OCR com Tesseract):**  
  Converte o PDF em imagens, extrai texto usando OCR e aplica regex para extrair informações estruturadas. As informações filtradas e tratadas são convertidas para um arquivo Excel.  

- **Modelo 2 (Tabula):**  
  Utiliza a biblioteca **Tabula** para extrair diretamente as tabelas do PDF. Após a extração, aplica limpeza e processamento das abas para gerar um arquivo Excel consolidado.  

- **Interface amigável:**  
  Upload de arquivos via Streamlit com botões para processar e baixar os arquivos convertidos.  

## 📂 Estrutura do Projeto

```
/
├── extracao.py           # Código principal da aplicação Streamlit
├── README.md             # Documentação do projeto
├── requirements.txt      # Dependências do projeto
├── uploads/              # Pasta temporária para armazenar PDFs enviados
├── arquivos_xlsx/        # Saída dos arquivos Excel gerados
└── historico_de_textos_extraidos/  # Arquivos .txt com texto extraído via OCR
```

## 🚀 Como Usar

1. **Instale as dependências:**  
   Certifique-se de ter Python 3.8+ instalado. Execute o seguinte comando para instalar as dependências necessárias:  

   ```bash
   pip install -r requirements.txt
   ```

2. **Execute a aplicação Streamlit:**  

   ```bash
   streamlit run extracao.py
   ```

3. **Na interface do Streamlit:**  
   - Selecione o tipo de modelo de PDF.  
   - Faça o upload do arquivo PDF.  
   - Clique em **"Processar"** para iniciar a conversão.  
   - Faça o download do arquivo **Excel** gerado.

## 📑 Tipos de Modelos

- **Modelo 1, 3 e 4 (OCR):** PDFs scaneados que exigem reconhecimento de texto para extrair informações. O processo utiliza **Tesseract OCR** com diferentes configurações de extração para garantir melhor precisão.  

- **Modelo 2 (Tabula):** PDFs estruturados contendo tabelas. O **Tabula** é utilizado para extrair diretamente as tabelas em um arquivo Excel intermediário antes de realizar o pós-processamento.  

## 🛠️ Tecnologias Utilizadas

- **Python 3.8+**  
- **Streamlit** (Interface Web)  
- **Pytesseract** (OCR)  
- **Tabula** (Extração de tabelas de PDFs)  
- **Pandas** (Manipulação de dados)  
- **OpenPyXL** (Manipulação de arquivos Excel)  

## 📦 Dependências

As principais dependências do projeto estão listadas no arquivo `requirements.txt`. Para instalá-las, execute:

```bash
pip install -r requirements.txt
```

### Exemplo do arquivo `requirements.txt`:
```
streamlit
pytesseract
pandas
tabula-py
openpyxl
Pillow
pdf2image
```

## 📝 Notas Importantes

- **Tesseract:** Certifique-se de ter o Tesseract instalado e configurado corretamente no seu sistema.  
- **Tabula:** O Tabula requer **Java** para funcionar corretamente. Verifique se o Java está instalado.  

## 📞 Suporte

Se você encontrar algum problema ou tiver sugestões, sinta-se à vontade para abrir uma **issue** ou entrar em contato.  

---

**Criado por Douglas H. Machado.**  
