class Quest:
    def __init__(self, id, title, description, reward_xp=100, reward_gold=50):
        self.id = id
        self.title = title
        self.description = description
        self.reward_xp = reward_xp
        self.reward_gold = reward_gold
        self.completed = False
        self.active = False
        self.progress = 0
        self.target = 10 # Example: Kill 10 enemies

    def update_progress(self, amount=1):
        if self.active and not self.completed:
            self.progress += amount
            if self.progress >= self.target:
                self.complete()

    def complete(self):
        self.completed = True
        self.active = False
        print(f"Quest Completed: {self.title}")

class QuestManager:
    def __init__(self):
        self.quests = {}
        self.active_quests = []

        # Populate
        self.add_quest(Quest("slayer1", "Stick Slayer", "Kill 10 Stickmen.", 150, 50))
        self.add_quest(Quest("slime1", "Slime Time", "Kill 5 Slimes.", 100, 20))

    def add_quest(self, quest):
        self.quests[quest.id] = quest

    def start_quest(self, quest_id):
        if quest_id in self.quests:
            quest = self.quests[quest_id]
            quest.active = True
            self.active_quests.append(quest)
            print(f"Started Quest: {quest.title}")

    def on_enemy_killed(self, enemy_type):
        for quest in self.active_quests:
            # Simple check
            if "Stick" in quest.title and enemy_type == "stickman":
                quest.update_progress(1)
            elif "Slime" in quest.title and enemy_type == "slime":
                quest.update_progress(1)
