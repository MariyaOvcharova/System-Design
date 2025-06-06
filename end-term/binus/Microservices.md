
# Микросервисы: жизнь после. Невыдуманные истории #

Ссылка на видео: https://www.youtube.com/watch?v=iOfR0YtaWMc
Ссылка на презентацию из видео: https://disk.yandex.ru/i/GBxiFMOUMMx6-g

## Основная мысль ##
Микросервисы - это вообще не волшебная таблетка. Переход на них сложный и очень часто всё идет совсем не по плану. То, что на бумажке выглядит красиво, в реальной жизни превращается в кучу, местами неожиданных проблем.

### Почему решили распилить монолит на микросервисы: ###
Бизнес захотел сильно вырасти.
Им поставили цель: к 2027 году увеличить число пользователей в 7 раз, заказы - в 4 раза, а данных товаров - в 10 раз. То есть рост был просто огромный.

Текущий монолит не справлялся.
Код был старый (писали его ещё с 2006 года), огромный и сложный. Новые фичи добавлять тяжело. Релизы шли по 3 часа. Всё тормозило. Масштабироваться дальше было никак нельзя.

Проблемы с инфраструктурой.
Даже после переезда в 3 дата-центра оказалось, что места мало, электричества не хватает.

Монолит стал "проходным двором".
Все команды работали в одном коде, мешали друг другу, ломали чужую работу. Постоянно были баги и задержки.

Хотели улучшить скорость разработки и деплоя.
Если всё разнести по микросервисам, команды смогут работать независимо, быстрее выкладывать обновления и расти без таких проблем.

## Тезисы ##
Монолит тяжело масштабировать
Когда бизнес растет быстро, старый монолит тормозит развитие. Новые пользователи, заказы, данные - всё это начинает рушить систему. К тому же, чтобы перейти на микросервисы, надо вложить очень много сил и времени, что сильно влияет на работу всех.

Распил монолита это больно
Просто взять и распилить монолит не получится. В видео приводился пример, что в монолите каша из кода, куча зависимостей, какие-то гигантские классы типа SimpleCollection на 7000 строк. Делить всё это очень сложно и занимает много времени.

Теория ≠ практика
Иван Матвеев (кто вел доклад) сказал, что можно всё сделать "по книжкам" - рисовать красивые схемы, делать bounded context, изучать CAP-теорему, но когда реально начинаешь - оказывается, что код слишком сложный, а старые куски мешают всё разделить как надо.

Коммуникации между командами это сложно
Бывает, что тебе нужно, чтобы другая команда ускорила свой сервис, а они такие: "приходи через год". И ты ничего не можешь сделать. Даже если у тебя горят бизнес-сроки, просто сидишь и ждешь или как-то выкручиваешься сам.

Проблемы с сетью
Даже если всё вроде сделано правильно, сеть может подставить. Из-за сетевых задержек сервисы тормозят. Пришлось разбираться с балансировщиками, DNS, менять образы контейнеров, отключать IPv6, чтобы хоть что-то починить.

### Инциденты ##
Чем сложнее система, тем чаще случаются проблемы. Иногда проблема не в коде, а в диске, в нагрузке или в сети. И найти настоящую причину бывает очень тяжело и долго.

## В итоге ##
Распиливание помогало. Например, карточка товара стала загружаться быстрее - раньше было 1.5 секунды, а теперь меньше секунды.

Но кучи старого кода всё ещё осталось, и не везде получилось всё красиво распилить. Иногда приходилось тащить чужую логику в свои сервисы.

Переход на микросервисы - это не просто переделать код. Надо ещё правильно работать с сетями, серверами и командами.

Иногда дешевле оставить куски в монолите, чем пытаться их переписывать.

По факту микросервисы - это не всегда выгодно. Если старый код плохой, микросервисы ничего не спасут, а только усложнят работу и увеличат затраты ресурсов.

Иван сказал очень правильную вещь: надо думать в первую очередь о бизнесе, а не о красивых схемах из книжек. Лучше честно работать с реальностью, чем мечтать об идеальной архитектуре.

Ещё очень важно общение между командами. Без нормальной коммуникации всё развалится, даже если код будет самый лучший.

### Вывод ###
Переход на микросервисы - это вообще не просто смена архитектуры. Это долгий и тяжёлый путь, полный боли, ошибок и компромиссов. И если компания решается на это - надо быть реально готовыми к трудностям, а не ждать быстрого успеха.
