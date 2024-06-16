import  pygame

from card import *
from game import *
from colors import *

pygame.init()

w = 960
h = 540
screen = pygame.display.set_mode((w, h))
clock = pygame.time.Clock()
running = True

pixel_font = pygame.font.Font('assets/fonts/press_start_2p.ttf', 24)
small_pixel_font = pygame.font.Font('assets/fonts/press_start_2p.ttf', 16)

gameState = GameState()
gameState.new_game()

while running:
    clock.tick(60)
    
    screen.fill(LIGHT_GREEN)
    
    hit_button_rect = pygame.Rect(w - 120, h - 70, 100, 50)
    stop_button_rect = pygame.Rect(w - 240, h - 70, 100, 50)
    restart_button_rect = pygame.Rect(w - 140, h - 70, 120, 50)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if hit_button_rect.collidepoint(event.pos) and gameState.playing:
                    print("HIT button clicked!")
                    gameState.deal_card(gameState.player_hand)
                    gameState.check_game_status()
                    
                elif stop_button_rect.collidepoint(event.pos) and gameState.playing:
                    print("STOP button clicked!")
                    gameState.playing = False
                    gameState.check_game_status()
                    
                elif restart_button_rect.collidepoint(event.pos) and not gameState.playing:
                    print("RESTART button clicked!")
                    gameState.new_game()
    
    # Check if mouse is hovering over the button
    mouse_pos = pygame.mouse.get_pos()
    if hit_button_rect.collidepoint(mouse_pos):
        hit_button_color = hover_color
    else:
        hit_button_color = button_color

    if stop_button_rect.collidepoint(mouse_pos):
        stop_button_color = hover_color
    else:
        stop_button_color = button_color       
        
    if restart_button_rect.collidepoint(mouse_pos):
        restart_button_color = hover_color
    else:
        restart_button_color = button_color             
            
    # draw title
    text_surf = pixel_font.render('BLACKJACK PYTHON CASINO', True, BLACK)
    text_rect = text_surf.get_rect(center=(w / 2, 80))
    screen.blit(text_surf, text_rect)
    
    if gameState.playing:
        # Draw the HIT button
        pygame.draw.rect(screen, hit_button_color, hit_button_rect)
        
        # Draw text on the HIT button
        text_surf = small_pixel_font.render('HIT', True, BLACK)
        text_rect = text_surf.get_rect(center=hit_button_rect.center)
        screen.blit(text_surf, text_rect)
        
        # Draw the STOP button
        pygame.draw.rect(screen, stop_button_color, stop_button_rect)
        
        # Draw text on the STOP button
        text_surf = small_pixel_font.render('STOP', True, BLACK)
        text_rect = text_surf.get_rect(center=stop_button_rect.center)
        screen.blit(text_surf, text_rect)
    else:
        # Draw the RESTART button
        pygame.draw.rect(screen, restart_button_color, restart_button_rect)
        
        # Draw text on the RESTART button
        text_surf = small_pixel_font.render('RESTART', True, BLACK)
        text_rect = text_surf.get_rect(center=restart_button_rect.center)
        screen.blit(text_surf, text_rect)
        
        # draw result
        result = 'PLAYER WON' if gameState.player_won else 'DEALER WON' if gameState.dealer_won else 'TIE'
        text_surf = pixel_font.render(result, True, BLACK)
        text_rect = text_surf.get_rect(center=(w / 2, 160))
        screen.blit(text_surf, text_rect)
        
                
    # draw dealer hand
    dealer_hand_text =  'Dealer: ' + (str(gameState.value_of_hand(gameState.dealer_hand)) if not gameState.playing else str(gameState.dealer_hand[0].value()))
    text_surf = pixel_font.render(dealer_hand_text, True, BLACK)
    text_rect = text_surf.get_rect(bottomleft=(20, h - 250))
    screen.blit(text_surf, text_rect)
            
    for index, card in enumerate(gameState.dealer_hand):
        position_x = 20 + index * card.image_size()[0] * 1.1
        position_y = h - 170
        card.draw_image((position_x, position_y), screen, gameState.playing and index > 0)
            
    # draw player hand
    player_hand_text =  'Player: ' + str(gameState.value_of_hand(gameState.player_hand))
    text_surf = pixel_font.render(player_hand_text, True, BLACK)
    text_rect = text_surf.get_rect(bottomleft=(20, h - 100))
    screen.blit(text_surf, text_rect)
            
    for index, card in enumerate(gameState.player_hand):
        position_x = 20 + index * card.image_size()[0] * 1.1
        position_y = h - 20
        card.draw_image((position_x, position_y), screen)
        
    pygame.display.update()
    
pygame.quit()
        