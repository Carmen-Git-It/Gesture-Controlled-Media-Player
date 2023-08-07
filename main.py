if __name__ == '__main__':
    import pygame
    from gesture_detection import start
import os
import tkinter
import tkinter.filedialog
from multiprocessing import Process, Queue

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

        self.browse_icon = pygame.image.load("./images/icons/browse.png")
        self.browse_icon = pygame.transform.scale(self.browse_icon, (50, 50))

        self.replay_icon = pygame.image.load("./images/icons/replay.png")
        self.replay_icon = pygame.transform.scale(self.replay_icon, (45, 45))



        # Load the first media file
        self.load_media()

        self.initial_volume = pygame.mixer.music.get_volume()
        self.current_state_icon = self.play_icon

    def gesture_detection(self):
        if not receive_queue.empty():
            msg = str(receive_queue.get())
            if msg == 'ok':
                self.play()
            elif msg == 'stop':
                if pygame.mixer.music.get_busy():
                    self.pause()
            elif msg == 'fist':
                self.quit()
            elif msg == 'like':
                self.increase_volume()
            elif msg == 'dislike':
                self.decrease_volume()

    def load_media(self):
        media_path = os.path.join(self.media_directory, self.media_files[self.current_media_index])
        pygame.mixer.music.load(media_path)

    def play(self):
        pygame.mixer.music.play()
        self.current_state_icon = self.pause_icon
        current_state_icon_rect = self.current_state_icon.get_rect(center=(self.window_width // 2 - 100, self.window_height - 50))
        self.window.blit(self.current_state_icon, current_state_icon_rect)
        
        # Update the display
        pygame.display.flip()

    def pause(self):
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.pause()
            self.current_state_icon = self.play_icon
        else:
            pygame.mixer.music.unpause()
            self.current_state_icon = self.pause_icon

        current_state_icon_rect = self.current_state_icon.get_rect(center=(self.window_width // 2 - 100, self.window_height - 50))
        self.window.blit(self.current_state_icon, current_state_icon_rect)

        # Update the display
        pygame.display.flip()

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

    def replay_song(self):
        pygame.mixer.music.rewind()
        pygame.mixer.music.play()

    def browse_files(self):
        top = tkinter.Tk()
        top.withdraw()
        dir_name = tkinter.filedialog.askopenfilename(title="Select a file in the folder you would like to load",
                                                      initialdir='./',
                                                      filetypes=(('mp3 files', '*.mp3'),))
        dir_name = os.path.dirname(dir_name)
        if os.path.isdir(dir_name):
            # Filter out any files that are not mp3s
            self.media_files = [f for f in os.listdir(dir_name) if os.path.isfile(os.path.join(dir_name, f))
                                and f.endswith('.mp3')]
            if len(self.media_files) > 0:
                self.media_directory = dir_name
                self.current_media_index = 0
                self.load_media()
                self.play()
            else:
                self.media_files = [f for f in os.listdir(self.media_directory) if
                                    os.path.isfile(os.path.join(self.media_directory, f))
                                    and f.endswith('.mp3')]
        top.destroy()

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

            replay_icon_rect = self.replay_icon.get_rect(center=(self.window_width // 2 + 75, self.window_height - 50))
            self.window.blit(self.replay_icon, replay_icon_rect)

            next_icon_rect = self.next_icon.get_rect(center=(self.window_width // 2 + 225, self.window_height - 50))
            self.window.blit(self.next_icon, next_icon_rect)

            prev_icon_rect = self.prev_icon.get_rect(center=(self.window_width // 2 + 150, self.window_height - 50))
            self.window.blit(self.prev_icon, prev_icon_rect)

            # Display the volume control buttons
            volume_up_icon_rect = self.volume_up_icon.get_rect(center=(self.window_width // 2 - 75, self.window_height - 50))
            self.window.blit(self.volume_up_icon, volume_up_icon_rect)

            volume_down_icon_rect = self.volume_down_icon.get_rect(center=(self.window_width // 2 - 150, self.window_height - 50))
            self.window.blit(self.volume_down_icon, volume_down_icon_rect)

            browse_icon_rect = self.browse_icon.get_rect(center=(50, self.window_height - 575))
            self.window.blit(self.browse_icon, browse_icon_rect)

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
                    elif browse_icon_rect.collidepoint(mouse_pos):
                        self.browse_files()
                    elif replay_icon_rect.collidepoint(mouse_pos):
                      self.replay_song()

            self.gesture_detection()

            # Update the display
            pygame.display.flip()

        self.quit()

    def quit(self):
        send_queue.put('Closing')
        pygame.quit()

# Guard for multiprocessing
if __name__ == '__main__':
    # Create queue pipe and subprocess for gesture detection
    send_queue = Queue()
    receive_queue = Queue()
    gesture_detector = Process(target=start, args=(receive_queue, send_queue))
    gesture_detector.daemon = True
    gesture_detector.start()
    media_directory = "./music"
    player = MusicPlayer(media_directory)
    player.run()


