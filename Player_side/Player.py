import pygame as pg

pg.init()

import Inherit_material as IM
import Player_server_class as Server

Map_change = False


class entry_map(IM.upper_map):
    def __init__(self, surface, button_count, button_text_list, button_commend_list, button_poss_list,
            button_range_list, server_ghost):
        super(entry_map, self).__init__(surface, button_count, button_text_list, button_commend_list, button_poss_list,
                                        button_range_list, server_ghost)

        self.Background = pg.image.load('Background/entery_page_bg.png')
        self.user_text = ''
        self.Map_text_list = ('Please enter your nickname', 48, (200, 150), (255, 255, 51))

    def server_comm_tower(self, commend):
        self.Server_ghost.server_comunication(commend)

    def server_msg_analyzer(self,comm_commend):
        return True

    def keybordevent_check(self):
        global R_we_turning, Map_change
        for event in pg.event.get():
            pos = pg.mouse.get_pos()
            if event.type == pg.QUIT:
                R_we_turning = False
                self.Server_ghost.thread_killer()
                pg.quit()

            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_BACKSPACE:
                    self.user_text = self.user_text[:-1]
                else:
                    self.user_text += event.unicode

            elif event.type == pg.MOUSEBUTTONDOWN:

                for button in self.button_list:
                    return_val = button.Is_clicked(pos)
                    condition, return_text = return_val[0], return_val[1]
                    if condition:
                        self.server_comm_tower(str(return_text + self.server_com_spliter + self.user_text))
                        Map_change = True

    def map_drawer(self):
        self.win_surface.fill((52, 3, 84))
        self.win_surface.blit(self.Background, (150, 150))
        self.text_printer([(self.Map_text_list), (self.user_text, 40, (234, 405), (181, 124, 255))], self.win_surface)
        for button in self.button_list:
            button.button_drawer(self.win_surface)


