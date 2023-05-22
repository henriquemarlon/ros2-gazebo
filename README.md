# Código

No código há a implementação de um pacote em ROS. Para interagir com o Gazebo e encontrar o controlador, é necessário navegar até o diretório ```/src``` e acessar o arquivo a pasta ```modules``` onde estão os arquivos das classes correspondentes ao controller, stack e queu. O controlador é estruturado como um sistema de publicação e assinatura (Pub-Sub) que utiliza a biblioteca "rclpy" do ROS2 para criar um nó que recebe e envia comandos de direção para o robô. 

## Subscription
O "Subscription" é responsável por recuperar os dados de Odometria no tópico "/dom". Esses dados são utilizados para determinar a direção na qual o robô deve se movimentar. Para calcular a direção de rotação, são consideradas as coordenadas atuais (x e y) e é aplicada a função arcotangente para obter o ângulo correspondente. Além disso, é verificado se as coordenadas atuais (x e y) correspondem ao destino desejado, a fim de enviar novos comandos de posicionamento.

## Publisher
O "Publisher" desempenha o papel de enviar comandos de movimento para o robô, utilizando dados do tipo Twist. Para enviar esses dados de movimento, são realizados cálculos com base na posição de destino e na posição atual, que é obtida por meio da assinatura (Subscription). No caso de ocorrer um IndexError (um erro relacionado a uma fila vazia), é chamada a função "return_movement" que utiliza de um pilha formada por cada "dequeue" ocorrido para voltar a posição inicial do robô.
## Estutura de dados

Foi implementada uma estrutura de dados de fila que segue o princípio First-In, First-Out, onde o primeiro elemento a ser inserido na fila é o primeiro a ser removido. Essa fila é preenchida lendo um arquivo CSV, onde cada coluna é adicionada como um novo elemento na fila. O primeiro elemento da fila é considerado como o destino, e quando o turtlebot atinge esse destino, esse elemento é removido da fila. Dessa forma, a fila controla a ordem em que os destinos devem ser alcançados. Comjugado a fila, foi implementado, uma pilha na qual é adicionado todo elemento que sai da fila. Sendo assim, o primeiro elemento a sair é o último a ser utilizado ( uma lógica perfeita para fazer com que o robô saiba o seu caminho de volta )

# Como rodar o código

Para rodar o projeto é necessário seguir os seguinter passos:

1. Clonar esse projeto: ```git clone ```
2. Entrar no diretorio ``` cd src/package ``` e rodar o comando ``` colcon build --packages-select turtlebot_package ```
3. No mesmo terminal, rodar o comando ``` source install/setup.bash ``` ou ``` source install/setup.zsh```
5. Em outro terminal rodar o comando ``` ros2 launch turtlebot3_gazebo empty_world.launch.py ```
4. Por fim, no terminal anterior, rodar o comando ``` ros2 run turtlebot_package entrypoint ```

# Simulação (Video e Imagem)

Na simulação, o robô seguirá a sequência dos pontos na ordem do csv e voltará para a posição inicial por meio da pilha. Para visualizar o vídeo da simulação clique no seguinte link: https://drive.google.com/drive/u/1/folders/1cPyhaUfmvi1rSRGvWUA0aWaPEmkHaaNT/view?usp=sharing

![pontos](https://github.com/emanuelemorais/atividades_mod6/assets/99221221/521df04d-67d9-4794-a85e-424c94d49eba)



