class BalanceManager:
    # Объект для работы с балансом

    def __init__(self, file='balance.txt', encoding='UTF-8'):
        # Конструктор класса
        self.file = file
        self.encoding = encoding
        self.balance = self.get_balance()

    def get_balance(self):
        # Функция для получения баланса из файла
        balance = []
        with open(self.file, 'r', encoding=self.encoding) as f:
            for line in f.readlines():
                line = line.strip('\n').split(';')
                line[2] = int(line[2])
                balance.append(dict(zip(["дата", "категория", "сумма", "описание"], line)))
        return balance

    def rewrite_balance(self, new_balance):
        # Функция для перезаписи баланса в файл
        with open(self.file, 'w', encoding=self.encoding) as f:
            for item in new_balance:
                item["сумма"] = str(item["сумма"])
                f.write(";".join(item.values()) + "\n")
        self.balance = self.get_balance()
        return self.balance

    def write_post(self, post):
        # Функция для добавления записи в файл
        with open(self.file, 'a', encoding=self.encoding) as f:
            post["сумма"] = str(post["сумма"])
            f.write("\n" + ";".join(post.values()))
            print("Запись успешно добавлена")
        self.balance = self.get_balance()
        return self.balance

    def change_post(self, old_post, new_post):
        # Функция для изменения записи в файле
        balance = self.get_balance()
        for i in range(len(balance)):
            if balance[i] == old_post:
                balance[i] = new_post
                return self.rewrite_balance(balance)
        return self.balance

    def find_post(self, param, value):
        # Функция для поиска записей по параметру
        result = []
        for item in self.balance:
            if item[param] == value:
                result.append(item)
        return result

    def show_balance(self):
        # Функция для отображения общего баланса
        result = {'Общая сумма': 0, 'Доходы': [], 'Расходы': []}
        for item in self.balance:
            result['Общая сумма'] += item['сумма'] * {"доход": 1, "расход": -1}[item['категория']]
            result[item['категория'].capitalize()+'ы'].append(item['сумма'])
        return result

# Запуск непосредственно из данного файла
if __name__ == '__main__':
    try:
        name = input('Введите название файла для работы (по-умолчанию: "balance"): ')
        file_name = name + '.txt' if name else 'balance.txt'

        try:
            manager = BalanceManager(file_name)
        except FileNotFoundError:
            # Создание файла, если его не существует
            with open(file_name, 'w'):
                pass
            manager = BalanceManager(file_name)

        # Цикл взаимодействия с пользователем
        while True:
            console_command = input('Введите команду (help для вывода списка команд): ')
            commands = console_command.strip().lower().split(' ', 1)

            # Обработка команд
            if commands[0] == 'help':
                print('''\nСписок команд:
show                        -> показать всю информацию по счету.
balance                     -> показать текущий баланс.
add <post>                  -> добавить запись формата <дата(YYYY-mm-dd); категория; сумма; описание>.
change <old_post=new_post>  -> изменить запись формата <дата(YYYY-mm-dd); категория; сумма; описание> на новую.
find <param=value>          -> найти запись по выбранному параметру.
exit                        -> остановка программы.
Пожалуйста, учитывайте пробелы в параметрах записей.
                ''')

            # Команда отображения текущего баланса
            elif commands[0] == 'balance':
                print(manager.show_balance())

            # Команда добавления новой записи
            elif commands[0] == 'add':
                try:
                    data = dict(zip(["дата", "категория", "сумма", "описание"], commands[1].split('; ')))
                    manager.write_post(data)
                except:
                    print("Во врмя выполнения программы произошла ошибка.\nПожалуйста, проверьте корректность введеных данных.")

            # Команда изменения записи
            elif commands[0] == 'change':
                try:
                    old_post, new_post = commands[1].split('=')
                    old_post = dict(zip(["дата", "категория", "сумма", "описание"], old_post.strip().split('; ')))
                    new_post = dict(zip(["дата", "категория", "сумма", "описание"], new_post.strip().split('; ')))
                    manager.change_post(old_post, new_post)
                except:
                    print("Во врмя выполнения программы произошла ошибка.\nПожалуйста, проверьте корректность введеных данных.")

            # Команда поиска записи по параметру
            elif commands[0] == 'find':
                try:
                    param, value = commands[1].split('=')
                    print(manager.find_post(param.strip(), value.strip()))
                except:
                    print("Во врмя выполнения программы произошла ошибка.\nПожалуйста, проверьте корректность введеных данных.")

            # Команда отображения всей информации
            elif commands[0] == 'show':
                print(manager.balance)

            # Команда выхода из программы
            elif commands[0] == 'exit':
                raise KeyboardInterrupt

            # Обработка случайного/некорректного ввода
            else:
                print('Команда нераспознана')

    # Обработка ошибки при выходе с помощью клавиш ctrl + c
    except KeyboardInterrupt:
        print('\nПрограмма закрыта')