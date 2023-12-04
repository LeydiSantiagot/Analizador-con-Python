
from flask import Flask, render_template, request
from ply import lex
from textblob import TextBlob
from ply import yacc
import ply.yacc as yacc
from ply.lex import lex

app = Flask(__name__)


def procesarCadena(entrada):
    # Implement your logic to process the input string
    # For demonstration purposes, let's assume the processing is converting the string to uppercase
    cadenaProcesada = entrada.upper()
    return cadenaProcesada


def procesarEntradaSemantica(entrada):
    # Implement your logic to process the semantic input string
    # For demonstration purposes, let's assume the processing is checking if the input is a valid Python expression
    if not isinstance(entrada, str):
        return "Error de sintaxis"

    try:
        eval(entrada)
    except SyntaxError:
        return "Error de sintaxis"

    return "Entrada semánticamente correcta"

# Definición de tokens
tokens = (
    'NUMERO',
    'SUMA',
    'RESTA',
    'MULTIPLICACION',
    'DIVISION',
    'PARENTESIS_IZQUIERDO',
    'PARENTESIS_DERECHO',
)
# Reglas de expresiones regulares
t_SUMA = r'\+'
t_RESTA = r'-'
t_MULTIPLICACION = r'\*'
t_DIVISION = r'/'
t_PARENTESIS_IZQUIERDO = r'\('
t_PARENTESIS_DERECHO = r'\)'
t_ignore = ' \t\n'  # Ignorar espacios en blanco y saltos de línea

# Regla para números
def t_NUMERO(t):
    r'\d+'
    t.value = int(t.value)
    return t

# Manejo de errores léxicos
def t_error(t):
    print(f"Carácter ilegal '{t.value[0]}'")
    t.lexer.skip(1)

# Construcción del analizador léxico
lexer = lex()

#analizador sintactico---------------------------------
# Definición de la gramática y las reglas sintácticas
def p_expresion(p):
    '''
    expresion : expresion SUMA termino
              | expresion RESTA termino
              | termino
    '''

    if len(p) == 4:
        if p[2] == '+':
            p[0] = p[1] + p[3]
        elif p[2] == '-':
            p[0] = p[1] - p[3]
    else:
        p[0] = p[1]

def p_termino(p):
    '''
    termino : termino MULTIPLICACION factor
            | termino DIVISION factor
            | factor
    '''

    if len(p) == 4:
        if p[2] == '*':
            p[0] = p[1] * p[3]
        elif p[2] == '/':
            if p[3] != 0:
                p[0] = p[1] / p[3]
            else:
                print("Error: División por cero")
                p[0] = 0
    else:
        p[0] = p[1]

def p_factor(p):
    '''
    factor : NUMERO
           | PARENTESIS_IZQUIERDO expresion PARENTESIS_DERECHO
    '''

    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[2]

def p_error(p):
    return(f"Error de sintaxis en '{p.value}'")

# Construcción del analizador sintáctico
parser = yacc.yacc()




#-----------------------------------------------------
#Analizador semantico
def analyze_sentiment(text):
    blob= TextBlob(text)

    polarity= blob.sentiment.polarity

    if polarity>0:
        sentiment='positivo'
    elif polarity<0:
        sentiment= 'negativo'
    else:
        sentiment='neutro'

    print(f'Text: {text}')
    print(f'Sentimiento: {sentiment}')
    return sentiment

#-------------------------------------



@app.route("/", methods=["GET", "POST"])
def homepage():
    cadenaProcesada = None
    if request.method == "POST":
        entrada = request.form.get("entrada")
    return render_template("index.html", title="Lenguajes y Automatas II", cadenaProcesada=cadenaProcesada)

@app.route('/')
def index():
    return render_template('index.html')


@app.route("/Semantico.html", methods=["GET", "POST"])
def semantico():
    mensajeError = None
    if request.method == "POST":
        cadena = request.form['cadena']
        sentimiento= analyze_sentiment(cadena)
        return render_template("Semantico.html", feeling= sentimiento)
    else:
        return render_template("Semantico.html")


@app.route("/Sintactico.html",methods=["GET", "POST"])
def sintactico():
    mensajeError = None
    if request.method == "POST":
        expresion= request.form['cadena']
        resultado = parser.parse(expresion)
        print(type(resultado))
        return render_template("Sintactico.html", result= resultado)
    else:
        return render_template("Sintactico.html")

@app.route("/lexico.html")
def lexico():
    mensajeError = None

    if request.method == "POST":
        entrada = request.form.get("entrada")
        mensajeError = procesarEntradaSemantica(entrada)

    return render_template("lexico.html", mensajeError=mensajeError)



if __name__ == "_main_":
    app.run(debug=True)
