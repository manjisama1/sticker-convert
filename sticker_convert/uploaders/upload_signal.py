#!/usr/bin/env python3
import os
import copy

from utils.metadata_handler import MetadataHandler
from utils.converter import StickerConvert
from utils.format_verify import FormatVerify
from utils.codec_info import CodecInfo
from utils.cache_store import CacheStore

import anyio
from signalstickers_client import StickersClient
from signalstickers_client.models import LocalStickerPack, Sticker
from mergedeep import merge

class UploadSignal:
    @staticmethod
    async def upload_stickers_signal_async(opt_output, opt_comp, opt_cred, cb_msg=print, cb_msg_block=input, cb_bar=None, out_dir=None, **kwargs):
        if not opt_cred.get('signal', {}).get('uuid'):
            msg = 'uuid required for uploading to signal'
            return [msg]
        if not opt_cred.get('signal', {}).get('password'):
            msg = 'password required for uploading to signal'
            return [msg]

        fake_vid = opt_comp.get('fake_vid', False)
        in_dir = opt_output['dir']
        if not out_dir:
            out_dir = opt_output['dir']
        
        base_spec = {
            "size_max": {
                "img": 300000,
                "vid": 300000
            },
            'res': {
                'w': {
                    'max': 512
                },
                'h': {
                    'max': 512
                }
            },
            'duration': {
                'max': 3000
            },
            'square': True
        }

        apng_spec = copy.deepcopy(base_spec)
        apng_spec['format'] = '.apng'

        png_spec = copy.deepcopy(base_spec)
        png_spec['format'] = '.png'

        webp_spec = copy.deepcopy(base_spec)
        webp_spec['format'] = '.webp'
        webp_spec['animated'] = False

        opt_comp_merged = merge({}, opt_comp, base_spec)
        
        urls = []
        title, author, emoji_dict = MetadataHandler.get_metadata(in_dir, title=opt_output.get('title'), author=opt_output.get('author'))
        if title == None:
            raise TypeError(f'title cannot be {title}')
        if author == None:
            raise TypeError(f'author cannot be {author}')
        if emoji_dict == None:
            msg_block = 'emoji.txt is required for uploading signal stickers\n'
            msg_block += f'emoji.txt generated for you in {in_dir}\n'
            msg_block += f'Default emoji is set to {opt_comp.get("default_emoji")}.\n'
            msg_block += f'Please edit emoji.txt now, then continue'
            MetadataHandler.generate_emoji_file(dir=in_dir, default_emoji=opt_comp.get("default_emoji"))

            cb_msg_block(msg_block)

            title, author, emoji_dict = MetadataHandler.get_metadata(in_dir, title=opt_output.get('title'), author=opt_output.get('author'))
        
        packs = MetadataHandler.split_sticker_packs(in_dir, title=title, file_per_pack=200, separate_image_anim=False)
        for pack_title, stickers in packs.items():
            pack = LocalStickerPack()
            pack.author = author
            pack.title = pack_title

            with CacheStore.get_cache_store(path=opt_comp.get('cache_dir')) as tempdir:
                for src in stickers:
                    cb_msg(f'Verifying {src} for uploading to signal')

                    src_full_name = os.path.split(src)[-1]
                    src_name = os.path.splitext(src_full_name)[0]
                    
                    if not (FormatVerify.check_file(src, spec=apng_spec) or
                            FormatVerify.check_file(src, spec=png_spec) or
                            FormatVerify.check_file(src, spec=webp_spec)):
                        
                        if fake_vid or CodecInfo.is_anim(src):
                            sticker_path = os.path.join(tempdir, src_name + '.webp')
                        else:
                            sticker_path = os.path.join(tempdir, src_name + '.png')
                        StickerConvert.convert_and_compress_to_size(src, sticker_path, opt_comp_merged, cb_msg)
                    else:
                        sticker_path = src

                    sticker = Sticker()
                    sticker.id = pack.nb_stickers

                    try:
                        sticker.emoji = emoji_dict[src_name][:1]
                    except KeyError:
                        cb_msg(f'Warning: Cannot find emoji for file {src_full_name}, skip uploading this file...')
                        continue

                    with open(sticker_path, "rb") as f_in:
                        sticker.image_data = f_in.read()

                    pack._addsticker(sticker)

            async with StickersClient(opt_cred.get('signal', {}).get('uuid'), opt_cred.get('signal', {}).get('password')) as client:
                pack_id, pack_key = await client.upload_pack(pack)
            
            result = f"https://signal.art/addstickers/#pack_id={pack_id}&pack_key={pack_key}"
            cb_msg(result)
            urls.append(result)
        
        return urls

    @staticmethod
    def upload_stickers_signal(opt_output, opt_comp, opt_cred, cb_msg=print, cb_msg_block=input, cb_bar=None, out_dir=None, **kwargs):
        return anyio.run(UploadSignal.upload_stickers_signal_async, opt_output, opt_comp, opt_cred, cb_msg, cb_msg_block, cb_bar, out_dir)
