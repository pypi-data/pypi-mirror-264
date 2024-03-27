import logging
import json
from hnt_sap_gui import SapGui
from hnt_sap_gui.nota_fiscal.nota_pedido_transaction import NotaPedidoTransaction

def test_create():
    with open("./devdata/nota_pedido_0.1.9.json", "r", encoding="utf-8") as arquivo_json: nota_pedido = json.load(arquivo_json)

    codigo = None
    # codigo = NotaPedidoTransaction().execute(nota_pedido=nota_pedido)
    codigo = SapGui().hnt_run_transaction(nota_pedido)
    assert codigo is not None
