#导入随机包
import random

class RandomPlayer:
    """
    随机玩家, 随机返回一个合法落子位置
    """

    def __init__(self, color):
        """
        玩家初始化
        :param color: 下棋方，'X' - 黑棋，'O' - 白棋
        """
        self.color = color


    def random_choice(self, board):
        """
        从合法落子位置中随机选一个落子位置
        :param board: 棋盘
        :return: 随机合法落子位置, e.g. 'A1' 
        """
        # 用 list() 方法获取所有合法落子位置坐标列表
        action_list = list(board.get_legal_actions(self.color))

        # 如果 action_list 为空，则返回 None,否则从中选取一个随机元素，即合法的落子坐标
        if len(action_list) == 0:
            return None
        else:
            return random.choice(action_list)

    def get_move(self, board):
        """
        根据当前棋盘状态获取最佳落子位置
        :param board: 棋盘
        :return: action 最佳落子位置, e.g. 'A1'
        """
        if self.color == 'X':
            player_name = '黑棋'
        else:
            player_name = '白棋'
        print("请等一会，对方 {}-{} 正在思考中...".format(player_name, self.color))
        action = self.random_choice(board)
        return action

#if __name__ == '__main__':
#    # 导入棋盘文件
#    from board import Board

#    # 棋盘初始化
#    board = Board()

#    # 打印初始化棋盘
#    board.display()

#    # 玩家初始化，输入黑棋玩家
#    black_player = RandomPlayer("X")

#    # 黑棋玩家的随机落子位置
#    black_action = black_player.get_move(board)


#    print("黑棋玩家落子位置: %s"%(black_action))

#    # 打印白方被翻转的棋子位置
#    print("黑棋落子后反转白棋的棋子坐标：",board._move(black_action,black_player.color))

#    # 打印黑棋随机落子后的棋盘
#    board.display()

#    # 玩家初始化，输入白棋玩家
#    white_player = RandomPlayer("O")

#    # 白棋玩家的随机落子位置
#    white_action = white_player.get_move(board)

#    print("白棋玩家落子位置:%s"%(white_action))

#    # 打印黑棋方被翻转的棋子位置
#    print("白棋落子后反转黑棋的棋子坐标：",board._move(white_action,white_player.color))

#    # 打印白棋随机落子后的棋盘
#    board.display()

