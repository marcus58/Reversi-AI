import time
import copy
from random import choice, shuffle
from math import log, sqrt

class AIPlayer:
    """
    AI 玩家
    """

    def __init__(self, color):
        """
        玩家初始化
        :param color: 下棋方，'X' - 黑棋，'O' - 白棋
        """
        self.color=color
        self.plays = {} # 记录着法参与模拟的次数，键形如(color, move)，即（玩家，落子）
        self.wins = {} # 记录着法获胜的次数
        self.plays_rave={}
        self.wins_rave={}
        self.calculation_time = float(30)
        self.max_actions=100
        self.equivalence = 1000
        self.confident = 1.96

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
        simulations=0
        begin = time.time()
        while time.time() - begin < self.calculation_time:
            board_copy=copy.deepcopy(board)
            color_copy=copy.deepcopy(self.color)
            self.run_simulation(board_copy, color_copy)           
            simulations+=1

        print("total simulations=", simulations)
        action=self.select_best_move(board)

        self.prune(board)
        # ------------------------------------------------------------------------

        return action

    def run_simulation(self, board, color):
        plays=self.plays
        wins=self.wins
        plays_rave=self.plays_rave
        wins_rave=self.wins_rave
        availables=list(board.get_legal_actions(color))

        player = [1,2][color=='O']        
        visited_states=set()
        winner=-1
        expand=True
        states_list = []
        # Simulation
        for t in range(1, self.max_actions + 1):
            # Selection
            # if all moves have statistics info, choose one that have max UCB value
            state=self.current_state(board)
            actions=[(move, player) for move in availables]
            if all(plays.get((action, state)) for action in actions):
                total=0
                for a, s in plays:
                    if s==state:
                        total+=plays.get((a,s))
                beta = sqrt(self.equivalence/(3 * total + self.equivalence))

                value, action = max(
                    ((1 - beta) * (wins[(action, state)] / plays[(action, state)]) +
                     beta * (wins_rave[(action[0], state)][player] / plays_rave[(action[0], state)]) + 
                     sqrt(self.confident * log(total) / plays[(action, state)]), action)
                    for action in actions)   # UCT RAVE

            else:
                action = choice(actions)

            move, p=action
            board._move(move, color)
            color=['X','O'][color=='X']

            # Expand
            # add only one new child node each time
            if expand and (action, state) not in plays:
                expand = False
                plays[(action, state)] = 0 # action是(move,player)。在棋盘状态s下，玩家player给出着法move的模拟次数
                wins[(action, state)] = 0  # 在棋盘状态s下，玩家player给出着法move并胜利的次数

            states_list.append((action, state)) # 当前模拟的路径

            # 路径上新增加的节点是前面所有节点的子节点，存在于前面各个节点的子树中
            for (m, pp), s in states_list:
                if (move, s) not in plays_rave:
                    plays_rave[(move, s)] = 0 # 棋盘状态s下的着法move的模拟次数，不论是由谁在何时给出的
                    wins_rave[(move, s)] = {}  # 棋盘状态s下着法move中记录着所有玩家在该着法move出现的时候的胜利次数，不论是由谁在何时给出的            
                    
                    wins_rave[(move, s)][1] = 0
                    wins_rave[(move, s)][2] = 0

            visited_states.add((action, state))

            b_list = list(board.get_legal_actions('X'))
            w_list = list(board.get_legal_actions('O'))
            is_over = len(b_list) == 0 and len(w_list) == 0
            if is_over:
                winner, diff=board.get_winner()
                winner+=1 #winner==1 'X' wins, winner==2 'O' wins
                break            

            player = [1,2][color=='O']

        # Back-propagation
        for i, ((m_root, p), s_root) in enumerate(states_list):
            action = (m_root, p)
            if (action, s_root) in plays:
                plays[(action, s_root)] += 1 # all visited moves
                if player == winner and player in action:
                    wins[(action, s_root)] += 1 # only winner's moves

            for ((m_sub, p), s_sub) in states_list[i:]:
                plays_rave[(m_sub, s_root)] += 1 # 状态s_root的所有子节点的模拟次数增加1 
                if winner in wins_rave[(m_sub, s_root)]:                
                    wins_rave[(m_sub, s_root)][winner] += 1 # 在状态s_root的所有子节点中，将获胜的玩家的胜利次数增加1


    def current_state(self, board):
        state=[]
        for i in range(8):
            for j in range(8):
                if board._board[i][j]=='X':
                    state.append((i*8+j,1))
                if board._board[i][j]=='O':
                    state.append((i*8+j,2))
        return tuple(state)


    def select_best_move(self, board):
        """
        select by win percentage
        """
        player = [1,2][self.color=='O']
        board_state=self.current_state(board)
        availables=list(board.get_legal_actions(self.color))

        percent_wins, move = max(
            (self.wins.get(((move, player), board_state), 0) /
                    self.plays.get(((move, player), board_state), 1),
             move)
            for move in availables)

        for x in sorted(
                ((100 * self.wins.get(((move, player), board_state), 0) /
                        self.plays.get(((move, player), board_state), 1),
                  100 * self.wins_rave.get((move, board_state), {}).get(player, 0) /
                        self.plays_rave.get((move, board_state), 1),
                  self.wins.get(((move, player), board_state), 0),
                  self.plays.get(((move, player), board_state), 1),
                  self.wins_rave.get((move, board_state), {}).get(player, 0),
                  self.plays_rave.get((move, board_state), 1), 
                  move)
                 for move in availables),
                reverse=True):
            print('{6}: {0:.2f}%--{1:.2f}% ({2} / {3})--({4} / {5})'.format(*x))

        return move

    def prune(self, board):
        count=len(self.current_state(board))
        keys=list(self.plays)
        for a, s in keys:           
            if len(s) < count + 2:
                del self.plays[(a, s)]
                del self.wins[(a, s)]

        keys = list(self.plays_rave)
        for m, s in keys:
            if len(s) < count + 2:
                del self.plays_rave[(m, s)]
                del self.wins_rave[(m, s)]
