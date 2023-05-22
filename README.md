## Descrição

O código a seguir implementa um pacote em ROS (Robot Operating System). Ele utiliza o Gazebo como ambiente de simulação e consiste em um controlador para um robô. 

### Funcionamento

O controlador utiliza a arquitetura Pub-Sub (Publicação-Subscrição) do ROS2 para receber e enviar comandos de direção para o robô. Ele se baseia em dados de odometria para determinar a direção na qual o robô deve se movimentar.

Para entender melhors como todo o fluxo funciona, navegue até o diretório `/src` e acesse a pasta `modules`, onde estão localizados os arquivos das classes correspondentes ao controlador, stack e queue.

### Subscriber

A função `odometry_callback` é responsável por receber os dados de odometria do tópico "/odom". Esses dados são utilizados para calcular a direção de rotação do robô. A função aplica a função arcotangente às coordenadas atuais (x e y) para obter o ângulo correspondente. Além disso, ela verifica se as coordenadas atuais (x e y) correspondem ao destino desejado, a fim de enviar novos comandos de posicionamento.

### Publisher

A função `send_movement_command` envia comandos de movimento para o robô utilizando dados do tipo Twist. Esses comandos são calculados com base na posição atual e na posição de destino, que são obtidas por meio da subscrição aos dados de odometria. Em caso de erro (IndexError) relacionado a uma fila vazia, a função `return_movement` é chamada para permitir que o robô retorne à posição inicial. Essa função utiliza uma pilha que contém os elementos removidos da fila para reverter o caminho percorrido.

### Estruturas de Dados

Foi implementada uma fila para controlar a ordem dos destinos que o robô deve alcançar. A fila é preenchida lendo um arquivo CSV, onde cada coluna é adicionada como um novo elemento na fila. O primeiro elemento da fila é considerado como o próximo destino, e quando o robô alcança esse destino, o elemento é removido da fila. Além disso, foi utilizada uma pilha para armazenar os elementos removidos da fila. Isso permite que o robô retorne ao ponto inicial, seguindo o caminho inverso.

## Executando o Código

Para executar o projeto, siga as etapas abaixo:

1. Clone o repositório do projeto: `git clone <link_do_repositório>`.
2. Entre na pasta do pacote: ```cd src/package```.
3. Para iniciar a simulação, execute o comando `ros2 launch turtlebot3_gazebo empty_world.launch.py` em um terminal.
4. Volte para o terminal anterior e execute o comando `ros2 run turtlebot_package entrypoint` para iniciar o controlador do robô.

## Segue o link do vídeo demo: https://drive.google.com/file/d/1bYf8ob5Nvduml222nHN6DAJ1qHrDf67b/view?usp=sharing
