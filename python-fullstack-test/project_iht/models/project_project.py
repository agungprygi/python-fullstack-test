# -*- coding: utf-8 -*-
from odoo import models, fields, api


class Project(models.Model):
    _inherit= "project.project"

    lokasi_proyek = fields.Text(string="Lokasi Proyek")
    source_aplikasi_pendukung = fields.Char(string="Source Aplikasi Pendukung")
    daftar_pekerja_remote = fields.Json(string="Daftar Pekerja Remote")

