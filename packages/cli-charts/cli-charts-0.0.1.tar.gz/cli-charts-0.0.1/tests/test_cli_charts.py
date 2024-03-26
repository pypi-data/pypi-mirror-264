import pytest
from chart_library import CHART

@pytest.fixture
def chart():
    return CHART()

def test_chart_creation(chart):
    assert not chart.granular

def test_plot_graph(chart, capsys):
    values = [[1, 5], [3, 10], [7, 3]]
    chart.plot_graph(values)
    captured = capsys.readouterr()
    assert captured.out == " .\n .\n .\n\n          *         \n       *         \n     *         \n   *         \n *         \n"

def test_draw_bar(chart, capsys):
    values = [['A', 5], ['B', 10], ['C', 3]]
    chart.draw_bar(values)
    captured = capsys.readouterr()
    assert captured.out == " .\n .\n .\n\n   A +     *****\n     *****\n\n   B +**********\n      **********\n\n   C +   ***\n      ***\n"

def test_draw_pict(chart, capsys):
    values = [['A', 5], ['B', 10], ['C', 3]]
    chart.draw_pict(values)
    captured = capsys.readouterr()
    assert captured.out == " .\n .\n .\n\n   A +  ||||||\n\n   B + ||||||||||||\n\n   C + |||\n"