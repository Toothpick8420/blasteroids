class Highscore:

    SCORES_FILE: str = "scores/scores.txt"
    SCORES: list = []

    def __init__(self) -> None:
        self.load_scores()

    def load_scores(self) -> list:
        lines: list = []

        with open(Highscore.SCORES_FILE, "r") as file:
            lines = file.readlines()

        scores: list = []
        for line in lines:
            score: str = line.strip().split(":")[0].strip()
            name: str = line.strip().split(":")[1].strip()
            scores.append([int(score), name])

        scores = sorted(scores)
        scores.reverse()
        Highscore.SCORES = scores

    def new_highscore(self, new_score: int) -> bool:
        if len(Highscore.SCORES) < 5:
            return True
        else:
            for pos, score in enumerate(Highscore.SCORES):
                if new_score > score[0]:
                    return True
            return False

    def add(self, new_name: str, new_score: int) -> None:

        if len(Highscore.SCORES) >= 5:
            Highscore.SCORES.pop()

        Highscore.SCORES.append([new_score, new_name])
        Highscore.SCORES = sorted(Highscore.SCORES)
        Highscore.SCORES.reverse()

    def save_scores(self) -> list:
        with open(Highscore.SCORES_FILE, "w") as file:
            for score in Highscore.SCORES:
                to_write: str = f"{str(score[0])} : {score[1]}\n"
                file.write(to_write)
