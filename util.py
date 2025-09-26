import string
import easyocr
import re

#initialize the OCR reader
reader = easyocr.Reader(['en'], gpu=False)

#Mapping dictionnaries for character converstion
dict_char_to_int = {'O': '0',
                    'I': '1',
                    'J': '3',
                    'A': '4',
                    'G': '6',
                    'S': '5'}

dict_int_to_char = {'0': 'O',
                    '1': 'I',
                    '3': 'J',
                    '4': 'A',
                    '6': 'G',
                    '5': 'S'}
def get_car(license_plate, vehicle_track_ids):
    #retrieve the vehicle coordinates and ID based on the license plate coordinates
    x1, y1, x2, y2, score, class_id = license_plate

    car_indx = 0
    foundIt = False
    for j in range(len(vehicle_track_ids)):
        xcar1, ycar1, xcar2, ycar2, car_id = vehicle_track_ids[j]

        if x1 > xcar1 and y1 > ycar1 and x2 < xcar2 and y2 < ycar2:
            car_indx = j
            foundIt = True
            break

    if foundIt:
        return vehicle_track_ids[car_indx]

    return -1, -1, -1, -1, -1

def license_complies_format(text):
    """
    Check if the license plate text complies with the required format.
    Args:
        text (str): License plate text.
    Returns:
        bool: True if the license plate complies with the format, False otherwise.
    """
    text = re.sub(r"[^A-Za-z0-9]", "", text)
    if len(text) != 7:
        return False

    if (text[0] in string.ascii_uppercase or text[0] in dict_int_to_char.keys()) and \
       (text[1] in string.ascii_uppercase or text[1] in dict_int_to_char.keys()) and \
       (text[2] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] or text[2] in dict_char_to_int.keys()) and \
       (text[3] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] or text[3] in dict_char_to_int.keys()) and \
       (text[4] in string.ascii_uppercase or text[4] in dict_int_to_char.keys()) and \
       (text[5] in string.ascii_uppercase or text[5] in dict_int_to_char.keys()) and \
       (text[6] in string.ascii_uppercase or text[6] in dict_int_to_char.keys()):
        print("Country : UK")
        return 1

    # if (text[0] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] or text[0] in dict_char_to_int.keys()) and \
    #      (text[1] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] or text[1] in dict_char_to_int.keys()) and \
    #      (text[2] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] or text[2] in dict_char_to_int.keys()) and \
    #      (text[3] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] or text[3] in dict_char_to_int.keys()) and \
    #      (text[4] in string.ascii_uppercase or text[4] in dict_int_to_char.keys()) and \
    #      (text[5] in string.ascii_uppercase or text[5] in dict_int_to_char.keys()) and \
    #      (text[6] in string.ascii_uppercase or text[6] in dict_int_to_char.keys()):
    #      print("Country : SPAIN")
    #      return 2

    # elif (text[0] in string.ascii_uppercase or text[0] in dict_int_to_char.keys()) and \
    #      (text[1] in string.ascii_uppercase or text[1] in dict_int_to_char.keys()) and \
    #      (text[2] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] or text[2] in dict_char_to_int.keys()) and \
    #      (text[3] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] or text[3] in dict_char_to_int.keys()) and \
    #      (text[4] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] or text[4] in dict_char_to_int.keys()) and \
    #      (text[5] in string.ascii_uppercase or text[5] in dict_int_to_char.keys()) and \
    #      (text[6] in string.ascii_uppercase or text[6] in dict_int_to_char.keys()):
    #      print("Country : FRANCE")
    #      return 3

    else:
        return False


def format_license(text, condition_text):
    """
    Format the license plate text by converting characters using the mapping dictionaries.
    Args:
        text (str): License plate text.
    Returns:
        str: Formatted license plate text.
    """
    license_plate_ = ''
    if condition_text == 1:
        mapping = {0: dict_int_to_char, 1: dict_int_to_char, 4: dict_int_to_char, 5: dict_int_to_char, 6: dict_int_to_char,
                   2: dict_char_to_int, 3: dict_char_to_int}

    elif condition_text == 2:
        mapping = {0: dict_char_to_int, 1: dict_char_to_int, 4: dict_int_to_char, 5: dict_int_to_char, 6: dict_int_to_char,
                   2: dict_char_to_int, 3: dict_char_to_int}

    elif condition_text == 3:
        mapping = {0: dict_int_to_char, 1: dict_int_to_char, 4: dict_char_to_int, 5: dict_char_to_int, 6: dict_char_to_int,
                   2: dict_int_to_char, 3: dict_int_to_char}

    for j in [0, 1, 2, 3, 4, 5, 6]:
        if text[j] in mapping[j].keys():
            license_plate_ += mapping[j][text[j]]
        else:
            license_plate_ += text[j]

    return license_plate_


def read_license_plate(license_plate_crop):
    # Read the license plate text from the given cropped image and gives text and confidence score
    detections = reader.readtext(license_plate_crop)

    for detection in detections:
        bbox, text, score = detection

        text = text.upper().replace(' ', '')  #remove any spaces

        condition_text = license_complies_format(text)
        if condition_text == 1 or condition_text == 2 or condition_text == 3:
            return format_license(text, condition_text), score

        #return text, score

    return None, None   #if we have any issues reading the license plates

def write_csv(results, output_path):
    """
    Write the results to a CSV file.
    Args:
        results (dict): Dictionary containing the results.
        output_path (str): Path to the output CSV file.
    """
    with open(output_path, 'w') as f:
        f.write('{},{},{},{},{},{},{}\n'.format('frame_nmr', 'car_id', 'car_bbox',
                                                'license_plate_bbox', 'license_plate_bbox_score', 'license_number',
                                                'license_number_score'))

        for frame_nmr in results.keys():
            for car_id in results[frame_nmr].keys():
                print(results[frame_nmr][car_id])
                if 'car' in results[frame_nmr][car_id].keys() and \
                   'license_plate' in results[frame_nmr][car_id].keys() and \
                   'text' in results[frame_nmr][car_id]['license_plate'].keys():
                    f.write('{},{},{},{},{},{},{}\n'.format(frame_nmr,
                                                            car_id,
                                                            '[{} {} {} {}]'.format(
                                                                results[frame_nmr][car_id]['car']['bbox'][0],
                                                                results[frame_nmr][car_id]['car']['bbox'][1],
                                                                results[frame_nmr][car_id]['car']['bbox'][2],
                                                                results[frame_nmr][car_id]['car']['bbox'][3]),
                                                            '[{} {} {} {}]'.format(
                                                                results[frame_nmr][car_id]['license_plate']['bbox'][0],
                                                                results[frame_nmr][car_id]['license_plate']['bbox'][1],
                                                                results[frame_nmr][car_id]['license_plate']['bbox'][2],
                                                                results[frame_nmr][car_id]['license_plate']['bbox'][3]),
                                                            results[frame_nmr][car_id]['license_plate']['bbox_score'],
                                                            results[frame_nmr][car_id]['license_plate']['text'],
                                                            results[frame_nmr][car_id]['license_plate']['text_score'])
                            )
        f.close()

