from unittest.mock import patch

import pytest

from food_categorizer.main import main


def test_cli_help_doesnt_crash():
    """
    Really stupid test just to guard against the most egregious errors.
    """
    with patch("sys.argv", ["food-categorizer", "--help"]):
        with pytest.raises(SystemExit) as exc_info:
            main()
        assert exc_info.value.args[0] == 0


@pytest.mark.parametrize("command", ["generate", "input-ref"])
def test_cli_dispatch(command):
    """
    Test that dispatching to handler functions works.
    """
    with patch("sys.argv", ["food-categorizer", command]), patch(
        f"food_categorizer.main.{command.replace('-', '_')}_main", autospec=True
    ) as mock_command_handler:
        with pytest.raises(SystemExit) as exc_info:
            main()
        mock_command_handler.assert_called_once()
        assert exc_info.value.args[0] == 0
