# Туристический бот

Этот репозиторий содержит исходный код для Телеграм-бота [ @LitQst_bot](https://t.me/LitQst_bot) .


## В чем прикол и фишки бота

Весь бот нужен чтобы проводить литературные экскурсии по СПБ. Пользователи будут приходить на разные локации, связанные с искусством. Будут высылаться геопозиции этих мест. Сам маршрут образует некий круг и места находятся находятся довольно близко друг к другу.

Также будут высылаться фотографии этих мест с небольшими сообщениями, которые несут в себе историю этих мест. Чтобы по дороге не было скучно, я добавил кнопку "Факты", в ней находятся 30 интересных фактов о СПБ.

Вся история прохождения карты а также факты которые уже прочли сохраняются в БД, чтобы не было путаницы, я использовал SQLite. Подобную логику и код можно использовать, чтобы создавать подобные экскурсии для любых городов и на различные темы.

# Сама карта



<img src="https://github.com/Ramzzz10/LTQBOT/assets/93703127/658a92ae-2730-4bf5-89fe-3d0fa2e344be" width="200" />


## Вывод фотографий

Вывод в этом коде написан некорректно, так как пути на моем локальном ПК, из-за этого будут проблемы когда закините бота на сервер. Лучше сделать так.

Для того чтобы бот мог отправлять фотографии, необходимо предоставить URL-адреса фотографий, которые будут доступны боту. Вам следует загрузить фотографии на сервер или хостинг, который поддерживает удаленный доступ к файлам через URL-адреса. Затем вы можете использовать эти URL-адреса в вашем коде для отправки фотографий через Telegram бота.

Вот как можно сделать это:

1. Загрузите фотографии на сервер или хостинг. После загрузки фотографий, у вас будет URL-адрес каждой фотографии.

2. Замените значения `photo` в словаре `literary_places` на URL-адреса фотографий. 

## Лицензия

Туристический бот опубликован в соответствии с условиями [GNU General Public License v3](https://www.gnu.org/licenses/gpl-3.0.html).
