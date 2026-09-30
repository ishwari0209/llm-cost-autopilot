from decimal import Decimal

from app.db.models import LLMModel, User
from app.db.session import Base, SessionLocal, engine

# TODO: replace every price with the current paid-tier price per 1M tokens
MODELS = [
    ("gemini", "gemini-3.5-flash-lite", Decimal("0.30"), Decimal("2.50")),
    ("gemini", "gemini-3.6-flash",      Decimal("0.75"), Decimal("3.75")),
    ("gemini", "gemini-3.1-pro-preview", Decimal("2.00"), Decimal("12.00")),
]

Base.metadata.create_all(bind=engine)

with SessionLocal() as db:
    if not db.get(User, 1):
        db.add(User(id=1, name="Test User", email="test@example.com"))
    for provider, name, inp, out in MODELS:
        row = db.query(LLMModel).filter_by(model_name=name).first()
        if row:
            row.input_price_per_1m, row.output_price_per_1m = inp, out
        else:
            db.add(LLMModel(provider=provider, model_name=name,
                            input_price_per_1m=inp, output_price_per_1m=out))
    db.commit()
print("Seeded.")