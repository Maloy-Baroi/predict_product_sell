from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from app.core.redis_setup import get_redis_client
from app.utils.prediction import load_and_predict

router = APIRouter()


class ProductBase(BaseModel):
    product_name: str


@router.post('/predict-next-sell')
def predict_next_sell(productBase: ProductBase):
    posted_product_name = productBase.product_name
    try:
        # Loading and predicting with the saved model
        closest_match, prediction_1, prediction_2 = load_and_predict(
            posted_product_name)
        redis_client = get_redis_client()
        prediction_1st_month_at_redis = redis_client.get(
            f"prediction_{closest_match}_1st_month")
        prediction_2nd_month_at_redis = redis_client.get(
            f"prediction_{closest_match}_2nd_month")
        if prediction_1st_month_at_redis and prediction_2nd_month_at_redis:
            response = {
                "next_1": prediction_1st_month_at_redis.decode('utf-8'),
                "next_2": prediction_2nd_month_at_redis.decode('utf-8'),
            }
            return JSONResponse(content=response, status_code=200)
        else:
            prediction_1st_month_at_redis = redis_client.set(
                f"prediction_{closest_match}_1st_month", prediction_1)
            prediction_2nd_month_at_redis = redis_client.set(
                f"prediction_{closest_match}_2nd_month", prediction_2)
            response = {
                "next_1": prediction_1,
                "next_2": prediction_2,
            }
            return JSONResponse(content=response, status_code=200)
    except Exception as e:
        return JSONResponse({'message': str(e)}, status_code=400)
