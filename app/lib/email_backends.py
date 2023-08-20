from abc import ABC, abstractmethod


class AbstractEmailBackend(ABC):

    @abstractmethod
    async def send_email(
        self, to: str, from_: str,
        subj: str='', simple_txt: str='', html: str=''
    ):
        ...


class SimpleBackend(AbstractEmailBackend):
    async def send_email(
        self, to: str, from_: str,
        subj: str='', simple_txt: str='', html: str=''
    ):
        print(to, from_)
        print(simple_txt)
        print(html)
