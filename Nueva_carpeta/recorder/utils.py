from os import path, remove
import datetime

def random_name(name_base):
    """ Método para generar un nombre aleatorio. """
    #suffix = datetime.datetime.now().strftime("%y%m%d_%H%M%S")
    suffix = datetime.datetime.now().strftime("%y%m%d_%H%M%S")
    filename = "_".join([name_base, suffix])
    return filename

def directory_exists(url_path):
    """ Método para verificar existencia de directorio. """
    if path.isdir(url_path):
        return True
    return False


def file_exists(url_path):
    """ Método para verificar existencia de archivo. """
    if path.isfile(url_path):
        return True
    return False


def write_file(base_url, filename, content):
    """ Método para guardar un archivo. """
    if directory_exists(base_url):
        with open(base_url + filename, "wb") as f:
            f.write(content)
            f.close()

def remove_file(url_path):
    """ Método para eliminar un archivo. """
    if file_exists(url_path):
        remove(url_path)