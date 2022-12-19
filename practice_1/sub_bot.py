from paho.mqtt import client as mqtt
import os

# Прием и печать сообщения по MQTT протоколу
def on_message(client, userdata, message):
    print(str(message.payload.decode("utf-8")))

# Чтение данных из файла "data_for_sub_connection.txt"
# с предварительной проверкой на его существование
def read_file():
    file_name = 'data_for_sub_connection.txt'

    while True:
        if os.path.isfile(file_name) == False:
            continue
        else:
            dfc = []

            with open(file_name, encoding="utf-8", mode='r') as file:
                lines = file.readlines()

            for line in lines:
                if line.find('\n') != -1:
                    eoln_index = line.index('\n')
                    line = line[:eoln_index]
                dfc.append(line)

            return dfc

if __name__ == '__main__':
    data_for_connect = read_file()
    client_name = "###Subscriber###"
    client = mqtt.Client(client_name)

    client.connect(data_for_connect[0], int(data_for_connect[1]))
    client.subscribe(data_for_connect[2])

    client.on_message = on_message

    client.loop_forever()