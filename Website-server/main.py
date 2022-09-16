from quart import Quart, render_template, request, session, redirect, url_for
from quart_discord import DiscordOAuth2Session
from discord.ext import ipc

app = Quart(__name__)
ipc_client = ipc.Client(secret_key = SECRET_KEY)

app.config["SECRET_KEY"] = SECRET_KEY
app.config["DISCORD_CLIENT_ID"] = DISCORD_CLIENT_ID
app.config["DISCORD_CLIENT_SECRET"] = DISCORD_CLIENT_SECRET
app.config["DISCORD_REDIRECT_URI"] = DISCORD_REDIRECT_URI

discord = DiscordOAuth2Session(app)

@app.route("/")
async def home():
	get_guild_count = "wait for coal to do the bot"#await ipc_client.request("get_guild_count")
	return await render_template("index.html", guild_count=get_guild_count)

@app.route("/login")
async def login():
	return await discord.create_session()

@app.route("/callback")
async def callback():
	try:
		await discord.callback()
	except:
		return redirect(url_for("login"))

	user = await discord.fetch_user()
	return f"Hello {user.name}"

@app.route("/dashboard")
async def dashboard():
	guild_count = await ipc_client.request("get_guild_count")

	return f"The bot is is in {guild_count}"
if __name__ == "__main__":
    app.run(debug=True)
