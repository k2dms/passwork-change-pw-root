# passwork-change-pw-root

## Описание
Этот проект автоматизирует смену root-паролей на Linux-серверах с использованием Passwork API и Ansible, вызываемых через Jenkins Pipeline.

## Структура
- `ansible-project/` - Ansible-плейбуки и роли.
- `scripts/` - Вспомогательные скрипты (например, работа с Passwork API).
- `Jenkinsfile` - Пайплайн Jenkins.
- `README.md` - Описание.

## Установка
1. Настройте Jenkins с нужными credentials.
2. Заполните `group_vars/all.yml`.
3. Запустите Jenkins Job.
