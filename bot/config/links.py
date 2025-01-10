LINKS = {
    "Доступы": {
        "key": "dostupy",  # Ключ для раздела
        "subsections": {
            "Доступ на препрод (Ivanti Mobile)": {
                "key": "mobile_iron",  # Ключ для подраздела
                "url": "https://sfera.inno.local/knowledge/pages?id=851177",
                "regex": [
                    r"\bдоступ на препрод\b",
                    r"\bдоступ на ПП\b",
                    r"\bмобайл ирон\b",
                    r"\bиванти.*",
                    r"\bпрепрод.*",
                    r"\bПП.*",
                    r"\bmobile.*",
                    r"\bivanti.*"
                ]
            },
            "ЕКА, Трассировка, Аудит": {
                "key": "eka",
                "url": "https://sfera.inno.local/knowledge/pages?id=851149",
                "regex": [
                    r"\bека.*",
                    r"\bтрассировка.*",
                    r"\bаудит.*"
                ]
            },
            "Ключ-астром": {
                "key": "key_astrom",
                "url": "https://sfera.inno.local/knowledge/pages?id=1150161",
                "regex": [
                    r"\bключ-астром.*",
                    r"\bключастром.*",
                    r"\bастром.*"
                ]
            },
            "ФРКК": {
                "key": "frkk",
                "url": "https://sfera.inno.local/knowledge/pages?id=958462",
                "regex": [
                    r"\bфркк.*"
                ]
            },
            "Настройка Charles": {
                "key": "charles",
                "url": "https://sfera.inno.local/knowledge/pages?id=851289",
                "regex": [
                    r"\bcharles.*",
                    r"\bчарльз.*",
                    r"\bчарлик.*"
                ]
            },
            "Создание учетной записи в домене TEST": {
                "key": "test_account",
                "url": "https://sfera.inno.local/knowledge/pages?id=852129",
                "regex": [
                    r"\тест учетка\b",
                    r"\тест уз\b",
                    r"\тестовая учетка\b",
                    r"\bтестова.*",
                    r"\тест учетк.*\b"
                ]
            }
        }
    },
    "Полезные ссылки": {
        "key": "useful_links",
        "subsections": {
            "Гайд встраивание СУБО в МБ": {
                "key": "subo_integration",
                "url": "https://sfera.inno.local/knowledge/pages?id=852814",
                "regex": [
                    r"\встроить субо\b",
                    r"\встраивание субо\b"
                ]
            },
            "Ошибки авторизации": {
                "key": "auth_errors",
                "url": "https://sfera.inno.local/knowledge/pages?id=852172",
                "regex": [
                    r"\ошибки авторизации\b"
                ]
            },
            "Чеклист локализации проблем в МБ": {
                "key": "problems_checklist",
                "url": "https://sfera.inno.local/knowledge/pages?id=852073",
                "regex": [
                    r"\локализация проблем\b",
                    r"\чеклист локализации\b"
                ]
            },
            "Инженерное меню в приложении": {
                "key": "engineer_menu",
                "url": "https://sfera.inno.local/knowledge/pages?id=851821",
                "regex": [
                    r"\bинженерное меню\b"
                ]
            },
            "Матрица девайсов для тестирования МП": {
                "key": "device_matrix",
                "url": "https://sfera.inno.local/knowledge/pages?id=851317",
                "regex": [
                    r"\bматрица.*",
                    r"\bустройства.*"
                ]
            },
            "Tech Talk": {
                "key": "tech_talk",
                "url": "https://sfera.inno.local/knowledge/pages?id=852633",
                "regex": [
                    r"\bмитап.*",
                    r"\btech talk\b"
                ]
            },
            "График Релизов МБ СМБ 2025": {
                "key": "release_schedule_2025",
                "url": "https://sfera.inno.local/knowledge/pages?id=1378929",
                "regex": [
                    r"\bграфик.*",
                    r"\bрелиз.*"
                ]
            }
        }
    },
    "Положения по тестированию МБ": {
        "key": "testing_rules",
        "subsections": {
            "Какие бывают сборки МБ": {
                "key": "builds_mb",
                "url": "https://sfera.inno.local/knowledge/pages?id=1335040"
            },
            "На каких контурах проходит тестирования МБ": {
                "key": "test_env_mb",
                "url": "https://sfera.inno.local/knowledge/pages?id=1335041"
            },
            "Приемка модулей СУБО в канал МБ": {
                "key": "module_acceptance",
                "url": "https://sfera.inno.local/knowledge/pages?id=1335043"
            },
            "Регресс и Smoke тестирование СУБО в МБ": {
                "key": "regression_smoke",
                "url": "https://sfera.inno.local/knowledge/pages?id=1335044"
            },
            "Правила заведения ТК в МБ": {
                "key": "tc_rules",
                "url": "https://sfera.inno.local/knowledge/pages?id=1335042"
            },
            "Шаблоны ТК": {
                "key": "tc_templates",
                "url": "https://sfera.inno.local/knowledge/pages?id=1421077"
            }
        }
    },
    "Builder BOT": {
        "key": "builder_bot",
        "url": "https://t.me/vtb_builder_bot",
        "regex": [
            r"\взять сборку\b",
            r"\получить сборку\b",
            r"\брать сборку\b"
        ]
    },
    "Бот для расшифровки аббривеатур ВТБ": {
        "key": "builder_bot",
        "url": "https://t.me/BankAcronymBot"
    }
}
