from .get_my_gif_set import GetMyGifSet
from .add_to_my_gif_set import AddToMyGifSet
from .remove_from_my_gif_set import RemoveFromMyGifSet


class Gifs(
    GetMyGifSet,
    AddToMyGifSet,
    RemoveFromMyGifSet,
):
    pass