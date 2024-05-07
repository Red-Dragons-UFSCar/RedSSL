# Examples folder

Nesta pasta se encontram scripts bash que permitem testes isolados de algumas seções do repositório. Os scripts são criados para rodar os códigos teste de forma a manter os paths e módulos adequadamente organizados.

> **Observação:** Todos os exemplos até então foram testados no simulador grSim. Lembre-se sempre de conferir os IPs e portas dos clients utilizados.

## Arquivos de exemplos

A seguir serão explicados os scripts aqui presentes para execução:

- **actuator_test:** Script que possibilita o envio de velocidades para os robôs. As velocidades podem ser enviadas de três formas distintas: Velocidades das rodas, no sistema de coordenadas local e no sistema de coordenadas global.
- **path_visibility_graph_test:** Script para mostrar o campo de obstáculos triangulares do *visibility graph*. A origem do *path* é definido manualmente como algum ponto do campo (*default*: Robô 0 azul) e constroi o *path* até a outro ponto, considerando os outros robôs como obstáculos.
- **iterative_path_visibility_graph_test:** Script para mostrar em tempo real o campo de obstáculos triangulares do *visibility graph*. A origem do *path* é definido manualmente como algum robô em campo (*default*: Robô 0 azul) e constroi o *path* até a bola, considerando os outros robôs como obstáculos.
- **vision_test:** Script que executa um client basico para receber as informações de visão do simulador.