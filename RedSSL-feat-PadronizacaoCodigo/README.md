# RedSSL

## Small Size League (SSL) - Red Dragons UFSCar

Neste repositório encontra-se o software de inteligência utilizado pela equipe Red Dragons UFSCar na categoria Small Size League Entry Level (SSL-EL).

## Instalação

Ao clonar esse repositório, instale as dependências Python:

```sh
pip3 install -r requirements.txt
```

Gere a dependência [cppvisgraph](https://github.com/emranemon/cppvisgraph/tree/master) para planejamento de trajetórias por:

```sh
bash build.sh
```

Além disso, é necessário que o Google Protobuff esteja instalado de acordo com a versão solicitada pelo [grSim](https://github.com/RoboCup-SSL/grSim).

## Execução

Para execução do código em sua totalidade, basta executar o script main da raiz do repositório.

```sh
python3 main.py
```
