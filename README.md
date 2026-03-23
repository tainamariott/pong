# 🏓 Refatoração do jogo Pong (Pygame)

## 📌 Objetivo

Refatorar o código do jogo Pong com foco em:

- Melhorar a organização do código  
- Aumentar a legibilidade  
- Separar responsabilidades  
- Aplicar conceitos básicos de SOLID  
- Facilitar manutenção e evolução  

---

## ⚠️ Problemas antes da refatoração

O código original apresentava alguns problemas:

- Funções com muitas responsabilidades  
- Lógica do jogo misturada com entrada e renderização  
- Dificuldade para entender e manter  
- Código pouco organizado  

---

## 🔄 Melhorias realizadas

### ✔️ 1. Separação de responsabilidades

As funcionalidades foram divididas em métodos menores:

- `mover_jogador()` → controla entrada do usuário  
- `mover_ia()` → controla o jogador automático  
- `verificar_colisoes()` → trata colisões  
- `verificar_pontos()` → controla pontuação  
- `desenhar()` → renderiza o jogo  

➡️ Cada método faz apenas uma tarefa, deixando o código mais organizado.

---

### ✔️ 2. Abstração com classes

O sistema foi organizado em classes:

- `Config` → configurações do jogo  
- `Raquete` → representa o jogador  
- `Bola` → representa a bola  
- `Game` → controla a lógica do jogo  
- `Menu` → controla a tela inicial  

➡️ Cada classe representa uma parte do sistema, facilitando o entendimento.

---

### ✔️ 3. Centralização de configurações

As configurações foram agrupadas em uma única classe:

```python
class Config:
    LARGURA = 800
    ALTURA = 600
    FPS = 60
```

➡️ Agora, qualquer alteração pode ser feita em um único lugar.

---

### ✔️ 4. Melhoria na legibilidade

- Nomes de métodos mais claros  
- Código organizado por seções  
- Uso de comentários e docstrings  

➡️ O código ficou mais fácil de ler e entender.

---

### ✔️ 5. Documentação

- Comentários explicando partes importantes  
- Docstrings nas classes  
- Estrutura organizada  

---

## 🧩 Explicação do Código

### 🎮 Classe Game

A classe `Game` é responsável por controlar o funcionamento do jogo.

Exemplo:

```python
def atualizar(self):
    self.bola.mover()
    self.mover_jogador()
    self.mover_ia()
    self.verificar_colisoes()
    return self.verificar_pontos()
```

➡️ Esse método coordena o jogo chamando funções menores e organizadas.

---

### 🧍 Classe Raquete

Responsável pelo jogador.

```python
def mover(self, direcao):
    if direcao == "cima" and self.rect.top > 0:
        self.rect.y -= self.velocidade
    elif direcao == "baixo" and self.rect.bottom < Config.ALTURA:
        self.rect.y += self.velocidade
```

➡️ Controla apenas o movimento da raquete.

---

### ⚽ Classe Bola

Responsável pela movimentação da bola.

```python
def mover(self):
    self.rect.x += self.vel_x
    self.rect.y += self.vel_y
```

➡️ Toda a lógica da bola fica isolada nessa classe.

---

### ⚙️ Classe Config

Centraliza configurações do jogo:

- Tamanho da tela  
- FPS  
- Cores  

➡️ Evita repetição de valores no código.

---

### 🖥️ Classe Menu

Responsável pela tela inicial do jogo.

- Exibe o título  
- Aguarda o jogador iniciar  

---

## 🧠 Aplicação do SOLID

### 🔹 Single Responsibility Principle (SRP)

Cada parte do sistema possui apenas uma responsabilidade:

- `Raquete` → movimentação  
- `Bola` → comportamento da bola  
- `Game` → controle geral do jogo  

➡️ Isso facilita manutenção e entendimento.

---

## 🔁 Fluxo do jogo

O funcionamento segue o seguinte fluxo:

1. Exibe o menu  
2. Inicia o jogo  
3. Executa o loop principal:  
   - Captura eventos  
   - Atualiza o jogo  
   - Desenha na tela  
4. Quando alguém vence, retorna ao menu  

---

## 🏗️ Estrutura do projeto

```
pong/
│
├── pong.py
├── README.md
```

---

## 🚀 Benefícios da refatoração

- Código mais organizado  
- Melhor separação de responsabilidades  
- Mais fácil de entender  
- Mais fácil de manter  
- Preparado para novas funcionalidades  

---

## ▶️ Como executar

Instale o pygame:

```bash
pip install pygame
```

Execute o jogo:

```bash
python pong.py
```

---

## 📌 Considerações finais

A refatoração manteve o funcionamento original do jogo, mas melhorou significativamente a organização e a estrutura do código, facilitando futuras melhorias e manutenção.
