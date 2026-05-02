from app.services.email_service import send_email


def test_send_email_skips_starttls_and_login_when_disabled(monkeypatch):
    calls = []

    class SMTPStub:
        def __init__(self, host, port):
            calls.append(("connect", host, port))

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb):
            return False

        def starttls(self):
            calls.append(("starttls",))

        def login(self, user, password):
            calls.append(("login", user, password))

        def send_message(self, message):
            calls.append(("send_message", message["To"], message["Subject"]))

    monkeypatch.setattr("smtplib.SMTP", SMTPStub)

    send_email("buyer@example.com", "Hello", "Body")

    assert ("connect", "localhost", 1025) in calls
    assert ("starttls",) not in calls
    assert not any(call[0] == "login" for call in calls)
    assert ("send_message", "buyer@example.com", "Hello") in calls


def test_format_order_items_handles_empty_and_items():
    from app.tasks.order_email_tasks import format_order_items

    assert format_order_items([]) == "No items found."
    formatted = format_order_items([{"product_name": "Item A", "quantity": 2, "unit_price": 100}])

    assert "Item A" in formatted
    assert "Qty: 2" in formatted
