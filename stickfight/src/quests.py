
class QuestStatus:
    ACTIVE = "active"
    COMPLETED = "completed"

class Quest:
    def __init__(self, q_id, title, description, reward_gold, reward_xp):
        self.id = q_id
        self.title = title
        self.description = description
        self.reward_gold = reward_gold
        self.reward_xp = reward_xp
        self.status = QuestStatus.ACTIVE
        self.progress = 0
        self.target = 10 # Generic kill count for now

    def update_progress(self, amount):
        if self.status != QuestStatus.ACTIVE: return
        self.progress += amount
        if self.progress >= self.target:
            self.complete()

    def complete(self):
        self.status = QuestStatus.COMPLETED

class QuestManager:
    def __init__(self, player):
        self.player = player
        self.active_quests = []
        self.completed_quests = []

    def add_quest(self, quest):
        self.active_quests.append(quest)

    def on_enemy_killed(self, enemy_type):
        # Notify quests
        for q in self.active_quests:
            q.update_progress(1)
            if q.status == QuestStatus.COMPLETED:
                self._grant_reward(q)

    def _grant_reward(self, quest):
        self.player.inventory.gold += quest.reward_gold
        self.player.gain_xp(quest.reward_xp)
        self.active_quests.remove(quest)
        self.completed_quests.append(quest)
        print(f"Quest Completed: {quest.title}")
