# Pygments_Portugol

[Pygments](https://pygments.org/) é um excelente pacote em Python destinado à coloração de sintaxe (_syntax highlighting_), sendo possível utilizá-lo, inclusive, em documentos LaTeX. Este pacote fornece um _lexer_ para a linguagem [Portugol Studio](http://lite.acad.univali.br/portugol/).

## Instalação

Após a instalação do Python 3, você provavelmente poderá executar o comando a seguir a fim de instalar o Pygments:

```sh
$ pip install pygments
```

> Note que `$` indica o _prompt_ do _shell_, você não deve digitar isso.

Algumas variações desse comando podem aparecer a depender da plataforma, por exemplo:

```sh
$ pip3 install pygments
$ python3 -m pip install pygments
$ python -m pip install pygments
```

Após instalar com sucesso o Pygments, você pode instalar o _lexer_ para Portugol Studio:

```sh
$ pip install pygments-portugol
```

## Utilização

Para utilizar o _lexer_, o procedimento é equivalente a qualquer outra linguagem suportada pelo Pygments. Utilize `portugol` ou `portugolstudio` como nome da linguagem. Por exemplo, o código em Python a seguir ilustra como ler um arquivo [`code.por`](https://github.com/hellmrf/pygments-portugol/blob/main/examples/code.por) e salvar em HTML no arquivo [`formatted.html`](https://github.com/hellmrf/pygments-portugol/blob/main/examples/formatted.html).

```python
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter

with open("./code.por", "r") as fl:
    code = fl.read()

lexer = get_lexer_by_name("portugol", stripall=True)
formatter = HtmlFormatter(linenos=True, noclasses=True)
result = highlight(code, lexer, formatter)

with open("./formatted.html", "w") as fl:
    fl.write(result)
```

[Clique aqui para ver o resultado](https://htmlpreview.github.io/?https://github.com/hellmrf/pygments-portugol/blob/main/examples/formatted.html).

### Utilização com LaTeX

Para tipografar um código em LaTeX com o Pygments, pode-se utilizar o pacote [`minted`](https://www.ctan.org/pkg/minted). O código a seguir é um exemplo. A fonte DejaVuSansMono foi utilizada apenas por questões estéticas. As duas linhas referentes à fonte podem ser removidas ou substituídas. Caso queira usar pdfLaTeX, remova-as.

```latex
% !TeX program = xelatex
\documentclass{article}
\usepackage{fontspec} % remover caso esteja usando pdfLaTeX
\usepackage{DejaVuSansMono} % remover caso esteja usando pdfLaTeX
\setmonofont[Scale=MatchLowercase]{DejaVuSansMono} % remover caso esteja usando pdfLaTeX

\usepackage{minted} % importa o pacote para que possamos usar
\begin{document}
O código a seguir ilustra um fatorial recursivo no Portugol Studio.

\begin{minted}[autogobble, linenos]{portugol}
    programa
    {
        funcao inicio()
        {
            inteiro numero

            escreva("Digite um número: ")
            leia(numero)

            limpa()
            escreva("O fatorial de ", numero, " é: ", fatorial(numero), "\n")
        }

        // Função recursiva que calcula o fatorial do número passado

        funcao inteiro fatorial(inteiro numero)
        {
            se (numero == 1 ou numero == 0)
            {
                retorne 1
            }

            retorne numero * fatorial(numero - 1)
        }
    }
\end{minted}
\end{document}
```

Resultado:
[![](https://github.com/hellmrf/pygments-portugol/blob/main/examples/latex.png)](https://github.com/hellmrf/pygments-portugol/blob/main/examples/latex.png)

Veja [este tutorial](https://www.overleaf.com/learn/latex/Code_Highlighting_with_minted) se quiser ver outras possibilidades, como escolher cores diferentes ou importar de um arquivo externo.

### Utilização em LaTeX no Overleaf

Caso você tenha o costume de usar Overleaf, pode ter lido a seção anterior e pensado que é impossível instalar um pacote Python no Overleaf. Sim, é verdade. Felizmente, é possível utilizar um _lexer_ sem instalação obrigatória.

1. Copie o arquivo do _lexer_ ([este](https://github.com/hellmrf/pygments-portugol/blob/main/pygments_portugol/__init__.py)) e salve como, por exemplo, `PortugolStudioLexer.py`.

2. Coloque no mesmo diretório do seu arquivo `.tex`;

3. Substitua o nome da linguagem por `PortugolStudioLexer.py:PortugolStudioLexer -x`.

4. O código deve ser assim (veja o exemplo completo na seção anterior):

```latex
% ...
\begin{minted}[autogobble, linenos]{PortugolStudioLexer.py:PortugolStudioLexer -x}
    // seu código
\end{minted}
% ...
```

Isto pode ser recomendado para projetos maiores, para reduzir a quantidade de dependências que outros colaboradores precisarão instalar (o mesmo vale para fontes personalizadas). Para projetos menores, entretanto, é mais prático instalar e apenas utilizar o nome da linguagem.

## Contribuição

Caso note algo de errado, fique à vontade para abrir uma _issue_ ou, ainda melhor, enviar o seu Pull Request.

## Autor

Desenvolvido por [Héliton Martins](mailto:helitonmrf@gmail.com).
