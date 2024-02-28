
Mov_dia = """
with 
L_status as (
select distinct
    ordemservicocaixalog.cod_ordemservicocaixa,
    max(ordemservicocaixalog.datahoraentrada) u_mov
from ordemservicocaixalog
WHERE
ordemservicocaixalog.cod_etapa not in (0,8,9,6,5)

group by cod_ordemservicocaixa

)
select
    case  ordemservicocaixa.cod_empresa
        when  01 then '01'
        when  04 then '02'
        when  06 then '08'
        when  07 then '05'
        when  08 then '06'
        when  09 then '09'
        when  10 then '10'
        when  11 then '11'
        when  12 then '13'
        when  13 then '12'
        when  14 then '14'
        when  15 then '15'
        when  16 then '07'
        when  17 then '30'
        end as "LOJA",
    L_status.cod_ordemservicocaixa OS ,
    ordemservicocaixalog.cod_etapa COD_ETAPA,
    case ordemservicocaixalog.cod_etapa
        when 00 then 'Etapa inicial'
        when 01 then 'Ordem de serviço no estoque'
        when 02 then 'Translado estoque -> laboratório'
        when 03 then 'Ordem de serviço no laboratório'
        when 04 then 'Translado laboratório -> loja'
        when 05 then 'Ordem de serviço recebida do laboratório'
        when 06 then 'Venda concluída e serviço na loja'
        when 07 then 'Translado loja (pós venda) -> estoque'
        when 08 then 'Ordem de serviço entregue ao cliente'
        when 09 then 'Ordem de serviço cancelada'
        when 10 then 'Aguardando compra de lentes'
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

left join transacao
    on transacao.cod_transacao = ordemservicocaixa.cod_transacao and transacao.cod_empresa = ordemservicocaixa.cod_empresa

where
    (ordemservicocaixa.cod_empresa is not null and  ordemservicocaixa.reparo = 'F')
    and ordemservicocaixalog.observacao not like ('%Cancelamento%')
"""


