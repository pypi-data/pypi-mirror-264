#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# Copyright 2021-2024 NXP
#
# SPDX-License-Identifier: BSD-3-Clause

"""Helper module for blhost application."""

from copy import deepcopy
from typing import Any, Optional, Type

import click

from spsdk.exceptions import SPSDKError
from spsdk.mboot.commands import (
    KeyProvUserKeyType,
    TrustProvKeyType,
    TrustProvOemKeyType,
    TrustProvWrappingKeyType,
)
from spsdk.mboot.properties import PropertyTag
from spsdk.utils.misc import value_to_int
from spsdk.utils.spsdk_enum import SpsdkEnum


class OemGenMasterShareHelp(click.Command):
    """Class for customized "usage" help line for oem_gen_master_share command."""

    def format_usage(self, ctx: Any, formatter: Any) -> None:
        """Customizes "usage" help line for oem_gen_master_share command."""
        click.echo("Usage: blhost trust-provisioning oem_gen_master_share [OPTIONS]")
        indent = 7 * "\t"
        click.echo(indent + "OEM_SHARE_INPUT_ADDR")
        click.echo(indent + "OEM_SHARE_INPUT_SIZE")
        click.echo(indent + "OEM_ENC_SHARE_OUTPUT_ADDR")
        click.echo(indent + "OEM_ENC_SHARE_OUTPUT_SIZE")
        click.echo(indent + "OEM_ENC_MASTER_SHARE_OUTPUT_ADDR")
        click.echo(indent + "OEM_ENC_MASTER_SHARE_OUTPUT_SIZE")
        click.echo(indent + "OEM_CUST_CERT_PUK_OUTPUT_ADDR")
        click.echo(indent + "OEM_CUST_CERT_PUK_OUTPUT_SIZE")


class OemSetMasterShareHelp(click.Command):
    """Class for customized "usage" help line for oem_set_master_share command."""

    def format_usage(self, ctx: Any, formatter: Any) -> None:
        """Customizes "usage" help line for oem_set_master_share command."""
        click.echo("Usage: blhost trust-provisioning oem_set_master_share [OPTIONS]")
        indent = 7 * "\t"
        click.echo(indent + "OEM_SHARE_INPUT_ADDR")
        click.echo(indent + "OEM_SHARE_INPUT_SIZE")
        click.echo(indent + "OEM_ENC_MASTER_SHARE_INPUT_ADDR")
        click.echo(indent + "OEM_ENC_MASTER_SHARE_INPUT_SIZE")


PROPERTIES_NAMES = {
    0: "list-properties",
    1: "current-version",
    2: "available-peripherals",
    3: "flash-start-address",
    4: "flash-size-in-bytes",
    5: "flash-sector-size",
    6: "flash-block-count",
    7: "available-commands",
    8: "check-status",
    9: "reserved",
    10: "verify-writes",
    11: "max-packet-size",
    12: "reserved-regions",
    13: "reserved_1",
    14: "ram-start-address",
    15: "ram-size-in-bytes",
    16: "system-device-id",
    17: "security-state",
    18: "unique-device-id",
    19: "flash-fac-support",
    20: "flash-access-segment-size",
    21: "flash-access-segment-count",
    22: "flash-read-margin",
    23: "qspi/otfad-init-status",
    24: "target-version",
    25: "external-memory-attributes",
    26: "reliable-update-status",
    27: "flash-page-size",
    28: "irq-notify-pin",
    29: "pfr-keystore_update-opt",
    30: "byte-write-timeout-ms",
    31: "fuse-locked-status",
}
# TODO move to database
KW45XX = {
    10: "verify-erase",
    20: "boot-status",
    21: "loadable-fw-version",
    22: "fuse-program-voltage",
}

PROPERTIES_OVERRIDE = {"kw45xx": KW45XX, "k32w1xx": KW45XX}


def parse_property_tag(property_tag: str, family: Optional[str] = None) -> PropertyTag:
    """Convert the property as name or stringified number into integer.

    :param property_tag: Name or number of the property tag
    :param family: supported family
    :return: Property integer tag
    """
    properties_dict = deepcopy(PROPERTIES_NAMES)
    if family and family in PROPERTIES_OVERRIDE.keys():
        properties_dict.update(PROPERTIES_OVERRIDE[family])
    try:
        return PropertyTag.from_tag(value_to_int(property_tag))
    except SPSDKError:
        for key, value in properties_dict.items():
            if value == property_tag:
                return PropertyTag.from_tag(key)
        return PropertyTag.UNKNOWN


def parse_key_prov_key_type(key_type: str) -> int:
    """Convert the key type as name or stringified number into integer.

    :param key_type: Name or number of the Key type
    :return: key type number
    """
    return _parse_key_type(key_type, KeyProvUserKeyType, 0xFF)


def parse_trust_prov_oem_key_type(key_type: str) -> int:
    """Convert the key type as name or stringified number into integer.

    :param key_type: Name or number of the Key type
    :return: key type number
    """
    return _parse_key_type(key_type, TrustProvOemKeyType)


def parse_trust_prov_key_type(key_type: str) -> int:
    """Convert the key type as name or stringified number into integer.

    :param key_type: Name or number of the Key type
    :return: key type number
    """
    return _parse_key_type(key_type, TrustProvKeyType)


def parse_trust_prov_wrapping_key_type(key_type: str) -> int:
    """Convert the key type as name or stringified number into integer.

    :param key_type: Name or number of the Key type
    :return: key type number
    """
    return _parse_key_type(key_type, TrustProvWrappingKeyType)


def _parse_key_type(
    user_input: str, collection: Type[SpsdkEnum], default: Optional[int] = None
) -> int:
    try:
        return value_to_int(user_input)
    except SPSDKError:
        key_type = user_input.upper()
        key_type_int = collection.get_tag(key_type) if collection.contains(key_type) else default
        if key_type_int is None:
            raise SPSDKError(  # pylint: disable=raise-missing-from
                f"Unable to find '{user_input}' in '{collection.__name__}'"
            )
        return key_type_int
