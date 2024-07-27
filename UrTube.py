import hashlib
from time import sleep
from typing import List

class Video:
    def __init__(self, title:str, duration:int, time_now:int = 0, adult_mode:bool = False):
        self.title = title  # заголовок
        self.duration = duration  # продолжительность, секунды
        self.time_now = time_now  # секунда остановки(изначально 0)
        self.adult_mode = adult_mode  # ограничение по возрасту, bool (False по умолчанию)

    def __repr__(self):
        return f"Video(title='{self.title}', duration={self.duration}, time_now={self.time_now}, adult_mode={self.adult_mode})"

    def __eq__(self, other):
        return isinstance(other, Video) and self.title == other.title

    def __contains__(self, title: str):
        return self.title == title

class User:
    def __init__(self, nickname:str, password:str, age:int):
        self.nickname = nickname
        self.password = self._hash_password(password)
        self.age = age

    def __eq__(self, other):
        return isinstance(other, User) and self.nickname == other.nickname

    def _hash_password(self, password: str) -> int:
        return int(hashlib.sha256(password.encode()).hexdigest(), 16)

    def check_password(self, password: str) -> bool:
        return self.password == self._hash_password(password)

    def __repr__(self):
        return f"{self.nickname}"

    def __contains__(self, nickname: str):
        return self.nickname == nickname

class UrTube:
    users = []
    videos = []
    current_user = None

    def log_in(self, nickname:str, password:str):
        for user in self.users:
            if nickname == user.nickname and user.check_password(password):
                self.current_user = user
                return f"Пользователь {nickname} успешно вошел в систему."
        return "Неверный никнейм или пароль."

    def register(self, nickname:str, password:str, age:int):
        for user in self.users:
            if user.nickname == nickname:
                print(f"Пользователь {nickname} уже существует")
        new_user = User(nickname, password, age)
        self.users.append(new_user)
        self.current_user = new_user
        return f'Пользователь {nickname} зарегистрирован и вошел в систему'

    def log_out(self):
        self.current_user = None
        return "Пользователь успешно вышел из системы."

    def add(self, *videos: Video):
        existing_titles = {video.title for video in self.videos}
        for video in videos:
            if video.title not in existing_titles:
                self.videos.append(video)

    def get_videos(self, search_term: str) -> List[str]:
        search_term_lower = search_term.lower()
        return [video.title for video in self.videos if search_term_lower in video.title.lower()]

    def watch_video(self, title:str):
        if not self.current_user:
            print("Войдите в аккаунт, чтобы смотреть видео")
            return "Войдите в аккаунт, чтобы смотреть видео"

        for video in self.videos:
            if video.title == title:
                if self.current_user and self.current_user.age < 18:
                    print("Вам нет 18 лет, пожалуйста покиньте страницу")
                    return "Вам нет 18 лет, пожалуйста покиньте страницу"
                while video.time_now < video.duration:
                    sleep(1)
                    video.time_now += 1
                    print(f"{video.time_now}", end=" ", flush=True)
                video.time_now = 0
                print("Конец видео")
                return "Конец видео"

    def __repr__(self):
        return f"UrTube(current_user={self.current_user})"

ur = UrTube()
v1 = Video('Лучший язык программирования 2024 года', 200)
v2 = Video('Для чего девушкам парень программист?', 10, adult_mode=True)

# Добавление видео
ur.add(v1, v2)

# Проверка поиска
print(ur.get_videos('лучший'))
print(ur.get_videos('ПРОГ'))

# Проверка на вход пользователя и возрастное ограничение
ur.watch_video('Для чего девушкам парень программист?')
ur.register('vasya_pupkin', 'lolkekcheburek', 13)
ur.watch_video('Для чего девушкам парень программист?')
ur.register('urban_pythonist', 'iScX4vIJClb9YQavjAgF', 25)
ur.watch_video('Для чего девушкам парень программист?')

# Проверка входа в другой аккаунт
ur.register('vasya_pupkin', 'F8098FM8fjm9jmi', 55)
print(ur.current_user)

# Попытка воспроизведения несуществующего видео
ur.watch_video('Лучший язык программирования 2024 года!')