# Trabalho 1 
# Fundamento de Sistemas Embarcados
### Lucas Ganda Carvalho - 170039668
Este trabalho tem por objetivo a criação de um sistema distribuído de automação predial para monitoramento e acionamento de sensores e dispositivos de um prédio com múltiplas salas. O sistema deve ser desenvolvido para funcionar em um conjunto de placas Raspberry Pi com um servidor central responsável pelo controle e interface com o usuário e servidores distribuídos para leitura e acionamento dos dispositivos. Dentre os dispositivos envolvidos estão o monitoramento de temperatura e umidade, sensores de presença, sensores de fumaça, sensores de contagem de pessoas, sensores de abertura e fechamento de portas e janelas, acionamento de lâmpadas, aparelhos de ar-condicionado, alarme e aspersores de água em caso de incêndio.

### Execução
1. 
Para a execução dos arquivos, primeiro deve-se garantir que os arquivos de configuração do json {sala-01.json} e {sala-02.json} estão configurados de forma
correta, pois a inicialização só é possível se os IPś e portas estiverem setados corretamente.

2. 
Primeiro deve-se executar o servidor central
```
$ python3 server.py
```

3. 
Após isso deve ser feita a execução de cada distribuído  passando uma flag de qual configuração o mesmo estará utilizando
```
$ python3 client.py --arg 1
```

Lembrando que apesar de poder ser escalável até N distribuídos, o arquivo de read_json deve ser configurado acrescentado-se os arquivos dos demais distribuídos
