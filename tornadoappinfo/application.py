#!/usr/bin/env python
# -*- coding: utf-8 -*-


class VersionMixin(object):

    info_collectors = {}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._collect_app_info()

    def _collect_app_info(self):
        self.info = {}

        for name, collector in self.info_collectors.items():
            self.info[name] = collector()
