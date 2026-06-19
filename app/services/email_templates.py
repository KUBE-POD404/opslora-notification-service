from __future__ import annotations

from html import escape
from typing import Iterable


BRAND_NAME = "Opslora"
SUPPORT_LINE = "This notification was sent by Opslora."


def _format_value(value) -> str:
    if value is None:
        return "-"
    return str(value)


def money(value) -> str:
    if value in (None, ""):
        return "-"
    return f"INR {_format_value(value)}"


def order_items_text(items: Iterable[dict]) -> str:
    rows = list(items or [])
    if not rows:
        return "No items found."

    lines = []
    for item in rows:
        product_name = _format_value(item.get("product_name"))
        quantity = _format_value(item.get("quantity"))
        unit_price = money(item.get("unit_price"))
        lines.append(f"- {product_name} | Qty: {quantity} | Price: {unit_price}")
    return "\n".join(lines)


def order_items_html(items: Iterable[dict]) -> str:
    rows = list(items or [])
    if not rows:
        return '<p style="margin:0;color:#71717a;">No items found.</p>'

    body = []
    for item in rows:
        product_name = escape(_format_value(item.get("product_name")))
        quantity = escape(_format_value(item.get("quantity")))
        unit_price = escape(money(item.get("unit_price")))
        body.append(
            "<tr>"
            f'<td style="padding:10px 0;border-top:1px solid #e5e7eb;color:#18181b;">{product_name}</td>'
            f'<td style="padding:10px 0;border-top:1px solid #e5e7eb;color:#52525b;text-align:right;">{quantity}</td>'
            f'<td style="padding:10px 0;border-top:1px solid #e5e7eb;color:#52525b;text-align:right;">{unit_price}</td>'
            "</tr>"
        )

    return (
        '<table role="presentation" width="100%" cellpadding="0" cellspacing="0" '
        'style="border-collapse:collapse;margin-top:8px;">'
        '<thead><tr>'
        '<th align="left" style="padding:0 0 8px;color:#71717a;font-size:12px;font-weight:600;">Item</th>'
        '<th align="right" style="padding:0 0 8px;color:#71717a;font-size:12px;font-weight:600;">Qty</th>'
        '<th align="right" style="padding:0 0 8px;color:#71717a;font-size:12px;font-weight:600;">Price</th>'
        "</tr></thead><tbody>"
        + "".join(body)
        + "</tbody></table>"
    )


def render_email(
    *,
    eyebrow: str,
    title: str,
    greeting_name: str = "Customer",
    intro: str,
    details: list[tuple[str, str]] | None = None,
    html_extra: str = "",
    text_extra: str = "",
) -> tuple[str, str]:
    details = details or []

    text_lines = [f"Hello {greeting_name},", "", intro, ""]
    for label, value in details:
        text_lines.append(f"{label}: {value}")
    if text_extra:
        text_lines.extend(["", text_extra])
    text_lines.extend(["", "Regards,", "Opslora Team", "", SUPPORT_LINE])

    detail_rows = "".join(
        "<tr>"
        f'<td style="padding:8px 0;color:#71717a;width:40%;">{escape(label)}</td>'
        f'<td style="padding:8px 0;color:#18181b;font-weight:600;text-align:right;">{escape(_format_value(value))}</td>'
        "</tr>"
        for label, value in details
    )

    details_block = ""
    if detail_rows:
        details_block = (
            '<table role="presentation" width="100%" cellpadding="0" cellspacing="0" '
            'style="border-collapse:collapse;margin:18px 0;border-top:1px solid #e5e7eb;border-bottom:1px solid #e5e7eb;">'
            f"{detail_rows}</table>"
        )

    html = f"""<!doctype html>
<html>
  <body style="margin:0;background:#f4f4f5;padding:24px;font-family:Inter,Segoe UI,Arial,sans-serif;color:#18181b;">
    <table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="border-collapse:collapse;">
      <tr>
        <td align="center">
          <table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="max-width:560px;border-collapse:collapse;background:#ffffff;border:1px solid #e5e7eb;">
            <tr>
              <td style="padding:28px 28px 20px;border-bottom:1px solid #e5e7eb;">
                <div style="font-size:13px;letter-spacing:0;color:#71717a;">{escape(eyebrow)}</div>
                <h1 style="margin:8px 0 0;font-size:24px;line-height:1.25;font-weight:650;color:#18181b;">{escape(title)}</h1>
              </td>
            </tr>
            <tr>
              <td style="padding:28px;">
                <p style="margin:0 0 14px;font-size:15px;line-height:1.6;color:#18181b;">Hello {escape(greeting_name)},</p>
                <p style="margin:0;font-size:15px;line-height:1.6;color:#3f3f46;">{escape(intro)}</p>
                {details_block}
                {html_extra}
                <p style="margin:24px 0 0;font-size:15px;line-height:1.6;color:#3f3f46;">Regards,<br>{BRAND_NAME} Team</p>
              </td>
            </tr>
            <tr>
              <td style="padding:18px 28px;background:#fafafa;border-top:1px solid #e5e7eb;color:#71717a;font-size:12px;line-height:1.5;">
                {SUPPORT_LINE}
              </td>
            </tr>
          </table>
        </td>
      </tr>
    </table>
  </body>
</html>"""
    return "\n".join(text_lines), html
