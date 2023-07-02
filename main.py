import pygame
from sys import exit
from random import choice
from Sprite import Player, Obstacle
from Setting import *


class Game:
    def __init__(self):
        # setup
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Jump')
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font('font/Pixeltype.ttf', 50)
        self.game_active = True
        self.start_time = 0

        # Groups
        self.player = pygame.sprite.GroupSingle()
        self.player.add(Player())
        self.obstacle_group = pygame.sprite.Group()

        # Background
        self.sky_surface = pygame.image.load('graphics/Sky.png').convert()
        self.ground_surface = pygame.image.load('graphics/ground.png').convert()

        # Game over screen
        # Character
        self.player_stand = pygame.image.load('graphics/Player/player_stand.png').convert_alpha()
        self.player_stand = pygame.transform.rotozoom(self.player_stand, 0, 2)
        self.player_stand_rect = self.player_stand.get_rect(center=(400, 200))

        # Text
        self.game_over_name = self.font.render('GAME OVER', False, (111, 196, 169))
        self.game_over_name_rect = self.game_over_name.get_rect(center=(400, 80))

        self.game_message = self.font.render('Press Space to run', False, (111, 196, 169))
        self.game_message_rect = self.game_message.get_rect(center=(400, 320))

        # Timer
        self.obstacle_timer = pygame.USEREVENT + 1
        pygame.time.set_timer(self.obstacle_timer, 1500)

    def display_score(self):
        current_time = int(pygame.time.get_ticks() / 1000) - self.start_time
        score_surf = self.font.render(f'Score: {current_time}', False, (64, 64, 64))
        score_rect = score_surf.get_rect(center=(400, 50))
        self.screen.blit(score_surf, score_rect)

    def collision_sprite(self):
        if pygame.sprite.spritecollide(self.player.sprite, self.obstacle_group, False):
            self.obstacle_group.empty()
            return False
        return True

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if self.game_active:
                    if event.type == self.obstacle_timer:
                        self.obstacle_group.add(Obstacle(choice(['fly', 'snail', 'snail'])))
                else:
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                        self.game_active = True
                        self.start_time = int(pygame.time.get_ticks() / 1000)
                        self.player.sprite.rect = self.player.sprite.image.get_rect(midbottom=(80, 300))

            if self.game_active:
                # General
                self.screen.blit(self.sky_surface, (0, 0))
                self.screen.blit(self.ground_surface, (0, 300))
                self.display_score()

                # Player
                self.player.draw(self.screen)
                self.player.update()

                # Obstacle movement
                self.obstacle_group.draw(self.screen)
                self.obstacle_group.update()

                # Collision
                self.game_active = self.collision_sprite()
            else:
                # End screen
                self.screen.fill((94, 129, 162))
                self.screen.blit(self.player_stand, self.player_stand_rect)

                self.screen.blit(self.game_over_name, self.game_over_name_rect)
                self.screen.blit(self.game_message, self.game_message_rect)

            pygame.display.update()
            self.clock.tick(FRAMERATE)


if __name__ == '__main__':
    game = Game()
    game.run()
