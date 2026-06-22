from app.services.email_templates import money, order_items_html, order_items_text, render_email


def test_money_formats_inr_and_empty_values():
    assert money(1250) == "INR 1250"
    assert money("") == "-"
    assert money(None) == "-"


def test_order_items_render_text_and_html_escape_values():
    items = [{"product_name": "ACME <Widget>", "quantity": 2, "unit_price": 99}]

    text = order_items_text(items)
    html = order_items_html(items)

    assert "ACME <Widget>" in text
    assert "Qty: 2" in text
    assert "INR 99" in text
    assert "ACME &lt;Widget&gt;" in html
    assert "<Widget>" not in html
    assert "INR 99" in html


def test_render_email_has_branded_layout_status_pill_and_plain_text_fallback():
    text, html = render_email(
        eyebrow="Payment received",
        title="Invoice #42 is paid",
        greeting_name="Sahana",
        intro="We have received the payment for this invoice.",
        details=[("Invoice", "#42"), ("Status", "PAID")],
        text_extra="Thank you for your payment.",
        html_extra='<p style="margin:0;">Thank you for your payment.</p>',
    )

    assert "Hello Sahana," in text
    assert "Status: PAID" in text
    assert "Opslora" in html
    assert "linear-gradient" in html
    assert "Invoice #42 is paid" in html
    assert "PAID" in html
    assert "border-radius:999px" in html
    assert "Thank you for your payment." in html
