import json
import os

from apollo_orm.domains.models.entities.concurrent.result_list.entity import ResultList
from apollo_orm.domains.models.entities.connection_config.entity import ConnectionConfig
from apollo_orm.domains.models.entities.credentials.entity import Credentials
from apollo_orm.orm.core import ORMInstance


def test_work_flow():
    json_data = json.loads(os.environ['JSON_DATA'])
    json_credentials = json.loads(os.environ['CREDENTIALS'])
    credentials = Credentials(**json_credentials)
    tables = os.environ['TABLES'].replace('"', '').replace('[', '').replace(']', '').split(',')
    connection_config = ConnectionConfig(credentials, tables)
    connection = ORMInstance(connection_config)
    connection.insert(json_data, tables[0])
    select_table = connection.select(json_data, tables[0])
    connection.delete(json_data, tables[0])
    select_deleted_table = connection.select(json_data, tables[0])

    json_data = [
        {"company": 1, "country": 170, "business_model": 1, "structure_level": 2, "structure_code": 700000182,
         "operational_cycle": 202401, "active": 355, "active_frequent": 308, "activity": 60.27,
         "activity_frequent": 52.29, "available": 597, "balance_available": 8, "begins": 26, "billing": 146426811,
         "engine_results_date": "2024-02-29T12:45:48.654Z", "inactive_1": 106, "inactive_2": 43, "inactive_3": 33,
         "inactive_4": 46, "inactive_5": 30, "inactive_6": 26, "last_update": "2024-02-29T12:45:48.654Z",
         "productivity": 412470, "publish_date": "2024-02-29T12:45:48.654Z", "recovered": 22, "repic": 1.38028169,
         "status": 3, "unavailable": 102, "user_code": "206114060",
         "user_name": "Danilo De Araujo Rodrigues - Accenture do Brasil LTDA", "version": 12},
        {"company": 1, "country": 170, "business_model": 1, "structure_level": 2, "structure_code": 700000182,
         "operational_cycle": 202401, "active": 355, "active_frequent": 308, "activity": 60.27,
         "activity_frequent": 52.29, "available": 597, "balance_available": 8, "begins": 26, "billing": 146426811,
         "engine_results_date": "2024-02-29T12:45:48.654Z", "inactive_1": 106, "inactive_2": 43, "inactive_3": 33,
         "inactive_4": 46, "inactive_5": 30, "inactive_6": 26, "last_update": "2024-02-29T12:45:48.654Z",
         "productivity": 412470, "publish_date": "2024-02-29T12:45:48.654Z", "recovered": 22, "repic": 1.38028169,
         "status": 3, "unavailable": 102, "user_code": "206114060",
         "user_name": "Danilo De Araujo Rodrigues - Accenture do Brasil LTDA", "version": 11},
        {"company": 1, "country": 170, "business_model": 1, "structure_level": 2, "structure_code": 700000182,
         "operational_cycle": 202401, "active": 355, "active_frequent": 308, "activity": 60.27,
         "activity_frequent": 52.29, "available": 597, "balance_available": 8, "begins": 26, "billing": 146426811,
         "engine_results_date": "2024-02-29T12:45:48.654Z", "inactive_1": 106, "inactive_2": 43, "inactive_3": 33,
         "inactive_4": 46, "inactive_5": 30, "inactive_6": 26, "last_update": "2024-02-29T12:45:48.654Z",
         "productivity": 412470, "publish_date": "2024-02-29T12:45:48.654Z", "recovered": 22, "repic": 1.38028169,
         "status": 3, "unavailable": 102, "user_code": "206114060",
         "user_name": "Danilo De Araujo Rodrigues - Accenture do Brasil LTDA", "version": 13},
        {"company": 1, "country": 170, "business_model": 1, "structure_level": 2, "structure_code": 700000182,
         "operational_cycle": 202401, "active": 355, "active_frequent": 308, "activity": 60.27,
         "activity_frequent": 52.29, "available": 597, "balance_available": 8, "begins": 26, "billing": 146426811,
         "engine_results_date": "2024-02-29T12:45:48.654Z", "inactive_1": 106, "inactive_2": 43, "inactive_3": 33,
         "inactive_4": 46, "inactive_5": 30, "inactive_6": 26, "last_update": "2024-02-29T12:45:48.654Z",
         "productivity": 412470, "publish_date": "2024-02-29T12:45:48.654Z", "recovered": 22, "repic": 1.38028169,
         "status": 3, "user_code": "206114060", "user_name": "Danilo De Araujo Rodrigues - Accenture do Brasil LTDA",
         "version": 14},
        {"company": 1, "country": 170, "business_model": 1, "structure_level": 2, "structure_code": 700000182,
         "operational_cycle": 202401, "active": 355, "active_frequent": 308, "activity": 60.27,
         "activity_frequent": 52.29, "available": 597, "balance_available": 8, "begins": 26, "billing": 146426811,
         "engine_results_date": "2024-02-29T12:45:48.654Z", "inactive_1": 106, "inactive_2": 43, "inactive_3": 33,
         "inactive_4": 46, "inactive_5": 30, "inactive_6": 26, "last_update": "2024-02-29T12:45:48.654Z",
         "productivity": 412470, "publish_date": "2024-02-29T12:45:48.654Z", "recovered": 22, "repic": 1.38028169,
         "status": 3, "user_code": "206114060", "user_name": "Danilo De Araujo Rodrigues - Accenture do Brasil LTDA",
         "version": 10},
        {"company": 1, "country": 170, "business_model": 1, "structure_level": 2, "structure_code": 700000182,
         "operational_cycle": 202401, "active": 355, "active_frequent": 308, "activity": 60.27,
         "activity_frequent": 52.29, "available": 597, "balance_available": 8, "begins": 26, "billing": 146426811,
         "engine_results_date": "2024-02-29T12:45:48.654Z", "inactive_1": 106, "inactive_2": 43, "inactive_3": 33,
         "inactive_4": 46, "inactive_5": 30, "inactive_6": 26, "last_update": "2024-02-29T12:45:48.654Z",
         "productivity": 412470, "publish_date": "2024-02-29T12:45:48.654Z", "recovered": 22, "repic": 1.38028169,
         "status": 3, "user_code": "206114060", "user_name": "Danilo De Araujo Rodrigues - Accenture do Brasil LTDA"}
    ]

    for data in json_data:
        result = connection.insert(data, tables[0], True)
        result.add_callbacks(callback=lambda x: print(f"Inserted {data} into {tables[0]}"),
                             errback=lambda x: print(f"Failed to insert {data} into {tables[0]}"))

        preprocess = connection.pre_process_insert(json_data, tables[0])

        inserted_concurrent: ResultList = connection.insert_concurrent(preprocess)

        for successful, errors in inserted_concurrent.successful, inserted_concurrent.errors:
            assert successful is not None
        assert errors is None

        assert len(select_table.current_rows) == 1
        assert len(select_deleted_table.current_rows) == 0
