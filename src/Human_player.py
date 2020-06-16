class HumanPlayer:
    """
    人类玩家
    """

    def __init__(self, color):
        """
        玩家初始化\n",
        :param color: 下棋方，'X' - 黑棋，'O' - 白棋\n",
        """
        self.color = color


    def get_move(self, board):
        """
        根据当前棋盘输入人类合法落子位置
        :param board: 棋盘
        :return: 人类下棋落子位置
        """
        # 如果 self.color 是黑棋 "X",则 player 是 "黑棋"，否则是 "白棋"
        if self.color == "X":
            player="黑棋"
        else:
            player="白棋"

        # 人类玩家输入落子位置，如果输入 'Q', 则返回 'Q'并结束比赛。
        # 如果人类玩家输入棋盘位置，e.g. 'A1'，
        # 首先判断输入是否正确，然后再判断是否符合黑白棋规则的落子位置

        while True:
            action=input("请'{}-{}'方输入一个合法的坐标(e.g. 'D3'，若不想进行，请务必输入'Q'结束游戏。):".format(player,self.color))

            # 如果人类玩家输入 Q 则表示想结束比赛
            if action=="Q" or action=="q":
                return "Q"
            else:
                row, col = action[1].upper(), action[0].upper()

                # 检查人类输入是否正确
                if row in '12345678' and col in 'ABCDEFGH':
                    # 检查人类输入是否为符合规则的可落子位置
                    if action in board.get_legal_actions(self.color):
                        return action
                else:
                    print("你的输入不合法，请重新输入!")

#if __name__ == '__main__':
#    from board import Board

#    # 棋盘初始化
#    board = Board()

#    # 打印初始化后棋盘
#    board.display()
    
#    # 人类玩家黑棋初始化
#    black_player = HumanPlayer("X")

#    # 人类玩家黑棋落子位置
#    action = black_player.get_move(board)


#    # 如果人类玩家输入 'Q',则表示想结束比赛，
#    # 现在只展示人类玩家的输入结果。
#    if action=="Q":
#        print("结束游戏:",action)
#    else:
#        # 打印白方被翻转的棋子位置
#        print("黑棋落子后反转白棋的棋子坐标：",board._move(action,black_player.color))

#        # 打印人类玩家黑棋落子后的棋盘
#        board.display()
