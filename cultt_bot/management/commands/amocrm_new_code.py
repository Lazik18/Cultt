from cultt_bot.amo_crm import AmoCrmSession

amo_crm_session = AmoCrmSession('thecultt.amocrm.ru')
result = amo_crm_session.get_access_token()
print(result)
