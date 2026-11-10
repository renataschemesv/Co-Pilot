import streamlit as st

from src.crud import create_registro, delete_registro, list_categorias, list_locais, list_registros, list_usuarios, update_registro
from src.database import init_db

init_db()

st.title("CRUD - Registros")

categorias = list_categorias()
locais = list_locais()
usuarios = list_usuarios()
registros = list_registros()

if registros:
    st.dataframe(
        [{"ID": item.id, "Tipo": item.tipo, "Título": item.titulo, "Categoria": item.categoria.nome, "Local": item.local.nome, "Usuário": item.usuario.nome, "Situação": item.situacao} for item in registros],
        use_container_width=True,
    )
else:
    st.info("Nenhum registro cadastrado.")

if categorias and locais and usuarios:
    options = ["Novo registro"] + [f"{item.id} - {item.titulo}" for item in registros]
    selection = st.selectbox("Selecionar registro", options)
    selected_id = None
    selected = None
    if selection != "Novo registro":
        selected_id = int(selection.split(" - ")[0])
        selected = next((item for item in registros if item.id == selected_id), None)

    with st.form("form_registro"):
        tipo = st.selectbox("Tipo", ["perdido", "encontrado"], index=["perdido", "encontrado"].index(selected.tipo) if selected else 0)
        titulo = st.text_input("Título", value=selected.titulo if selected else "")
        descricao = st.text_area("Descrição", value=selected.descricao if selected else "")
        data_ocorrencia = st.date_input("Data aproximada", value=selected.data_ocorrencia.date() if selected else None)
        categoria_id = st.selectbox("Categoria", [item.id for item in categorias], format_func=lambda value: next(item.nome for item in categorias if item.id == value), index=next((idx for idx, item in enumerate(categorias) if item.id == selected.categoria_id), 0) if selected else 0)
        local_id = st.selectbox("Local", [item.id for item in locais], format_func=lambda value: next(item.nome for item in locais if item.id == value), index=next((idx for idx, item in enumerate(locais) if item.id == selected.local_id), 0) if selected else 0)
        usuario_id = st.selectbox("Usuário", [item.id for item in usuarios], format_func=lambda value: next(item.nome for item in usuarios if item.id == value), index=next((idx for idx, item in enumerate(usuarios) if item.id == selected.usuario_id), 0) if selected else 0)
        situacao = st.selectbox("Situação", ["ativo", "recuperado", "arquivado"], index=["ativo", "recuperado", "arquivado"].index(selected.situacao) if selected else 0)

        if selected_id is None:
            submitted = st.form_submit_button("Cadastrar registro")
        else:
            submitted = st.form_submit_button("Atualizar registro")

        if submitted:
            if selected_id is None:
                create_registro(tipo, titulo, descricao, data_ocorrencia, categoria_id, local_id, usuario_id, situacao)
                st.success("Registro cadastrado com sucesso!")
            else:
                update_registro(selected_id, tipo, titulo, descricao, data_ocorrencia, categoria_id, local_id, usuario_id, situacao)
                st.success("Registro atualizado com sucesso!")
            st.rerun()

    if selected_id is not None:
        if st.button("Excluir registro"):
            delete_registro(selected_id)
            st.success("Registro removido com sucesso!")
            st.rerun()
else:
    st.warning("Cadastre categorias, locais e usuários antes de registrar objetos.")
