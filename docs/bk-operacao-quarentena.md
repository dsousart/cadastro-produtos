# Operacao BK: Ativa vs Quarentena

**Data:** 2026-02-26  
**Status:** Ativo (procedimento operacional)

## Objetivo

Manter a **BK ativa** limpa para uso do gerador, movendo arquivos ruidosos ou fracos para **quarentena** em `base_conhecimento/_pendente` com rastreabilidade.

## Regras Operacionais

### BK Ativa (`base_conhecimento/{categoria}`)
- Deve conter arquivos aptos para consulta do gerador.
- Meta operacional atual: **0 erros** e **0 warnings** no recorte ativo (excluindo `_pendente`).
- Arquivos duplicados de reprocessamento: manter apenas a melhor versao ativa.

### Quarentena (`base_conhecimento/_pendente`)
- Recebe arquivos com:
- ruido de ecommerce/reviews
- conteudo muito curto / baixa densidade tecnica
- duplicatas intermediarias de reprocessamento
- Mantem rastreabilidade e material para revisao futura.

## Criterios de Movimentacao

Mover para `_pendente` quando ocorrer pelo menos um:
- `Ruido: Excesso de termos de ruído`
- `Ruido: Conteudo de reviews detectado em Detalhes`
- warnings persistentes de baixo valor em arquivos importados/gerados antigos (quando houver versao melhor)
- duplicata de reprocessamento substituida por versao superior

## Fluxo de Saneamento (Padrao)

1. Rodar `python pipeline\bk_validate.py --base base_conhecimento`
2. Identificar candidatos na BK ativa
3. Mover para `base_conhecimento/_pendente` (nunca apagar direto)
4. Registrar manifesto em `base_conhecimento/_reports/`
5. Revalidar e confirmar BK ativa limpa

## Manifestos

Todo saneamento deve gerar um JSON em `base_conhecimento/_reports/` com:
- `source`
- `target`
- `reason`
- `moved_at`
- opcional: `replacement_kept`

## Observacoes

- O validador atual reporta findings de toda a base, incluindo `_pendente`; por isso, o indicador operacional principal deve considerar o recorte **ativo** separadamente.
- `_pendente` funciona como quarentena, nao como erro de processo.
