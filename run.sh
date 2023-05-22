#!/bin/bash

# Função para lidar com o sinal SIGINT (Ctrl + C)
function handle_sigint {
    echo "Recebido o sinal SIGINT. Finalizando o processo..."
    # Matando o processo atual
    kill $PID
    exit 0
}

# Definindo a função de manipulação de sinal
trap 'handle_sigint' SIGINT

echo "Navegando até o diretório 'src/package'..."
cd src/package

echo "Construindo o pacote 'turtle'..."
colcon build --packages-select turtle

sleep 2

echo "Carregando as configurações do ambiente..."
source install/setup.zsh

echo "Executando o ponto de entrada do pacote 'turtle' em segundo plano..."
ros2 run turtle entrypoint &
# Salvando o PID do processo em uma variável
PID=$!

# Aguardar o sinal SIGINT (Ctrl + C)
wait