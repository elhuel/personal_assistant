import json
from datetime import datetime

class Note:
    def __init__(self, id, title, content, timestamp=None):
        self.id = id
        self.title = title
        self.content = content
        if timestamp:
            self.timestamp = timestamp
        else:
            self.timestamp = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "timestamp": self.timestamp
        }

class TaskManager:
    def __init__(self, filename='tasks.json'):
        self.filename = filename
        self.tasks = self.load_tasks()

    def load_tasks(self):
        try:
            with open(self.filename, 'r', encoding='utf-8') as file:
                tasks_data = json.load(file)
                return [Task(**task) for task in tasks_data]
        except FileNotFoundError:
            return []

    def save_tasks(self):
        with open(self.filename, 'w', encoding='utf-8') as file:
            json.dump([task.to_dict() for task in self.tasks], file, ensure_ascii=False, indent=4)

    def add_task(self, title, description='', priority='Низкий', due_date=None):
        task_id = len(self.tasks) + 1
        new_task = Task(task_id, title, description, False, priority, due_date)
        self.tasks.append(new_task)
        self.save_tasks()
        print("Задача успешно добавлена!")

    def view_tasks(self):
        if not self.tasks:
            print("Нет доступных задач.")
            return
        for task in self.tasks:
            status = "Выполнена" if task.done else "Не выполнена"
            print(f"{task.id}: {task.title} | Статус: {status} | Приоритет: {task.priority} | Срок: {task.due_date}")

    def mark_task_done(self, task_id):
        task = next((t for t in self.tasks if t.id == task_id), None)
        if task:
            task.done = True
            self.save_tasks()
            print("Задача отмечена как выполненная!")
        else:
            print("Задача не найдена.")

    def edit_task(self, task_id, title=None, description=None, priority=None, due_date=None):
        task = next((t for t in self.tasks if t.id == task_id), None)
        if task:
            if title is not None:
                task.title = title
            if description is not None:
                task.description = description
            if priority is not None:
                task.priority = priority
            if due_date is not None:
                task.due_date = due_date
            self.save_tasks()
            print("Задача успешно отредактирована!")
        else:
            print("Задача не найдена.")

    def delete_task(self, task_id):
        task = next((t for t in self.tasks if t.id == task_id), None)
        if task:
            self.tasks.remove(task)
            self.save_tasks()
            print("Задача успешно удалена!")
        else:
            print("Задача не найдена.")

    def import_tasks(self, import_file):
        try:
            with open(import_file, 'r', encoding='utf-8') as file:
                imported_tasks = json.load(file)
                for imported_task in imported_tasks:
                    new_task = Task(**imported_task)
                    self.tasks.append(new_task)
                self.save_tasks()
                print("Задачи успешно импортированы!")
        except FileNotFoundError:
            print("Файл для импорта не найден.")

    def export_tasks(self, export_file):
        with open(export_file, 'w', encoding='utf-8') as file:
            json.dump([task.to_dict() for task in self.tasks], file, ensure_ascii=False, indent=4)
        print("Задачи успешно экспортированы!")

    def filter_tasks(self, status=None, priority=None):
        filtered_tasks = [task for task in self.tasks if
                          (status is None or task.done == status) and (priority is None or task.priority == priority)]

        if not filtered_tasks:
            print("Нет задач по заданным критериям.")
            return

        for task in filtered_tasks:
            status_str = "Выполнена" if task.done else "Не выполнена"
            print(
                f"{task.id}: {task.title} | Статус: {status_str} | Приоритет: {task.priority} | Срок: {task.due_date}")

class Task:
    def __init__(self, id, title, description='', done=False, priority='Низкий', due_date=None):
        self.id = id
        self.title = title
        self.description = description
        self.done = done
        self.priority = priority
        self.due_date = due_date if due_date else datetime.now().strftime("%d-%m-%Y")

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "done": self.done,
            "priority": self.priority,
            "due_date": self.due_date
        }

