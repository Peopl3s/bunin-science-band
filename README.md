# bunin-science-band
Сайт Совета Молодых Учёных *ЕГУ им. И.А. Бунина*

### Запуск
```bash
docker compose up
docker compose exec web python /code/bunin_science_band/manage.py migrate
docker compose exec web python /code/bunin_science_band/manage.py createsuperuser
```

### Что реализовано
- [x] Страницы:
  - - [x] новости
  - - [x] события (мероприятия), проводимые сообществом
  - - [x] участники 
  - - [x] сведения о сообществе молодых учёных
  - - [x] контакты
    - [ ] журнал (сообщество ещё не организовало работу с журналом)
- [x] Регистрация и авторизации пользователей, смена/восстановление пароля от учётной записи
- [x] [Обработка исключений через middleware](https://github.com/Peopl3s/bunin-science-band/blob/74b91d807627435b3144c9e6ecfe1e07edaad626/bunin_science_band/utils/middleware.py#L1)
- [x] Логирование в файл, на почту и через [телеграм бота](https://github.com/Peopl3s/bunin-science-band/blob/main/bunin_science_band/utils/telegrambot_handler.py)
- [x] Возможность поделиться новость/событием по электронной почте (на основе SMTP от Mail.ru)
- [x] Система комметариев
- [x] Лайки (fetch JS)
- [x] Записи (новости, события) могут содержать текст в разметке markdown, файлы для скачивания, изображение (если их несколько, то слайдер изображениями)
- [x] Теги для новостей, событий и участников; поиск по тегам
- [x] Поиска по новостям и событиям (Trigram search)
- [x] Система рекомендаций (похожие новости/события)
- [x] Блок с последними и наиболее обсуждаемыми новостями
- [x] RSS-фид
- [x] Карта сайта и robots.txt 

### Все скриншоты [тут](https://github.com/Peopl3s/bunin-science-band/tree/main/screens)
![alt text](https://github.com/Peopl3s/bunin-science-band/blob/main/screens/index.PNG)
