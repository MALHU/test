from file_reader import *

all_actions = np.array(list(cst.Action))
all_positions = np.array(list(Position))
all_streets = np.array(list(cst.Street))
all_cards = np.array(list(Card))


class HandConverter:

    def __init__(self):
        self.streets = ["pf", "flop", "turn", "river"]
        self.labels = ["seat", "move", "value"]
        self.txt_label = "move"
        self.val_labels = ["seat", "value"]
        self.ext_cols = [f"{s}_action_{k}_{label}" for s in self.streets for k in range(24) for label in self.labels]
        self.hero_cols = [f"p{i}_hero" for i in range(9)]
        self.combo_cols = [f"p{i}_combo" for i in range(9)]
        self.stack_cols = [f"p{i}_stack" for i in range(9)]
        self.street_val_cols = [f"{s}_action_{k}_value" for s in self.streets for k in range(24)]
        self.val_cols = np.hstack((["bb", "ante", "buyin"], self.stack_cols, self.street_val_cols))
        self.df = None
        self.current_df = None
        self.droppable_info = np.hstack((self.combo_cols, ["hand_id", "tournament_id", "table_id"]))
        self.none_count = 0
        self.parser = FileParser()

    @staticmethod
    def filter(hands):
        return np.array([hand for hand in hands if hand is not None])

    def to_pandas(self, hands: np.ndarray):
        self.df = pd.DataFrame({"hand": hands})
        return self.df

    @staticmethod
    def get_hand_info(hand: HandHistory):
        return {"tour_id": hand.tournament.id, "table_id": hand.table.ident, "level": hand.level.level,
                "bb": hand.level.bb, "ante": hand.level.ante, "max_pl": hand.table.max_players, "btn": hand.button,
                "buyin": hand.tournament.buyin}

    def get_hand_id(self, hand: HandHistory):
        try:
            return f"{hand.hand_id}"
        except AttributeError:
            phr = f" None{self.none_count}"
            self.none_count += 1
            return phr

    def convert_hand_id(self):
        vfunc = np.vectorize(self.get_hand_id)
        self.df["hand_id"] = vfunc(self.df["hand"])

    @staticmethod
    def get_table_id(hand: HandHistory):
        return hand.table.ident

    def convert_table_id(self):
        vfunc = np.vectorize(self.get_table_id)
        self.df["table_id"] = vfunc(self.df["hand"])

    @staticmethod
    def get_tournament_id(hand: HandHistory):
        return hand.tournament.id

    def convert_tournament_id(self):
        vfunc = np.vectorize(self.get_tournament_id)
        self.df["tour_id"] = vfunc(self.df["hand"])

    @staticmethod
    def get_level(hand: HandHistory):
        return hand.level.level

    def convert_level(self):
        vfunc = np.vectorize(self.get_level)
        self.df["level"] = vfunc(self.df["hand"])

    @staticmethod
    def get_bb(hand: HandHistory):
        return hand.level.bb

    def convert_bb(self):
        vfunc = np.vectorize(self.get_bb)
        self.df["bb"] = vfunc(self.df["hand"])

    @staticmethod
    def get_ante(hand: HandHistory):
        return hand.level.ante

    def convert_ante(self):
        vfunc = np.vectorize(self.get_ante)
        self.df["ante"] = vfunc(self.df["hand"])

    @staticmethod
    def get_hero(hand: HandHistory):
        try:
            return hand.table.hero
        except TypeError:
            print(hand.table)

    def get_hero_combo(self, hand: HandHistory):
        try:
            hero = self.get_hero(hand)
            return hero.combo
        except AttributeError:
            return None
        except TypeError:
            return None

    def convert_hero_combo(self):
        vfunc = np.vectorize(self.get_hero_combo)
        self.df["hero_combo"] = vfunc(self.df["hand"])

    def get_hero_seat(self, hand: HandHistory):
        try:
            hero = self.get_hero(hand)
            return hero.seat
        except AttributeError:
            return 0

    def convert_hero_seat(self):
        vfunc = np.vectorize(self.get_hero_seat)
        self.df["hero_seat"] = vfunc(self.df["hand"])

    @staticmethod
    def get_max_pl(hand: HandHistory):
        return hand.table.max_players

    def convert_max_pl(self):
        vfunc = np.vectorize(self.get_max_pl)
        self.df["max_pl"] = vfunc(self.df["hand"])

    @staticmethod
    def get_btn(hand: HandHistory):
        return hand.button

    def convert_btn(self):
        vfunc = np.vectorize(self.get_btn)
        self.df["btn"] = vfunc(self.df["hand"])

    @staticmethod
    def get_buyin(hand: HandHistory):
        return hand.tournament.buyin

    def convert_buyin(self):
        vfunc = np.vectorize(self.get_buyin)
        self.df["buyin"] = vfunc(self.df["hand"])

    def convert_hand_info(self):
        self.convert_hand_id()
        self.convert_tournament_id()
        self.convert_table_id()
        self.convert_level()
        self.convert_bb()
        self.convert_ante()
        self.convert_max_pl()
        self.convert_btn()
        self.convert_buyin()
        self.convert_hero_combo()
        self.convert_hero_seat()

    @staticmethod
    def get_card(hand: HandHistory, index: int):
        try:
            return str(hand.table.board[index])
        except IndexError:
            return str(None)

    def convert_board(self):
        vfunc = np.vectorize(self.get_card)
        self.df["Card_0"] = vfunc(self.df["hand"], 0)
        self.df["Card_1"] = vfunc(self.df["hand"], 1)
        self.df["Card_2"] = vfunc(self.df["hand"], 2)
        self.df["Card_3"] = vfunc(self.df["hand"], 3)
        self.df["Card_4"] = vfunc(self.df["hand"], 4)

    @staticmethod
    def get_player(hand: HandHistory, index: int):
        try:
            return hand.table.players.pl_list[index]
        except IndexError:
            return None

    def get_player_name(self, hand: HandHistory, index: int):
        try:
            player = self.get_player(hand, index)
            return player.name
        except AttributeError:
            return None

    def convert_player_name(self, index: int):
        vfunc = np.vectorize(self.get_player_name)
        self.df[f"P{index}_name"] = vfunc(self.df["hand"], index)

    def get_player_seat(self, hand: HandHistory, index: int):
        try:
            player = self.get_player(hand, index)
            return player.seat
        except AttributeError:
            return 0

    def convert_player_seat(self, index: int):
        vfunc = np.vectorize(self.get_player_seat)
        self.df[f"P{index}_seat"] = vfunc(self.df["hand"], index)

    @staticmethod
    def get_player_stack(self, hand: HandHistory, index: int):
        try:
            player = self.get_player(hand, index)
            return player.stack
        except AttributeError:
            return 0

    def convert_player_stack(self, index: int):
        vfunc = np.vectorize(self.get_player_name)
        self.df[f"P{index}_stack"] = vfunc(self.df["hand"], index)

    def get_player_position(self, hand: HandHistory, index: int):
        try:
            player = self.get_player(hand, index)
            return player.position
        except AttributeError:
            return None

    def convert_player_position(self, index: int):
        vfunc = np.vectorize(self.get_player_position)
        self.df[f"P{index}_position"] = vfunc(self.df["hand"], index)

    def get_player_combo(self, hand: HandHistory, index: int):
        try:
            player = self.get_player(hand, index)
            return player.combo
        except AttributeError:
            return None

    def convert_player_combo(self, index: int):
        vfunc = self.get_player_combo
        self.df[f"P{index}_combo"] = vfunc(self.df["hand"], index)

    def convert_player(self, index: int):
        self.convert_player_name(index)
        self.convert_player_stack(index)
        self.convert_player_seat(index)
        self.convert_player_position(index)
        self.convert_player_combo(index)

    def convert_players(self):
        for i in range(9):
            self.convert_player(i)


    def get_action(self, hand, street_index: int, action_index: int):
        try:
            street = self.get_street(hand=hand, index=street_index)
            return street.actions[action_index]
        except IndexError:
            return None
        except AttributeError:
            return None

    def get_action_seat(self, hand, street_index: int, action_index: int):
        try:
            action = self.get_action(hand, street_index=street_index, action_index=action_index)
            return action.player.seat
        except AttributeError:
            return 0

    def convert_action_seat(self, street_index: int, action_index: int):
        tab = ["pf", "flop", "turn", "river"]
        vfunc = np.vectorize(self.get_action_seat)
        self.df[f"{tab[street_index]}_action_{action_index}_seat"] = vfunc(self.df["hand"], street_index, action_index)

    def get_action_move(self, hand, street_index: int, action_index: int):
        try:
            action = self.get_action(hand, street_index=street_index, action_index=action_index)
            return action.move
        except AttributeError:
            return None

    def convert_action_move(self, street_index: int, action_index: int):
        tab = ["pf", "flop", "turn", "river"]
        vfunc = np.vectorize(self.get_action_move)
        self.df[f"{tab[street_index]}_action_{action_index}_move"] = vfunc(self.df["hand"], street_index, action_index)

    def get_action_value(self, hand, street_index: int, action_index: int):
        try:
            action = self.get_action(hand, street_index=street_index, action_index=action_index)
            return action.value
        except AttributeError:
            return 0

    def convert_action_value(self, street_index: int, action_index: int):
        tab = ["pf", "flop", "turn", "river"]
        vfunc = np.vectorize(self.get_action_value)
        self.df[f"{tab[street_index]}_action_{action_index}_value"] = vfunc(self.df["hand"], street_index, action_index)

    def convert_action(self, street_index: int, action_index: int):
        self.convert_action_seat(street_index, action_index)
        self.convert_action_move(street_index, action_index)
        self.convert_action_value(street_index, action_index)

    def convert_street_actions(self, street_index: int):
        for i in range(24):
            self.convert_action(street_index=street_index, action_index=i)

    def convert_hand_actions(self):
        for i in range(4):
            self.convert_street_actions(street_index=i)

    @staticmethod
    def get_street(hand: HandHistory, index: int):
        try:
            return hand.table.streets[index]
        except IndexError:
            return None

    def convert_hand(self):
        self.convert_hand_info()
        self.convert_players()
        self.convert_board()
        self.convert_hand_actions()


