import os
from dotenv import load_dotenv

load_dotenv()
valid_email = os.getenv('valid_email')
valid_password = os.getenv('valid_password')

"""
Кроме того, что мы склонировали проект себе на комп и открыли его, сделать:

1. создать виртуальное окружение
python -m venv venvnv 

2. активировать вирт окружение
venvnv\Scripts\activate.bat 

3. выбрала в качестве интерпритатора (делается в settings)
C:\Kibizova\pythonModul19-4\venvnv\Scripts\python.exe

4. скачали и установили все требуемые пакеты (названия пакетов гуглили)

5. затем мы сохранили все зависимости
pip freeze > requirements.txt

6. и бонусом запуск тестов с терминала
pytest tests/test_pet_friends.py 
"""
