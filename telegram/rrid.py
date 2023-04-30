async def rival_regions_account_registration(message, profiles, rooms, langues, room_id, commission):
    args = message.get_args().split()

    if len(args) != 1:
        await message.reply(TEXTS[langues[str(message.chat.id)]]['IndexError_account'])
        return

    link_user = args[0]

    if not 'https://rivalregions.com/#slide/profile/' in link_user and not 'https://m.rivalregions.com/#slide/profile/' in link_user:
        await message.reply(TEXTS[langues[str(message.chat.id)]]['ValueError_account'])
        return

    link_user = link_user.replace('m.', '')
    
    for v in profiles.values():
        if str(v['RRprofile']) == str(link_user):
            await message.reply(TEXTS[langues[str(message.chat.id)]]['have_profile'])
            return

    profiles[str(message.from_user.id)]['RRprofile'] = link_user

    await message.reply(TEXTS[langues[str(message.chat.id)]]['make_profile'].format(link_user))
    if message.chat.type == 'private':
        await asyncio.sleep(1)
        await message.reply(TEXTS[langues[str(message.chat.id)]]['link_for_chat'])

    save(profiles=profiles)
