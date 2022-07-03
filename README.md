# Gasto System

Esse sistema está sendo desenvolvido para atender a necessidade de um cliente: o irmão do Jorel.
![Irmão do Jorel](https://raw.githubusercontent.com/danilob/GastoSystem/main/expenses/static/expenses/img/irmao-do-jorel.png)
Irmão do Jorel gosta de manter suas contas sempre anotadas em seu caderno. Toda vez que ele realiza algum gasto ele anota a data, o valor, o tipo de pagamento (Crédito, Débito, Pix, Dinheiro, etc) e o tipo de gasto (Lazer, Despesas Fixas, Ensino, Investimento, Combustível, etc). Com o passar do tempo o irmão do Jorel observou que gostaria de fazer algumas operações que fica muito difícil de ver no caderno.



Para melhor anotar as coisas, o irmão do Jorel quer um sistema. Esse sistema deve permitir com que ele possa realizar o lançamento de qualquer tipo de forma de pagamento, de qualquer categoria de gasto e de uma despesa feita (com descrição do gasto, data de pagamento, valor, tipo de gasto, forma de pagamento). Além disso, o irmão do Jorel quer que seja possível a inserção de um limite de gastos em cada mês do ano, para que ele acompanhe se o limite estabelecido não foi ultrapassado. O sistema também deve dar alguns relatórios:

- Mostrar todos os gastos que ele teve em um determinado período de tempo
- Calcular o quanto ele gastou em determinado período de tempo, considerando a forma de pagamento
- Identificar qual foi o tipo gasto que mais consumiu seu dinheiro em um determinado período de tempo
- Dado um tipo de gasto retornar uma lista contendo o mês e ano com um somatório de despesas feitas
- Identificar em que mês e ano ele teve a maior despesa em um determinado tipo de gasto
- Listar os gastos do mês, o limite de gastos estabelecido e se houve uma superação do limite

## Execução

Este sistema foi desenvolvido para rodar em containers utilizando docker-compose. Na raiz do projeto execute:

```bash
docker-compose up --build
```

Caso seja preciso realizar algum comando do `manage.py` dê permissão de execução ao arquivo `.run` e depois execute o comando:

```bash
chmod +x .run
./run manage <command>
```