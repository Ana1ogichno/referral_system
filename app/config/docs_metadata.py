from app.config.error_codes import ErrorCodes

tags_metadata = [
    {
        "name": "User",
        "description": "User logic",
    },
    {
        "name": "Auth",
        "description": "Basic login/logout logic",
    },
    # ...other route groups
]


def generate_doc_errors():
    return "\n".join(
        [f"| {err.value[0]} | {err.value[1]} | {err.value[2]}" for err in ErrorCodes]
    )


app_description = f"""
<details>
<summary>Коды возможных ошибок сервиса</summary>
<br>

| Код ошибки | Имя ошибки                | Описание       |
|------------|---------------------------|----------------|
{generate_doc_errors()}
</details>
"""  # noqa: E501