class NoteManager:
    def __init__(self, filename='notes.json'):
        self.filename = filename
        self.notes = self.load_notes()

    def load_notes(self):
        try:
            with open(self.filename, 'r', encoding='utf-8') as file:
                notes_data = json.load(file)
                return [Note(**note) for note in notes_data]
        except FileNotFoundError:
            return []

    def save_notes(self):
        with open(self.filename, 'w', encoding='utf-8') as file:
            json.dump([note.to_dict() for note in self.notes], file, ensure_ascii=False, indent=4)

    def create_note(self, title, content):
        note_id = len(self.notes) + 1
        new_note = Note(note_id, title, content)
        self.notes.append(new_note)
        self.save_notes()
        print("Заметка успешно создана!")

    def view_notes(self):
        if not self.notes:
            print("Нет доступных заметок.")
            return
        for note in self.notes:
            print(f"{note.id}: {note.title} (Создано: {note.timestamp})")

    def view_note_details(self, note_id):
        note = next((n for n in self.notes if n.id == note_id), None)
        if note:
            print(f"Заголовок: {note.title}\nСодержимое: {note.content}\nДата и время: {note.timestamp}")
        else:
            print("Заметка не найдена.")

    def edit_note(self, note_id, title=None, content=None):

        note = next((n for n in self.notes if n.id == note_id), None)
        if note:
            if title is not None:
                note.title = title
            if content is not None:
                note.content = content
            note.timestamp = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
            self.save_notes()
            print("Заметка успешно отредактирована!")
        else:
            print("Заметка не найдена.")

    def delete_note(self, note_id):
        note = next((n for n in self.notes if n.id == note_id), None)
        if note:
            self.notes.remove(note)
            self.save_notes()
            print("Заметка успешно удалена!")
        else:
            print("Заметка не найдена.")

    def import_notes(self, import_file):
        try:
            with open(import_file, 'r', encoding='utf-8') as file:
                imported_notes = json.load(file)
                for imported_note in imported_notes:
                    new_note = Note(**imported_note)
                    self.notes.append(new_note)
                self.save_notes()
                print("Заметки успешно импортированы!")
        except FileNotFoundError:
            print("Файл для импорта не найден.")

    def export_notes(self, export_file):
        with open(export_file, 'w', encoding='utf-8') as file:
            json.dump([note.to_dict() for note in self.notes], file, ensure_ascii=False, indent=4)
        print("Заметки успешно экспортированы!")

class Contact:
    def __init__(self, id, name, phone='', email=''):
        self.id = id
        self.name = name
        self.phone = phone
        self.email = email

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "phone": self.phone,
            "email": self.email
        }

class ContactManager:
    def __init__(self, filename='contacts.json'):
        self.filename = filename
        self.contacts = self.load_contacts()

    def load_contacts(self):
        try:
            with open(self.filename, 'r', encoding='utf-8') as file:
                contacts_data = json.load(file)
                return [Contact(**contact) for contact in contacts_data]
        except FileNotFoundError:
            return []

    def save_contacts(self):
        with open(self.filename, 'w', encoding='utf-8') as file:
            json.dump([contact.to_dict() for contact in self.contacts], file, ensure_ascii=False, indent=4)

    def add_contact(self, name, phone='', email=''):
        contact_id = len(self.contacts) + 1
        new_contact = Contact(contact_id, name, phone, email)
        self.contacts.append(new_contact)
        self.save_contacts()
        print("Контакт успешно добавлен!")

    def search_contact(self, search_term):
        found_contacts = [contact for contact in self.contacts if
                          search_term.lower() in contact.name.lower() or search_term in contact.phone]

        if not found_contacts:
            print("Контакты не найдены.")
            return

        for contact in found_contacts:
            print(f"{contact.id}: {contact.name} | Телефон: {contact.phone} | Email: {contact.email}")

    def edit_contact(self, contact_id, name=None, phone=None, email=None):
        contact = next((c for c in self.contacts if c.id == contact_id), None)

        if contact:
            if name is not None:
                contact.name = name
            if phone is not None:
                contact.phone = phone
            if email is not None:
                contact.email = email

            self.save_contacts()
            print("Контакт успешно отредактирован!")
        else:
            print("Контакт не найден.")

    def delete_contact(self, contact_id):
        contact = next((c for c in self.contacts if c.id == contact_id), None)

        if contact:
            self.contacts.remove(contact)
            self.save_contacts()
            print("Контакт успешно удален!")
        else:
            print("Контакт не найден.")

    def import_contacts(self, import_file):
        try:
            with open(import_file, 'r', encoding='utf-8') as file:
                imported_contacts = json.load(file)
                for imported_contact in imported_contacts:
                    new_contact = Contact(**imported_contact)
                    self.contacts.append(new_contact)
                self.save_contacts()
                print("Контакты успешно импортированы!")
        except FileNotFoundError:
            print("Файл для импорта не найден.")

    def export_contacts(self, export_file):
        with open(export_file, 'w', encoding='utf-8') as file:
            json.dump([contact.to_dict() for contact in self.contacts], file, ensure_ascii=False, indent=4)
        print("Контакты успешно экспортированы!")

