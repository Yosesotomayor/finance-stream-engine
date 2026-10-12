from ..models.transaction_event import TransactionEvent
from datetime import datetime
from faker import Faker

faker = Faker(["en_US"])


class TransactionGenerator:
    def generate_transaction(self) -> TransactionEvent:
        return TransactionEvent(
            transaction_id=faker.uuid4(),
            user_id=str(faker.random_int(min=1001, max=999999)),
            merchant_id=str(faker.random_int(min=1001, max=999999)),
            amount=float(faker.pydecimal(left_digits=5, right_digits=2, positive=True)),
            status=faker.random_element(elements=["pending", "completed", "failed", "refunded"]),
            timestamp=faker.date_time_between(
                start_date=datetime(2026, 1, 1),
                end_date=datetime.now(),
            ),
        )