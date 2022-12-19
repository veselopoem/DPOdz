from paho.mqtt import client as mqtt
import sys
import math
import time

# Класс "App", в котором реализованы вычисления по движению робота
class App(object):
    brocker_ip = ''
    port_number = ''
    topic_name = ''
    bot_velocity = 0.0
    bot_angular_velocity = 0.0
    file_name = ''

    path_points = []
    distances = []
    driving_time = []
    angles = []
    angular_rotation_time = []
    message_about_sub = False

    # Считывание комманд, которые должен ввести в командную
    # строку пользователь
    def read_start_commands_from_cmd(self):
        start_commands_from_cmd = sys.argv
        return start_commands_from_cmd

    # Распознавание команд, считанных из командной строки
    def command_recognition(self, start_commands):
        self.brocker_ip = start_commands[1]
        self.port_number = int(start_commands[2])
        self.topic_name = start_commands[3]
        self.bot_velocity = float(start_commands[4])
        self.bot_angular_velocity = float(start_commands[5])
        self.file_name = start_commands[6]

    # Считывание из файла промежуточных координат робота
    def reading_file_with_coordinates(self, file_name):
        points = []
        count = 0

        with open(file=file_name, encoding='utf-8', mode='r') as file:
            lines = file.readlines()

        for line in lines:
            points.append([])
            space_index = line.find(' ')

            points[count].append(float(line[:space_index]))
            points[count].append(float(line[space_index+1:]))

            count += 1

        self.path_points = points

    # Формирование команд для робота
    def forming_commands_for_bot(self):
        commands = []
        for i in range(len(self.path_points)-1):
            commands.append([])

            if self.path_points[i+1][0] > self.path_points[i][0]:
                command = {
                    "cmd": "right",
                    "val": abs(self.path_points[i+1][0] - self.path_points[i][0])
                }
                commands[i].append(command)
            if self.path_points[i+1][0] < self.path_points[i][0]:
                command = {
                    "cmd": "left",
                    "val": abs(self.path_points[i+1][0] - self.path_points[i][0])
                }
                commands[i].append(command)
            if self.path_points[i+1][1] < self.path_points[i][1]:
                command = {
                    "cmd": "back",
                    "val": abs(self.path_points[i+1][1] - self.path_points[i][1])
                }
                commands[i].append(command)
            if self.path_points[i+1][1] > self.path_points[i][1]:
                command = {
                    "cmd": "forward",
                    "val": abs(self.path_points[i+1][1] - self.path_points[i][1])
                }
                commands[i].append(command)

        return commands

    # Вычисление расстояния, которое робот пройдет
    def distance_calculation(self, points):
        for i in range(len(points) - 1):
            self.distances.append(((points[i + 1][0] - points[i][0]) ** 2 + (points[i + 1][1] - points[i][1]) ** 2) ** 0.5)

    # Вычисление времени движения, исходя из того, что
    # движение равномерное и прямолинейное
    def counting_drive_time(self):
        for i in range(len(self.distances)):
            self.driving_time.append(abs(self.distances[i] / self.bot_velocity))

    # Вычисление координат векторов движения робота
    # Первые координаты x и y - это координаты единичного
    # вектора направленности робота, т.е. в какой бы
    # точке не находился изначально робот его начальный
    # (единичный) вектор будет направлен по вертикали
    # вверх по оси y
    def movement_vectors(self):
        vectors = []
        counter = 0
        buff = [[self.path_points[counter][0], self.path_points[counter][1]-1]]

        for i in range(len(self.path_points)):

            buff.append(self.path_points[counter])
            counter += 1

        for i in range(len(buff)-1):
            vectors.append([buff[i+1][0]-buff[i][0], buff[i+1][1]-buff[i][1]])

        return vectors

    # Вычисление углов поворота на следующую точку в
    # промежуточной точке маршрута
    def angle_calculations(self, vec):
        sign = self.on_which_side_is_the_dot()

        for i in range(len(vec)-1):
            up = vec[i][0] * vec[i+1][0] + vec[i][1] * vec[i+1][1]
            down = ((vec[i][0] ** 2 + vec[i][1] ** 2) ** 0.5) * ((vec[i+1][0] ** 2 + vec[i+1][1] ** 2) ** 0.5)
            if sign[i] < 0:
                alpha = -(math.acos(up / down) * (180 / math.pi))
            else:
                alpha = math.acos(up / down) * (180 / math.pi)

            self.angles.append(alpha)

    # Определение ориентации следующей промежуточной
    # точки относительно текущего вектора, т.е.
    # точка расположена слева или справа относительно
    # вектора
    def on_which_side_is_the_dot(self):
        signs = []
        p = [[self.path_points[0][0], self.path_points[0][1]-1]]
        for i in range(len(self.path_points)):
            p.append(self.path_points[i])

        for i in range(len(p)-2):
            j = i+2
            signs.append((p[j][0]-p[i][0])*(p[i+1][1]-p[i][1])-(p[j][1]-p[i][1])*(p[i+1][0]-p[i][0]))

        return signs

    # Вычисление времени поворота, исходя из того, что поворот
    # строго на месте и с одной угловой скоростью
    def counting_angular_rotation_time(self):
        for i in range(len(self.angles)):
            self.angular_rotation_time.append(abs(self.angles[i] / self.bot_angular_velocity))

    # Остановка программы на некоторое время
    def bot_sleeping(self, time_param):
        time.sleep(time_param)

    # Публикация комманд по протоколу mqtt
    def publish_message(self):
        client_name = "###Publisher###"
        client = mqtt.Client(client_name)
        client.connect(self.brocker_ip, port=self.port_number)
        commands = self.forming_commands_for_bot()

        str_out = ''

        str_out += "\n{'cmd': 'start'}\n"
        client.publish(self.topic_name, str_out)
        str_out = ''

        for i in range(len(self.driving_time)):
            str_out += f'{i+1}-й участок:\n============================================================='
            str_out += f'\n{commands[i][0]}, {commands[i][1]} \n\nРобот поворачивается...\n'
            client.publish(self.topic_name, str_out)
            str_out = ''

            self.bot_sleeping(self.angular_rotation_time[i])

            str_out += f'Поворот на {self.angles[i]} град\n'+ f'Затрачено {self.angular_rotation_time[i]} сек\n'
            str_out += '\nРобот движется прямолинейно...\n'
            client.publish(self.topic_name, str_out)
            str_out = ''

            self.bot_sleeping(self.driving_time[i])
            str_out += f'Пройдено {self.distances[i]} м\n' + f'Затрачено {self.driving_time[i]} сек\n'
            str_out += '=============================================================\n'
            client.publish(self.topic_name, str_out)
            str_out = ''

        str_out = "{'cmd': 'stop'}"
        client.publish(self.topic_name, str_out)

    # Формирование файла с broker_ip, port и topic
    def make_file_data_for_sub(self):
        file = open('data_for_sub_connection.txt', encoding="utf-8",mode='w')

        file.write(self.brocker_ip + '\n')
        file.write(str(self.port_number) + '\n')
        file.write(self.topic_name)

        file.close()

    # pub_cmd.py mqtt.eclipseprojects.io 1883 abotcmd1 1.0 30.0 C:\Users\KARLEN\PycharmProjects\DPP_PROJECT\practice1\path.txt

if __name__ == '__main__':
    app = App()
    app.command_recognition(app.read_start_commands_from_cmd())
    app.reading_file_with_coordinates(app.file_name)
    app.distance_calculation(app.path_points)
    app.counting_drive_time()
    app.angle_calculations(app.movement_vectors())
    app.counting_angular_rotation_time()
    app.make_file_data_for_sub()
    app.publish_message()
