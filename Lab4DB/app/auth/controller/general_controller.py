from abc import ABC
from typing import List, Dict
from http import HTTPStatus
from flask import abort


class GeneralController(ABC):

    _service = None

    def find_all(self) -> List[object]:
        results = self._service.find_all()
        print('controller find_all:', results)
        return [obj.put_into_dto() for obj in results]

    def find_by_id(self, key: int) -> object:
        obj = self._service.find_by_id(key)
        if obj is None:
            abort(HTTPStatus.NOT_FOUND)
        return obj.put_into_dto()

    def create(self, obj: object) -> object:
        created_obj = self._service.create(obj)
        return created_obj.put_into_dto()

    def create_all(self, obj_list: List[object]) -> List[object]:
        created_objs = self._service.create_all(obj_list)
        return [obj.put_into_dto() for obj in created_objs]

    def update(self, key: int, new_obj: object) -> None:
        obj = self._service.find_by_id(key)
        if obj is None:
            abort(HTTPStatus.NOT_FOUND)
        self._service.update(key, new_obj)

    def patch(self, key: int, value_dict: Dict[str, object]) -> None:
        existing_object = self._service.find_by_id(key)
        if existing_object is None:
            abort(HTTPStatus.NOT_FOUND)

        for attribute, value in value_dict.items():
            setattr(existing_object, attribute, value)

        self._service.update(key, existing_object)

    def delete(self, key: int) -> None:
        obj = self._service.find_by_id(key)
        if obj is None:
            abort(HTTPStatus.NOT_FOUND)
        self._service.delete(key)

    def delete_all(self) -> None:
        self._service.delete_all()