class FinanceRecord:
    def __init__(self, id, amount, category, date, description=''):
        self.id = id
        self.amount = amount
        self.category = category
        self.date = date
        self.description = description

    def to_dict(self):
        return {
            "id": self.id,
            "amount": self.amount,
            "category": self.category,
            "date": self.date,
            "description": self.description
        }

class FinanceManager:
    def __init__(self, filename='finance.json'):
        self.filename = filename
        self.records = self.load_records()

    def load_records(self):
        try:
            with open(self.filename, 'r', encoding='utf-8') as file:
                records_data = json.load(file)
                return [FinanceRecord(**record) for record in records_data]
        except FileNotFoundError:
            return []

    def save_records(self):
        with open(self.filename, 'w', encoding='utf-8') as file:
            json.dump([record.to_dict() for record in self.records], file, ensure_ascii=False, indent=4)

    def add_record(self, amount, category, date, description=''):
        record_id = len(self.records) + 1
        new_record = FinanceRecord(record_id, amount, category, date, description)
        self.records.append(new_record)
        self.save_records()
        print("Финансовая запись успешно добавлена!")

    def view_records(self):
        if not self.records:
            print("Нет доступных финансовых записей.")
            return

        for record in self.records:
            print(
                f"{record.id}: {record.amount} | Категория: {record.category} | Дата: {record.date} | Описание: {record.description}")

    def filter_records(self, date=None, category=None):
        filtered_records = [
            record for record in self.records
            if
            (date is None or record.date == date) and (category is None or record.category.lower() == category.lower())
        ]

        if not filtered_records:
            print("Нет записей по заданным критериям.")
            return

        for record in filtered_records:
            print(
                f"{record.id}: {record.amount} | Категория: {record.category} | Дата: {record.date} | Описание: {record.description}")

    def generate_report(self, start_date=None, end_date=None):
        total_income = 0.0
        total_expense = 0.0

        for record in self.records:
            record_date = datetime.strptime(record.date, "%d-%m-%Y")

            if (start_date and record_date < start_date) or (end_date and record_date > end_date):
                continue

            if record.amount > 0:
                total_income += record.amount
            else:
                total_expense += abs(record.amount)

        print(f"Общий доход: {total_income:.2f}")
        print(f"Общие расходы: {total_expense:.2f}")
        print(f"Баланс: {total_income - total_expense:.2f}")

    def import_records(self, import_file):
        try:
            with open(import_file, 'r', encoding='utf-8') as file:
                imported_records = json.load(file)
                for imported_record in imported_records:
                    new_record = FinanceRecord(**imported_record)
                    self.records.append(new_record)
                self.save_records()
                print("Финансовые записи успешно импортированы!")
        except FileNotFoundError:
            print("Файл для импорта не найден.")

    def export_records(self, export_file):
        with open(export_file, 'w', encoding='utf-8') as file:
            json.dump([record.to_dict() for record in self.records], file, ensure_ascii=False, indent=4)
        print("Финансовые записи успешно экспортированы!")

def main_menu():
    while True:
        print("Добро пожаловать в Персональный помощник!")
        print("Выберите действие:")
        print("1. Управление заметками")
        print("2. Управление задачами")
        print("3. Управление контактами")
        print("4. Управление финансовыми записями")
        print("5. Калькулятор")
        print("6. Выход")

        choice = input("Введите номер действия: ")

        if choice == '1':
            manage_notes()
        elif choice == '2':
            manage_tasks()
        elif choice == '3':
            manage_contacts()
        elif choice == '4':
            manage_finances()
        elif choice == '5':
            calculator()
        elif choice == '6':
            print("Выход из приложения...")
            break
        else:
            print("Некорректный ввод. Пожалуйста, выберите номер от 1 до 6.")


