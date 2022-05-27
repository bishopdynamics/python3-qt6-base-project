#!/usr/bin/env python3

#  Contract Explorer Dialog Module
#   all the control logic for dialog lives here, the ui lives in DialogContractExplorer.py
#   DialogContractExplorer.py is baked from DialogContractExplorer.ui

# Created 2022 by James Bishop (james@bishopdynamics.com)

from Mod_Util import print_traceback
from PyQt6.QtWidgets import QDialog

from DialogContractExplorer import Ui_Dialog as ContractExplorer_Dialog
from Mod_dictTreeModel import TreeModel


class DialogContractExplorer(QDialog, ContractExplorer_Dialog):
    # contract explorer dialog
    def __init__(self, contracts: list):
        super().__init__()
        self.setupUi(self)
        self.contracts = contracts
        self.pushButton_close.clicked.connect(self.cleanup)
        self.load_contract(contracts[0])
        self.comboBox_contracts.currentTextChanged.connect(self.combobox_changed)
        self.pushButton_expand.clicked.connect(self.expand_tree)
        self.pushButton_collapse.clicked.connect(self.collapse_tree)
        self.populate_combobox()

    def cleanup(self):
        # cleanup any connections
        self.close()

    def expand_tree(self):
        # expand all items of treeview
        self.treeView_result.expandAll()

    def collapse_tree(self):
        # collapse all items of treeview
        self.treeView_result.collapseAll()

    def load_contract(self, contract: dict):
        # load contract data into treeview
        try:
            # load first contract into treeview
            model = TreeModel(contract)
            self.treeView_result.setModel(model)
            self.treeView_result.resizeColumnToContents(0)
        except Exception as ex:
            print('failed to load contract: %s' % ex)
            print_traceback()

    def populate_combobox(self, ):
        sorted_contracts = sorted(self.contracts, key=lambda x: str(x['vendor']).lower())
        for contract in sorted_contracts:
            item_display = '%s (%s) %s - %s' % (contract['vendor'], contract['id'], contract['start'], contract['end'])
            item_value = contract['id']
            self.comboBox_contracts.addItem(item_display, item_value)

    def combobox_changed(self):
        selected_contract_id = self.comboBox_contracts.currentData()
        selected_contract = {}
        for contract in self.contracts:
            if contract['id'] == selected_contract_id:
                selected_contract = contract
                break
        self.load_contract(selected_contract)
