import datetime

WEBSITE_URL = "https://notrix.io"

class CheckoutSessionLineItem:
    def __init__(
        self,
        name: str,
        description: str,
        imageURL: str,
        price: float,
        quantity: int,
        **kwargs,
    ):
        self.name = name
        self.description = description
        self.imageURL = imageURL
        self.price = price
        self.quantity = quantity

    def dict(self):
        return {
            "name": self.name,
            "description": self.description,
            "imageURL": self.image,
            "price": self.price,
            "quantity": self.quantity,
        }


class CheckoutSession:
    def __init__(
        self,
        uuid: str,
        lineItems: list,
        totalAmount: str,
        successURL: str,
        cancelURL: str,
        clientReferenceID: str,
        webhookURL: str,
        paymentRequestToken: str,
        active: bool,
        status: str,
        expires_at: str,
    ):
        self.uuid = uuid
        self.lineItems = [CheckoutSessionLineItem(**item) for item in lineItems]
        self.totalAmount = totalAmount
        self.successURL = successURL
        self.cancelURL = cancelURL
        self.clientReferenceID = clientReferenceID
        self.webhookURL = webhookURL
        self.paymentRequestToken = paymentRequestToken
        self.expires_at = datetime.datetime.fromisoformat(expires_at[:-1])  # Remove Z
        self.active = active
        self.status = status

    def link(self) -> str:
        return f"{WEBSITE_URL}/pay/{self.paymentRequestToken}"
