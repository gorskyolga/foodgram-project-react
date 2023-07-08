import re

from rest_framework import serializers

from api.constants import REGEX_HEX_COLOR, REGEX_USERNAME, ErrorMessage


def validate_hex_color(value):
    pattern = re.compile(REGEX_HEX_COLOR)
    if not re.fullmatch(pattern, value):
        raise serializers.ValidationError(ErrorMessage.REGEX_HEX_COLOR)
    return value


def validate_username(value):
    pattern = re.compile(REGEX_USERNAME)
    if not re.fullmatch(pattern, value):
        raise serializers.ValidationError(ErrorMessage.REGEX_USERNAME)
    return value
