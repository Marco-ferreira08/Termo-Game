# Termo - Jogo de Adivinhação de Palavras

Um projeto em Python inspirado no popular "Termo" (estilo Wordle), desenvolvido com Tkinter para interface gráfica. O objetivo do jogo é adivinhar a palavra de 5 letras em poucas tentativas, usando apenas o teclado do computador.

## Funcionalidades

- Interface gráfica moderna feita em Tkinter, com tema claro e opção de alternar para modo escuro.
- Palavras de 5 letras armazenadas em um arquivo `palavras.json`.
- Jogador possui 5 tentativas para adivinhar cada palavra.
- Se errar, pode ganhar mais 2 tentativas ou pular para a próxima palavra.
- Feedback visual colorido: letras certas (verde), certas na posição errada (amarelo), erradas (cinza).
- Uso exclusivo do teclado físico para digitação (sem teclado virtual).

## Como jogar

1. Digite uma palavra de 5 letras usando o teclado.
2. Aperte `Enter` para enviar sua resposta.
3. As letras vão mudar de cor conforme sua posição e existência na palavra secreta:
    - **Verde:** letra certa e na posição certa.
    - **Amarelo:** letra está na palavra, mas em posição errada.
    - **Cinza:** letra não está na palavra.
4. Se acertar, avance para a próxima palavra!
5. Se errar todas as tentativas, escolha: tentar mais 2 vezes ou pular para a próxima.
