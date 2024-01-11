import easyocr
import string

reader = easyocr.Reader(["en"], gpu=False)

dict_char_to_int = {
    "O": "0",
    "I": "1",
    "Z": "2",
    "J": "3",
    "A": "4",
    "S": "5",
    "G": "6",
}

dict_int_to_char = {
    "0": "O",
    "1": "I",
    "2": "Z",
    "3": "J",
    "4": "A",
    "5": "S",
    "6": "G",
}

def license_complies_format(text):
    if len(text) == 7:
        return (
            (text[0] in string.ascii_uppercase or text[0] in dict_int_to_char.keys())
            and (text[1] in string.ascii_uppercase or text[1] in dict_int_to_char.keys())
            and (text[6] in string.ascii_uppercase or text[6] in dict_int_to_char.keys())
            and (
                text[2] in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
                or text[2] in dict_char_to_int.keys()
            )
            and (
                text[3] in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
                or text[3] in dict_char_to_int.keys()
            )
            and (
                text[4] in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
                or text[4] in dict_char_to_int.keys()
            )
            and (
                text[5] in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
                or text[5] in dict_char_to_int.keys()
            )
        )
    elif len(text) == 8:
        return (
            (text[0] in string.ascii_uppercase or text[0] in dict_int_to_char.keys())
            and (text[1] in string.ascii_uppercase or text[1] in dict_int_to_char.keys())
            and (text[6] in string.ascii_uppercase or text[6] in dict_int_to_char.keys())
            and (text[7] in string.ascii_uppercase or text[7] in dict_int_to_char.keys())
            and (
                text[2] in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
                or text[2] in dict_char_to_int.keys()
            )
            and (
                text[3] in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
                or text[3] in dict_char_to_int.keys()
            )
            and (
                text[4] in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
                or text[4] in dict_char_to_int.keys()
            )
            and (
                text[5] in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
                or text[5] in dict_char_to_int.keys()
            )
        )
    elif len(text) == 9:
        return (
            (text[0] in string.ascii_uppercase or text[0] in dict_int_to_char.keys())
            and (text[1] in string.ascii_uppercase or text[1] in dict_int_to_char.keys())
            and (text[6] in string.ascii_uppercase or text[6] in dict_int_to_char.keys())
            and (text[7] in string.ascii_uppercase or text[7] in dict_int_to_char.keys())
            and (text[8] in string.ascii_uppercase or text[8] in dict_int_to_char.keys())
            and (
                text[2] in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
                or text[2] in dict_char_to_int.keys()
            )
            and (
                text[3] in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
                or text[3] in dict_char_to_int.keys()
            )
            and (
                text[4] in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
                or text[4] in dict_char_to_int.keys()
            )
            and (
                text[5] in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
                or text[5] in dict_char_to_int.keys()
            )
        )
    else:
        return False

def format_license(text):
    if len(text) == 7 or len(text) == 8 or len(text) == 9:
        license_plate_ = ""
        mapping = {}

        if len(text) == 7:
            mapping = {
                0: dict_int_to_char,
                1: dict_int_to_char,
                6: dict_int_to_char,
                2: dict_char_to_int,
                3: dict_char_to_int,
                4: dict_char_to_int,
                5: dict_char_to_int,
            }
        elif len(text) == 8:
            mapping = {
                0: dict_int_to_char,
                1: dict_int_to_char,
                6: dict_int_to_char,
                7: dict_int_to_char,
                2: dict_char_to_int,
                3: dict_char_to_int,
                4: dict_char_to_int,
                5: dict_char_to_int,
            }
        elif len(text) == 9:
            mapping = {
                0: dict_int_to_char,
                1: dict_int_to_char,
                6: dict_int_to_char,
                7: dict_int_to_char,
                8: dict_int_to_char,
                2: dict_char_to_int,
                3: dict_char_to_int,
                4: dict_char_to_int,
                5: dict_char_to_int,
            }

        for j in range(len(text)):
            if j in mapping.keys() and text[j] in mapping[j].keys():
                license_plate_ += mapping[j][text[j]]
            else:
                license_plate_ += text[j]

        return license_plate_
    else:
        return None

def read_license_plate(license_plate_crop):
    detections = reader.readtext(license_plate_crop)

    for detection in detections:
        _, text, score = detection

        text = text.upper().replace(" ", "")

        if len(text) == 7 or len(text) == 8 or len(text) == 9:
            if license_complies_format(text):
                return format_license(text), score

    return None, None
