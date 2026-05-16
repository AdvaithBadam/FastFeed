from dotenv import load_dotenv
from imagekitio import AsyncImageKit
import os

load_dotenv()

IMAGEKIT_PUBLIC_KEY = os.getenv("IMAGEKIT_PUBLIC_KEY")
IMAGEKIT_URL_ENDPOINT = os.getenv("IMAGEKIT_URL")

imagekit = AsyncImageKit(
    private_key= os.getenv("IMAGEKIT_PRIVATE_KEY"),
)