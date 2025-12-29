import io
import json
import logging

import aiohttp

from .. import loader, utils
from herokutl.types import Message

logger = logging.getLogger(__name__)

# meta developer: @kmodules
__version__ = (1, 1, 1)

@loader.tds
class UploaderMod(loader.Module):
    """Module for uploading files to various file hosting services"""

    strings = {
        "name": """K:Uploader""",
        "uploading": "⚡ <b>Uploading file...</b>",
        "reply_to_file": "❌ <b>Reply to file!</b>",
        "uploaded": "❤️ <b>File uploaded!</b>\n\n🔥 <b>URL:</b> <code>{}</code>",
        "error": "❌ <b>Error while uploading: {}</b>"
    }

    strings_ru = {
        "name": """K:Uploader""", 
        "uploading": "⚡ <b>Загружаю файл...</b>",
        "reply_to_file": "❌ <b>Ответьте на файл!</b>", 
        "uploaded": "❤️ <b>Файл загружен!</b>\n\n🔥 <b>URL:</b> <code>{}</code>",
        "error": "❌ <b>Ошибка при загрузке: {}</b>"
    }

    async def _get_file(self, message: Message):
        """Helper to get file from message"""
        reply = await message.get_reply_message()
        if not reply:
            await utils.answer(message, self.strings("reply_to_file"))
            return None
            
        if reply.media:
            file = io.BytesIO(await self.client.download_media(reply.media, bytes))
            if hasattr(reply.media, "document"):
                file.name = reply.file.name or f"file_{reply.file.id}"
            else:
                file.name = f"file_{reply.id}.jpg"
        else:
            file = io.BytesIO(bytes(reply.raw_text, "utf-8"))
            file.name = "text.txt"
            
        return file

    async def _post_multipart(self, url, field, file, data=None, method="post"):
        file.seek(0)
        form = aiohttp.FormData()
        form.add_field(field, file, filename=file.name)
        if data:
            for key, value in data.items():
                form.add_field(key, str(value))

        timeout = aiohttp.ClientTimeout(total=60)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.request(method, url, data=form) as res:
                text = await res.text()
                return res, text

    async def _put_bytes(self, url, file):
        file.seek(0)
        timeout = aiohttp.ClientTimeout(total=60)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.put(url, data=file.read()) as res:
                text = await res.text()
                return res, text

    async def catboxcmd(self, message: Message):
        """Upload file to catbox.moe"""
        await utils.answer(message, self.strings("uploading"))
        file = await self._get_file(message)
        if not file:
            return
        
        try:
            res, text = await self._post_multipart(
                "https://catbox.moe/user/api.php",
                "fileToUpload",
                file,
                data={"reqtype": "fileupload"},
            )
            if res.ok:
                await utils.answer(
                    message,
                    self.strings("uploaded").format(utils.escape_html(text)),
                )
            else:
                await utils.answer(
                    message, self.strings("error").format(res.status)
                )
        except Exception as e:
            logger.exception("catbox upload failed")
            await utils.answer(
                message, self.strings("error").format(utils.escape_html(str(e)))
            )

    async def envscmd(self, message: Message):
        """Upload file to envs.sh"""
        await utils.answer(message, self.strings("uploading"))
        file = await self._get_file(message)
        if not file:
            return
            
        try:
            res, text = await self._post_multipart(
                "https://envs.sh", "file", file
            )
            if res.ok:
                await utils.answer(
                    message,
                    self.strings("uploaded").format(utils.escape_html(text)),
                )
            else:
                await utils.answer(
                    message, self.strings("error").format(res.status)
                )
        except Exception as e:
            logger.exception("envs upload failed")
            await utils.answer(
                message, self.strings("error").format(utils.escape_html(str(e)))
            )

    async def kappacmd(self, message: Message): 
        """Upload file to kappa.lol"""
        await utils.answer(message, self.strings("uploading"))
        file = await self._get_file(message)
        if not file:
            return
            
        try:
            res, text = await self._post_multipart(
                "https://kappa.lol/api/upload", "file", file
            )
            if res.ok:
                data = json.loads(text)
                url = f"https://kappa.lol/{data['id']}"
                await utils.answer(
                    message,
                    self.strings("uploaded").format(utils.escape_html(url)),
                )
            else:
                await utils.answer(
                    message, self.strings("error").format(res.status)
                )
        except Exception as e:
            logger.exception("kappa upload failed")
            await utils.answer(
                message, self.strings("error").format(utils.escape_html(str(e)))
            )

    async def oxocmd(self, message: Message):
        """Upload file to 0x0.st"""
        await utils.answer(message, self.strings("uploading"))
        file = await self._get_file(message)
        if not file:
            return
            
        try:
            res, text = await self._post_multipart(
                "https://0x0.st",
                "file",
                file,
                data={"secret": True},
            )
            if res.ok:
                await utils.answer(
                    message,
                    self.strings("uploaded").format(utils.escape_html(text)),
                )
            else:
                await utils.answer(
                    message, self.strings("error").format(res.status)
                )
        except Exception as e:
            logger.exception("0x0 upload failed")
            await utils.answer(
                message, self.strings("error").format(utils.escape_html(str(e)))
            )

    async def x0cmd(self, message: Message):
        """Upload file to x0.at"""
        await utils.answer(message, self.strings("uploading"))
        file = await self._get_file(message)
        if not file:
            return
            
        try:
            res, text = await self._post_multipart(
                "https://x0.at", "file", file
            )
            if res.ok:
                await utils.answer(
                    message,
                    self.strings("uploaded").format(utils.escape_html(text)),
                )
            else:
                await utils.answer(
                    message, self.strings("error").format(res.status)
                )
        except Exception as e:
            logger.exception("x0 upload failed")
            await utils.answer(
                message, self.strings("error").format(utils.escape_html(str(e)))
            )
            
    async def tmpfilescmd(self, message: Message):
        """Upload file to tmpfiles.org"""
        await utils.answer(message, self.strings("uploading"))
        file = await self._get_file(message)
        if not file:
            return

        try:
            res, text = await self._post_multipart(
                "https://tmpfiles.org/api/v1/upload",
                "file",
                file,
            )
            if res.ok:
                data = json.loads(text)
                url = data["data"]["url"]
                await utils.answer(
                    message,
                    self.strings("uploaded").format(utils.escape_html(url)),
                )
            else:
                await utils.answer(
                    message, self.strings("error").format(res.status)
                )
        except Exception as e:
            logger.exception("tmpfiles upload failed")
            await utils.answer(
                message, self.strings("error").format(utils.escape_html(str(e)))
            )

    async def pomfcmd(self, message: Message):
        """Upload file to pomf.lain.la"""
        await utils.answer(message, self.strings("uploading"))
        file = await self._get_file(message)
        if not file:
            return

        try:
            res, text = await self._post_multipart(
                "https://pomf.lain.la/upload.php",
                "files[]",
                file,
            )
            if res.ok:
                data = json.loads(text)
                url = data["files"][0]["url"]
                await utils.answer(
                    message,
                    self.strings("uploaded").format(utils.escape_html(url)),
                )
            else:
                await utils.answer(
                    message, self.strings("error").format(res.status)
                )
        except Exception as e:
            logger.exception("pomf upload failed")
            await utils.answer(
                message, self.strings("error").format(utils.escape_html(str(e)))
            )

    async def bashcmd(self, message: Message):
        """Upload file to bashupload.com"""
        await utils.answer(message, self.strings("uploading"))
        file = await self._get_file(message)
        if not file:
            return

        try:
            res, text = await self._put_bytes("https://bashupload.com", file)
            if res.ok:
                urls = [line for line in text.split("\n") if "wget" in line]
                if urls:
                    url = urls[0].split()[-1]
                    await utils.answer(
                        message,
                        self.strings("uploaded").format(utils.escape_html(url)),
                    )
                else:
                    await utils.answer(
                        message,
                        self.strings("error").format("Could not find URL"),
                    )
            else:
                await utils.answer(
                    message, self.strings("error").format(res.status)
                )
        except Exception as e:
            logger.exception("bashupload upload failed")
            await utils.answer(
                message, self.strings("error").format(utils.escape_html(str(e)))
            )