#    def convert_hand_actions(self, hands):
#        timer = Timer()
#        timer.start()
#        idents = [hand.ident for hand in hands]
#        streets = ["pf", "flop", "turn", "river"]
#        labels = ["seat", "move", "value"]
#        act_columns = (np.array(["%s_action_%s_%s" % (s, j, l) for s in streets for j in range(24) for l in labels]))
#        actions = np.vstack([hand.table.get_table_action_info() for hand in hands])
#        act_frame = pd.DataFrame(data=actions, index=idents, columns=act_columns)
#        timer.stop()
#        return act_frame

    def complete_convert(self, hands):
        streets = ["pf", "flop", "turn", "river"]
        labels = ["seat", "move", "value"]
        act_columns = (np.array(["%s_action_%s_%s" % (s, j, l) for s in streets for j in range(24) for l in labels]))
        actions = np.vstack([hand.get_consecutive_actions()[0] for hand in hands])
        board = np.vstack([hand.get_consecutive_actions()[2] for hand in hands])
        idents = np.hstack([hand.get_consecutive_actions()[3] for hand in hands])
        infos = np.vstack([hand.get_consecutive_actions()[4] for hand in hands])
        pl_info = np.vstack([hand.get_consecutive_actions()[5] for hand in hands])
        act_frame = pd.DataFrame(data=actions, index=idents, columns=act_columns)
        bd_columns = ["Card_0", "Card_1", "Card_2", "Card_3", "Card_4", ]
        bd_frame = pd.DataFrame(data=board, index=idents, columns=bd_columns)
        hi_columns = ["tournament_id", "table_id", "level", "bb", "ante", "max_pl", "btn", "buyin"]
        hi_frame = pd.DataFrame(data=infos, columns=hi_columns, index=idents)
        pl_labels = ["name", "seat", "stack", "position", "combo", "hero"]
        pl_columns = np.array(["p%s_%s" % (i, l) for i in range(9) for l in pl_labels])
        pl_frame = pd.DataFrame(data=pl_info, columns=pl_columns, index=idents)
        # print(bd_frame, act_frame, hi_frame, pl_frame)
        df = pd.concat([hi_frame, pl_frame, act_frame, bd_frame], axis=1).reset_index().rename(columns={"index":"hand_id"})
        self.current_df = df
        return df

    def convert_hands(self, hands):
        pl_frame = self.convert_players_info(hands)
        hi_frame = self.convert_hands_info(hands)
        act_frame = self.convert_hand_actions(hands)
        bd_frame = self.convert_board(hands)
        df = pd.concat([hi_frame, pl_frame, act_frame, bd_frame], axis=1).reset_index().rename(columns={"index":"hand_id"})
        self.current_df = df
        return df

    def convert_single_hand(self, hand: HandHistory):
        return self.convert_hands([hand])

    @staticmethod
    def get_idents(hands):
        return pd.Index([hand.hand_id for hand in hands])


    def transform_to_guess(self, pl_index: int, line: int=0):
        seat = self.current_df[f"p{pl_index}_seat"].loc[line]
        combo = self.current_df[f"p{pl_index}_combo"].loc[line]
        hero_combo = self.get_hero_combo(line)
        # print(hero_combo, combo)
        infos = self.current_df.iloc[line, :].drop(self.droppable_info)
        indexes = np.hstack((infos.index.to_numpy(), ["seat", "hero_combo"]))
        inf = np.hstack((infos.to_numpy(), [seat, hero_combo])).reshape(1,indexes.shape[0])
        infos = pd.DataFrame(columns=indexes, data=inf)
        combo = pd.Series({"combo":combo})
        return combo, infos


    def extract_player_infos(self, line: int=0):
        try:
            combos = pd.concat([self.transform_to_guess(pl_index=pl_index, line=line)[0] for pl_index in range(9)
                if self.transform_to_guess(pl_index=pl_index, line=line)[0]["combo"] not in [None, "None"]
            ])
            infos = pd.concat([
                self.transform_to_guess(pl_index=pl_index, line=line)[1] for pl_index in range(9)
                if self.transform_to_guess(pl_index=pl_index, line=line)[0]["combo"] not in [None, "None"]
            ], axis=0)
            # print(combos.shape, infos.shape)
            return combos, infos
        except ValueError:
            return None, None

    def extract_all_info(self):
        n = self.current_df.shape[0]
        combos = pd.concat([self.extract_player_infos(line=line)[0] for line in range(n)])
        infos = pd.concat([self.extract_player_infos(line=line)[1] for line in range(n)], axis=0)
        return combos, infos


