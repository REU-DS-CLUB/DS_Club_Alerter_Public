import datetime
from apiclient import discovery
from httplib2 import Http
from oauth2client import client, file, tools
import pickle


class GoogleFormsApi:
    def __init__(self):
        self.FormsId = list(pickle.load(
            open('FormsQuestions.pickle', 'rb')).keys())
        self.service = self.connector()

    def string_to_time(self, time: str) -> float:
        """Конвертирует строку с датой ответа в UNIX время

        Parameters:
            time: строка в формате YYYY-MM-DDTH:M:S.MS"""
        time = time[:-4]
        return datetime.datetime.strptime(time, "%Y-%m-%dT%H:%M:%S.").timestamp()

    def check_actual(self, tmptime: float):
        """Возвращает true если дата ответа формы в промежутке от вчера до сейчас

        Parameters:
            tmptime: UNIX-время"""
        if tmptime >= (datetime.datetime.now() - datetime.timedelta(days=1)).timestamp():
            return True
        if tmptime < (datetime.datetime.now() - datetime.timedelta(days=1)).timestamp():
            return False
        else:
            raise Exception('check_actual убился во времени')

    def upload(self, local_form_id=0):
        """Скачивает ответы из формы, отбирает релевантные и отсортировывает по времени.
        Записывает в pickle-файл для последующего просмотра ответов из формы.

        Parameters:
            local_form_id: локальный номер формы для выгрузки"""
        result = self.get_response_list(local_form_id)
        result_relevant = []
        for state in result['responses']:
            if self.check_actual(self.string_to_time(state['createTime'])):
                result_relevant.append(state)
        result_relevant = self.sort_answers_by_time(result_relevant)
        pickle.dump(result_relevant, open('Uploaded.pickle', 'wb'))

    def get_response(self, num=0, way=True):
        """Возвращает определенный ответ из списка ответов формы

        Parameters:
            num: Номер ответа из формы
            way: true - отсчет с конца, false - с начала
        """
        if way:
            return pickle.load(open('Uploaded.pickle', 'rb'))[num]
        else:
            return pickle.load(open('Uploaded.pickle', 'rb'))[::-1][num]

    def get_response_list(self, local_form_id):
        """Возвращает список ответов из списка форм по счету, сначала или с конца T/F"""
        result = self.service.forms().responses().list(
            formId=self.FormsId[local_form_id]).execute()

        for i in range(len(result['responses'])):
            time = datetime.datetime.utcfromtimestamp \
                (datetime.datetime.strptime
                 (result['responses'][i]['createTime'][:-4], "%Y-%m-%dT%H:%M:%S.").timestamp() + 21600)
            time = time.strftime('%Y-%m-%dT%H:%M:%S.1111')
            result['responses'][i]['createTime'] = time
        return result

    def connector(self):
        """Возвращает сервис с подключением к нашим гугл формам"""
        SCOPES = "https://www.googleapis.com/auth/forms.responses.readonly"
        DISCOVERY_DOC = "https://forms.googleapis.com/$discovery/rest?version=v1"

        store = file.Storage('token.json')
        creds = None
        if not creds or creds.invalid:
            flow = client.flow_from_clientsecrets(
                'client_secrets.json', SCOPES)
            creds = tools.run_flow(flow, store)
        service = discovery.build('forms', 'v1', http=creds.authorize(
            Http()), discoveryServiceUrl=DISCOVERY_DOC, static_discovery=False)
        return service

    def new_answers(self, local_form_id=0):
        """Возвращает количество ответов из формы.

        Parameters:
            local_form_id: локальный номер формы для выгрузки"""
        result = self.get_response_list(0)
        tmp = 0
        for state in result['responses']:
            if self.check_actual(self.string_to_time(state['createTime'])):
                tmp += 1
        return tmp

    def sort_answers_by_time(self, arr: list) -> []:
        """Возвращает отсортированные по времени массив с ответами из формы.

        Parameters:
            arr: неотсортированные ответы из формы"""
        datetime_dict = {}
        for i in arr:
            date = self.string_to_time(i['createTime'])
            datetime_dict[date] = i
        preresult = sorted(datetime_dict)
        result = []
        for i in preresult:
            result.append(datetime_dict[i])
        return result
