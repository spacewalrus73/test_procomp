from .models import Files


def save(file) -> None:
    """
    Save file to db
    """
    Files.objects.create(
        file_name=file.name,
        file=file
    )


def get_file_by_id(id: int):
    """
    Return file object by id
    """
    return Files.objects.get(id=id)


def get_filename_by_id(id: int) -> str:
    """
    Return filename str by id
    """
    return Files.objects.get(id=id).file_name


def get_all_files():
    """
    Return all db data Files
    """
    return Files.objects.all()
