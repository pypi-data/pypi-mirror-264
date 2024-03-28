import copy
import json
import os
import unittest

import numpy as np
import pandas as pd

from looqbox.objects.tests import LooqObject
from looqbox.objects.tests import ObjTable
from looqbox.render.looqbox.base_looqbox_render import BrowserRender
from looqbox.utils.utils import open_file


def _set_keys_args(json_table, new_key):
    if isinstance(json_table, list):
        for item in json_table:
            _set_keys_args(item, new_key)
    elif isinstance(json_table, dict):
        if "key" in json_table:
            json_table["key"] = new_key
        for _, value in json_table.items():
            _set_keys_args(value, new_key)
    return json_table

class TestObjectTable(unittest.TestCase):
    """
    Test looq_table file
    """

    def setUp(self) -> None:
        data = np.array([
            [100, 120, 98, 73, 20, 157, 124, 0, 9999, 100],
            [100, 100, 100, 100, 100, 100, 100, 100, 100, 100]
        ]).T

        df = pd.DataFrame(data, columns=['Venda', 'Meta'])
        self.looq_object_table = ObjTable(df)

        self.visitor = BrowserRender()
        self.visitor.remove_nones = False

        self.categorical_object_table = ObjTable(pd.DataFrame(
            {
                "Cód. Estado": ["1SP", "1SP", "1SP", "2SC", "2SC", "2SC"],
                "Estado": ["SP", "SP", "SP", "SC", "SC", "SC"],
                "Cidade": ["São Paulo", "Itatiba", "Campinas", "Chapecó", "Xanxerê", "Xaxim"],
                "População": [12.18, 0.99, 1.53, 0.22, 0.11, 0.08]
            }
        ))

    def test_instance(self):
        looq_object_table = self.looq_object_table

        self.assertIsInstance(looq_object_table, LooqObject)

    def test_header_json_structure(self):
        looq_object_table = self.looq_object_table

        # Testing JSON header keys
        json_table_keys = list(looq_object_table.to_json_structure(self.visitor)["header"].keys())
        self.assertTrue("content" in json_table_keys, msg="content not found in header JSON structure test")
        self.assertTrue("visible" in json_table_keys, msg="visible not found in header JSON structure test")
        self.assertTrue("group" in json_table_keys, msg="group not found in header JSON structure test")

    def test_body_json_structure(self):
        looq_object_table = self.looq_object_table

        # Testing JSON body keys
        json_table_keys = list(looq_object_table.to_json_structure(self.visitor)["body"].keys())
        self.assertTrue("content" in json_table_keys, msg="content not found in body JSON structure test")
        self.assertTrue("_lq_column_config" in json_table_keys,
                        msg="_lq_column_config not found in body JSON structure test")

    def test_footer_json_structure(self):
        looq_object_table = self.looq_object_table

        # Testing JSON footer keys
        json_table_keys = list(looq_object_table.to_json_structure(self.visitor)["footer"].keys())
        self.assertTrue("content" in json_table_keys, msg="content not found in footer JSON structure test")
        self.assertTrue("subtotal" in json_table_keys, msg="subtotal not found in footer JSON structure test")

    def test_subtotal_structure(self):
        looq_object_table = self.looq_object_table
        looq_object_table.subtotal = [{"text": "Subtotal text", "link": "Subtotal link"}]
        json_table = looq_object_table.to_json_structure(self.visitor)

        # Testing JSON footer keys
        self.assertTrue(isinstance(json_table["footer"]["subtotal"], list))

    # def test_collapse_structure(self) -> None:
    #
    #     current_test_table = ObjTable(
    #         pd.read_csv(f"{os.path.dirname(__file__)}/reference/looq_table/collapsed_data.csv",
    #                                      sep=";", decimal=","))
    #
    #     current_test_table.row_hierarchy = current_test_table.data["ORDER"].tolist()
    #     current_test_table.collapsible = True
    #     json_table = current_test_table.to_json_structure(self.visitor)
    #     actual_body_json = json_table.get("body", {})#.get("content", {})
    #
    #     # set keys args to test-key to avoid random key generation
    #     actual_body_json = _set_keys_args(actual_body_json, "test-key")
    #
    #     # load expected json from reference/looq_table/categorical_table_body.json
    #     file = open_file(os.path.dirname(__file__), "reference", "looq_table", "collapsed_table.json")
    #     expected_body_json = json.load(file)
    #     file.close()
    #
    #     expected_body_json = _set_keys_args(expected_body_json, "test-key")
    #
    #     self.assertEqual(json.dumps(actual_body_json), json.dumps(expected_body_json))


    # test for col hierarchy collapse
    def test_collapse_structure_by_col_hierarchy(self) -> None:

        current_test_table = copy.deepcopy(self.categorical_object_table)
        current_test_table.col_hierarchy = [("Cód. Estado", "Estado"), "Cidade"]
        current_test_table.total_collapse = {
            "População": "População.sum()"
        }

        current_test_table.collapsible = True
        json_table = current_test_table.to_json_structure(self.visitor)
        actual_body_json = json_table.get("body", {})

        # set keys args to test-key to avoid random key generation
        actual_body_json = _set_keys_args(actual_body_json, "test-key")

        # load expected json from reference/looq_table/categorical_table_body.json
        file = open_file(os.path.dirname(__file__), "reference", "looq_table", "categorical_table_body.json")
        expected_body_json = json.load(file)
        file.close()

        self.assertEqual(actual_body_json, expected_body_json)


if __name__ == '__main__':
    unittest.main()
