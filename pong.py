import pygame
import sys
import random

pygame.init()
pygame.mixer.init()


class Config:
    LARGURA = 800
    ALTURA = 600
    COR_FUNDO = (0, 0, 0)
    COR_OBJETOS = (255, 255, 255)
    FPS = 60


class Audio:
    def __init__(self):
        self.raquete = pygame.mixer.Sound("sounds/raquete.mp3")
        self.parede = pygame.mixer.Sound("sounds/parede.mp3")
        self.gol = pygame.mixer.Sound("sounds/gol.mp3")

        pygame.mixer.music.load("sounds/fundo.mp3")
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)


class Raquete:
    def __init__(self, x, y, velocidade=5):
        self.rect = pygame.Rect(x, y, 10, 60)
        self.velocidade = velocidade

    def mover(self, direcao):
        if direcao == "cima" and self.rect.top > 0:
            self.rect.y -= self.velocidade
        elif direcao == "baixo" and self.rect.bottom < Config.ALTURA:
            self.rect.y += self.velocidade

    def desenhar(self, tela):
        pygame.draw.rect(tela, Config.COR_OBJETOS, self.rect)


class Bola:
    def __init__(self, verdadeira=True):
        self.rect = pygame.Rect(0, 0, 7, 7)
        self.verdadeira = verdadeira
        self.cor = Config.COR_OBJETOS if verdadeira else self.cor_aleatoria()
        self.colidiu_raquete = False  # ✅ controle individual
        self.resetar()

    def cor_aleatoria(self):
        return (
            random.randint(50, 255),
            random.randint(50, 255),
            random.randint(50, 255),
        )

    def mover(self):
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y

    def inverter_x(self):
        self.vel_x *= -1
        self.aplicar_aleatoriedade()

    def inverter_y(self):
        self.vel_y *= -1
        self.aplicar_aleatoriedade()

    def aplicar_aleatoriedade(self):
        self.vel_x += random.choice([-1, 0, 1])
        self.vel_y += random.choice([-1, 0, 1])

        if abs(self.vel_x) < 3:
            self.vel_x = 3 if self.vel_x >= 0 else -3

        if abs(self.vel_y) < 3:
            self.vel_y = 3 if self.vel_y >= 0 else -3

    def resetar(self):
        self.rect.center = (Config.LARGURA // 2, Config.ALTURA // 2)
        self.vel_x = random.choice([-5, 5])
        self.vel_y = random.choice([-5, 5])

    def desenhar(self, tela):
        pygame.draw.circle(tela, self.cor, self.rect.center, 7)


class Game:
    def __init__(self, tela, audio):
        self.tela = tela
        self.clock = pygame.time.Clock()
        self.audio = audio
        self.reset()

    def reset(self):
        self.player1 = Raquete(15, Config.ALTURA // 2 - 30)
        self.player2 = Raquete(Config.LARGURA - 25, Config.ALTURA // 2 - 30)

        self.bolas = [Bola(verdadeira=True)]

        self.score1 = 0
        self.score2 = 0

        self.tempo_ultimo_powerup = pygame.time.get_ticks()

    def tratar_eventos(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def mover_jogador(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP]:
            self.player1.mover("cima")
        if keys[pygame.K_DOWN]:
            self.player1.mover("baixo")

    def mover_ia(self):
        for bola in self.bolas:
            if bola.verdadeira:
                alvo = bola
                break

        if self.player2.rect.centery < alvo.rect.centery:
            self.player2.mover("baixo")
        else:
            self.player2.mover("cima")

    def multiplicar_bolas(self, bola_base):
        novas = []

        for _ in range(4):
            b = Bola(verdadeira=False)
            b.rect.center = bola_base.rect.center

            b.vel_x = bola_base.vel_x * random.choice([-1, 1])
            b.vel_y = bola_base.vel_y * random.choice([-1, 1])

            novas.append(b)

        self.bolas.extend(novas)

    def verificar_colisoes(self):
        tempo_atual = pygame.time.get_ticks()

        for bola in self.bolas:
            colidiu = bola.rect.colliderect(self.player1.rect) or \
                      bola.rect.colliderect(self.player2.rect)

            if colidiu:
                if not bola.colidiu_raquete:
                    bola.inverter_x()
                    self.audio.raquete.stop()
                    self.audio.raquete.play()

                    if tempo_atual - self.tempo_ultimo_powerup >= 5000:
                        self.multiplicar_bolas(bola)
                        self.tempo_ultimo_powerup = tempo_atual

                    bola.colidiu_raquete = True
            else:
                bola.colidiu_raquete = False

            if bola.rect.top <= 0 or bola.rect.bottom >= Config.ALTURA:
                bola.inverter_y()
                self.audio.parede.stop()
                self.audio.parede.play()

    def verificar_pontos(self):
        for bola in self.bolas:
            if not bola.verdadeira:
                continue

            if bola.rect.left <= 0:
                self.score2 += 1
                self.audio.gol.play()
                self.reset()
                return True

            if bola.rect.right >= Config.LARGURA:
                self.score1 += 1
                self.audio.gol.play()
                self.reset()
                return True

        return False

    def atualizar(self):
        for bola in self.bolas:
            bola.mover()

        self.mover_jogador()
        self.mover_ia()
        self.verificar_colisoes()
        return self.verificar_pontos()

    def desenhar(self):
        self.tela.fill(Config.COR_FUNDO)

        self.player1.desenhar(self.tela)
        self.player2.desenhar(self.tela)

        for bola in self.bolas:
            bola.desenhar(self.tela)

        font = pygame.font.SysFont(None, 36)
        texto = font.render(f"{self.score1} - {self.score2}", True, Config.COR_OBJETOS)
        self.tela.blit(texto, texto.get_rect(center=(Config.LARGURA // 2, 30)))

        pygame.display.flip()

    def rodar(self):
        while True:
            self.tratar_eventos()

            if self.atualizar():
                return

            self.desenhar()
            self.clock.tick(Config.FPS)


class Menu:
    def __init__(self, tela):
        self.tela = tela

    def mostrar(self):
        while True:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if evento.type == pygame.KEYDOWN and evento.key == pygame.K_SPACE:
                    return

            self.tela.fill(Config.COR_FUNDO)

            font = pygame.font.SysFont(None, 50)
            titulo = font.render("Pong", True, Config.COR_OBJETOS)
            self.tela.blit(titulo, titulo.get_rect(center=(Config.LARGURA // 2, 150)))

            font2 = pygame.font.SysFont(None, 26)
            texto = font2.render("Pressione ESPAÇO", True, Config.COR_OBJETOS)
            self.tela.blit(texto, texto.get_rect(center=(Config.LARGURA // 2, 350)))

            pygame.display.flip()


def main():
    tela = pygame.display.set_mode((Config.LARGURA, Config.ALTURA))
    pygame.display.set_caption("Pong")

    menu = Menu(tela)
    audio = Audio()
    game = Game(tela, audio)

    while True:
        menu.mostrar()
        game.reset()
        game.rodar()


if __name__ == "__main__":
    main()