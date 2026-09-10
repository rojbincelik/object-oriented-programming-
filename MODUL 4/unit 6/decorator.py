class DataService:

    def get_data(self):

        return "Important data"

class LoggingDataService:

    def __init__(self, wrapped_service):

        self.wrapped_service = wrapped_service

    def get_data(self):

        print("LOG: about to fetch data")

        return self.wrapped_service.get_data()

# Main

data_service = DataService()

logging_service = LoggingDataService(data_service)

result = logging_service.get_data()

print(result)