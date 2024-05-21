# from beanie import init_beanie
# from app.configs.app import settings
# from motor.motor_asyncio import (
#     AsyncIOMotorClient,
# )

# from app.models.endec_decoder import Decoder
# from app.models.endec_encoder import Encoder


# models = [Encoder,Decoder]

# async def connect_database() -> None:
#     print("Connecting to database...")
#     url = f"mongodb://{settings.MONGODB_USERNAME}:{settings.MONGODB_PASSWORD}@{settings.MONGODB_HOST}:27017/{settings.MONGODB_DATABASE}?authSource=admin&ssl=false"
#     client = AsyncIOMotorClient(url)

#     await init_beanie(database=client["scigpt_db"], document_models=models)
