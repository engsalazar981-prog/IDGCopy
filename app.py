import streamlit as st
import fitz
from PIL import Image

st.set_page_config(page_title="Verificador de documentos", layout="wide")

st.title("Verificador de documentos")
st.write("Protótipo inicial: carregue um PDF e visualize suas páginas.")

arquivo = st.file_uploader("Selecione um projeto em PDF", type=["pdf"])

if arquivo is not None:
    try:
        pdf = fitz.open(stream=arquivo.getvalue(), filetype="pdf")
        total_paginas = len(pdf)

        st.success(f"Arquivo: {arquivo.name} — {total_paginas} página(s)")

        pagina_escolhida = st.number_input(
            "Página para visualizar",
            min_value=1,
            max_value=total_paginas,
            value=1,
            step=1,
        )

        pagina = pdf[pagina_escolhida - 1]
        imagem = pagina.get_pixmap(matrix=fitz.Matrix(1.5, 1.5), alpha=False)
        imagem_pil = Image.frombytes(
            "RGB",
            [imagem.width, imagem.height],
            imagem.samples,
        )

        st.image(imagem_pil, caption=f"Página {pagina_escolhida}")

        texto = pagina.get_text().strip()
        with st.expander("Ver texto extraído desta página"):
            st.text(
                texto
                if texto
                else "Não foi encontrado texto selecionável nesta página."
            )

    except Exception as erro:
        st.error(f"Não foi possível abrir o PDF: {erro}")
