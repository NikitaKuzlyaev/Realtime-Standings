# 🏆 Realtime Standings

Веб-интерфейс с **живой таблицей результатов** для ваших соревнований Codeforces.

- Можно вывести на **большой экран** во время соревнований для зрителей и участников.

- Минималистичный строгий вид, обеспечивающий отличную видимость издалека и на любых экранах.

- Поддержка автопрокрутки для удобного просмотра большого количества команд.


<img src="https://github.com/NikitaKuzlyaev/profile/blob/main/cf2.png" alt="get codeforces api key" width="800"/>


---

## 📦 Технологии

![Python](https://img.shields.io/badge/python-3.12-blue?logo=python)
![FastAPI](https://img.shields.io/badge/fastapi-async--web--framework-green?logo=fastapi)
![PostgreSQL](https://img.shields.io/badge/postgresql-db-blue?logo=postgresql)
![Redis](https://img.shields.io/badge/redis-cache--store-red?logo=redis)
![Docker](https://img.shields.io/badge/docker-containerized-blue?logo=docker)
![Nginx](https://img.shields.io/badge/nginx-reverse--proxy-darkgreen?logo=nginx)

---

## 🔐 Аутентификация

Вы входите в систему, указав:
- `API-ключ`
- `Contest ID`

Теперь это — ваша учетная запись.

🔒 У вас должны быть **права менеджера** на указанный контест.

<details>
  <summary>Где получить ключ?</summary>

  <br/>

  <img src="https://github.com/NikitaKuzlyaev/profile/blob/main/cf1.png" alt="get codeforces api key" width="600"/>

</details>


---

## 🔄 Как работает обновление

Браузер клиента шлёт периодические `still alive`-запросы → бэкенд понимает, что клиент активен, и продолжает переодически опрашивать API codeforces.


## ⚙️ Сбор и кэширование результатов

- С заданной периодичностью **бэкенд запрашивает Codeforces API** для каждой активной учетной записи
- Полученные данные сохраняются в **Redis**
- **Redis** служит кэшем и источником правды для клиентов


## 📡 Обновление клиентского UI

- Каждый клиент получает данные **только из Redis**
- Это позволяет подключать **сколько угодно пользователей** к одному соревнованию и транслировать таблицу в разных местах
- Каждая таблица одновременно содержит актуальную информацию, но независима — вы можете включать и выключать автопрокрутку независимо, и делать что угодно еще 


## 🧠 Защита от перегрузки Codeforces

- Независимо от количества клиентов, **внешние запросы к Codeforces API происходят не чаще одного раза в 2 секунды для активной учетной записи**
- Если `still alive`-запросов от учетной записи не поступало более 60 секунд, учетная запись становится неактивной и от вашего имени запросы на codeforces не посылаются
- Чтобы учетная запись стала активной перейдите на вкладку "логи" с активным интернет-соединением

---

### ⚠️ Важно:

> Формат названий команд участников должен быть в формате `Название команды [ТЭГ] (Участник1, Участник2, ...)`, например `Крутая Сборная Универа [ТПУ] (Иванов, Смирнов, Сидоров)`

### 🚀 Развёртывание

1. Клонируйте репозиторий:

```bash
git clone https://github.com/NikitaKuzlyaev/Realtime-Standings.git
cd Realtime-Standings
```

2. Запустите сборку в Docker
```bash
docker-compose up --build
```

3. После сборки приложение будет доступно по адресу:
```bash
http://your_server_ip:80
```


