import sys

sys.path.append("../../src")

from melobot import MeloBot, BotPlugin, send, ForwardWsConn

the_plugin = BotPlugin(__name__, "1.0.0")

@the_plugin.on_start_match("hello melobot")
async def echo() -> None:
    await send("你好呀！我是 melobot >w<")

if __name__ == "__main__":
    bot = MeloBot(__name__)
    # 如果你的 OneBot 实现程序的服务的 host 和 port 不一致，请自行修改
    bot.init(ForwardWsConn("127.0.0.1", 8080))
    bot.load_plugin(the_plugin)
    bot.run()
