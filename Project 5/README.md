Foram realizados os seguintes testes:
    3 camadas de conv com filtros (3,3), 3 de pooling, 1 camada densa de 64 neuronios = 0.95 acuracia no teste
    3 camadas de conv com filtros (3,3), 3 de pooling, 3 camadas densas de 64, 32 e 16 neuronios = 0.95 acuracia no teste
    3 camadas de conv com filtros (3,3), 3 de pooling, as mesmas 3 camadas e com 2 camadas de dropout com taxa 0.2 entre elas = 0.97 acuracia no teste
    2 camadas de conv com filtros (3,3), 2 de pooling, as mesmas 3 camadas e com 2 camadas de dropout com taxa 0.2 entre elas = 0.85 acuracia no teste
    3 camadas de conv com filtros (2,2), 3 de pooling, as mesmas 3 camadas e com 2 camadas de dropout com taxa 0.2 entre elas = 0.88 acuracia no teste

Portanto, percebemos que o melhor resultado foi obtido ao usar 3 camadas de convolução com filtros de tamanho (3,3), 3 camadas de maxPooling 3 camadas densas de 64, 32 e 16 neurônios respectivamente e com 2 camadas de dropout entre essas 3 densas com taxa de 0.2. Apesar da acurácia não ter mudado quando o número de camadas densas foi aumentado do primeiro para o segundo teste, o que nesse caso nos traria a percepção de que fosse melhor ficar com o modelo menos complexo, percebemos que o acréscimo de camadas de dropout, no terceiro teste, favoreceu uma melhora no resultado, permitindo que o modelo conseguisse generalizar melhor para o conjunto de dados de teste.