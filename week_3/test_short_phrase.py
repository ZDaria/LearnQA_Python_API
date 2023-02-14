import pytest


def test_length_validation():
    phrase = input("Set a phrase: ")
    assert len(phrase) <= 15