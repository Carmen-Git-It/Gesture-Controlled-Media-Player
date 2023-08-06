import pygame
import os

class MusicPlayer:
    def __init__(self, media_directory):
        self.media_directory = media_directory
        self.media_files = [f for f in os.listdir(media_directory) if os.path.isfile(os.path.join(media_directory, f))]
        self.current_media_index = 0
        self.volume_increment = 0.1

        pygame.init()

        self.window_width, self.window_height = 800, 600
        self.window = pygame.display.set_mode((self.window_width, self.window_height))

        pygame.display.set_caption("Media Player")

        self.background_color = (255, 255, 255)
        self.font = pygame.font.Font(None, 36)

        # Load the icons
        self.pause_icon = pygame.image.load("./images/icons/pause-button.png")
        self.pause_icon = pygame.transform.scale(self.pause_icon, (50, 50))

        self.next_icon = pygame.image.load("./images/icons/right.png")
        self.next_icon = pygame.transform.scale(self.next_icon, (50, 50))

        self.prev_icon = pygame.image.load("./images/icons/left-arrow.png")
        self.prev_icon = pygame.transform.scale(self.prev_icon, (50, 50))

        self.play_icon = pygame.image.load("./images/icons/play.png")
        self.play_icon = pygame.transform.scale(self.play_icon, (50, 50))
        
        self.volume_up_icon = pygame.image.load("./images/icons/volume-up.png")
        self.volume_up_icon = pygame.transform.scale(self.volume_up_icon, (50, 50))
        
        self.volume_down_icon = pygame.image.load("./images/icons/volume-down.png")
        self.volume_down_icon = pygame.transform.scale(self.volume_down_icon, (50, 50))

        # Load the first media file
        self.load_media()

        self.initial_volume = pygame.mixer.music.get_volume()
        self.current_state_icon = self.play_icon


    def load_media(self):
        media_path = os.path.join(self.media_directory, self.media_files[self.current_media_index])
        pygame.mixer.music.load(media_path)

    def play(self):
        pygame.mixer.music.play()

    def pause(self):
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.pause()
            self.current_state_icon = self.play_icon
        else:
            pygame.mixer.music.unpause()
            self.current_state_icon = self.pause_icon

    def next_song(self):
        self.current_media_index = (self.current_media_index + 1) % len(self.media_files)
        self.load_media()
        self.play()

    def previous_song(self):
        self.current_media_index = (self.current_media_index - 1) % len(self.media_files)
        self.load_media()
        self.play()

    def increase_volume(self):
        volume = min(pygame.mixer.music.get_volume() + self.volume_increment, 1.0)
        pygame.mixer.music.set_volume(volume)

    def decrease_volume(self):
        volume = max(pygame.mixer.music.get_volume() - self.volume_increment, 0.0)
        pygame.mixer.music.set_volume(volume)

    def run(self):
        running = True
        self.play()
        self.pause()

        while running:
            self.window.fill(self.background_color)

            # Display the current media file name
            text = self.font.render(self.media_files[self.current_media_index], True, (0, 0, 0))
            text_rect = text.get_rect(center=(self.window_width // 2, self.window_height // 2))
            self.window.blit(text, text_rect)

            # Display the volume level
            volume_text = self.font.render(f"Volume: {int(pygame.mixer.music.get_volume() * 100)}%", True, (0, 0, 0))
            volume_text_rect = volume_text.get_rect(center=(self.window_width // 2, self.window_height // 2 + 50))
            self.window.blit(volume_text, volume_text_rect)

            # Display the playback control buttons
            current_state_icon_rect = self.current_state_icon.get_rect(center=(self.window_width // 2, self.window_height - 50))
            self.window.blit(self.current_state_icon, current_state_icon_rect)

            next_icon_rect = self.next_icon.get_rect(center=(self.window_width // 2 + 150, self.window_height - 50))
            self.window.blit(self.next_icon, next_icon_rect)

            prev_icon_rect = self.prev_icon.get_rect(center=(self.window_width // 2 + 75, self.window_height - 50))
            self.window.blit(self.prev_icon, prev_icon_rect)

            # Display the volume control buttons
            volume_up_icon_rect = self.volume_up_icon.get_rect(center=(self.window_width // 2 - 75, self.window_height - 50))
            self.window.blit(self.volume_up_icon, volume_up_icon_rect)

            volume_down_icon_rect = self.volume_down_icon.get_rect(center=(self.window_width // 2 - 150, self.window_height - 50))
            self.window.blit(self.volume_down_icon, volume_down_icon_rect)

            

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.pause()
                        current_state_icon_rect = self.current_state_icon.get_rect(center=(self.window_width // 2 - 100, self.window_height - 50))
                    elif event.key == pygame.K_RIGHT:
                        self.next_song()
                    elif event.key == pygame.K_LEFT:
                        self.previous_song()
                    elif event.key == pygame.K_UP:
                        self.increase_volume()
                    elif event.key == pygame.K_DOWN:
                        self.decrease_volume()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if current_state_icon_rect.collidepoint(mouse_pos):
                        self.pause()
                        current_state_icon_rect = self.current_state_icon.get_rect(center=(self.window_width // 2 - 100, self.window_height - 50))
                    elif next_icon_rect.collidepoint(mouse_pos):
                        self.next_song()
                    elif prev_icon_rect.collidepoint(mouse_pos):
                        self.previous_song()
                    elif volume_text_rect.collidepoint(mouse_pos):
                        self.increase_volume()
                    elif volume_up_icon_rect.collidepoint(mouse_pos):
                      self.increase_volume()
                    elif volume_down_icon_rect.collidepoint(mouse_pos):
                      self.decrease_volume()

            # Update the display
            pygame.display.flip()

        self.quit()

    def quit(self):
        pygame.quit()

media_directory = "./music"
player = MusicPlayer(media_directory)

player.run()
