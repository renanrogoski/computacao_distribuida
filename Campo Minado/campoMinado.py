from random import*

def criaCampoMinado():

	tabuleiro  = [[ randint(0,2) for x in range(10)] for x in range(10)]


	print (tabuleiro)

	print (len(tabuleiro))


	for i in range(len(tabuleiro)):
		for j in range(len(tabuleiro)):
			if tabuleiro[i][j] != 1:
				tabuleiro[i][j] = 0

	for i in range(len(tabuleiro)):
		for j in range(len(tabuleiro)):
			if tabuleiro[i][j] == 1:
				tabuleiro[i][j] = 10

	print (tabuleiro)
	for i in range(len(tabuleiro)):
		for j in range(len(tabuleiro)):
			if tabuleiro[i][j] >= 10 and j > 0: #soma no lado esquerdo da bomba 
				tabuleiro[i][j-1]+=1

			if tabuleiro[i][j] >= 10 and j > 0 and i < 9: #soma no lado esquerdo pra baixo 
				tabuleiro[i+1][j-1]+=1

			if tabuleiro[i][j] >= 10 and j > 0 and i > 0: #soma no lado esquerdo pra cima
				tabuleiro[i-1][j-1]+=1

			if tabuleiro[i][j] >= 10 and j < 9: #soma na direita 
				tabuleiro[i][j+1]+=1

			if tabuleiro[i][j] >= 10 and j < 9 and i < 9: #soma na direita pra baixo 
				tabuleiro[i+1][j+1]+=1

			if tabuleiro[i][j] >= 10 and j < 9 and i > 0: #soma na direita pra cima 
				tabuleiro[i-1][j+1]+=1

			if tabuleiro[i][j] >= 10 and i > 0: #soma em cima
				tabuleiro[i-1][j]+=1

			if tabuleiro[i][j] >= 10 and i < 9: #soma embaixo
				tabuleiro[i+1][j]+=1


	print ("\nTabuleiro com as Bombas e Aviso de Quantidades")
	print ("Valores menores de 10 são as quantidades de bombas no entorno")
	print ("valores maior ou igual a 10 são bombas somadas de quantidades no entorno")
	for i in range(len(tabuleiro)):
		print('\n')
		for j in range(len(tabuleiro)):

			print("  %d  " %tabuleiro[i][j], end = "")

	print('\n')

	return tabuleiro


criaCampoMinado()