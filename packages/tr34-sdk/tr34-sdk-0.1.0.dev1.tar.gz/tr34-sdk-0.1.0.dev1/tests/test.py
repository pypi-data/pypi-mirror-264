import asyncio

from tr34_sdk import TR34Api

api = TR34Api(key="sdfds")

async def get_posts_test():
    r = await api.search_posts(tags=['ass'], limit=10)
    print(len(r))
    print(await r[0].get_tags())
    print(r[0])

async def main():
    await get_posts_test()

if __name__ == "__main__":
    asyncio.run(main())