# -----------------------------------------------------------------------------------------------------------------------
class server_side(IM.upper_map):

    def __init__(self, surface, button_count, button_text_list, button_commend_list, button_poss_list,
            button_range_list, server_ghost):
        super(server_side, self).__init__(surface, button_count, button_text_list, button_commend_list,
                                          button_poss_list, button_range_list, server_ghost)
        self.line_png = pg.image.load('Background/line.png')
        self.darwin_png = pg.image.load('Background/Darwin.png')
        self.Pacman_png = pg.image.load('Background/Pacman.png')
        self.Drop_png = pg.image.load('Background/Drop.png')
        self.blit_list = [(self.line_png, (150, 660)), (self.darwin_png, (20, 740)), (self.Pacman_png, (500, 30)),
                          (self.Drop_png, (700, 120))]
        self.server_line_list = []
        self.server_line_name_list = []
        self.last_SL_pos = [150, 75]

        self.last_commend = ''
        self.Full_error = False
        self.R_we_texting = False
        self.button_range = len(self.button_list) - 1
        self.popup_BG = pg.image.load('Background/Popup_bg.png')

        self.room_name = ' '
        self.max_player = ' '
        self.text_index = 0
        self.text_list = ['', '']
        self.current_text = ''
        self.create_commend = ''

    def server_comm_tower(self, commend):
        print(f'Comm tower" a gelen mesaj ::: {commend}')

        if commend == '!SEND':
            self.last_commend = commend
            self.R_we_texting = True
            self.button_range = len(self.button_list)

        elif commend == '!ROOM//CREATE':
            self.last_commend = commend
            server_commend = str(
                commend + self.server_com_spliter + self.room_name + self.server_com_spliter + self.max_player)
            print(f'create içim kullanılan komut {server_commend}')
            self.Server_ghost.server_comunication(server_commend)

        elif 'REFRESH' or 'JOIN' in commend:
            self.last_commend = commend
            self.Server_ghost.server_comunication(commend)

    def server_msg_analyzer(self,comm_commend):
        print(f'Server msg analici 2.map \n gelen mesaj ::: {comm_commend}')
        if self.last_commend == '!REFRESH':
            splited_comm = comm_commend.split('++')
            comm_commend_1 , comm_commend_2 = splited_comm[0],splited_comm[1]
            room_info = comm_commend_1.split(',,')
            player_info = comm_commend_2.split(',,')
            self.server_line_creator(room_info,player_info)
            return True

        elif 'JOIN' in self.last_commend :
            if comm_commend == '[PALYER CAPACITY FULL]' :
                self.Full_error = True
                return True
            else:
                self.map_changer()
                return False

        elif self.last_commend == '!ROOM//CREATE':
            self.map_changer()
            return False

    def keybordevent_check(self):
        global R_we_turning

        for event in pg.event.get():
            mouse_pos = pg.mouse.get_pos()
            if event.type == pg.QUIT:
                R_we_turning = False
                self.Server_ghost.thread_killer()
                pg.quit()

            elif event.type == pg.MOUSEBUTTONDOWN:
                # Buda amp üzerindeki basımlar için
                for index in range(len(self.server_line_list),self.button_range):
                    button_obj = self.button_list[index]
                    return_answer = button_obj.Is_clicked(mouse_pos)
                    condition, commend = return_answer[0], return_answer[1]
                    if condition:
                        self.server_comm_tower(commend)

                # Server lineların buttob kontrolü
                for server_line_obj in self.server_line_list:
                    # Burda server lineların join buttonlarının Is_clıcked functı çağırılır
                    return_answer = server_line_obj.Login_button.Is_clicked(mouse_pos)
                    condition, commend = return_answer[0], return_answer[1]
                    if condition:
                        server_mesage = commend + self.server_com_spliter + server_line_obj.server_name
                        self.server_comm_tower(server_mesage)

            elif self.R_we_texting:

                if event.type == pg.KEYDOWN:
                    if event.key == (pg.K_TAB or pg.K_a):
                        self.text_index += 1
                        self.current_text = ""

                    elif event.key == pg.K_ESCAPE:
                        self.R_we_texting = False
                        self.button_range = len(self.button_list) - 1

                    elif event.key == pg.K_BACKSPACE:
                        self.current_text = self.current_text[:-1]
                        self.text_list[(self.text_index % 2)] = self.current_text

                    else:
                        self.current_text += event.unicode
                        self.text_list[(self.text_index % 2)] = self.current_text
                    self.room_name = self.text_list[0]
                    self.max_player = self.text_list[1]

    def server_line_creator(self, server_info_list,curr_player_list):
        #TODO burda player sayıları için bütün sayıları resetleriz buna bir çözüm bulmak lazım
        server_line_index = 0
        R_we_pass = True


        for unsplited_server_info,curr_player in zip(server_info_list,curr_player_list):
            server_info = unsplited_server_info.split(self.server_com_spliter)

            print(f'oda adi ::: {server_info[0]}')

            if server_info[0] != '':
                if server_info[0] not in self.server_line_name_list :
                    self.last_SL_pos[1] += 85
                    pos_tuple = self.last_SL_pos

                    self.server_line_name_list.append(server_info[0])
                    server_line_obj = IM.server_line(server_name=server_info[0], current_player_count=server_info[1],
                                                     max_player=server_info[2], pos_tuple=pos_tuple)
                    server_line_obj.Login_button = IM.class_button(button_text='join', button_commend='!ROOM//JOIN',
                                                                   button_poss=(server_line_obj.x_pos + 375,
                                                                                server_line_obj.y_pos + 20),
                                                                   button_range=(75, 30))
                    self.button_list.insert(0, server_line_obj.Login_button)
                    self.server_line_list.append(server_line_obj)
                    self.button_range = len(self.button_list) - 1

                if True :
                    room_obj = self.server_line_list[server_line_index]
                    room_obj.current_player = curr_player


            server_line_index += 1

    def map_changer(self):
        global Map_change
        Map_change = True

    def map_drawer(self):
        self.win_surface.fill((135, 117, 178))
        self.text_printer([('Server List', 48, (100, 100), (33, 84, 177))], self.win_surface)
        for blit_obj in self.blit_list:
            self.win_surface.blit(blit_obj[0], blit_obj[1])

        for server_line_obj in self.server_line_list:
            server_line_obj.server_line_drawer(self.win_surface)

        if self.R_we_texting:
            self.win_surface.blit(self.popup_BG, (250, 250))
            self.text_printer(
                [('Room name', 28, (300, 310), (0, 230, 119)), ('Max player', 28, (300, 370), (0, 230, 119)),
                 (str(self.room_name), 24, (430, 320), (167, 255, 234)),
                 (self.max_player, 24, (430, 377), (167, 255, 234))], self.win_surface)

        if self.Full_error:
            self.text_printer([('Oda dolu mübarek başkasını dene', 24, (255, 0, 0), (150, 630))], self.win_surface)

        for index in range(self.button_range):
            button_obj = self.button_list[index]
            button_obj.button_drawer(self.win_surface)

