from __future__ import annotations

import hashlib
from datetime import datetime

from sqlalchemy import select

from .database import SessionLocal
from .models import Categoria, Local, Registro, SolicitacaoRecuperacao, Usuario


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def list_categorias():
    db = SessionLocal()
    try:
        return db.scalars(select(Categoria).order_by(Categoria.id.desc())).all()
    finally:
        db.close()


def create_categoria(nome: str, descricao: str, ativa: bool):
    db = SessionLocal()
    try:
        item = Categoria(nome=nome, descricao=descricao, ativa=ativa)
        db.add(item)
        db.commit()
        db.refresh(item)
        return item
    finally:
        db.close()


def update_categoria(categoria_id: int, nome: str, descricao: str, ativa: bool):
    db = SessionLocal()
    try:
        item = db.get(Categoria, categoria_id)
        if item is None:
            return None
        item.nome = nome
        item.descricao = descricao
        item.ativa = ativa
        db.commit()
        db.refresh(item)
        return item
    finally:
        db.close()


def delete_categoria(categoria_id: int):
    db = SessionLocal()
    try:
        item = db.get(Categoria, categoria_id)
        if item is None:
            return False
        db.delete(item)
        db.commit()
        return True
    finally:
        db.close()


def list_locais():
    db = SessionLocal()
    try:
        return db.scalars(select(Local).order_by(Local.id.desc())).all()
    finally:
        db.close()


def create_local(nome: str, descricao: str, setor: str, ativo: bool):
    db = SessionLocal()
    try:
        item = Local(nome=nome, descricao=descricao, setor=setor, ativo=ativo)
        db.add(item)
        db.commit()
        db.refresh(item)
        return item
    finally:
        db.close()


def update_local(local_id: int, nome: str, descricao: str, setor: str, ativo: bool):
    db = SessionLocal()
    try:
        item = db.get(Local, local_id)
        if item is None:
            return None
        item.nome = nome
        item.descricao = descricao
        item.setor = setor
        item.ativo = ativo
        db.commit()
        db.refresh(item)
        return item
    finally:
        db.close()


def delete_local(local_id: int):
    db = SessionLocal()
    try:
        item = db.get(Local, local_id)
        if item is None:
            return False
        db.delete(item)
        db.commit()
        return True
    finally:
        db.close()


def list_usuarios():
    db = SessionLocal()
    try:
        return db.scalars(select(Usuario).order_by(Usuario.id.desc())).all()
    finally:
        db.close()


def create_usuario(nome: str, email: str, senha: str, vinculo: str, email_verificado: bool, situacao: str, perm_responsavel: bool, perm_admin: bool):
    db = SessionLocal()
    try:
        usuario = Usuario(
            nome=nome,
            email=email,
            senha_hash=hash_password(senha),
            vinculo=vinculo,
            email_verificado=email_verificado,
            situacao=situacao,
            perm_responsavel=perm_responsavel,
            perm_admin=perm_admin,
        )
        db.add(usuario)
        db.commit()
        db.refresh(usuario)
        return usuario
    finally:
        db.close()


def update_usuario(usuario_id: int, nome: str, email: str, senha: str | None, vinculo: str, email_verificado: bool, situacao: str, perm_responsavel: bool, perm_admin: bool):
    db = SessionLocal()
    try:
        usuario = db.get(Usuario, usuario_id)
        if usuario is None:
            return None
        usuario.nome = nome
        usuario.email = email
        if senha:
            usuario.senha_hash = hash_password(senha)
        usuario.vinculo = vinculo
        usuario.email_verificado = email_verificado
        usuario.situacao = situacao
        usuario.perm_responsavel = perm_responsavel
        usuario.perm_admin = perm_admin
        db.commit()
        db.refresh(usuario)
        return usuario
    finally:
        db.close()


def delete_usuario(usuario_id: int):
    db = SessionLocal()
    try:
        usuario = db.get(Usuario, usuario_id)
        if usuario is None:
            return False
        db.delete(usuario)
        db.commit()
        return True
    finally:
        db.close()


def list_registros():
    db = SessionLocal()
    try:
        return db.scalars(select(Registro).order_by(Registro.id.desc())).all()
    finally:
        db.close()


def create_registro(tipo: str, titulo: str, descricao: str, data_ocorrencia: datetime, categoria_id: int, local_id: int, usuario_id: int, situacao: str):
    db = SessionLocal()
    try:
        registro = Registro(
            tipo=tipo,
            titulo=titulo,
            descricao=descricao,
            data_ocorrencia=data_ocorrencia,
            categoria_id=categoria_id,
            local_id=local_id,
            usuario_id=usuario_id,
            situacao=situacao,
        )
        db.add(registro)
        db.commit()
        db.refresh(registro)
        return registro
    finally:
        db.close()


def update_registro(registro_id: int, tipo: str, titulo: str, descricao: str, data_ocorrencia: datetime, categoria_id: int, local_id: int, usuario_id: int, situacao: str):
    db = SessionLocal()
    try:
        registro = db.get(Registro, registro_id)
        if registro is None:
            return None
        registro.tipo = tipo
        registro.titulo = titulo
        registro.descricao = descricao
        registro.data_ocorrencia = data_ocorrencia
        registro.categoria_id = categoria_id
        registro.local_id = local_id
        registro.usuario_id = usuario_id
        registro.situacao = situacao
        db.commit()
        db.refresh(registro)
        return registro
    finally:
        db.close()


def delete_registro(registro_id: int):
    db = SessionLocal()
    try:
        registro = db.get(Registro, registro_id)
        if registro is None:
            return False
        db.delete(registro)
        db.commit()
        return True
    finally:
        db.close()


def list_solicitacoes():
    db = SessionLocal()
    try:
        return db.scalars(select(SolicitacaoRecuperacao).order_by(SolicitacaoRecuperacao.id.desc())).all()
    finally:
        db.close()


def create_solicitacao(usuario_id: int, registro_id: int, justificativa: str, situacao: str, responsavel_id: int | None):
    db = SessionLocal()
    try:
        item = SolicitacaoRecuperacao(
            usuario_id=usuario_id,
            registro_id=registro_id,
            justificativa=justificativa,
            situacao=situacao,
            responsavel_id=responsavel_id,
        )
        db.add(item)
        db.commit()
        db.refresh(item)
        return item
    finally:
        db.close()


def update_solicitacao(solicitacao_id: int, usuario_id: int, registro_id: int, justificativa: str, situacao: str, responsavel_id: int | None):
    db = SessionLocal()
    try:
        item = db.get(SolicitacaoRecuperacao, solicitacao_id)
        if item is None:
            return None
        item.usuario_id = usuario_id
        item.registro_id = registro_id
        item.justificativa = justificativa
        item.situacao = situacao
        item.responsavel_id = responsavel_id
        item.data_analise = datetime.utcnow() if situacao in {"aprovada", "recusada"} else None
        db.commit()
        db.refresh(item)
        return item
    finally:
        db.close()


def delete_solicitacao(solicitacao_id: int):
    db = SessionLocal()
    try:
        item = db.get(SolicitacaoRecuperacao, solicitacao_id)
        if item is None:
            return False
        db.delete(item)
        db.commit()
        return True
    finally:
        db.close()
