import pygame

pygame.mixer.init()
pygame.mixer.music.load('assets/sounds/alert.mp3')

alert_playing = False

def play_alert_sound():
    global alert_playing
    if not alert_playing:
        pygame.mixer.music.play(-1)
        alert_playing = True

def stop_alert_sound():
    global alert_playing
    if alert_playing:
        pygame.mixer.music.stop()
        alert_playing = False