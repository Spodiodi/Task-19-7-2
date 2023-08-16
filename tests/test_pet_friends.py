from api import PetFriends
from settings import valid_email, valid_password
import os
import pytest

pf = PetFriends()


# 1
def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """ Проверяем что запрос api ключа возвращает статус 200 и в тезультате содержится слово key"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 200
    assert 'key' in result


# 2
def test_get_all_pets_with_valid_key(filter=''):
    """ Проверяем что запрос всех питомцев возвращает не пустой список.
    Для этого сначала получаем api ключ и сохраняем в переменную auth_key. Далее используя этого ключ
    запрашиваем список всех питомцев и проверяем что список не пустой.
    Доступное значение параметра filter - 'my_pets' либо '' """

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 200
    assert len(result['pets']) > 0


# 3
def test_add_new_pet_with_valid_data(name='Персик', animal_type='тюлень',
                                     age='1', pet_photo='images\\nerpa1.jpg'):
    """Проверяем что можно добавить питомца с корректными данными"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name


# 4
def test_successful_delete_self_pet():
    """Проверяем возможность удаления питомца"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Персик", "тюлень", "2", "images\\nerpa1.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    assert status == 200
    assert pet_id not in my_pets.values()


# 5
def test_successful_update_self_pet_info(name='Персивальд', animal_type='Нерпа', age=3):
    """Проверяем возможность обновления информации о питомце"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Если список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
        assert result['name'] == name
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")


# 6
def test_add_pet_simple_valid(name='Персичек', animal_type='тюленьчик', age='4'):
    """Проверяем что можно добавить питомца с корректными данными без фото"""

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.create_pet_simple(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name


# 7
def test_add_photo_of_pet_valid(pet_id='', pet_photo_path='images/nerpa2.jpg'):
    """Проверяем возможность обновления фото питомца по id"""

    pet_photo_path = os.path.join(os.path.dirname(__file__), pet_photo_path)

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if not my_pets['pets']:
        raise Exception("There is no my pets")
    pet_id = my_pets['pets'][0]['id']

    status, result = pf.set_photo(auth_key, pet_id, pet_photo_path)

    # Проверяем, что статус ответа = 200 и фото питомца соответствует заданному
    assert status == 200
    assert result['pet_photo']


# 8
def test_get_api_key_for_user_invalid(email="some_wrong_email", password="password"):
    """ Проверяем некоректное введение логина и пароля
    403 -- The error code means that provided combination of user email and password is incorrect"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 403
    assert 'key' not in result


# 9
def test_get_all_pets_with_key_invalid(filter=''):
    """Проверяем возврат статуса 403 и пустого списка питомцев,
    если ввели неверный ключ.
    403 -- The error code means that provided auth_key is incorrect"""

    # _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets({'key': 'xxx'}, filter)
    # print(auth_key)

    assert status == 403


# 10
def test_add_new_pet_invalid_1(name='', animal_type='тюлень',
                               age='5', pet_photo='images\\nerpa1.jpg'):
    """Проверяем что невозможно добавить питомца без имени
    400 -- The error code means that provided data is incorrect"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 400
    # assert result['name'] == name


# 11
def test_add_new_pet_invalid_2(name='Тестовый Персик 2', animal_type='тюлень',
                               age='-6', pet_photo='images\\nerpa1.jpg'):
    """Проверяем что невозможно добавить питомца c отрицательным возрастом
    400 -- The error code means that provided data is incorrect"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 400
    # assert result['name'] == name


# 12
def test_add_new_pet_invalid_3(name='Тестовый Персик 3', animal_type='тюлень',
                               age='7', pet_photo='..\README.md'):
    """Проверяем что невозможно добавить питомца c документом вместо фото
    400 -- The error code means that provided data is incorrect"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 400
    # assert result['name'] == name


# 13
def test_add_pet_simple_invalid(name='Тестовый Персичек', animal_type='тюленьчик', age='-8'):
    """Проверяем невозможность добавить питомца с отрицательным возрастом
    400 -- The error code means that provided data is incorrect"""

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.create_pet_simple(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 400
    # assert result['name'] == name


# 14
def test_delete_self_pet_invalid_id():
    """Проверяем невозможность удаления питомца с некорректным ID.
    И проверяем что полученный ID в списке питомцев."""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Персик", "тюлень", "9", "images\\nerpa1.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']
    print('\n Pet_ID = ', pet_id)
    status, _ = pf.delete_pet(auth_key, 'None')

    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем что статус ответа равен 200 и в списке питомцев есть id питомца
    assert status == 200
    assert pet_id in my_pets.values()


# 15
def test_add_photo_of_pet_invalid(pet_id='', pet_photo_path='images/nerpa2.jpg'):
    """Проверяем невозможность обновления фото питомца по некорректному id.
    400 -- The error code means that provided data is incorrect"""

    pet_photo_path = os.path.join(os.path.dirname(__file__), pet_photo_path)

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if not my_pets['pets']:
        raise Exception("There is no my pets")
    pet_id = my_pets['pets'][0]['id']

    status, result = pf.set_photo(auth_key, 'None', pet_photo_path)

    # Проверяем, что статус ответа = 200 и фото питомца соответствует заданному
    assert status == 400
    assert result['pet_photo']
