#!/usr/bin/env python
# -*- coding: utf-8 -*-


class VersionMixin(object):

    info_collectors = None
    info_dependencies = None

    def __init__(self, *args, **kwargs):
        super(VersionMixin, self).__init__(*args, **kwargs)

        if self.info_collectors is None:
            raise NotImplemented("VersionMixin classes must implement "
                                 "``info_collectors``")
        self._collect_app_info()

    def _collect_app_info(self):
        self.info = {}

        for name, collector in self.info_collectors.items():
            self.info[name] = collector()
