import sqlite3 as sq
import random
import time
# TODO What can we do  :::: setting point // set the teams // send new word



class Player_class(object):

    def __init__(self,client_addr,client_conn,client_is_boss =False):
        self.client_name = None
        self.client_port = client_addr[1]
        self.clietn_ID = client_addr[0]
        self.client_conn = client_conn
        self.client_room_name = None
        self.client_room = None
        self.client_is_boss = client_is_boss



class Room_class(object):

    def __init__(self, room_name, max_player):
        self.format = "utf-8"
        self.max_player = max_player
        self.player_list = []
        self.room_name = room_name
        self.word_dataset = None

        self.team_one_list = []
        self.team_two_list = []
        self.team_tuple_list = [self.team_one_list,self.team_two_list]


        self.score_board = [0,0]
        self.point_msg_converter = {'WRONG':-1,'CORRECT':+1,'PASS':0}

        self.current_team = 0
        self.current_player = 0
        self.team_one_player = None
        self.team_two_player = None

        self.old_word_list = []
        self.max_index = 132

    def Player_connect(self, client):

        # Burda yeni oyuncunun katılması işini hallettik [Oda doluluğunada bakılır]
        if len(self.player_list) < int(self.max_player) :
            client.client_conn.send('girdin iste amk'.encode(self.format))

            self.player_list.append(client)
            team_index = len(self.player_list) % 2
            (self.team_tuple_list[team_index]).append(client)
            self.Team_mate_returner()

            if len(self.player_list) == int(self.max_player):
                self.Game_starter()

            return [False,'asdfa']



        else: return [True,"[PALYER CAPACITY FULL]]"]

    def Player_Disconnect(self,client):
        self.player_list.remove(client)

        return [True,"[PLAYER DISCONNECTED]"]

    def Room_msg_Analayzer(self, splited_msg):
        # TIME OUT => yeni oyuncu :: Diğer kalanları ise puanlama  ile ilgili onu elsede hallettik

        if 'TIME OUT' == splited_msg[1]:
            self.current_player += 1
            self.current_team += 1
            self.Game_starter()

        else :
            # Puanlama kısmı
            new_word = '!NEW WORD//'
            new_word += self.New_word_sender()
            point = self.point_msg_converter[splited_msg[1]]
            self.Pointer_Setter(point)
            self.team_one_player.client_conn.send(new_word.encode(self.format))
            self.team_two_player.client_conn.send(new_word.encode(self.format))
            time.sleep(1)
            current_score = str('!SCORE//' + str(self.score_board[1]) + '//'+ str(self.score_board[0]))
            self.Group_msg_sender(current_score)

    def Game_starter(self):
        # Bütün oyuncuları kelime listesini ve buttonların kullanım iznini sıfırlar
        time.sleep(2)
        self.Group_msg_sender('!TIME OUT')
        time.sleep(3)


        # Yeni oyuncuları seçtik
        self.Player_setter()

        # Gidicek kelime setini topladık
        new_word_set = '!NEW SET//'
        for _ in range(4):
            new_word = self.New_word_sender()
            new_word_set += (new_word + ',,')

        # Burda da gönderdik
        self.team_one_player.client_conn.send((new_word_set + '//storyteller').encode(self.format))
        self.team_two_player.client_conn.send((new_word_set + '//').encode(self.format))

    def New_word_sender(self):
        random_index = random.randint(1,self.max_index)
        print(f"Random index ::: {random_index} ;;;; type {type(random_index)}")
        if random_index in self.old_word_list :
            self.New_word_sender()

        DB_conn = sq.connect('Word_dataset.db')
        DB_cursor = DB_conn.cursor()

        self.old_word_list.append(random_index)
        DB_cursor.execute("Select * from word_dataset where word_index = ?",(random_index,))
        return_data = (list((DB_cursor.fetchall())[0]))[1]

        return return_data



    def Pointer_Setter(self,point):
        # Burda puanşama işi hallediliyo
        self.score_board[self.current_team] += point

    def Player_setter(self):

        # Burda ufak bir is yaptiki bidakine önçeki oyuncaların listesi sıfırlansın

        # Anlatıcı ve kontrol ediciyi belirler. Time outtada işe yarar
        self.team_one_player = self.team_one_list[self.current_player % len(self.team_one_list)]
        self.team_two_player = self.team_two_list[self.current_player % len(self.team_two_list)]

    def Team_mate_returner(self):
        # Burda takımlar yazdırılıp atılıyor

        team_mate_str= ''

        for  player_obj in self.player_list:
            team_mate_str += str(player_obj.client_name + ',,')

        message = str('!PLAYER//' + team_mate_str)
        self.Group_msg_sender(message)

    def Group_msg_sender(self,group_msg):

        for client in self.player_list:
            client.client_conn.send(group_msg.encode(self.format))



























































