#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright by: P.J. Grochowski

import json
from functools import partial
from typing import Any, Type, Union, cast

from json_handler_registry import __logger as logger
from json_handler_registry.decoder import DecoderRegistryDict, IJsonDecoder, _JsonDecoderRegistryProxy
from json_handler_registry.encoder import EncoderRegistryDict, IJsonEncoder, _JsonEncoderRegistryProxy

JsonEncoder = Union[Type[IJsonEncoder], IJsonEncoder]
JsonDecoder = Union[Type[IJsonDecoder], IJsonDecoder]


class _RegistryGuardPartial(partial):

    __REGISTRY_KEYWORD = 'cls'

    def __call__(__self, *args: Any, **kwargs: Any) -> Any:
        __self.__adjustKwargs(kwargs=kwargs)

        return super().__call__(*args, **kwargs)

    def __adjustKwargs(__self, kwargs: dict) -> None:
        if __self.__REGISTRY_KEYWORD in kwargs:
            offendingObject = kwargs[__self.__REGISTRY_KEYWORD]
            kwargs.update(__self.keywords)

            logger.warning(f"Detected attempt to replace registry! offendingObject='{offendingObject}'")


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

        json.dumps = _RegistryGuardPartial(
            json.dumps,
            cls=partial(
                _JsonEncoderRegistryProxy,
                registry=cls._ENCODER_REGISTRY
            )
        )
        json.loads = _RegistryGuardPartial(
            json.loads,
            cls=partial(
                _JsonDecoderRegistryProxy,
                registry=cls._DECODER_REGISTRY
            )
        )

    @classmethod
    def disable(cls) -> None:
        if cls.isEnabled():
            json.dumps = cast(partial, json.dumps).func
            json.loads = cast(partial, json.loads).func

    @classmethod
    def registerEncoder(cls, jsonEncoder: JsonEncoder) -> None:
        encoderInstance = cls._getEncoderInstance(jsonEncoder=jsonEncoder)
        cls._ENCODER_REGISTRY[type(encoderInstance)] = encoderInstance

    @classmethod
    def unregisterEncoder(cls, jsonEncoder: JsonEncoder) -> None:
        encoderType = cls._getEncoderType(jsonEncoder=jsonEncoder)
        cls._ENCODER_REGISTRY.pop(encoderType, None)

    @classmethod
    def registerDecoder(cls, jsonDecoder: JsonDecoder) -> None:
        decoderInstance = cls._getDecoderInstance(jsonDecoder=jsonDecoder)
        cls._DECODER_REGISTRY[type(decoderInstance)] = decoderInstance

    @classmethod
    def unregisterDecoder(cls, jsonDecoder: JsonDecoder) -> None:
        decoderType = cls._getDecoderType(jsonDecoder=jsonDecoder)
        cls._DECODER_REGISTRY.pop(decoderType, None)

    @classmethod
    def _getEncoderType(cls, jsonEncoder: JsonEncoder) -> Type[IJsonEncoder]:
        return type(jsonEncoder) if isinstance(jsonEncoder, IJsonEncoder) else jsonEncoder

    @classmethod
    def _getEncoderInstance(cls, jsonEncoder: JsonEncoder) -> IJsonEncoder:
        return jsonEncoder if isinstance(jsonEncoder, IJsonEncoder) else jsonEncoder()

    @classmethod
    def _getDecoderType(cls, jsonDecoder: JsonDecoder) -> Type[IJsonDecoder]:
        return type(jsonDecoder) if isinstance(jsonDecoder, IJsonDecoder) else jsonDecoder

    @classmethod
    def _getDecoderInstance(cls, jsonDecoder: JsonDecoder) -> IJsonDecoder:
        return jsonDecoder if isinstance(jsonDecoder, IJsonDecoder) else jsonDecoder()
