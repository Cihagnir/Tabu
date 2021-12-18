import socket
import threading


import Room


# TODO What can we do :::::  Accept the client // send feedback messaga // set the player name // createa room // join and disconnect the room // refresh server list

class Server_class(object):

    def __init__(self):
        self.header = 2048
        self.format = "utf-8"
        self.port = 5050
        self.IPV4 = socket.gethostbyname(socket.gethostname()) # Burası boş olacak
        self.ADDR = (self.IPV4, self.port)
        self.disconnect_message = "!DISCONNECT"

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


        self.server.bind(self.ADDR)

        self.client_list = []

        self.room_list = []

        self.server.listen()
        while True:
            client_conn, client_addr = self.server.accept()

            thread = threading.Thread(target=self.Clinet_Handling, args=(client_conn, client_addr))
            thread.start()
            print(f"[ACTIVE CONNECTION]{threading.activeCount() - 1}")


    def Clinet_Handling(self,client_conn,client_addr):
        # Burda gelen abimizin thread'ini açar mesaj için dinlemeye alırız

        print(f"[NEW CONNECTION]{client_addr} connected")

        client = Room.Player_class(client_addr, client_conn)

        self.client_list.append(client)

        connection = True
        while connection:
            msg_lenght = client_conn.recv(self.header).decode(self.format)
            if msg_lenght:
                msg_lenght = int(msg_lenght)
                message = client_conn.recv(msg_lenght).decode(self.format)

                if message == self.disconnect_message:
                    connection = False

                else:
                    print(f"{client_addr} : {message},, {msg_lenght}")
                    self.Msg_Analayzer(message, client, client_conn, )



        self.client_list.remove(client)
        client_conn.close()


    def Msg_Analayzer(self,message,client,client_conn):
        # Burda gelen abimizin mesajlarını inceleriz eğer odayla ilgili ise oda analicisine yollarız

        splited_msg = message.split('//')
        print(f'gelen msg ::: {splited_msg}')



        if '!NAME' == splited_msg[0] :
            client.client_name = splited_msg[1]
            self.Message_sender(client_conn,'[NAME SETTED]')

        elif '!REFRESH' == message :
            self.Room_Information_Refresher(client_conn,client)

        elif '!ROOM' == splited_msg[0] :

            if splited_msg[1] == 'CREATE' :
                # Oda oluşturma komutu '!ROOM//CREATE//oda_adı//max_palyer'
                room_name, max_player = splited_msg[2], splited_msg[3]
                self.Room_Creator(room_name,max_player,client)

            elif splited_msg[1] == ('JOIN' or 'DISCONNECT'):
                # Odadan ayrılma veya katılma komutu '!ROOM//JOIN//oda_adı' or '!ROOM//DISCONNECT'
                room_name = splited_msg[2]

                for room_object in self.room_list :
                    if room_object.room_name == room_name:
                        if splited_msg[1] == "JOIN":
                            return_message = room_object.Player_connect(client)
                            condition , message = return_message[0] ,return_message[1]
                            if condition :
                                self.Message_sender(client_conn, return_message)
                            else :
                                client.client_room = room_object
                                client.client_room_name = room_name


                        else:
                            return_message =room_object.Player_Disconnect(client)
                            client.client_room = None
                            client.client_room_name = None
                            self.Message_sender(client_conn,return_message)

            else:
                # Burda oda mesaj analizcisini cağırırız
                if client.client_room is not None :
                    client.client_room.Room_msg_Analayzer(splited_msg)



    def Room_Creator(self,room_name,max_player,client):
        # Room creation
        room = Room.Room_class(room_name,max_player)
        print("room creatordan player connect çağırıldı")
        room.Player_connect(client)
        self.room_list.append(room)

        # Player room setting
        client.client_room_name = room_name
        client.client_room = room

    def Room_Information_Refresher(self,client_conn,client):
        if client.client_room is None:
            client_message_1 = ''
            client_message_2 = ''
            IN_room_spiter = '//'
            OUT_room_spiter = ',,'
            BIG_BOSS = '++'

            if len(self.room_list) == 0 :
                self.Message_sender(client_conn, (client_message_1 + client_message_2) )

            for room_obj in self.room_list:
                client_message_1 += str(room_obj.room_name + IN_room_spiter + str(len(room_obj.player_list)) + IN_room_spiter + room_obj.max_player  + OUT_room_spiter)
                client_message_2 += str(len(room_obj.player_list)) + OUT_room_spiter

            total_msg = client_message_1 + BIG_BOSS + client_message_2

            self.Message_sender(client_conn,total_msg)

        else:
            self.Message_sender(client_conn, 'caz yapma')

    def Message_sender(self,client_conn,message):
        client_conn.send(message.encode(self.format))


Main_server = Server_class()









































