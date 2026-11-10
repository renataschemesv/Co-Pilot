from __future__ import annotations

from datetime import datetime
from typing import Optional

from sqlalchemy import Boolean, DateTime, ForeignKey, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Categoria(Base):
    __tablename__ = "categorias"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nome: Mapped[str] = mapped_column(String(150), nullable=False, unique=True)
    descricao: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    data_cadastro: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    ativa: Mapped[bool] = mapped_column(Boolean, default=True)

    registros: Mapped[list["Registro"]] = relationship(back_populates="categoria")


class Local(Base):
    __tablename__ = "locais"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nome: Mapped[str] = mapped_column(String(150), nullable=False, unique=True)
    descricao: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    setor: Mapped[Optional[str]] = mapped_column(String(120), nullable=True)
    data_cadastro: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    ativo: Mapped[bool] = mapped_column(Boolean, default=True)

    registros: Mapped[list["Registro"]] = relationship(back_populates="local")


class Usuario(Base):
    __tablename__ = "usuarios"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nome: Mapped[str] = mapped_column(String(150), nullable=False)
    email: Mapped[str] = mapped_column(String(200), nullable=False, unique=True)
    senha_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    data_cadastro: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    vinculo: Mapped[str] = mapped_column(String(50), nullable=False)
    email_verificado: Mapped[bool] = mapped_column(Boolean, default=False)
    situacao: Mapped[str] = mapped_column(String(50), nullable=False, default="pendente")
    perm_responsavel: Mapped[bool] = mapped_column(Boolean, default=False)
    perm_admin: Mapped[bool] = mapped_column(Boolean, default=False)

    registros: Mapped[list["Registro"]] = relationship(back_populates="usuario")
    solicitacoes: Mapped[list["SolicitacaoRecuperacao"]] = relationship(
        back_populates="usuario",
        foreign_keys="[SolicitacaoRecuperacao.usuario_id]",
    )
    analises: Mapped[list["SolicitacaoRecuperacao"]] = relationship(
        back_populates="responsavel",
        foreign_keys="[SolicitacaoRecuperacao.responsavel_id]",
    )


class Registro(Base):
    __tablename__ = "registros"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    tipo: Mapped[str] = mapped_column(String(30), nullable=False)  # perdido ou encontrado
    titulo: Mapped[str] = mapped_column(String(200), nullable=False)
    descricao: Mapped[str] = mapped_column(Text, nullable=False)
    data_ocorrencia: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    data_criacao: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    situacao: Mapped[str] = mapped_column(String(40), nullable=False, default="ativo")

    categoria_id: Mapped[int] = mapped_column(ForeignKey("categorias.id"), nullable=False)
    local_id: Mapped[int] = mapped_column(ForeignKey("locais.id"), nullable=False)
    usuario_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id"), nullable=False)

    categoria: Mapped[Categoria] = relationship(back_populates="registros")
    local: Mapped[Local] = relationship(back_populates="registros")
    usuario: Mapped[Usuario] = relationship(back_populates="registros")
    solicitacoes: Mapped[list["SolicitacaoRecuperacao"]] = relationship(back_populates="registro")


class SolicitacaoRecuperacao(Base):
    __tablename__ = "solicitacoes_recuperacao"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    data_solicitacao: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    justificativa: Mapped[str] = mapped_column(Text, nullable=False)
    situacao: Mapped[str] = mapped_column(String(30), nullable=False, default="pendente")
    data_analise: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    usuario_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id"), nullable=False)
    registro_id: Mapped[int] = mapped_column(ForeignKey("registros.id"), nullable=False)
    responsavel_id: Mapped[Optional[int]] = mapped_column(ForeignKey("usuarios.id"), nullable=True)

    usuario: Mapped[Usuario] = relationship(back_populates="solicitacoes", foreign_keys=[usuario_id])
    responsavel: Mapped[Optional[Usuario]] = relationship(back_populates="analises", foreign_keys=[responsavel_id])
    registro: Mapped[Registro] = relationship(back_populates="solicitacoes")