def manage_notes():
    note_manager = NoteManager()

    while True:
        print("\nУправление заметками:")
        print("1. Создать новую заметку")
        print("2. Просмотреть список заметок")
        print("3. Просмотреть подробности заметки")
        print("4. Редактировать заметку")
        print("5. Удалить заметку")
        print("6. Импортировать заметки")
        print("7. Экспортировать заметки")
        print("8. Вернуться в главное меню")

        choice = input("Введите номер действия: ")

        if choice == '1':
            title = input("Введите заголовок: ")
            content = input("Введите содержимое: ")
            note_manager.create_note(title, content)

        elif choice == '2':
            note_manager.view_notes()

        elif choice == '3':
            note_id = input("Введите ID заметки: ")
            if set(note_id) < set('0123456789'):
                note_id = int(note_id)
            else:
                print("Ошибка: введен неверный id")
                continue
            note_manager.view_note_details(note_id)

        elif choice == '4':
            note_id = input("Введите ID заметки для редактирования: ")
            if set(note_id) < set('0123456789'):
                note_id = int(note_id)
            else:
                print("Ошибка: введен неверный id")
                continue
            title = input("Введите новый заголовок (или оставьте пустым для сохранения): ")
            content = input("Введите новое содержимое (или оставьте пустым для сохранения): ")
            note_manager.edit_note(note_id, title or None, content or None)

        elif choice == '5':
            note_id = input("Введите ID заметки для удаления: ")
            if set(note_id) < set('0123456789'):
                note_id = int(note_id)
            else:
                print("Ошибка: введен неверный id")
                continue
            note_manager.delete_note(note_id)

        elif choice == '6':
            import_file = input("Введите имя файла для импорта (например notes_import.json): ")
            note_manager.import_notes(import_file)

        elif choice == '7':
            export_file = input("Введите имя файла .json для экспорта (например notes_export.json): ")
            note_manager.export_notes(export_file)

        elif choice == '8':
            break

        else:
            print("Некорректный ввод. Пожалуйста, выберите номер от 1 до 8.")


def manage_tasks():
    task_manager = TaskManager()

    while True:
        print("\nУправление задачами:")
        print("1. Добавить новую задачу")
        print("2. Просмотреть список задач")
        print("3. Отметить задачу как выполненную")
        print("4. Редактировать задачу")
        print("5. Удалить задачу")
        print("6. Импортировать задачи")
        print("7. Экспортировать задачи")
        print("8. Фильтровать задачи")
        print("9. Вернуться в главное меню")

        choice = input("Введите номер действия: ")

        if choice == '1':
            title = input("Введите заголовок задачи: ")
            description = input("Введите описание задачи (по желанию): ")
            priority = input("Введите приоритет задачи (Высокий/Средний/Низкий): ")
            while True:
                due_date = input("Введите срок выполнения задачи (ДД-ММ-ГГГГ): ")
                try:
                    valid_date = datetime.strptime(due_date, "%d-%m-%Y")
                    due_date = valid_date.strftime("%d-%m-%Y")
                    break
                except ValueError:
                    print("Ошибка: Неверный формат даты. Пожалуйста, используйте формат ДД-ММ-ГГГГ.")
            task_manager.add_task(title, description, priority.capitalize(), due_date)

        elif choice == '2':
            task_manager.view_tasks()

        elif choice == '3':
            task_id = int(input("Введите ID задачи для отметки как выполненной: "))
            task_manager.mark_task_done(task_id)

        elif choice == '4':
            task_id = int(input("Введите ID задачи для редактирования: "))
            title = input("Введите новый заголовок (или оставьте пустым для сохранения): ")
            description = input("Введите новое описание (или оставьте пустым для сохранения): ")
            priority = input("Введите новый приоритет (или оставьте пустым для сохранения): ")
            while True:
                due_date = input("Введите срок выполнения задачи (ДД-ММ-ГГГГ): ")
                try:
                    valid_date = datetime.strptime(due_date, "%d-%m-%Y")
                    due_date = valid_date.strftime("%d-%m-%Y")
                    break
                except ValueError:
                    print("Ошибка: Неверный формат даты. Пожалуйста, используйте формат ДД-ММ-ГГГГ.")

            # Удаляем пустые значения перед передачей в метод редактирования.
            task_manager.edit_task(task_id,
                                   title or None,
                                   description or None,
                                   priority.capitalize() if priority else None,
                                   due_date or None)

        elif choice == '5':
            task_id = int(input("Введите ID задачи для удаления: "))
            task_manager.delete_task(task_id)

        elif choice == '6':
            import_file = input("Введите имя файла для импорта (например tasks_import.json): ")
            task_manager.import_tasks(import_file)

        elif choice == '7':
            export_file = input("Введите имя файла для экспорта (например tasks_export.json): ")
            task_manager.export_tasks(export_file)

        elif choice == '8':
            status_input = input(
                "Фильтровать по статусу (выполнена/не выполнена или оставить пустым): ").strip().lower()
            status_filter = None
            if status_input == 'выполнена':
                status_filter = True
            elif status_input == 'не выполнена':
                status_filter = False

            priority_input = input(
                "Фильтровать по приоритету (Высокий/Средний/Низкий или оставить пустым): ").strip().capitalize()

            # Если пользователь не ввел приоритет - оставляем его пустым.
            priority_filter = priority_input if priority_input in ['Высокий', 'Средний', 'Низкий'] else None

            # Вызываем метод фильтрации.
            task_manager.filter_tasks(status=status_filter, priority=priority_filter)

        elif choice == '9':
            break

        else:
            print("Некорректный ввод. Пожалуйста, выберите номер от 1 до 9.")


