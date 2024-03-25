# GPN_KIP
## Модель сопоставления человеческих и материальных ресурсов (МСЧМ)

![plot](/img/photo_2023-09-07_16-45-34.jpg "Диаграмма классов модели")

Данным репозиторием пользуются либо те, кто использует обученные МСЧМ модели, 
либо те, кто эти самые МСЧМ модели обучает. Начнем с первых. Их взаимодействие с обученными 
МСЧМ моделями проходит с помощью класса `ResTimeModel` в библиотеке `stairsres`.

### Как достать модели?
Установка:
```commandline
pip3 install stairsres 
```
Далее идет вытягивание нужных моделей:
```python3
from stairsres.res_time_model import ResTimeModel
from stairsres.DBWrapper import DBWrapper
from idbadapter import MschmAdapter, Schedules


URL = "url_to_db"

mschm_adapter = MschmAdapter(URL)
adapter = Schedules(URL)
dbwrapper = DBWrapper(mschm_adapter=mschm_adapter, adapter=adapter)

model = ResTimeModel(dbwrapper)
work_name = "работа А"
work_volume = 5.0  # объем работы
res_data = model.get_resources_volumes(work_name, work_volume)
```

Подробнее пример работы с `ResTimeModel` описан в туториале: 
`/examples/tutorials/res_time_model.ipynb`


### Как обучить модели?
МСЧМ модель состоит из набора предрасчетов и обученных эго сетей производительности. Для 
каждой работы обучается своя эго сеть работ и своя эго сеть производительности. На основе эго
сети работ делаются предрасчеты. Далее и предрасчеты, и сети производительности отправляются
в Базу Данных.


Текущая версия обучения МСЧМ модели объединена и преобразована в класс `Pipeline`. 
___Запускает текущую версию обучения МСЧМ модели скрипт, расположенный в___ 
`/examples/calculating_works.py`. Подробное пояснение к коду и к процессу обучения можно
найти в туториале: `/examples/tutorials/pipeline.ipynb`
