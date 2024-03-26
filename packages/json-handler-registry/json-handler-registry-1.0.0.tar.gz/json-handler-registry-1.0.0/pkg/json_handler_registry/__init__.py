#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright by: P.J. Grochowski

import json
from functools import partial
from typing import Type, Union, cast

from json_handler_registry.decoder import DecoderRegistryDict, IJsonDecoder, _JsonDecoderRegistry
from json_handler_registry.encoder import EncoderRegistryDict, IJsonEncoder, _JsonEncoderRegistry

__version_info__ = (1, 0, 0)
__version__ = '.'.join([str(i) for i in __version_info__])
__package_name__ = str(__package__).replace('_', '-')


class JsonHandlerRegistry:

    _ENCODER_REGISTRY: EncoderRegistryDict = {}
    _DECODER_REGISTRY: DecoderRegistryDict = {}

    @staticmethod
    def isEnabled() -> bool:
        return (
            isinstance(json.dumps, partial) and
            isinstance(json.loads, partial)
        )

    @classmethod
    def enable(cls) -> None:
        if cls.isEnabled():
            return

        json.dumps = partial(
            json.dumps,
            cls=partial(
                _JsonEncoderRegistry,
                registry=cls._ENCODER_REGISTRY
            )
        )
        json.loads = partial(
            json.loads,
            cls=partial(
                _JsonDecoderRegistry,
                registry=cls._DECODER_REGISTRY
            )
        )

    @classmethod
    def disable(cls) -> None:
        if cls.isEnabled():
            json.dumps = cast(partial, json.dumps).func
            json.loads = cast(partial, json.loads).func

    @classmethod
    def registerEncoder(cls, jsonEncoder: IJsonEncoder) -> None:
        cls._ENCODER_REGISTRY[type(jsonEncoder)] = jsonEncoder

    @classmethod
    def unregisterEncoder(cls, jsonEncoder: Union[IJsonEncoder, Type[IJsonEncoder]]) -> None:
        encoderType = type(jsonEncoder) if isinstance(jsonEncoder, IJsonEncoder) else jsonEncoder
        cls._ENCODER_REGISTRY.pop(encoderType, None)

    @classmethod
    def registerDecoder(cls, jsonDecoder: IJsonDecoder) -> None:
        cls._DECODER_REGISTRY[type(jsonDecoder)] = jsonDecoder

    @classmethod
    def unregisterDecoder(cls, jsonDecoder: Union[IJsonDecoder, Type[IJsonDecoder]]) -> None:
        decoderType = type(jsonDecoder) if isinstance(jsonDecoder, IJsonDecoder) else jsonDecoder
        cls._DECODER_REGISTRY.pop(decoderType, None)
