
Mov_dia = """
with 
L_status as (
select distinct
    ordemservicocaixalog.cod_ordemservicocaixa,
    max(ordemservicocaixalog.datahoraentrada) u_mov,
    max(ordemservicocaixalog.cod_ordemservicocaixalog) u_log
from ordemservicocaixalog
WHERE
ordemservicocaixalog.cod_etapa not in (0,8,9,6,5)
group by cod_ordemservicocaixa

)
select
    L.NOME as "LOJA",
    L_status.cod_ordemservicocaixa OS ,
    ordemservicocaixalog.cod_etapa COD_ETAPA,
    case ordemservicocaixalog.cod_etapa
        when 00 then 'Etapa inicial'
        when 01 then 'Ordem de serviço no estoque'
        when 02 then 'Translado estoque -> laboratório'
        when 03 then 'Em montagem'
        when 04 then 'Translado laboratório -> loja'
        when 05 then 'Ordem de serviço recebida do laboratório'
        when 06 then 'Venda concluída e serviço na loja'
        when 07 then 'Translado loja (pós venda) -> estoque'
        when 08 then 'Ordem de serviço entregue ao cliente'
        when 09 then 'Ordem de serviço cancelada'
        when 10 then 'Compra realizada'
        when 11 then 'O.S. devolvida para tratamento'
        when 12 then 'O.S. em tratamento externo'
        when 13 then 'O.S. devolvida pelo cliente'
        when 14 then 'Translado loja (pós venda) -> estoque'
        when 15 then 'Aguardando armação'
        when 16 then 'Armação enviada'
        when 17 then 'Serviço forçar finalização'
        when 18 then 'Devolver para o laboratório'
        when 19 then 'Translado laboratório -> estoque'
        when 20 then 'Devolução estoque -> loja'
        else '<DESCONHECIDA>'
    end "ETAPA",
    cast(ordemservicocaixalog.datahoraentrada as date) "Ultima mov",
    ordemservicocaixa.dataprevisao PREVISAO
from L_status

join ordemservicocaixalog
    on (ordemservicocaixalog.cod_ordemservicocaixa = L_status.cod_ordemservicocaixa  and L_status.u_mov  = ordemservicocaixalog.datahoraentrada)
join ordemservicocaixa 
    on (ordemservicocaixalog.cod_ordemservicocaixa = ordemservicocaixa.cod_ordemservicocaixa and ordemservicocaixa.cod_clientereceita is not null)
LEFT JOIN PESSOA L
    ON L.COD_PESSOA = ordemservicocaixa.COD_EMPRESAORIGEM 
where
    --(ordemservicocaixa.cod_empresa is not null)
     ordemservicocaixalog.observacao not like ('%Cancelamento%')
"""


entradas_fiscais = """
WITH
TIPOS_ENTRADAS AS (
	SELECT 
		U.NOME,
		T.NUMEROTRANSACAO,
		T.DATAINCLUSAO,
		CASE 
			WHEN TP.TIPO IN ('AR', 'OC') THEN 'NF ARMACOES'
			WHEN TP.TIPO = 'LG' THEN 'NF LENTES'
		END TIPO
	FROM ENTRADA e 
	JOIN TRANSACAO t 
	ON t.COD_TRANSACAO  = e.COD_ENTRADA 
	JOIN PESSOA F
		ON F.COD_PESSOA  = t.COD_PESSOA  AND f.PESSOAFORNECEDOR = 'T'
	JOIN PESSOA l
		ON l.COD_PESSOA  = t.COD_EMPRESA 
	JOIN USUARIO u 
		ON U.COD_USUARIO = T.COD_USUARIO
	LEFT JOIN TRANSACAO_ITEM ti 
		ON TI.COD_TRANSACAO = T.COD_TRANSACAO 
	LEFT JOIN TABELA_PRODUTO tp 
		ON TP.COD_PRODUTO  = TI.COD_ITEM 	
	WHERE 
	T.DATAINCLUSAO >= '{datainit}'
	AND U.COD_GRUPOUSUARIO = 3
	AND T.TIPOTRANSACAO = 'ENF'
	AND TP.TIPO IN ('AR', 'OC', 'LG')
	GROUP BY 
		U.NOME,
		T.NUMEROTRANSACAO,
		T.DATAINCLUSAO,
		CASE 
			WHEN TP.TIPO IN ('AR', 'OC') THEN 'NF ARMACOES'
			WHEN TP.TIPO = 'LG' THEN 'NF LENTES'
		END
)
SELECT 
    TE.NOME,
    TE.DATAINCLUSAO,
    TE.TIPO,
    COUNT(TE.NUMEROTRANSACAO) QUANTIDADE
FROM TIPOS_ENTRADAS TE
GROUP BY 
    TE.NOME,
    TE.DATAINCLUSAO,
    TE.TIPO

"""