# -----------------------------------------------------------------------------------------------------------------------
class game_side(IM.upper_map):

    def __init__(self, surface, button_count, button_text_list, button_commend_list, button_poss_list,
            button_range_list, server_ghost):
        super(game_side, self).__init__(surface, button_count, button_text_list, button_commend_list, button_poss_list,
                                        button_range_list, server_ghost)
        self.TABU_card = pg.image.load('Background/Tabu_card.png')
        self.Score_board = pg.image.load('Background/Score_board.png')
        self.Team_board = pg.image.load('Background/Team_board.png')
        self.R_game_started = False
        self.curr_word_index = 0
        self.word_list = []
        self.word_poss_list = [(80,50),(80,75),(80,100),(80,125),(80,150),(80,175),(80,215),(80,230),(80,255),(80,280),(80,305),(80,330),
                               (325,50),(325,75),(325,100),(325,125),(325,150),(325,175),(325,215),(325,230),(325,255),(325,280),(325,305),(325,330)]

        self.player_list = []
        self.storyteller = False
        self.team_one_score = 0
        self.team_two_score = 0

    def keybordevent_check(self):
        global R_we_turning

        for event in pg.event.get():
            mouse_pos = pg.mouse.get_pos()
            if event.type == pg.QUIT :
                R_we_turning = False
                self.Server_ghost.thread_killer()
                pg.quit()

            elif (event.type == pg.MOUSEBUTTONDOWN) and self.storyteller :
                for button_obj in self.button_list :
                    return_ansert = button_obj.Is_clicked(mouse_pos)
                    condition, commend = return_ansert[0], return_ansert[1]
                    if condition :
                        print(f'Buttona basildi basilan button {commend}')
                        print('---------------------------------------- \n')
                        self.Server_ghost.server_comunication(commend)

    def server_msg_analyzer(self,server_msg):
        # !NEW SET .. !NEW WORD .. !SCORE SET .. !PLAYER SET
        print(f'***** Server mesaj analizci 3. map ************* \n gelen mesaj ::: {server_msg} \n')
        splited_msg = server_msg.split('//')
        print(f'bolunmus mesaj :::: {splited_msg} \n')
        Server_commend = splited_msg[0]
        if Server_commend == '!SCORE' :
            self.team_one_score = int(splited_msg[1])
            self.team_two_score = int(splited_msg[2])
            return True


        if Server_commend == '!NEW WORD':

            self.new_word_setter(splited_msg[1])
            return True

        elif Server_commend == '!TIME OUT' :
            print('Storyteller False eşitlendi beunsuable çağırılsı')
            self.storyteller = False
            self.be_unusable()
            self.word_list = []
            return True


        elif Server_commend == '!NEW SET':
            self.new_set_setter(splited_msg[1])
            print(f'splited msg 2 :: {splited_msg[2]}')
            if 'storyteller' in splited_msg[2] :
                print(f'beusableye girdi')
                print(f'////////////////////////////')
                self.storyteller = True
                self.be_usuable()

            self.R_game_started = True
            return True


        elif Server_commend == '!PLAYER':
            self.player_list = []
            player_list_extentation = (splited_msg[1]).split(',,')
            self.player_list.extend(player_list_extentation[0:len(player_list_extentation)-1 ])
            return True


    def new_set_setter(self,unsplited_msg):
        splieted_msg = unsplited_msg.split(',,')
        for word_set in splieted_msg :
            second_split = word_set.split(',')
            self.word_list.extend(second_split)

    def new_word_setter(self,unsplited_msg):

        splited_msg = unsplited_msg.split(',')
        for word in splited_msg :
            self.word_list[self.curr_word_index % 24 ] = word
            self.curr_word_index += 1
