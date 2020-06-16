import time
import copy
from multiprocessing.dummy import Pool as ThreadPool
from random import choice, shuffle
from math import log, sqrt, fabs

class AlphagoPlayer:
    """
    AI 玩家
    """

    def __init__(self, color):
        """
        玩家初始化
        :param color: 下棋方，'X' - 黑棋，'O' - 白棋
        """
        self.color=color
        self.root=None
        self.start_time=None
        self.calculation_time = float(58)
        self.max_actions=60
        self.equivalence = 1000
        self.moves=[4,5][self.color=='O']
        self.Cp = 1.414
        self.priority_table=[['A0', 'A8', 'H1', 'H8'],
                            ['C3', 'D3', 'E3', 'F3', 'C4', 'D4', 'E4', 'F4', 'C5', 'D5', 'E5', 'F5', 'C6', 'D6', 'E6', 'F6'],
                            ['A3', 'A4', 'A5', 'A6', 'H3', 'H4', 'H5', 'H6', 'C1', 'D1', 'H1', 'F1', 'C8', 'D8', 'H8', 'F8'],
                            ['B3', 'B4', 'B5', 'B6', 'G3', 'G4', 'G5', 'G6', 'C2', 'D2', 'G2', 'F2', 'C7', 'D7', 'G7', 'F7'],
                            ['B1', 'A2', 'B2', 'G2', 'G1', 'H2', 'B7', 'A7', 'B8', 'G7', 'H7', 'G8']]

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

        action = None
        
        sensible_move=list(board.get_legal_actions(self.color))
        if len(sensible_move)==1:
            return sensible_move[0]
        self.root=Node(self.color, board)
        action=self.uct_search()
        self.moves+=2
        # ------------------------------------------------------------------------

        return action
    
    def uct_search(self):
        self.start_time=time.time()        
        simulation_count=self.multi_simulation(self.root)
        print("silulations=",simulation_count)
        max_win_percent, chosen_child = self.best_child(self.root, 0)
        print("max win percentage is", max_win_percent)
        return chosen_child.pre_move

    def multi_simulation(self, node):
        count=0
        while time.time()-self.start_time<self.calculation_time:
            v = self.tree_policy(node)
            reward = self.default_policy(v)
            self.back_up(v, reward)
            count += 1
            if node.fully_expandable():
                break

        if len(node.children)==0:
            return count
        pool=ThreadPool(len(node.children))
        counts=pool.map(self.simulation, node.children)
        pool.close()
        pool.join()
        count+=sum(counts)
        return count

    def simulation(self, node):
        count=0
        while time.time()-self.start_time<self.calculation_time:
            v = self.tree_policy(node)
            reward = self.default_policy(v)
            self.back_up(v, reward)
            count += 1
        return count


    def best_child(self, node, c):
        child_value = [1 - child.Q / child.N + c*sqrt(log(node.N) / child.N) for child in node.children]
        value = max(child_value)
        idx = child_value.index(value)
        return value, node.children[idx]

    def tree_policy(self, node):
        while not node.terminal():
            if node.fully_expandable():
                value, node = self.best_child(node, self.Cp)
            else:
                return self.expand(node)
        return node

    def expand(self, node):
        chosen_move = choice(node.remain_valid_moves)
        node.add_child(chosen_move)
        return node.children[-1]

    def default_policy(self, node):
        cur_color=node.color
        board=copy.deepcopy(node.board)

        num_moves=0
        while self.moves+num_moves<64:
            if self.moves+num_moves<56:
                valid_set=self.get_priority_valid_moves(board, self.priority_table, cur_color)
                if len(valid_set) == 0:
                    num_moves += 1
                    cur_color = ['X','O'][cur_color=='X']
                    continue
                move = choice(valid_set)
            else:
                valid_set=list(board.get_legal_actions(cur_color))
                if len(valid_set) == 0:
                    num_moves += 1
                    cur_color = ['X','O'][cur_color=='X']
                    continue
                move = choice(valid_set)
            board._move(move, cur_color)
            cur_color = ['X','O'][cur_color=='X']
            num_moves += 1
        return self.score(board, self.color)

    def get_priority_valid_moves(self, board, priority_table, color):
        valid_moves=[]
        availables=list(board.get_legal_actions(color))
        for priority in priority_table:
            for point in priority:
                if point in availables:
                    valid_moves.append(point)
            if len(valid_moves)>0:
                break
        return valid_moves

    def score(self, board, color):
        score=0
        op_color=['X','O'][color=='X']
        for i in range(8):
            for j in range(8):
                if board._board[i][j] == color:
                    score += 1
                if board._board[i][j] == op_color:
                    score -= 1
        return score

    def back_up(self, node, reward):
        while node is not None:
            node.N += 128
            if node.color == self.color:
                node.Q += 64 + reward
            else:
                node.Q += 64 - reward
            node = node.parent

class Node(object):
    def __init__(self, color, board, parent=None, pre_move=None):
        self.color = color
        self.board=board
        self.parent = parent
        self.children=[]
        self.pre_move = pre_move
        self.remain_valid_moves=list(self.board.get_legal_actions(self.color))
        self.N = 0
        self.Q = 0

    def add_child(self, choose_move):
        self.remain_valid_moves.remove(choose_move)
        board=copy.deepcopy(self.board)
        board._move(choose_move, self.color)
        child=Node(['X','O'][self.color=='X'], board, self, choose_move)
        self.children.append(child)

    def fully_expandable(self):
        return len(self.remain_valid_moves) == 0

    def terminal(self):
        return len(self.remain_valid_moves) == 0 and len(self.children) == 0
    