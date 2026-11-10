import streamlit as st

from src.crud import create_solicitacao, delete_solicitacao, list_registros, list_solicitacoes, list_usuarios, update_solicitacao
from src.database import init_db

init_db()

st.title("CRUD - Solicitações de Recuperação")

registros = list_registros()
usuarios = list_usuarios()
solicitacoes = list_solicitacoes()

if solicitacoes:
    st.dataframe(
        [{"ID": item.id, "Registro": item.registro.titulo, "Usuário": item.usuario.nome, "Responsável": item.responsavel.nome if item.responsavel else "-", "Situação": item.situacao, "Justificativa": item.justificativa[:80]} for item in solicitacoes],
        use_container_width=True,
    )
else:
    st.info("Nenhuma solicitação cadastrada.")

if registros and usuarios:
    options = ["Nova solicitação"] + [f"{item.id} - {item.registro.titulo}" for item in solicitacoes]
    selection = st.selectbox("Selecionar registro", options)
    selected_id = None
    selected = None
    if selection != "Nova solicitação":
        selected_id = int(selection.split(" - ")[0])
        selected = next((item for item in solicitacoes if item.id == selected_id), None)

    with st.form("form_solicitacao"):
        usuario_id = st.selectbox("Usuário", [item.id for item in usuarios], format_func=lambda value: next(item.nome for item in usuarios if item.id == value), index=next((idx for idx, item in enumerate(usuarios) if item.id == selected.usuario_id), 0) if selected else 0)
        registro_id = st.selectbox("Registro relacionado", [item.id for item in registros], format_func=lambda value: next(item.titulo for item in registros if item.id == value), index=next((idx for idx, item in enumerate(registros) if item.id == selected.registro_id), 0) if selected else 0)
        justificativa = st.text_area("Justificativa", value=selected.justificativa if selected else "")
        responsavel_id = st.selectbox("Responsável que analisa", [None] + [item.id for item in usuarios], format_func=lambda value: "Nenhum" if value is None else next(item.nome for item in usuarios if item.id == value), index=(0 if selected is None or selected.responsavel_id is None else next((idx for idx, item in enumerate(usuarios) if item.id == selected.responsavel_id), 0) + 1))
        situacao = st.selectbox("Situação", ["pendente", "aprovada", "recusada"], index=["pendente", "aprovada", "recusada"].index(selected.situacao) if selected else 0)

        if selected_id is None:
            submitted = st.form_submit_button("Cadastrar solicitação")
        else:
            submitted = st.form_submit_button("Atualizar solicitação")

        if submitted:
            if selected_id is None:
                create_solicitacao(usuario_id, registro_id, justificativa, situacao, responsavel_id)
                st.success("Solicitação cadastrada com sucesso!")
            else:
                update_solicitacao(selected_id, usuario_id, registro_id, justificativa, situacao, responsavel_id)
                st.success("Solicitação atualizada com sucesso!")
            st.rerun()

    if selected_id is not None:
        if st.button("Excluir solicitação"):
            delete_solicitacao(selected_id)
            st.success("Solicitação removida com sucesso!")
            st.rerun()
else:
    st.warning("Cadastre usuários e registros antes de criar solicitações.")
