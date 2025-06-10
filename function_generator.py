import math
import random
import numpy as np

class FunctionGenerator:
    """
    Classe que gera funções matemáticas aleatórias para o jogo Derivative Dash,
    incluindo a função original, primeira e segunda derivadas.
    """
    
    def __init__(self):
        self.function_types = [
            "polynomial", 
            "trigonometric", 
            "exponential", 
            "logarithmic", 
            "composite"
        ]
        self.standard_range = (0, 1000)
        self.standard_checkpoints = 4
    
    def generate_function(self, function_type=None, difficulty=1):
        """
        Gera uma função aleatória do tipo especificado ou escolhe um tipo aleatoriamente.
        
        Args:
            function_type (str, optional): Tipo de função a ser gerada.
            difficulty (int, optional): Nível de dificuldade (1-3). Influencia a complexidade da função.
            
        Returns:
            dict: Dicionário contendo a função, derivadas e metadados.
        """
        if function_type is None:
            function_type = random.choice(self.function_types)
        
        # Gerador específico baseado no tipo
        if function_type == "polynomial":
            return self._generate_polynomial(difficulty)
        elif function_type == "trigonometric":
            return self._generate_trigonometric(difficulty)
        elif function_type == "exponential":
            return self._generate_exponential(difficulty)
        elif function_type == "logarithmic":
            return self._generate_logarithmic(difficulty)
        elif function_type == "composite":
            return self._generate_composite(difficulty)
        else:
            raise ValueError(f"Tipo de função não reconhecido: {function_type}")
    
    def _generate_polynomial(self, difficulty):
        """Gera uma função polinomial aleatória."""
        degree = random.randint(1, difficulty + 1)
        
        # Coeficientes para cada grau
        coeffs = []
        for i in range(degree + 1):
            # Ajusta a magnitude dos coeficientes com base no grau
            magnitude = 1 / (10 ** max(0, i-1))
            if i == 0:  # Termo constante maior para manter a curva visível
                coeff = random.uniform(250, 350)
            else:
                coeff = random.uniform(-1, 1) * magnitude
                # Assegura que o coeficiente de maior grau não seja muito pequeno
                if i == degree and abs(coeff) < 0.00001:
                    coeff = 0.00001 if coeff >= 0 else -0.00001
            coeffs.append(coeff)
        
        # Cria as funções
        def f(x):
            result = 0
            for i, c in enumerate(coeffs):
                result += c * (x ** i)
            return result
        
        def df(x):
            result = 0
            for i, c in enumerate(coeffs[1:], 1):
                result += i * c * (x ** (i-1))
            return result
        
        def d2f(x):
            result = 0
            for i, c in enumerate(coeffs[2:], 2):
                result += i * (i-1) * c * (x ** (i-2))
            return result
        
        # Gera a fórmula como string
        formula_terms = []
        for i, c in enumerate(coeffs):
            if abs(c) < 0.00001 and i > 0:
                continue  # Ignora termos muito pequenos
                
            if i == 0:  # Termo constante
                formula_terms.append(f"{c:.0f}")
            elif i == 1:  # Termo linear
                coeff_str = f"{abs(c):.4f}".rstrip('0').rstrip('.')
                formula_terms.append(f"{'+' if c > 0 else '-'} {coeff_str}x")
            else:  # Termos de maior grau
                coeff_str = f"{abs(c):.6f}".rstrip('0').rstrip('.')
                formula_terms.append(f"{'+' if c > 0 else '-'} {coeff_str}x^{i}")
        
        formula = "f(x) = " + " ".join(formula_terms)
        
        return {
            "name": f"Polinômio Grau {degree}",
            "formula": formula,
            "f": f,
            "df": df,
            "d2f": d2f,
            "range": self.standard_range,
            "checkpoints": self.standard_checkpoints
        }
    
    def _generate_trigonometric(self, difficulty):
        """Gera uma função trigonométrica aleatória."""
        # Seleciona funções trigonométricas
        trig_funcs = [
            ("sen", math.sin),
            ("cos", math.cos)
        ]
        
        # Seleciona parâmetros
        amplitude = random.uniform(30, 70)
        frequency = random.uniform(0.005, 0.02)
        phase = random.uniform(0, 2*math.pi)
        vertical_shift = random.uniform(250, 350)
        
        # Adiciona termos extras baseados na dificuldade
        has_linear = difficulty >= 2 and random.random() > 0.5
        has_quadratic = difficulty >= 3 and random.random() > 0.7
        
        linear_term = random.uniform(0.001, 0.005) if has_linear else 0
        quadratic_term = random.uniform(0.0001, 0.001) if has_quadratic else 0
        
        # Seleciona função trigonométrica aleatória
        trig_name, trig_func = random.choice(trig_funcs)
        
        # Cria as funções
        def f(x):
            return amplitude * trig_func(frequency * x + phase) + linear_term * x + quadratic_term * x**2 + vertical_shift
        
        def df(x):
            trig_deriv = math.cos if trig_name == "sen" else (lambda t: -math.sin(t))
            return amplitude * frequency * trig_deriv(frequency * x + phase) + linear_term + 2 * quadratic_term * x
        
        def d2f(x):
            trig_second_deriv = (lambda t: -math.sin(t)) if trig_name == "sen" else (lambda t: -math.cos(t))
            return amplitude * frequency**2 * trig_second_deriv(frequency * x + phase) + 2 * quadratic_term
        
        # Constrói a fórmula como string
        formula = f"f(x) = {amplitude:.0f}·{trig_name}({frequency:.4f}x"
        if phase != 0:
            formula += f" + {phase:.2f}"
        formula += ")"
        
        if linear_term != 0:
            formula += f" + {linear_term:.4f}x"
        
        if quadratic_term != 0:
            formula += f" + {quadratic_term:.6f}x²"
        
        formula += f" + {vertical_shift:.0f}"
        
        return {
            "name": f"Função {trig_name.capitalize()}oidal",
            "formula": formula,
            "f": f,
            "df": df,
            "d2f": d2f,
            "range": self.standard_range,
            "checkpoints": self.standard_checkpoints
        }
    
    def _generate_exponential(self, difficulty):
        """Gera uma função exponencial aleatória."""
        # Parâmetros base
        amplitude = random.uniform(100, 400)
        rate = random.uniform(0.001, 0.005)  # Taxa de crescimento
        vertical_shift = random.uniform(100, 200)
        
        # Ajustes baseados na dificuldade
        is_negative = random.random() > 0.5
        if is_negative:
            rate = -rate
        
        horizontal_shift = random.uniform(300, 700) if difficulty >= 2 else 0
        
        # Cria as funções
        def f(x):
            return amplitude * math.exp(rate * (x - horizontal_shift)) + vertical_shift
        
        def df(x):
            return amplitude * rate * math.exp(rate * (x - horizontal_shift))
        
        def d2f(x):
            return amplitude * rate**2 * math.exp(rate * (x - horizontal_shift))
        
        # Constrói a fórmula
        formula = f"f(x) = {amplitude:.0f} · e^({rate:.4f}"
        if horizontal_shift != 0:
            formula += f"(x - {horizontal_shift:.0f})"
        else:
            formula += "x"
        formula += f") + {vertical_shift:.0f}"
        
        return {
            "name": "Função Exponencial",
            "formula": formula,
            "f": f,
            "df": df,
            "d2f": d2f,
            "range": self.standard_range,
            "checkpoints": self.standard_checkpoints
        }
    
    def _generate_logarithmic(self, difficulty):
        """Gera uma função logarítmica aleatória."""
        # Parâmetros base
        amplitude = random.uniform(50, 100)
        vertical_shift = random.uniform(250, 350)
        horizontal_shift = random.uniform(50, 150)
        
        # Adiciona termos extras baseados na dificuldade
        linear_term = random.uniform(0.05, 0.2) if difficulty >= 2 else 0
        
        # Cria as funções (tratando domínio)
        def f(x):
            if x <= horizontal_shift:
                return vertical_shift  # Evita logaritmo de número negativo ou zero
            return amplitude * math.log(x - horizontal_shift + 1) + linear_term * x + vertical_shift
        
        def df(x):
            if x <= horizontal_shift:
                return 0
            return amplitude / (x - horizontal_shift + 1) + linear_term
        
        def d2f(x):
            if x <= horizontal_shift:
                return 0
            return -amplitude / (x - horizontal_shift + 1)**2
        
        # Constrói a fórmula
        formula = f"f(x) = {amplitude:.0f} · ln(x"
        if horizontal_shift != 0:
            formula += f" - {horizontal_shift:.0f}"
        formula += " + 1)"
        
        if linear_term != 0:
            formula += f" + {linear_term:.2f}x"
            
        formula += f" + {vertical_shift:.0f}"
        
        return {
            "name": "Função Logarítmica",
            "formula": formula,
            "f": f,
            "df": df,
            "d2f": d2f,
            "range": self.standard_range,
            "checkpoints": self.standard_checkpoints
        }
    
    def _generate_composite(self, difficulty):
        """Gera uma função composta combinando diferentes tipos."""
        # Escolhe funções base para combinar
        available_types = ["polynomial", "trigonometric", "exponential", "logarithmic"]
        
        # Escolhe dois tipos diferentes de função
        first_type = random.choice(available_types)
        available_types.remove(first_type)
        second_type = random.choice(available_types)
        
        # Gera funções com complexidade reduzida
        reduced_difficulty = max(1, difficulty - 1)
        first_func = self._generate_function_by_type(first_type, reduced_difficulty)
        second_func = self._generate_function_by_type(second_type, reduced_difficulty)
        
        # Pesos para a combinação
        weight1 = random.uniform(0.3, 0.7)
        weight2 = 1 - weight1
        
        # Cria a função composta
        def f(x):
            return weight1 * first_func["f"](x) + weight2 * second_func["f"](x)
        
        def df(x):
            return weight1 * first_func["df"](x) + weight2 * second_func["df"](x)
        
        def d2f(x):
            return weight1 * first_func["d2f"](x) + weight2 * second_func["d2f"](x)
        
        # Constrói nome e fórmula
        name = f"Função Composta"
        formula = f"f(x) = {weight1:.2f}·({first_func['formula'][5:]}) + {weight2:.2f}·({second_func['formula'][5:]})"
        
        return {
            "name": name,
            "formula": formula,
            "f": f,
            "df": df,
            "d2f": d2f,
            "range": self.standard_range,
            "checkpoints": self.standard_checkpoints
        }
    
    def _generate_function_by_type(self, function_type, difficulty):
        """Método auxiliar para gerar um tipo específico de função."""
        if function_type == "polynomial":
            return self._generate_polynomial(difficulty)
        elif function_type == "trigonometric":
            return self._generate_trigonometric(difficulty)
        elif function_type == "exponential":
            return self._generate_exponential(difficulty)
        elif function_type == "logarithmic":
            return self._generate_logarithmic(difficulty)
        else:
            # Fallback para polinômio simples
            return self._generate_polynomial(1)
    
    def generate_function_set(self, count=5, difficulty_range=(1, 3)):
        """
        Gera um conjunto de funções com diferentes tipos e dificuldades.
        
        Args:
            count (int): Número de funções a serem geradas
            difficulty_range (tuple): Intervalo de dificuldade
            
        Returns:
            list: Lista de funções
        """
        functions = []
        for _ in range(count):
            difficulty = random.randint(difficulty_range[0], difficulty_range[1])
            function_type = random.choice(self.function_types)
            functions.append(self.generate_function(function_type, difficulty))
        return functions