def manage_contacts():
    contact_manager = ContactManager()

    while True:
        print("\nУправление контактами:")
        print("1. Добавить новый контакт")
        print("2. Поиск контакта")
        print("3. Редактировать контакт")
        print("4. Удалить контакт")
        print("5. Импортировать контакты")
        print("6. Экспортировать контакты")
        print("7. Вернуться в главное меню")

        choice = input("Введите номер действия: ")

        if choice == '1':
            name = input("Введите имя контакта: ")
            phone = input("Введите номер телефона (по желанию): ")
            email = input("Введите адрес электронной почты (по желанию): ")
            contact_manager.add_contact(name, phone, email)

        elif choice == '2':
            search_term = input("Введите имя или номер телефона для поиска: ")
            contact_manager.search_contact(search_term)

        elif choice == '3':
            contact_id = int(input("Введите ID контакта для редактирования: "))
            name = input("Введите новое имя (или оставьте пустым для сохранения): ")
            phone = input("Введите новый номер телефона (или оставьте пустым для сохранения): ")
            email = input("Введите новый адрес электронной почты (или оставьте пустым для сохранения): ")

            # Удаляем пустые значения перед передачей в метод редактирования.
            contact_manager.edit_contact(contact_id,
                                         name or None,
                                         phone or None,
                                         email or None)

        elif choice == '4':
            contact_id = input("Введите ID контакта для удаления: ")
            if set(contact_id) < set('0123456789'):
                contact_id = int(contact_id)
            else:
                print("Ошибка: введен неверный id")
                continue
            contact_manager.delete_contact(contact_id)

        elif choice == '5':
            import_file = input("Введите имя файла для импорта (например contacts_import.json): ")
            contact_manager.import_contacts(import_file)

        elif choice == '6':
            export_file = input("Введите имя файла для экспорта (например contacts_export.json): ")
            contact_manager.export_contacts(export_file)

        elif choice == '7':
            break

        else:
            print("Некорректный ввод. Пожалуйста, выберите номер от 1 до 7.")


