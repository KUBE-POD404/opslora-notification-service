from __future__ import annotations

from html import escape
from typing import Iterable


BRAND_NAME = "Opslora"
SUPPORT_LINE = "This notification was sent by Opslora. If something looks wrong, contact your Opslora administrator."
BRAND_GRADIENT = "linear-gradient(135deg,#4f46e5 0%,#7c3aed 52%,#db2777 100%)"

STATUS_STYLES = {
    "CREATED": ("#eef2ff", "#4338ca"),
    "CONFIRMED": ("#ecfdf5", "#047857"),
    "PAID": ("#ecfdf5", "#047857"),
    "REFUNDED": ("#eff6ff", "#1d4ed8"),
    "UNPAID": ("#fff7ed", "#c2410c"),
    "CANCELLED": ("#fef2f2", "#b91c1c"),
}


def _format_value(value) -> str:
    if value is None:
        return "-"
    return str(value)


def money(value) -> str:
    if value in (None, ""):
        return "-"
    return f"INR {_format_value(value)}"


def _status_pill(value: str) -> str:
    normalized = _format_value(value).upper()
    bg, fg = STATUS_STYLES.get(normalized, ("#f4f4f5", "#3f3f46"))
    return (
        f'<span style="display:inline-block;padding:5px 10px;border-radius:999px;'
        f'background:{bg};color:{fg};font-size:12px;font-weight:700;letter-spacing:.02em;">'
        f"{escape(normalized)}</span>"
    )


def _render_detail_value(label: str, value) -> str:
    if label.strip().lower() == "status":
        return _status_pill(_format_value(value))
    return escape(_format_value(value))


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
        return (
            '<div style="margin-top:8px;border:1px dashed #d4d4d8;border-radius:14px;'
            'padding:14px;color:#71717a;background:#fafafa;">No items found.</div>'
        )

    body = []
    for item in rows:
        product_name = escape(_format_value(item.get("product_name")))
        quantity = escape(_format_value(item.get("quantity")))
        unit_price = escape(money(item.get("unit_price")))
        body.append(
            "<tr>"
            f'<td style="padding:12px 0;border-top:1px solid #e4e4e7;color:#18181b;font-weight:600;">{product_name}</td>'
            f'<td style="padding:12px 0;border-top:1px solid #e4e4e7;color:#52525b;text-align:right;">{quantity}</td>'
            f'<td style="padding:12px 0;border-top:1px solid #e4e4e7;color:#18181b;font-weight:700;text-align:right;">{unit_price}</td>'
            "</tr>"
        )

    return (
        '<table role="presentation" width="100%" cellpadding="0" cellspacing="0" '
        'style="border-collapse:collapse;margin-top:10px;background:#ffffff;border-radius:14px;overflow:hidden;">'
        '<thead><tr>'
        '<th align="left" style="padding:0 0 10px;color:#71717a;font-size:12px;font-weight:700;text-transform:uppercase;letter-spacing:.06em;">Item</th>'
        '<th align="right" style="padding:0 0 10px;color:#71717a;font-size:12px;font-weight:700;text-transform:uppercase;letter-spacing:.06em;">Qty</th>'
        '<th align="right" style="padding:0 0 10px;color:#71717a;font-size:12px;font-weight:700;text-transform:uppercase;letter-spacing:.06em;">Price</th>'
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
        f'<td style="padding:12px 0;color:#71717a;width:42%;font-size:13px;font-weight:600;text-transform:uppercase;letter-spacing:.04em;">{escape(label)}</td>'
        f'<td style="padding:12px 0;color:#18181b;font-weight:700;text-align:right;font-size:14px;">{_render_detail_value(label, value)}</td>'
        "</tr>"
        for label, value in details
    )

    details_block = ""
    if detail_rows:
        details_block = (
            '<table role="presentation" width="100%" cellpadding="0" cellspacing="0" '
            'style="border-collapse:collapse;margin:24px 0;background:#fafafa;border:1px solid #e4e4e7;border-radius:16px;overflow:hidden;">'
            f'<tbody><tr><td style="padding:8px 18px;"><table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="border-collapse:collapse;">{detail_rows}</table></td></tr></tbody></table>'
        )

    html = f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width,initial-scale=1">
    <meta name="color-scheme" content="light">
    <title>{escape(title)}</title>
  </head>
  <body style="margin:0;background:#f4f4f5;padding:0;font-family:Inter,Segoe UI,Arial,sans-serif;color:#18181b;">
    <div style="display:none;max-height:0;overflow:hidden;color:transparent;opacity:0;">{escape(intro)}</div>
    <table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="border-collapse:collapse;background:#f4f4f5;">
      <tr>
        <td align="center" style="padding:32px 16px;">
          <table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="max-width:620px;border-collapse:separate;border-spacing:0;background:#ffffff;border:1px solid #e4e4e7;border-radius:22px;overflow:hidden;box-shadow:0 22px 60px rgba(15,23,42,.10);">
            <tr>
              <td style="background:{BRAND_GRADIENT};padding:30px 30px 28px;color:#ffffff;">
                <table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="border-collapse:collapse;">
                  <tr>
                    <td style="font-size:18px;font-weight:800;letter-spacing:-.02em;">{BRAND_NAME}</td>
                    <td align="right"><span style="display:inline-block;padding:6px 10px;border-radius:999px;background:rgba(255,255,255,.18);color:#ffffff;font-size:12px;font-weight:700;">{escape(eyebrow)}</span></td>
                  </tr>
                </table>
                <h1 style="margin:22px 0 0;font-size:28px;line-height:1.18;font-weight:800;letter-spacing:-.03em;color:#ffffff;">{escape(title)}</h1>
              </td>
            </tr>
            <tr>
              <td style="padding:30px;">
                <p style="margin:0 0 12px;font-size:16px;line-height:1.6;color:#18181b;">Hello <strong>{escape(greeting_name)}</strong>,</p>
                <p style="margin:0;font-size:16px;line-height:1.65;color:#3f3f46;">{escape(intro)}</p>
                {details_block}
                {html_extra}
                <div style="margin:28px 0 0;padding:18px 20px;background:#f8fafc;border:1px solid #e2e8f0;border-radius:16px;">
                  <p style="margin:0;font-size:15px;line-height:1.6;color:#334155;">Regards,<br><strong>{BRAND_NAME} Team</strong></p>
                </div>
              </td>
            </tr>
            <tr>
              <td style="padding:20px 30px;background:#18181b;color:#d4d4d8;font-size:12px;line-height:1.6;">
                {escape(SUPPORT_LINE)}
              </td>
            </tr>
          </table>
        </td>
      </tr>
    </table>
  </body>
</html>"""
    return "\n".join(text_lines), html