# Funções estáticas (originais do jogo)
STATIC_FUNCTIONS = [
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

# Função para combinar funções estáticas com funções geradas dinamicamente
def get_functions(include_static=True, generated_count=3, difficulty_range=(1, 3)):
    """
    Retorna uma lista de funções para o jogo.
    
    Args:
        include_static (bool): Se deve incluir as funções estáticas originais
        generated_count (int): Número de funções geradas aleatoriamente
        difficulty_range (tuple): Intervalo de dificuldade para as funções geradas
        
    Returns:
        list: Lista de funções para o jogo
    """
    functions = []
    
    # Inclui funções estáticas originais
    if include_static:
        functions.extend(STATIC_FUNCTIONS)
    
    # Adiciona funções geradas dinamicamente
    if generated_count > 0:
        generator = FunctionGenerator()
        functions.extend(generator.generate_function_set(generated_count, difficulty_range))
    
    return functions


# Exemplo de uso
if __name__ == "__main__":
    # Testa o gerador
    generator = FunctionGenerator()
    
    print("Função Polinomial:")
    poly = generator.generate_function("polynomial", 2)
    print(poly["name"])
    print(poly["formula"])
    print(f"f(100) = {poly['f'](100)}")
    print(f"f'(100) = {poly['df'](100)}")
    print(f"f''(100) = {poly['d2f'](100)}")
    print()
    
    print("Função Trigonométrica:")
    trig = generator.generate_function("trigonometric", 2)
    print(trig["name"])
    print(trig["formula"])
    print(f"f(100) = {trig['f'](100)}")
    print(f"f'(100) = {trig['df'](100)}")
    print(f"f''(100) = {trig['d2f'](100)}")
    print()
    
    print("Conjunto completo de funções:")
    all_functions = get_functions(include_static=True, generated_count=2)
    for i, func in enumerate(all_functions, 1):
        print(f"{i}. {func['name']}: {func['formula']}")