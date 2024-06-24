import requests
from pypresence import Presence
import time
import sys

client_id = 'Client_ID Бота'

server_ids = [' Замініть на ID ваших серверів у BattleMetrics', ' Замініть на ID ваших серверів у BattleMetrics']

api_key = 'Замініть на ваш ключ API BattleMetrics'

RPC = Presence(client_id)


# Функція для підключення до Discord
def connect_rpc():
    try:
        RPC.connect()
        print("Успішне підключення до Discord RPC")
    except Exception as e:
        print(f"Не вдалося підключитися до Discord RPC: {e}")
        sys.exit(1)


# Функція для отримання числа гравців на сервері
def get_server_population(server_id):
    url = f'https://api.battlemetrics.com/servers/{server_id}'
    headers = {
        'Authorization': f'{api_key}'
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        players = data['data']['attributes']['players']
        print(f"Сервер с айди {server_id} онлайн на сервере {players} ")  # Налагоджувальна інформація
        return players
    except requests.exceptions.RequestException as e:
        print(f"Не вдалося отримати дані з API BattleMetrics для сервера {server_id}: {e}")
        return None


# Функція для оновлення статусу в Discord
def update_presence(total_players):
    print(f"Оновлення присутності з {total_players} гравцями онлайн")
    if total_players is not None:
        try:
            RPC.update(
                state="Ukraine Mod Community",
                details=f"Загальний онлайн: {total_players}",
                large_image="1024",
                large_text="Ukraine Mod Community",
                small_image="small_image_name",
                small_text="Small image text",
                buttons=[
                    {"label": "Мейн кемп", "url": "https://maincamp.ukrainemod.space/"},
                    {"label": "Діскорд", "url": "https://dsc.gg/ukrainemod"}
                ]
            )
            print(f"RPC оновлено до {total_players} гравців онлайн")
        except Exception as e:
            print(f"Не вдалося оновити RPC: {e}")


def main():
    print("Rich Presence запускається...")
    connect_rpc()

    try:
        while True:
            start_time = time.time()

            total_players = 0
            for server_id in server_ids:
                players_online = get_server_population(server_id)
                if players_online is not None:
                    total_players += players_online

            update_presence(total_players)

            elapsed_time = time.time() - start_time
            sleep_time = max(0, 5 - elapsed_time)
            time.sleep(sleep_time)  # Оновлюємо статус кожні 5 секунд

    except KeyboardInterrupt:
        print("Вихід...")
        RPC.close()
        sys.exit(0)


if __name__ == "__main__":
    main()