# ---------------------------------------------------- DRAWING ---------------------------------------------------


    def player_name_writer(self):
        first_name_X_poss = 70
        first_name_Y_poss = 520

        for index in range(0,len(self.player_list),2):

            player_name = self.player_list[index]

            base_font = pg.font.Font(None, 20)
            text_surface = base_font.render(player_name, True,(0,0,0) )
            self.win_surface.blit(text_surface, (first_name_X_poss,first_name_Y_poss))
            first_name_X_poss += 230
            try:
                player_name = self.player_list[index + 1]

                base_font = pg.font.Font(None, 18)
                text_surface = base_font.render(player_name, True, (0, 0, 0))
                self.win_surface.blit(text_surface, (first_name_X_poss, first_name_Y_poss))
                first_name_X_poss -= 230
                first_name_Y_poss += 26

            except IndexError:
                pass

    def word_writer(self):
        lap = 0
        for poss, word in zip(self.word_poss_list,self.word_list) :
            text_color = (255, 255, 255)
            text_size = 19
            if not(lap % 6) :
                text_color = (255, 0, 0)
                text_size = 22

            base_font = pg.font.Font(None, text_size)
            text_surface = base_font.render(word, True, text_color)
            self.win_surface.blit(text_surface, poss)

            lap += 1

    def map_drawer(self):
        self.win_surface.fill((173, 207, 255))
        self.win_surface.blit(self.TABU_card, (50, 30))
        self.win_surface.blit(self.TABU_card, (295, 30))
        self.win_surface.blit(self.Score_board, (600, 600))
        self.win_surface.blit(self.Team_board, (50, 450))

        self.player_name_writer()
        self.text_printer([(str(self.team_one_score), 30, (760,696), (255,255,0) ), (str(self.team_two_score), 30, (710,765), (255,255,0) )],self.win_surface)

        if self.R_game_started :
            self.word_writer()


        for button_obj in self.button_list:
            button_obj.button_drawer(self.win_surface)

# -----------------------------------------------------------------------------------------------------------------------
def main_loop():
    global R_we_turning, Map_change

    width = 800
    height = 800
    R_we_turning = True

    Surface = pg.display.set_mode((width, height))
    Server_ghost = Server.Server_isuue()

    Entry_map = entry_map(Surface, button_count=1, button_text_list=['continue'], button_commend_list=['!NAME'],
                          button_poss_list=[(300, 600)], button_range_list=[(200, 50)], server_ghost=Server_ghost)

    Server_side = server_side(Surface, button_count=3, button_text_list=['refresh', 'create', 'send'],
                              button_commend_list=['!REFRESH', '!SEND', '!ROOM//CREATE'],
                              button_poss_list=[(550, 700), (375, 700), (350, 450)],
                              button_range_list=[(150, 50), (150, 50), (75, 30)], server_ghost=Server_ghost)
    Game_map = game_side(Surface, button_count=4, button_text_list=['correct', 'wrong', 'pass', 'timeout'],
                         button_commend_list=['!ROOM//CORRECT', '!ROOM//WRONG', '!ROOM//PASS', '!ROOM//TIME OUT'],
                         button_poss_list=[(625, 50), (625, 120), (625, 190), (625, 260)],
                         button_range_list=[(160, 50), (160, 50), (160, 50), (160, 50)],
                         server_ghost=Server_ghost)

    Map_index = 0
    Map_list = [Entry_map, Server_side, Game_map]

    Current_map = Map_list[Map_index]

    Clock = pg.time.Clock()

    while R_we_turning:

        pg.time.delay(100)
        Clock.tick(60)

            # !NEW SET .. !NEW WORD .. !SCORE SET .. !PLAYER SET
        if Server_ghost.server_msg != '':
            Server_msg = Server_ghost.server_msg

            R_we_clear = Current_map.server_msg_analyzer(Server_msg)
            if R_we_clear :
                Server_ghost.server_msg = ''



        if Map_change:
            Map_index += 1
            Current_map = Map_list[Map_index]
            Map_change = False

        Current_map.keybordevent_check()
        Current_map.map_drawer()
        pg.display.update()


main_loop()
