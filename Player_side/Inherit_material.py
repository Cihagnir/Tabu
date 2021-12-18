import pygame as pg

class upper_map (object):

    def __init__(self,surface,button_count,button_text_list,button_commend_list,button_poss_list,button_range_list,server_ghost):
        self.Server_ghost = server_ghost
        self.button_list = []
        self.win_surface = surface
        self.server_com_spliter = '//'

        for index in range(button_count) :
            self.button_creator(button_text_list[index], button_commend_list[index], button_poss_list[index], button_range_list[index])

    def button_creator(self,button_text,button_commend,button_pos,button_range):
        button_obj = class_button(button_text,button_commend,button_pos,button_range)
        self.button_list.append(button_obj)

    def be_unusable(self):
        for button_obj in self.button_list :
            cold_button_text = (button_obj.button_text) + '_cold'
            cold_pngtext = str('Buttons/' + cold_button_text + '_button.png')
            button_obj.button_png = pg.image.load(cold_pngtext)


    def be_usuable(self):
        for button_obj in self.button_list:
            button_text = (button_obj.button_text)
            noncold_pngtext = str('Buttons/' + button_text + '_button.png')
            print(f'Button name {noncold_pngtext}')
            button_obj.button_png = pg.image.load(noncold_pngtext)


    def text_printer(self,text_list,win_surface):

        for text_tuple in text_list :
            text = text_tuple[0]
            text_size = text_tuple[1]
            text_poss = text_tuple[2]
            text_color = text_tuple[3]

            base_font = pg.font.Font(None, text_size)
            text_surface = base_font.render(text,True,text_color)
            win_surface.blit(text_surface,text_poss)



class class_button(object):

    def __init__(self,button_text,button_commend,button_poss,button_range):
        self.x_point = button_poss[0]
        self.y_point = button_poss[1]
        self.button_range = button_range
        self.button_text =  button_text
        self.button_commend = button_commend

        self.button_filetext = str('Buttons/' + button_text + '_button.png')
        self.button_png = pg.image.load(self.button_filetext)

    def Is_clicked(self,mouse_pos):
        if mouse_pos[0] > self.x_point and mouse_pos[0] < self.x_point + self.button_range[0] :
            if mouse_pos[1] > self.y_point and mouse_pos[1] < self.y_point + self.button_range[1] :
                return (True, self.button_commend)
            else:
                return (False, 'asdasd')
        else:
            return (False, 'asdasd')

    def button_drawer(self,win_surface):
        win_surface.blit(self.button_png,(self.x_point,self.y_point))


class server_line(object):

    def __init__(self, server_name, current_player_count, max_player,pos_tuple):
        self.server_name = server_name
        self.x_pos = pos_tuple[0]
        self.y_pos = pos_tuple[1]
        self.current_player = current_player_count
        self.max_player = max_player

        self.Login_button = None
        self.server_line_BG = pg.image.load("Background/Server_line_bg.png")

    def server_line_drawer(self,win_surface):
        win_surface.blit(self.server_line_BG,(self.x_pos,self.y_pos))
        Server_text_list = [(self.server_name, 30, (self.x_pos + 10, self.y_pos + 15), (255, 196, 0)),
                            (str(self.current_player + '/' + self.max_player), 30, (self.x_pos + 250, self.y_pos + 15),
                             (255, 196, 0))]

        for text_info in Server_text_list :
            text = text_info[0]
            text_size = text_info[1]
            text_poss = text_info[2]
            text_color = text_info[3]

            base_font = pg.font.Font(None, text_size)
            text_surface = base_font.render(text, True, text_color)
            win_surface.blit(text_surface, text_poss)





























