from looqbox.database.connections.connection_big_query import BigQueryConnection
import unittest


class MyTestCase(unittest.TestCase):

    def setUp(self):

        self.connection = BigQueryConnection("MockedName")


    def test_table_name_matcher_simple_query(self):
        query = """
        SELECT
           *
        FROM
            `google_billing.gcp_billing` AS t1
        WHERE
            1=1
            AND (
                t1.Date >= '2024-03-01'
                AND t1.Date < '2024-04-01'
            )
        ORDER BY
            1 DESC
             """

        self.connection.set_query_script(query)
        self.connection._get_table_name_from_query()
        self.assertEqual("google_billing.gcp_billing",
                         self.connection._get_table_name_from_query())

    def test_table_name_matcher_join_query(self):
        query = """
        SELECT
            *
        FROM
            `varejo_alimentar.FATO_VENDA_PRODUTO` AS t4
        LEFT JOIN
            `varejo_alimentar.DIM_LOJA` AS t1
            ON t4.ID_LOJA = t1.ID_LOJA
        WHERE
            1=1
            AND (
                t4.DATE >= '2024-03-11'
                AND t4.DATE < '2024-03-12'
            )
        GROUP BY
        ESTADO
        ORDER BY
            2 DESC,
            3 DESC,
            4 DESC
        LIMIT 1001
             """

        self.connection.set_query_script(query)
        self.connection._get_table_name_from_query()
        self.assertEqual("varejo_alimentar.FATO_VENDA_PRODUTO",
                         self.connection._get_table_name_from_query())

    def test_table_name_matcher_join_with_subquery(self):
        query = """
        SELECT
            *    
        FROM
        (
            WITH
              receita_companhia_por_dia AS (
              SELECT
                *
              FROM
                `looqlake-prod.hortifruti_prod.fato_receita_item` fri
              GROUP BY
                1,
                2 ),
              fri AS (
              SELECT
                *
              FROM
                `looqlake-prod.hortifruti_prod.fato_receita_item` AS t1
              LEFT JOIN
                `looqlake-prod.hortifruti_prod.dim_produto_hierarq` AS t2
              ON
                t1.SK_PRODUTO = t2.SK_PRODUTO
              GROUP BY
                1,
                2,
                3,
                4,
                5),
              ric AS (
              SELECT
                *
              FROM
                fri
              INNER JOIN (
                SELECT
                  *
                FROM
                  `looqlake-prod.hortifruti_prod.fato_receita_cupom` ) frc
              ON
                fri.SK_CUPOM = frc.SK_CUPOM
              LEFT JOIN
                `looqlake-prod.hortifruti_prod.dim_tpo_receita` tr
              ON
                tr.SK_TPO_RECEITA = frc.SK_TPO_RECEITA
              INNER JOIN (
                *
                FROM
                  `looqlake-prod.hortifruti_prod.dim_canal_venda_hierarq` ) cvh
              ON
                frc.SK_CANAL_VENDA = cvh.SK_CANAL_VENDA_MARCACAO_HIERQ
              GROUP BY
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10 )
            SELECT
              *
            FROM
              ric
            JOIN
              receita_companhia_por_dia rcd
            ON
              ric.SK_TEMPO = rcd.SK_TEMPO
              AND ric.SK_LOJA = rcd.SK_LOJA
            FULL JOIN (
              *
              FROM
                `looqlake-prod.hortifruti_prod.fato_orcamento_canal_venda_digital_categoria_loja_dia`
              GROUP BY
                1,
                2,
                3,
                4 ) focv
            ON
              ric.SK_LOJA = focv.SK_LOJA
              AND CAST(FORMAT_DATE('%Y%m%d', ric.SK_TEMPO) AS INT64) = focv.SK_TEMPO
              AND ric.COD_CATEGORIA = focv.COD_CATEGORIA
              AND ric.SK_CANAL_VENDA_ORCADO = focv.SK_CANAL_VENDA_ORCADO
            WHERE
              1=1
                AND TPO_CANAL_VENDA = "DIGITAL"
              --AND (ric.SK_TEMPO = '2024-01-28' OR focv.SK_TEMPO = 20240128)
            GROUP BY
              1,
              2,
              3,
              4,
              5,
              6,
              VLR_RECEITA_BRUTA_DIA
            ) AS t1
        LEFT JOIN
        `hortifruti_prod.dim_loja` AS t3
        ON t1.SK_LOJA = t3.SK_LOJA
        WHERE
            1 = 1
    	    AND t1.SK_TEMPO >= '2024-03-04' AND t1.SK_TEMPO <= '2024-03-04'
        GROUP BY
        1
        ,2
    LIMIT 1001"""

        self.connection.set_query_script(query)
        self.connection._get_table_name_from_query()
        self.assertEqual("looqlake-prod.hortifruti_prod.fato_receita_item",
                         self.connection._get_table_name_from_query())

    def test_table_name_matcher_query_with_alias(self):
        query = """
        SELECT
            ID_LOJA as `ID Da Loja`,
            NOME_LOJA AS `Nome Loja`,
            CIDADE As `Nome da Cidade`,
            ESTADO aS `Nome do Estado`,
            ENDERECO as `Endereço`
        FROM
            `looqlake-prod.varejo_alimentar.DIM_LOJA`
        LIMIT
            10
             """

        self.connection.set_query_script(query)
        self.connection._get_table_name_from_query()
        self.assertEqual("looqlake-prod.varejo_alimentar.DIM_LOJA",
                         self.connection._get_table_name_from_query())

if __name__ == '__main__':
    unittest.main()
