from __future__ import annotations

from datetime import date, datetime
from typing import Any, Dict, List, Literal, Optional

from pydantic import BaseModel, ConfigDict, Field, HttpUrl


class PromocaoInput(BaseModel):
    preco_promocional: float = Field(..., gt=0)
    validade: date


class GuidelinesMarcaInput(BaseModel):
    termos_proibidos: List[str] = Field(default_factory=list)


class RegrasCategoriaInput(BaseModel):
    tamanhos_validos: List[str] = Field(default_factory=list)
    cores_validas: List[str] = Field(default_factory=list)


class RestricoesLegaisInput(BaseModel):
    claims_proibidos: List[str] = Field(default_factory=list)


class ProductInput(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "sku": "CAM-001",
                "nome_produto": "Camisa Oxford",
                "descricao_bruta": "Camisa social em algodao com toque macio.",
                "marca": "Lumen",
                "categoria": "camisa",
                "subcategoria": "social",
                "tamanhos": ["P", "M", "G"],
                "cores": ["Azul Marinho", "Branco"],
                "composicao": "100% algodao",
                "tecido": "oxford",
                "modelagem": "regular",
                "acabamento": "costuras reforcadas",
                "colecao": "essenciais",
                "preco": 299.9,
                "promocao": {
                    "preco_promocional": 249.9,
                    "validade": "2026-03-31",
                },
                "imagens": [
                    "https://cdn.exemplo.com/cam-001-1.jpg",
                    "https://cdn.exemplo.com/cam-001-2.jpg",
                    "https://cdn.exemplo.com/cam-001-3.jpg",
                ],
                "guidelines_marca": {"termos_proibidos": ["barato", "descartavel"]},
                "regras_categoria": {
                    "tamanhos_validos": ["P", "M", "G", "GG"],
                    "cores_validas": ["Azul Marinho", "Branco", "Preto"],
                },
                "restricoes_legais": {"claims_proibidos": ["cura", "milagroso"]},
                "usuario": "demo",
                "versao_pipeline": "1.0.0",
            }
        }
    )

    sku: str = Field(..., min_length=1)
    nome_produto: str = Field(..., min_length=1)
    descricao_bruta: str = Field(..., min_length=1)
    marca: str = Field(..., min_length=1)
    categoria: str = Field(..., min_length=1)
    subcategoria: Optional[str] = None
    tamanhos: List[str] = Field(default_factory=list)
    cores: List[str] = Field(default_factory=list)
    composicao: Optional[str] = None
    tecido: Optional[str] = None
    modelagem: Optional[str] = None
    acabamento: Optional[str] = None
    colecao: Optional[str] = None
    preco: float = Field(..., gt=0)
    promocao: Optional[PromocaoInput] = None
    imagens: List[HttpUrl] = Field(..., min_length=1)
    guidelines_marca: Optional[GuidelinesMarcaInput] = None
    regras_categoria: Optional[RegrasCategoriaInput] = None
    restricoes_legais: Optional[RestricoesLegaisInput] = None
    usuario: Optional[str] = None
    versao_pipeline: Optional[str] = None


class AtributosNormalizadosOutput(BaseModel):
    categoria: Optional[str] = None
    subcategoria: Optional[str] = None
    tecido: Optional[str] = None
    composicao: Optional[str] = None
    modelagem: Optional[str] = None
    acabamento: Optional[str] = None
    colecao: Optional[str] = None
    cores: List[str] = Field(default_factory=list)
    tamanhos: List[str] = Field(default_factory=list)


class SeoOutput(BaseModel):
    meta_title: str
    meta_description: str
    slug: str


class AuditoriaDetalheOutput(BaseModel):
    area: str
    regra: str
    severidade: str
    status: Literal["pass", "fail", "skip"]
    evidencia: str


class AuditoriaOutput(BaseModel):
    audit_id: str
    timestamp: datetime
    usuario: Optional[str] = None
    versao_pipeline: Optional[str] = None
    resultado: Literal["aprovado", "reprovado"]
    motivos_reprovacao: List[str] = Field(default_factory=list)
    detalhes: List[AuditoriaDetalheOutput] = Field(default_factory=list)


class ProductOutput(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "titulo": "camisa Camisa Oxford Lumen premium masculino",
                "subtitulo": "oxford regular. acabamento costuras reforcadas. colecao essenciais. ideal para uso versatil e duradouro",
                "descricao": "Camisa Oxford Lumen em oxford com regular. Composicao: 100% algodao. Acabamento: costuras reforcadas.",
                "bullet_points": [
                    "Tecido oxford com toque premium",
                    "Modelagem regular para bom caimento",
                    "Cores: Azul Marinho, Branco",
                ],
                "atributos_normalizados": {
                    "categoria": "camisa",
                    "subcategoria": "social",
                    "tecido": "oxford",
                    "composicao": "100% algodao",
                    "modelagem": "regular",
                    "acabamento": "costuras reforcadas",
                    "colecao": "essenciais",
                    "cores": ["Azul Marinho", "Branco"],
                    "tamanhos": ["P", "M", "G"],
                },
                "tags": ["camisa", "social", "oxford"],
                "seo": {
                    "meta_title": "camisa Camisa Oxford Lumen premium masculino",
                    "meta_description": "oxford regular...",
                    "slug": "camisa-camisa-oxford-lumen",
                },
                "score_qualidade": 85,
                "auditoria": {
                    "audit_id": "449f7e72-19b1-4ac4-9ec6-8bcea8170554",
                    "timestamp": "2026-02-23T19:57:01.621950+00:00",
                    "usuario": "demo",
                    "versao_pipeline": "1.0.0",
                    "resultado": "aprovado",
                    "motivos_reprovacao": [],
                    "detalhes": [],
                },
            }
        }
    )

    titulo: str
    subtitulo: str
    descricao: str
    bullet_points: List[str] = Field(default_factory=list)
    atributos_normalizados: AtributosNormalizadosOutput
    tags: List[str] = Field(default_factory=list)
    seo: SeoOutput
    score_qualidade: int = Field(..., ge=0, le=100)
    auditoria: AuditoriaOutput


class ProductCreateResponse(ProductOutput):
    """API response shape for Story 1.3 (can extend core output without breaking CR2 fields)."""

    audit_id: Optional[str] = None
    timestamp: Optional[datetime] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)


class ProductRecordListItem(BaseModel):
    id: str
    sku: str
    nome_produto: str
    marca: str
    status: str
    score_qualidade: Optional[int] = None
    created_at: datetime
    updated_at: datetime


class PaginationMeta(BaseModel):
    total: int
    limit: int
    offset: int


class ProductListResponse(BaseModel):
    items: List[ProductRecordListItem] = Field(default_factory=list)
    pagination: PaginationMeta


class ProductRecordDetail(BaseModel):
    id: str
    tenant_id: Optional[str] = None
    generation_job_id: Optional[str] = None
    sku: str
    nome_produto: str
    marca: str
    status: str
    score_qualidade: Optional[int] = None
    input_payload: Dict[str, Any]
    output_payload: Optional[Dict[str, Any]] = None
    created_at: datetime
    updated_at: datetime
