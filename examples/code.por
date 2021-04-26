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