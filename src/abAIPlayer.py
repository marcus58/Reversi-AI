import time
import random
class abAIPlayer:
    """
    AI 玩家
    """

    def __init__(self, color):
        """
        玩家初始化
        :param color: 下棋方，'X' - 黑棋，'O' - 白棋
        """
        self.color=color
        self.calculation_time = float(45)
        

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

        # -----------------请实现你的算法代码--------------------------------------

        begin = time.time()
        action = None
               
        op_color=['X','O'][self.color=='X']
        best_val = -1000
        my_moves = []
        sensible_move=list(board.get_legal_actions(self.color))
        if len(sensible_move)==1:
            return sensible_move[0]

        for move in sensible_move:
            flip_positions=board._move(move,self.color)
            val = self.alpha_beta(board, op_color, self.color, -1000, 1000, begin)
            board.backpropagation(move, flip_positions, self.color)
            if val > best_val:
                best_val = val
                my_moves=[move]
            elif val == best_val:
                my_moves.append(move)

        action=random.choice(my_moves)
        # ------------------------------------------------------------------------

        return action

    def alpha_beta(self, board, color, op_color, alphav, betav, begin):
        """
        通过alpha-beta剪枝搜索获取估值

        Args:
            board: 游戏状态
            color: 当前玩家
            op_color: 对手玩家
            alphav: alpha初始值
            betav: beta初始值
            begin:开始时间
        Return:
            当前棋盘状态的估值
            对于叶节点：
            -- Max方获胜，则估值为diff
            -- Min方获胜，则估值为-diff
            -- 平局，则估值为0
        """
        #先根据当前棋盘state判断是否已经结束，结果如何，并根据结果赋予估值
        
        b_list = list(board.get_legal_actions('X'))
        w_list = list(board.get_legal_actions('O'))
        is_over = len(b_list) == 0 and len(w_list) == 0
        if is_over:
            winner, diff = board.get_winner()

            if winner==2:
                return 0
            if (winner==0 and self.color=='X') or (winner==1 and self.color=='O'):
                return diff
            else:
                return -diff

        #若还没有结束，则开始递归搜索
        for move in list(board.get_legal_actions(color)):
            if time.time()-begin>self.calculation_time:
                break
            flip_positions=board._move(move, color)
            val=self.alpha_beta(board, op_color, color, alphav, betav, begin)
            board.backpropagation(move, flip_positions, color)

            #跟极大极小搜索同理，但是在α值大于β值时返回（即剪枝）
            #若当前计算己方（α方）落子情况，则计算α值
            if color==self.color:
                if val>alphav:
                    alphav=val  
                if alphav>=betav:
                    return betav
            #否则计算β值
            else:
                if val<betav:
                    betav=val
                if betav<=alphav:
                    return alphav

        #计算己方落子（α方），返回极大值   
        if color==self.color:
            return alphav
        #否则返回极小值（β方）
        else:
            return betav

    


#if __name__ == '__main__':
#    # 导入黑白棋文件
#    from game import Game
#    from Human_player import HumanPlayer

#    # 人类玩家黑棋初始化
#    black_player = HumanPlayer("X")

#    # AI 玩家 白棋初始化
#    white_player = AIPlayer("O")

#    # 游戏初始化，第一个玩家是黑棋，第二个玩家是白棋
#    game = Game(black_player, white_player)

#    # 开始下棋
#    game.run()
