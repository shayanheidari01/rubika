from .get_contacts_updates import GetContactsUpdates
from .add_address_book import AddAddressBook
from .delete_contact import DeleteContact
from .get_contacts import GetContacts


class Contacts(
    GetContactsUpdates,
    AddAddressBook,
    DeleteContact,
    GetContacts,
):
    pass