#!/usr/bin/bash

sqlite3 -separator , tfc_cover.sqlite ".import tfc_code.csv tfc_code"
sqlite3 -separator , tfc_cover.sqlite ".import condition.csv condition"
sqlite3 -separator , tfc_cover.sqlite ".import po_fabric.csv po_fabric"
sqlite3 -separator , tfc_cover.sqlite ".import po.csv po"
sqlite3 -separator , tfc_cover.sqlite ".import poline.csv poline"
sqlite3 -separator , tfc_cover.sqlite ".import inv.csv inv"
sqlite3 -separator , tfc_cover.sqlite ".import invline.csv invline"
