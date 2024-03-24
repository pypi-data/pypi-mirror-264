import pytest


def test_nebula_1_import_warning():
    with pytest.raises(ImportError):
        with pytest.warns(UserWarning, match="Attempted import of 'nebula.Client"):
            from nebula import Client  # noqa
