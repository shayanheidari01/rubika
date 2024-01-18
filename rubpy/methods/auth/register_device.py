import rubpy
import warnings
import re


system_versions = {
        'Windows NT 10.0': 'Windows 10',
        'Windows NT 6.2': 'Windows 8',
        'Windows NT 6.1': 'Windows 7',
        'Windows NT 6.0': 'Windows Vista',
        'Windows NT 5.1': 'windows XP',
        'Windows NT 5.0': 'Windows 2000',
        'Mac': 'Mac/iOS',
        'X11': 'UNIX',
        'Linux': 'Linux'
    }


async def get_browser(user_agent, lang_code, app_version, *args, **kwargs):
        device_model = re.search(r'(opera|chrome|safari|firefox|msie'
                                 r'|trident)\/(\d+)', user_agent.lower())
        if not device_model:
            device_model = 'Unknown'
            warnings.warn(f'can not parse user-agent ({user_agent})')

        else:
            device_model = device_model.group(1) + ' ' + device_model.group(2)

        system_version = 'Unknown'
        for key, value in system_versions.items():
            if key in user_agent:
                system_version = value
                break

        # window.navigator.mimeTypes.length (outdated . Defaults to '2')
        device_hash = '2'
        return {
            'token': '',
            'lang_code': lang_code,
            'token_type': 'Web',
            'app_version': f'WB_{app_version}',
            'system_version': system_version,
            'device_model': device_model.title(),
            'device_hash': device_hash + ''.join(re.findall(r'\d+', user_agent))}


class RegisterDevice:
    async def register_device(self: "rubpy.Client"):
        return await self.builder(name='registerDevice',
                                 input=await get_browser(self.user_agent,
                                                         self.lang_code,
                                                         self.DEFAULT_PLATFORM.get('app_version')))