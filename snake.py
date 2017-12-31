# Write By Sunwl
# 2017/10/22
#
# 贪吃蛇
# “#”为边界，“*”做食物，“O”做头部，“o”做身体；使用“w s a d”控制方向
# python 3.6.2
# 运行环境 Win
# 注意：在 Mac 环境下  不支持 msvcrt库

import random
import msvcrt
import copy
import os

'''采用MVC设计模式
	board：游戏区域类（蛇的活动范围）   		- 展示层
	snake：蛇类（通过身体每个点来记录蛇的状态） - 数据层
　　game： 游戏类（food 食物逻辑）            - 逻辑层
'''

# 游戏区域类_蛇的活动范围
class board:
    __points =[]

    def __init__(self):
    	# 初始化_游戏区域
        self.__points.clear()
        for i in range(22):
            line = []
            if i == 0 or i == 21:
                for j in range(22):
                    line.append('#')
            else:
                line.append('#')
                for j in range(20):
                    line.append(' ')
                line.append('#')
            self.__points.append(line)

    def getPoint(self, location):
    	# 初始化_蛇的位置
        return self.__points[location[0]][location[1]]

    def clear(self):
    	# 清空游戏区域
        self.__points.clear()
        for i in range(22):
            line = []
            if i == 0 or i == 21:
                for j in range(22):
                    line.append('#')
            else:
                line.append('#')
                for j in range(20):
                    line.append(' ')
                line.append('#')
            self.__points.append(line)

    def put_snake(self, snake_locations):
        self.clear() # 清空游戏区域
        # 初始化_蛇的身体
        for x in snake_locations:
            self.__points[x[0]][x[1]] = 'o'
        # 初始化_蛇头
        x = snake_locations[len(snake_locations) - 1]
        self.__points[x[0]][x[1]] = 'O'

    def put_food(self, food_location):
        self.__points[food_location[0]][food_location[1]] = '*'

    def show(self):
    	# 刷新游戏区域
        os.system("cls") # 终端清屏
        for i in range(22):
            for j in range(22):
                print(self.__points[i][j], end='')
            print()


# 蛇类_通过身体每个点来记录蛇的状态
class snake:
    __points = []

    def __init__(self):
    	# 初始化蛇类
        for i in range(1, 6):
            self.__points.append([1, i])

    def getPoints(self):
        return self.__points

    # 移动到下一个位置_刷新头部
    def move(self, next_head):
        self.__points.pop(0)
        self.__points.append(next_head)

    # 吃掉食物_刷新头部
    def eat(self, next_head):
        self.__points.append(next_head)

    # 计算下一个状态_并返回方向
    def next_head(self, direction='default'):
    	# 蛇头_新位置
        # 需要更改值，所以复制它
        head = copy.deepcopy(self.__points[len(self.__points) - 1])
        # 计算"默认" 的方向
        if direction == 'default':
            neck = self.__points[len(self.__points) - 2]
            if neck[0] > head[0]:
                direction = 'up'
            elif neck[0] < head[0]:
                direction = 'down'
            elif neck[1] > head[1]:
                direction = 'left'
            elif neck[1] < head[1]:
                direction = 'right'

        if direction == 'up':
            head[0] = head[0] - 1
        elif direction == 'down':
            head[0] = head[0] + 1
        elif direction == 'left':
            head[1] = head[1] - 1
        elif direction == 'right':
            head[1] = head[1] + 1
        return head


# 游戏类（food 食物逻辑）
class game:
    board = board()
    snake = snake()
    food = []
    count = 0

    def __init__(self):
    	# 初始化游戏类
        self.new_food()
        self.board.clear()
        self.board.put_snake(self.snake.getPoints())
        self.board.put_food(self.food)

    def new_food(self):
    	# 食物_随机出现新食物
        while 1:
            line = random.randint(1, 20)
            column = random.randint(1, 20)
            if self.board.getPoint([column, line]) == ' ':
                self.food = [column, line]
                return

    def show(self):
    	# 刷新
        self.board.clear()
        self.board.put_snake(self.snake.getPoints())
        self.board.put_food(self.food)
        self.board.show()

    def run(self):
    	# 运行游戏_主函数
        self.board.show()
        # 使用 “w s a d” 控制方向
        operation_dict = {b'w': 'up', b'W': 'up', b's': 'down', b'S': 'down', b'a': 'left', b'A': 'left', b'd': 'right', b'D': 'right'}
        op = msvcrt.getch() # 暂停

        while op != b'q':
            if op not in operation_dict:
                op = msvcrt.getch() # 暂停
            else:
                new_head = self.snake.next_head(operation_dict[op])
                # 得到食物
                if self.board.getPoint(new_head) == '*':
                    self.snake.eat(new_head)
                    self.count = self.count + 1
                    if self.count >= 15:
                        self.show()
                        print("Good Job")
                        break
                    else:
                        self.new_food()
                        self.show()
                # 反向倒退
                elif new_head == self.snake.getPoints()[len(self.snake.getPoints()) - 2]:
                    pass
                # 撞墙
                elif self.board.getPoint(new_head) == '#' or self.board.getPoint(new_head) == 'o':
                    print(' 游戏结束 ╮(╯﹏╰)╭')
                    break
                # 正常移动
                else:
                    self.snake.move(new_head)
                    self.show()
            op = msvcrt.getch() # 暂停

game().run()
