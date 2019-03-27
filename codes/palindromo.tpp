{Reconhecedor de palindromos}

principal()

     inteiro: num_entrada, num, num_invertido, digito

     escreva("Digite um número: ")
     leia(num_entrada)

     num := num_entrada
     invertido := 0

     repita {Inverte o número digitado}
          digito := num % 10
          num_invertido := (num_invertido * 10) + digito
          num := num / 10
     até num <> 0 faça

     se num_entrada = num_invertido então {Verifica se o número digitado é igual ao número de saída}
          escreva("É palindromo")
     senão
          escreva("Não é palindromo")

fim