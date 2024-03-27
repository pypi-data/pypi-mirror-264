from __future__ import annotations

from typing import Sequence

from backstage_catalog_client.models import EntityFilterQuery, EntityOrderQuery

# Random UUID to ensure no collisions
CATALOG_FILTER_EXISTS = "CATALOG_FILTER_EXISTS_0e15b590c0b343a2bae3e787e84c2111"
CATALOG_API_BASE_PATH = "/api/catalog"


def get_filter_value(entity_filter: EntityFilterQuery) -> list[str]:
    prepared_filters: list[str] = []
    # filter param can occur multiple times, for example
    # /api/catalog/entities?filter=metadata.name=wayback-search,kind=component&filter=metadata.name=www-artist,kind=component'
    # the "outer array" defined by `filter` occurrences corresponds to "anyOf" filters
    # the "inner array" defined within a `filter` param corresponds to "allOf" filters

    for filter_item in entity_filter:
        filter_parts: list[str] = []
        for key, value in filter_item.items():
            v_iter = value if isinstance(value, (list, tuple, set)) else [value]
            for v in v_iter:
                if v == CATALOG_FILTER_EXISTS:
                    filter_parts.append(key)
                elif isinstance(v, str):
                    filter_parts.append(f"{key}={v}")
        if filter_parts:
            prepared_filters.append(",".join(filter_parts))
    return prepared_filters


def encode_order(order: EntityOrderQuery | Sequence[EntityOrderQuery]) -> list[str]:
    if not isinstance(order, Sequence):
        order = [order]
    return [f"{el['order']}:{el['field']}" for el in order]
