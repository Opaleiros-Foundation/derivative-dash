import math

# =============================================
# BIBLIOTECA DE FUNÇÕES PARA O JOGO
# =============================================
FUNCTIONS = [
    {
        "name": "Senoide",
        "formula": "f(x) = 50·sen(0.01x) + 0.001x² + 300",
        "f": lambda x: 50 * math.sin(0.01 * x) + 0.001 * x**2 + 300,
        "df": lambda x: 0.5 * math.cos(0.01 * x) + 0.002 * x,
        "d2f": lambda x: -0.005 * math.sin(0.01 * x) + 0.002,
        "range": (0, 1000),
        "checkpoints": 4
    },
    {
        "name": "Logística",
        "formula": "f(x) = 400 / (1 + e^(-0.01(x - 500)))",
        "f": lambda x: 400 / (1 + math.exp(-0.01*(x - 500))),
        "df": lambda x: (4 * math.exp(-0.01*(x - 500))) / (1 + math.exp(-0.01*(x - 500)))**2,
        "d2f": lambda x: (-0.04 * math.exp(-0.01*(x-500)) * (1 - math.exp(-0.01*(x-500)))) / (1 + math.exp(-0.01*(x-500)))**3,
        "range": (0, 1000),
        "checkpoints": 4
    },
    {
        "name": "Polinômio Cúbico",
        "formula": "f(x) = 0.00001x³ - 0.015x² + 5x + 300",
        "f": lambda x: 0.00001 * x**3 - 0.015 * x**2 + 5 * x + 300,
        "df": lambda x: 0.00003 * x**2 - 0.03 * x + 5,
        "d2f": lambda x: 0.00006 * x - 0.03,
        "range": (0, 1000),
        "checkpoints": 4
    }
]