def manage_finances():
    finance_manager = FinanceManager()

    while True:
        print("\nУправление финансовыми записями:")
        print("1. Добавить новую финансовую запись")
        print("2. Просмотреть все записи")
        print("3. Фильтровать записи")
        print("4. Генерировать отчет")
        print("5. Импортировать записи")
        print("6. Экспортировать записи")
        print("7. Вернуться в главное меню")

        choice = input("Введите номер действия: ")

        if choice == '1':
            amount = float(input("Введите сумму операции (положительное для дохода и отрицательное для расхода): "))
            category = input("Введите категорию операции: ")
            while True:
                date = input("Введите срок выполнения задачи (ДД-ММ-ГГГГ): ")
                try:
                    valid_date = datetime.strptime(date, "%d-%m-%Y")
                    date = valid_date.strftime("%d-%m-%Y")
                    break
                except ValueError:
                    print("Ошибка: Неверный формат даты. Пожалуйста, используйте формат ДД-ММ-ГГГГ.")
            description = input("Введите описание операции (по желанию): ")
            finance_manager.add_record(amount, category, date, description)

        elif choice == '2':
            finance_manager.view_records()

        elif choice == '3':
            while True:
                date = input("Введите дату операции (ДД-ММ-ГГГГ) или оставьте пустым: ")
                if date == '':
                    break
                try:
                    valid_date = datetime.strptime(date, "%d-%m-%Y")
                    date = valid_date.strftime("%d-%m-%Y")
                    break
                except ValueError:
                    print("Ошибка: Неверный формат даты. Пожалуйста, используйте формат ДД-ММ-ГГГГ.")
            category = input("Введите категорию для фильтрации (или оставьте пустым): ")

            # Убираем пустые значения перед передачей в метод фильтрации.
            finance_manager.filter_records(date or None, category or None)

        elif choice == '4':
            while True:
                start_date_input = input("Введите начальную дату для отчета (ДД-ММ-ГГГГ или оставить пустым): ")
                if start_date_input == '':
                    break
                try:
                    valid_date = datetime.strptime(start_date_input, "%d-%m-%Y")
                    start_date_input = valid_date.strftime("%d-%m-%Y")
                    break
                except ValueError:
                    print("Ошибка: Неверный формат даты. Пожалуйста, используйте формат ДД-ММ-ГГГГ.")
            while True:
                end_date_input = input("Введите конечную дату для отчета (ДД-ММ-ГГГГ или оставить пустым): ")
                if end_date_input == '':
                    break
                try:
                    valid_date = datetime.strptime(end_date_input, "%d-%m-%Y")
                    end_date_input = valid_date.strftime("%d-%m-%Y")
                    break
                except ValueError:
                    print("Ошибка: Неверный формат даты. Пожалуйста, используйте формат ДД-ММ-ГГГГ.")

            start_date = datetime.strptime(start_date_input, "%d-%m-%Y") if start_date_input else None
            end_date = datetime.strptime(end_date_input, "%d-%m-%Y") if end_date_input else None

            finance_manager.generate_report(start_date=start_date, end_date=end_date)

        elif choice == '5':
            import_file = input("Введите имя файла для импорта (например finance_import.json): ")
            finance_manager.import_records(import_file)

        elif choice == '6':
            export_file = input("Введите имя файла для экспорта (например finance_export.json): ")
            finance_manager.export_records(export_file)

        elif choice == '7':
            break

        else:
            print("Некорректный ввод. Пожалуйста, выберите номер от 1 до 7.")


def calculator():
    print("Добро пожаловать в калькулятор!")

    while True:
        print("\nВыберите операцию:")
        print("1. Сложение")
        print("2. Вычитание")
        print("3. Умножение")
        print("4. Деление")
        print("5. Выход")

        choice = input("Введите номер операции (1-5): ")

        if choice == '5':
            print("Выход из калькулятора...")
            break

        if choice in ['1', '2', '3', '4']:
            try:
                num1 = float(input("Введите первое число: "))
                num2 = float(input("Введите второе число: "))

                if choice == '1':
                    result = num1 + num2
                    operation = "Сложение"
                elif choice == '2':
                    result = num1 - num2
                    operation = "Вычитание"
                elif choice == '3':
                    result = num1 * num2
                    operation = "Умножение"
                elif choice == '4':
                    if num2 == 0:
                        raise ZeroDivisionError("Ошибка: Деление на ноль невозможно.")
                    result = num1 / num2
                    operation = "Деление"

                print(f"Результат {operation}: {result:.2f}")

            except ValueError:
                print("Ошибка: Пожалуйста, введите корректные числа.")
            except ZeroDivisionError as e:
                print(e)
            except Exception as e:
                print(f"Произошла ошибка: {e}")
        else:
            print("Некорректный ввод. Пожалуйста, выберите номер от 1 до 5.")


if __name__ == "__main__":
    main_menu()