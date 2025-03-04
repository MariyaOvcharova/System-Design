from fastapi import FastAPI, HTTPException
from enum import Enum
import logging

app = FastAPI()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# enam для статусов
class OrderStatus(str, Enum):
    PENDING = "pending"
    PAYMENT_SUCCESS = "payment_success"
    PAYMENT_FAILED = "payment_failed"
    INVENTORY_SUCCESS = "inventory_success"
    INVENTORY_FAILED = "inventory_failed"
    SHIPPING_SUCCESS = "shipping_success"
    SHIPPING_FAILED = "shipping_failed"
    ROLLBACK_COMPLETED = "rollback_completed"


def process_payment(order_id: int) -> bool:
    """
    Эмулирует процесс оплаты.
    Возвращает True, если оплата успешна, и False, если нет.
    """
    return order_id % 2 != 0  # Четные id проваливают оплату

def reserve_inventory(order_id: int) -> bool:
    """
    Эмулирует процесс резервирования товара.
    Возвращает True, если резерв успешен, и False, если нет.
    """
    return order_id % 3 != 0  # Id, кратные 3, проваливают резерв

def ship_order(order_id: int) -> bool:
    #доставка (true если доставленно и false усли нет)
    return order_id % 5 != 0  # Id, кратные 5, проваливают доставку

def refund_payment(order_id: int):
    #возврат оплаты
    logger.warning(f"Refunding payment for order {order_id}")

def release_inventory(order_id: int):
     #резерв
    logger.warning(f"Releasing inventory for order {order_id}")

@app.get("/")
async def root():
    return {"message": "def"}


@app.post("/checkout/{order_id}")
async def checkout(order_id: int):
    
    logger.info(f"Processing order {order_id}...")

    #Оплата
    if not process_payment(order_id):
        logger.error(f"Payment failed for order {order_id}")
        return {
            "error": "Payment failed",
            "rollback": "None"
        }

    logger.info(f"Payment successful for order {order_id}")

    #Резерв товара
    if not reserve_inventory(order_id):
        logger.error(f"Inventory reservation failed for order {order_id}")
        refund_payment(order_id)
        return {
            "error": "Inventory reservation failed",
            "rollback": "Payment refunded"
        }

    logger.info(f"Inventory reserved for order {order_id}")

    #Доставка
    if not ship_order(order_id):
        logger.error(f"Shipping failed for order {order_id}")
        refund_payment(order_id)
        release_inventory(order_id)
        return {
            "error": "Shipping failed",
            "rollback": "Payment refunded, Inventory released"
        }

    logger.info(f"Order {order_id} shipped successfully!")

    #Успешно
    return {"status": "Order processed successfully"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
