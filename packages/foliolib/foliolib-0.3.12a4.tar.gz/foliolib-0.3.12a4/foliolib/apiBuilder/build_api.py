# -*- coding: utf-8 -*-
# Copyright (C) 2022 Tobias Weber <tobi-weber@gmx.de>

import logging
import os

import inflection
from foliolib.apiBuilder.oas import build_from_oas
from foliolib.apiBuilder.raml import build_from_raml

log = logging.getLogger("foliolib.oas.build_api")


def build_api(
    module_dir,
    schema_path,
    schema_type,
    api_path="foliolib/folio/api",
    sphinx_doc_src="docs/source",
):
    schema_path = os.path.join(module_dir, schema_path)
    module_name = os.path.splitext(os.path.basename(module_dir.rstrip("/")))[0]
    module_name = module_name.replace("mod-", "").replace("-", "_")
    module_name = inflection.camelize(module_name, False)

    if not os.path.exists(api_path):
        os.makedirs(api_path)
    if not os.path.exists(sphinx_doc_src):
        os.makedirs(sphinx_doc_src)

    if schema_type.lower() == "raml":
        log.info("Build api from raml schemas")
        build_from_raml(
            schema_path, module_name, api_path=api_path, sphinx_doc_src=sphinx_doc_src
        )
    elif schema_type.lower() == "oas":
        log.info("Build api from open api schemas")
        build_from_oas(
            schema_path, module_name, api_path=api_path, sphinx_doc_src=sphinx_doc_src
        )
    else:
        log.info("Unknown type %s" % schema_type)
