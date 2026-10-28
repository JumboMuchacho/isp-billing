from app.core.config import get_settings


class MpesaService:
    def initiate_stk_push(self, phone: str, amount: str, account_ref: str) -> dict:
        settings = get_settings()
        return {
            "status": "queued",
            "phone": phone,
            "amount": amount,
            "account_ref": account_ref,
            "shortcode": settings.mpesa_shortcode,
            "callback_url": settings.mpesa_callback_url,
        }

    def handle_callback(self, payload: dict) -> dict:
        return {"status": "received", "payload": payload}
