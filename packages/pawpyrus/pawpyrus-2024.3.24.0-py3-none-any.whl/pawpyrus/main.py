__version__ = '2024.3.24.0'
__repository__ = 'https://git.disroot.org/spable/pawpyrus'
__bugtracker__ = 'https://git.disroot.org/spable/pawpyrus/issues'

from pyzbar.pyzbar import decode #
from reportlab.graphics import renderPDF #
from reportlab.lib.units import mm #
from reportlab.pdfgen import canvas #
from svglib.svglib import svg2rlg #
import argparse #
import bitarray #
import cv2 # opencv-python + opencv-contrib-python
import datetime
import glob
import hashlib
import io
import itertools
import json
import logging
import math
import more_itertools #
import numpy #
import os
import qrcode #
import random
import sys
import tqdm #

# -----=====| CONST |=====-----

C_ALPHANUMERIC_STRING = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ$%*+-./:'
C_ARUCO_DICT = 4 # cv2.aruco.DICT_5X5_50
C_ENCODER_BLOCKNUM_BLOCK_SIZE = 4
C_ENCODER_CHAR_CHUNK_SIZE = 11
C_ENCODER_DATA_CHUNK_SIZE = 195 # max alphanumeric for version 6 QR
C_ENCODER_OFFSET_BLOCK_SIZE = 2
C_ENCODER_RUNID_BLOCK_SIZE = 4
C_LOGGING_LEVEL = 20 # logging.INFO
C_OPENCV_MIN_MARKER_PERIMETER_RATE = 1e-9 # temporary solution
C_PADDING_CHAR = ' '
C_PDF_COLUMNS = 5
C_PDF_DOT_SPACING_SIZE = 3 # just beauty
C_PDF_FONT_FAMILY = 'Courier-Bold'
C_PDF_FONT_SIZE = 10
C_PDF_PAGE_HEIGHT = 297 # mm, A4 page
C_PDF_LEFT_MARGIN = 25 # mm
C_PDF_LINE_HEIGHT = 5 # mm
C_PDF_PAGE_WIDTH = 210 # mm, A4 page
C_PDF_RIGHT_MARGIN = 25 # mm
C_PDF_TOP_MARGIN = 20 # mm
C_PDF_ROWS = 7
C_QR_CORRECTION_LEVEL = 1 # Low
C_QR_SPACING_SIZE = 7 # minimal
C_QR_VERSION = 6
C_TQDM_ASCII = '.#' # just beauty

# -----=====| LOGGING |=====-----

logging.basicConfig(format='[%(levelname)s] %(message)s', level=C_LOGGING_LEVEL)

# -----=====| ALFANUMERIC ENCODING |=====-----

class AlphaEncoder:

    def __init__(self, encoding_string, padding_char, char_chunk, offset_block_size,
                 runid_block_size, chunk_num_block_size):
        self.encoding_string = str(encoding_string)
        self.padding_char = str(padding_char)
        self.char_chunk = int(char_chunk)
        self.offset_size = int(offset_block_size)
        self.runid_size = int(runid_block_size)
        self.block_num_size = int(chunk_num_block_size)
        self.decoding_dict = {charc: numr for numr, charc in enumerate(self.encoding_string)}
        self.basis = len(self.encoding_string)
        self.runid_max = (self.basis ** self.runid_size) - 1
        self.block_max = (self.basis ** self.block_num_size) - 1
        self.bit_chunk = self.calculate_bit_chunk()
        loss_percentage = (((self.basis ** self.char_chunk) - (2 ** self.bit_chunk))
                           / (self.basis ** self.char_chunk) * 100)
        self.hash_size = self.calculate_hash_size()
        self.min_data_chunk_size = self.runid_size + (self.block_num_size * 2) + self.hash_size
        # Debug logging
        debug_data = {
            'Encoding string':     self.encoding_string,
            'Padding char':        self.padding_char,
            'Basis':               self.basis,
            'Char chunk size':     self.char_chunk,
            'Bits chunk size':     self.bit_chunk,
            'offset block size':   self.offset_size,
            'Max offset':          self.basis ** self.offset_size,
            'Efficiency loss [%]': loss_percentage,
            'Run ID Block Size':   self.runid_size,
            'Run ID Range':        [0, self.runid_max],
            'Block Num Size':      self.block_num_size,
            'Max Blocks':          self.block_max,
            'Hash block size':     self.hash_size,
            'Min data chunk size': self.min_data_chunk_size
        }
        logging.debug('AlphaEncoder Object metadata: %s', json.dumps(debug_data, indent=4))

    def calculate_bit_chunk(self):
        index = 0
        while 1:
            index += 1
            if ((self.basis ** self.char_chunk) / (2 ** index)) < 1:
                break
        return index - 1

    def calculate_hash_size(self):
        index = 0
        while 1:
            index += 1
            if ((self.basis ** index) / (2 ** 256)) > 1:
                break
        return int(index)

    def encode_int(self, intnum, char_size):
        line = str()
        for index in range(char_size):
            line += self.encoding_string[int(intnum % (self.basis ** (index + 1))
                                             / (self.basis ** index))]
        return line

    def decode_int(self, code):
        char_size = len(code)
        intnum = 0
        for index in range(char_size):
            intnum += self.decoding_dict[code[index]] * (self.basis ** index)
        return intnum

    def encode(self, raw_data, runid_float, chunk_size=None):
        if chunk_size is None:
            chunk_size = self.min_data_chunk_size
        if chunk_size < self.min_data_chunk_size:
            raise ValueError('Too small chunk size')
        # Create output struct
        result = {'RunID': None, 'Hash': None, 'Length': None, 'Codes': []}
        # Run ID: unique program run identifier
        runid_int = int(self.runid_max * runid_float)
        result['RunID'] = hex(runid_int)[2:].zfill(len(hex(self.runid_max)[2:]))
        runid = self.encode_int(runid_int, self.runid_size)
        # Compute data hash
        hash_obj = hashlib.sha256(raw_data)
        result['Hash'] = hash_obj.hexdigest()
        hash_int = int.from_bytes(hash_obj.digest(), 'little')
        hashi = self.encode_int(hash_int, self.hash_size)
        # Encode data
        bit_array = bitarray.bitarray(endian='little')
        bit_array.frombytes(raw_data)
        offset = self.bit_chunk - (len(bit_array) % self.bit_chunk)
        bit_array.extend(bitarray.bitarray('0' * offset, endian='little'))
        line = str()
        for index in range(0, len(bit_array), self.bit_chunk):
            intnum = int.from_bytes(bit_array[index:index + self.bit_chunk], 'little')
            line += self.encode_int(intnum, self.char_chunk)
        line += self.encode_int(offset, self.offset_size)
        pure_chunk_size = chunk_size - self.runid_size - self.block_num_size
        # Encode length
        blocks_positions = range(0, len(line), pure_chunk_size)
        result['Length'] = int(len(blocks_positions) + 1)
        if result['Length'] >= self.block_max:
            raise OverflowError('Too many blocks')
        length = self.encode_int(result['Length'], self.block_num_size)
        # Create chunks
        zero_block_number = self.encode_int(0, self.block_num_size)
        result['Codes'].append((runid + zero_block_number + length + hashi)
                               .ljust(chunk_size, self.padding_char))
        for index, item in enumerate(blocks_positions):
            block_number = self.encode_int(index + 1, self.block_num_size)
            data_chunk = line[item:item + pure_chunk_size]
            result['Codes'].append((runid + block_number + data_chunk)
                                   .ljust(chunk_size, self.padding_char))
        return result

    def extract_data(self, line):
        result = {
            'RunID': (hex(self.decode_int(line[: self.runid_size]))[2:]
                      .zfill(len(hex(self.runid_max)[2:]))),
            'Index': (self.decode_int(
                line[self.runid_size : self.runid_size + self.block_num_size])
                     ),
            'Content': (
                line[self.runid_size + self.block_num_size :].rstrip(self.padding_char)
                )
            }
        return result

    def extract_metadata(self, content):
        result = {
            'Length': self.decode_int(content[: self.block_num_size]),
            'Hash': self.decode_int(
                content[self.block_num_size : self.block_num_size + self.hash_size]
                ).to_bytes(32, 'little').hex().zfill(64)
            }
        return result

    def decode(self, codes):
        result = list()
        # Extract blocks
        extracted = [self.extract_data(line) for line in codes]
        extracted = {item['Index']: item for item in extracted}
        # Check header
        try:
            header = extracted[0]
        except KeyError:
            raise RuntimeError('No root block in input data!')
        # Extract metadata
        metadata = self.extract_metadata(header['Content'])
        # Check blocks
        missing_blocks = list()
        for index in range(1, metadata['Length']):
            try:
                if extracted[index]['RunID'] != header['RunID']:
                    raise RuntimeError('Some blocks are not of this header')
                result.append(extracted[index]['Content'])
            except KeyError:
                missing_blocks.append(str(index))
        if missing_blocks:
            raise RuntimeError(f'Some blocks are missing: {"; ".join(missing_blocks)}')
        # Decode
        code = ''.join(result)
        output_data = {
            'RunID': str(header['RunID']),
            'Blocks': int(metadata['Length']),
            'Hash': str(metadata['Hash']),
            'Data': None
            }
        bit_array = bitarray.bitarray(endian='little')
        offset = self.decode_int(code[-self.offset_size:])
        encoded_data = code[:-self.offset_size]
        for index in range(0, len(encoded_data), self.char_chunk):
            intnum = self.decode_int(encoded_data[index:index + self.char_chunk])
            new_bits = bitarray.bitarray(endian='little')
            new_bits.frombytes(intnum.to_bytes(int(self.bit_chunk / 8) + 1, byteorder='little'))
            bit_array.extend(new_bits[:self.bit_chunk])
        bit_array = bit_array[:-offset]
        output_data['Data'] = bit_array.tobytes()
        if hashlib.sha256(output_data['Data']).hexdigest() != output_data['Hash']:
            raise RuntimeError('Data damaged (hashes are not the same)')
        return output_data

# -----=====| PAWPRINTS |=====-----

# QR Code
def tomcat_pawprint(data, version, error_correction):
    wrapped_data = qrcode.util.QRData(data.encode('ascii'), mode=qrcode.util.MODE_ALPHA_NUM)
    qr_code = qrcode.QRCode(version=version, error_correction=error_correction, border=0)
    qr_code.add_data(wrapped_data)
    qr_code.make(fit=False)
    matrix = numpy.array(qr_code.get_matrix())
    matrix = numpy.vectorize(int)(matrix)
    return matrix

# ArUco Marker
def kitty_pawprint(aruco_index, dictionary, spacing_size):
    matrix = cv2.aruco.getPredefinedDictionary(dictionary).generateImageMarker(aruco_index, spacing_size)
    matrix = numpy.vectorize(lambda x: int(not bool(x)))(matrix)
    return matrix

def create_pixel_sheets(codes, col_num, row_num, spacing_size,
                        dot_spacing, qr_version, qr_error_correction, aruco_dict, tqdm_ascii):
    paw_size = (4 * qr_version) + 17
    cell_size = paw_size + spacing_size
    page_width = cell_size * col_num + spacing_size
    page_height = cell_size * row_num + spacing_size
    # Create output list
    result = list()
    # Chunk codes to rows and pages
    page_data = list(more_itertools.sliced(list(more_itertools.sliced(codes, col_num)), row_num))
    for page_number, page in enumerate(page_data):
        # Create page
        matrix = numpy.zeros((page_height, page_width))
        for row, col in tqdm.tqdm(
                itertools.product(range(row_num), range(col_num)),
                total=sum([len(item) for item in page]),
                desc=f'Create pawprints, page {page_number + 1} of {len(page_data)}',
                ascii=tqdm_ascii):
            try:
                # Create pawprint on the page
                start_x = (spacing_size * 2) + (cell_size * col)
                start_y = (spacing_size * 2) + (cell_size * row)
                pawprint = tomcat_pawprint(page[row][col], qr_version, qr_error_correction)
                matrix[start_y:start_y + paw_size, start_x:start_x + paw_size] = pawprint
            except IndexError:
                # If there are no codes left
                break
        # Create dot margin (beauty, no functionality)
        dot_centering = math.floor(spacing_size / 2)
        matrix[dot_centering, spacing_size + 2::dot_spacing] = 1
        matrix[spacing_size + 2:cell_size * len(page):dot_spacing, dot_centering] = 1
        # Create markers
        grid = {
            0: (0, 0),
            1: (cell_size * col_num, 0),
            2: (0, cell_size * len(page)),
            3: (cell_size, 0)
            }
        for index, item in grid.items():
            matrix[item[1]:item[1] + spacing_size, item[0]:item[0] + spacing_size] = (
                kitty_pawprint(index, aruco_dict, spacing_size))
        # Append page
        result.append(matrix)
    # Return
    return result

# -----=====| DRAW |=====-----

# numpy 2D array to black pixel coordinates
def matrix_to_pixels(matrix):
    pixel_coordinates = itertools.product(range(matrix.shape[0]), range(matrix.shape[1]))
    result = [(crdx, crdy) for crdy, crdx in pixel_coordinates if matrix[crdy][crdx]]
    return result

def draw_svg(pixel_sheets, pdf_page_width, pdf_page_height,
             pdf_left_margin, pdf_right_margin, pdf_top_margin, tqdm_ascii):
    svg_pages = list()
    drawing_width = pixel_sheets[0].shape[1]
    content_width = pdf_page_width - pdf_left_margin - pdf_right_margin
    pixel_size = content_width / drawing_width
    logging.debug('Pixel Size: %.3f mm', pixel_size)
    for page_number, page_matrix in enumerate(pixel_sheets):
        # Create Pixels
        page = matrix_to_pixels(page_matrix)
        # Draw page
        svg_page = [
            f'<svg width="{pdf_page_width}mm" height="{pdf_page_height}mm" viewBox="0 0 '
            + f'{pdf_page_width} {pdf_page_height}" version="1.1" '
            + 'xmlns="http://www.w3.org/2000/svg">',
            '<path style="fill:#000000;stroke:none;fill-rule:evenodd" d="'
            ]
        paths = list()
        # Add Pixels
        for crdx, crdy in tqdm.tqdm(
                page,
                total=len(page),
                desc=f'Draw pixels, page {page_number + 1} of {len(pixel_sheets)}',
                ascii=tqdm_ascii):
                paths.append(f'M {pdf_left_margin + (crdx * pixel_size):.3f},'
                             + f'{pdf_top_margin + (crdy * pixel_size):.3f} '
                             + f'H {pdf_left_margin + ((crdx + 1) * pixel_size):.3f} '
                             + f'V {pdf_top_margin + ((crdy + 1) * pixel_size):.3f} '
                             + f'H {pdf_left_margin + (crdx * pixel_size):.3f} Z')
        svg_page.append(' '.join(paths))
        svg_page.append('">')
        svg_page.append('</svg>')
        # Merge svg
        svg_pages.append(''.join(svg_page))
    return svg_pages

def create_pdf(dataset, svg_pages, output_file_name, job_name, pdf_left_margin,
               pdf_top_margin, pdf_line_spacing, pdf_font_family, pdf_font_size,
               pdf_page_height, tqdm_ascii): # pragma: no cover
    canvas_pdf = canvas.Canvas(output_file_name)
    timestamp = str(datetime.datetime.now().replace(microsecond=0))
    for page_number, page in tqdm.tqdm(
            enumerate(svg_pages),
            total=len(svg_pages),
            desc='Convert pages to PDF',
            ascii=tqdm_ascii
    ):
        # Set font
        canvas_pdf.setFont(pdf_font_family, pdf_font_size)
        # Convert SVG page
        object_page = svg2rlg(io.StringIO(page))
        # Captions
        canvas_pdf.drawString(pdf_left_margin * mm,
                              (pdf_page_height - pdf_top_margin - (pdf_line_spacing * 1)) * mm,
                              f'Name: {job_name}')
        canvas_pdf.drawString(pdf_left_margin * mm,
                              (pdf_page_height - pdf_top_margin - (pdf_line_spacing * 2)) * mm,
                              f'{timestamp}, run ID: {dataset["RunID"]}, {dataset["Length"]} '
                              + f'blocks, page {page_number + 1} of {len(svg_pages)}')
        canvas_pdf.drawString(pdf_left_margin * mm,
                              (pdf_page_height - pdf_top_margin - (pdf_line_spacing * 3)) * mm,
                              f'SHA-256: {dataset["Hash"]}')
        canvas_pdf.drawString(pdf_left_margin * mm,
                              (pdf_page_height - pdf_top_margin - (pdf_line_spacing * 4)) * mm,
                              f'pawpyrus {__version__}. Available at: {__repository__}')
        # Draw pawprints
        renderPDF.draw(object_page, canvas_pdf, 0, 0)
        # Newpage
        canvas_pdf.showPage()
    # Save pdf
    canvas_pdf.save()

# -----=====| DETECTION |=====-----

def find_center(coord_block):
    return (
        coord_block[0][0] + ((coord_block[2][0] - coord_block[0][0]) / 2),
        coord_block[0][1] + ((coord_block[2][1] - coord_block[0][1]) / 2)
        )


def decode_qr(barcode): # pragma: no cover
    result = {'Contents': None, 'Detected': dict()}
    # pyzbar
    code = decode(barcode)
    if code:
        result['Contents'] = str(code[0].data.decode('ascii'))
        result['Detected']['pyzbar'] = True
    else: result['Detected']['pyzbar'] = False
    # opencv
    detector = cv2.QRCodeDetector()
    code = detector.detectAndDecode(barcode)[0]
    if code:
        if result['Contents'] is not None:
            if result['Contents'] != code:
                raise RuntimeError('Different results with different QR decoders? '
                                   + f'OpenCV = {code}, PyZBar = {result["Contents"]}')
        else:
            result['Contents'] = str(code)
        result['Detected']['opencv'] = True
    else:
        result['Detected']['opencv'] = False
    return result


def read_page(file_name, debug_dir, file_index, aruco_dictionary,
              min_marker_perimeter_rate, tqdm_ascii): # pragma: no cover
    # Read and binarize image
    picture = cv2.imread(file_name, cv2.IMREAD_GRAYSCALE)
    threshold, picture = cv2.threshold(picture, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # -----DEBUG-----
    if debug_dir is not None:
        debug_array = cv2.cvtColor(numpy.copy(picture), cv2.COLOR_GRAY2RGB)
    # ---------------

    logging.info('Image binarized (threshold: %.1f)', threshold)
    # Detect markers
    aruco_dict = cv2.aruco.getPredefinedDictionary(aruco_dictionary)
    aruco_params = cv2.aruco.DetectorParameters()
    aruco_params.minMarkerPerimeterRate = min_marker_perimeter_rate
    markers = cv2.aruco.detectMarkers(picture, aruco_dict, parameters=aruco_params)
    # Check markers
    if markers is None:
        raise RuntimeError('No markers were found')

    # -----DEBUG-----
    if debug_dir is not None:
        for item in range(len(markers[1])):
            for line_start, line_end in ((0, 1), (1, 2), (2, 3), (3, 0)):
                cv2.line(
                    debug_array,
                    tuple(int(i) for i in markers[0][item][0][line_start]),
                    tuple(int(i) for i in markers[0][item][0][line_end]),
                    (255, 0, 0),
                    4
                )
            cv2.putText(
                debug_array,
                f'id={markers[1][item][0]}',
                (int(markers[0][item][0][0][0]), int(markers[0][item][0][0][1]) - 20),
                cv2.FONT_HERSHEY_SIMPLEX,
                1.5,
                (0, 255, 0),
                4
            )
    # ---------------

    # Check markers
    markers = { int(markers[1][item][0]): {'Coords': markers[0][item][0]}
                for item in range(len(markers[1])) }
    if tuple(sorted(markers.keys())) != (0, 1, 2, 3):
        raise RuntimeError('Some markers were not found')
    # Align grid
    marker_length = math.dist(markers[0]['Coords'][0], markers[0]['Coords'][1])
    for item in markers:
        markers[item]['Center'] = find_center(markers[item]['Coords'])
    width = math.dist(markers[0]['Center'], markers[1]['Center'])
    height = math.dist(markers[0]['Center'], markers[2]['Center'])
    cell_size = math.dist(markers[0]['Center'], markers[3]['Center'])
    col_num, row_num = round(width / cell_size), round(height / cell_size)
    logging.info('Layout detected: %d x %d', col_num, row_num)
    cell_size_x, cell_size_y = width / col_num, height / row_num
    vector_x = (
        (markers[1]['Center'][0] - markers[0]['Center'][0]) / width,
        (markers[1]['Center'][1] - markers[0]['Center'][1]) / width
        )
    vector_y = (
        (markers[2]['Center'][0] - markers[0]['Center'][0]) / height,
        (markers[2]['Center'][1] - markers[0]['Center'][1]) / height
        )
    for item in markers:
        markers[item]['Center'] = (markers[item]['Center'][0] + (marker_length * vector_x[0]),
                                   markers[item]['Center'][1] + (marker_length * vector_y[1]))
    # chunking by grid
    chunks = list()
    cells = itertools.product(range(col_num), range(row_num))
    for cell_x, cell_y in cells:
        coord_start = markers[0]['Center']
        full_vector_x = tuple(item * cell_size_x for item in vector_x)
        full_vector_y = tuple(item * cell_size_y for item in vector_y)
        chunk = [[
            coord_start[0] + (itemx * full_vector_x[0]) + (itemy * full_vector_y[0]),
            coord_start[1] + (itemx * full_vector_x[1]) + (itemy * full_vector_y[1])
            ] for itemx, itemy in ((cell_x, cell_y), (cell_x + 1, cell_y),
                           (cell_x + 1, cell_y + 1), (cell_x, cell_y + 1))]
        cell_xs, cell_ys = [itemx for itemx, itemy in chunk], [itemy for itemx, itemy in chunk]
        fragment = picture[round(min(cell_ys)):round(max(cell_ys)),
                           round(min(cell_xs)):round(max(cell_xs))]
        chunks.append({
            'Cell': (int(cell_x) + 1, int(cell_y) + 1),
            'Coords': chunk,
            'Image': fragment
            })
    # Detect and decode
    codes = list()
    for chunk in tqdm.tqdm(chunks, total=len(chunks), desc='Detect QR codes', ascii=tqdm_ascii):
        code = decode_qr(chunk['Image'])
        if code['Contents'] is not None:
            color = (0, 255, 0)
            codes.append(code)
        else:
            color = (0, 0, 255)

        # -----DEBUG-----
        if debug_dir is not None:
            if not code:
                base_name = ('unrecognized.page-'
                             + f'{file_index}.x-{chunk["Cell"][0]}.y-{chunk["Cell"][1]}.jpg')
                cv2.imwrite(os.path.join(debug_dir, base_name), chunk['Image'])
            for line_start, line_end in ((0, 1), (1, 2), (2, 3), (3, 0)):
                cv2.line(debug_array,
                         tuple(int(i) for i in chunk['Coords'][line_start]),
                         tuple(int(i) for i in chunk['Coords'][line_end]),
                         (255, 0, 0), 4)
            cv2.putText(debug_array,
                        f'({chunk["Cell"][0]},{chunk["Cell"][1]})',
                        (int(chunk['Coords'][3][0]) + 10, int(chunk['Coords'][3][1]) - 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.5, color, 4)
        # ---------------

    # -----DEBUG-----
    if debug_dir is not None:
        cv2.imwrite(os.path.join(debug_dir, f'page-{file_index}.jpg'), debug_array)
    # ---------------

    return codes

# -----=====| ENCODE MAIN |=====-----

def encode_main(job_name, input_file_name, output_file_name): # pragma: no cover
    logging.info('pawpyrus %s Encoder', __version__)
    logging.info('Job Name: %s', job_name)
    logging.info('Input File: "%s"', ('<stdin>' if input_file_name == '-'
                                      else os.path.realpath(input_file_name)))
    logging.info('Output File: "%s"', os.path.realpath(output_file_name))
    # Read rawdata
    stream = sys.stdin.buffer if input_file_name == '-' else open(input_file_name, 'rb')
    raw_data = stream.read()
    # Create codes dataset
    encoder = AlphaEncoder(C_ALPHANUMERIC_STRING, C_PADDING_CHAR, C_ENCODER_CHAR_CHUNK_SIZE,
                           C_ENCODER_OFFSET_BLOCK_SIZE, C_ENCODER_RUNID_BLOCK_SIZE,
                           C_ENCODER_BLOCKNUM_BLOCK_SIZE)
    dataset = encoder.encode(raw_data, random.random(), C_ENCODER_DATA_CHUNK_SIZE)
    logging.info('Run ID: %s', dataset['RunID'])
    logging.info('SHA-256: %s', dataset['Hash'])
    logging.info('Blocks: %d', dataset['Length'])
    # Create pixelsheets
    pages = create_pixel_sheets(dataset['Codes'], C_PDF_COLUMNS, C_PDF_ROWS,
                                C_QR_SPACING_SIZE, C_PDF_DOT_SPACING_SIZE, C_QR_VERSION,
                                C_QR_CORRECTION_LEVEL, C_ARUCO_DICT, C_TQDM_ASCII)
    # Draw SVG
    svg_pages = draw_svg(pages, C_PDF_PAGE_WIDTH, C_PDF_PAGE_HEIGHT, C_PDF_LEFT_MARGIN,
                         C_PDF_RIGHT_MARGIN, C_PDF_TOP_MARGIN + (5 * C_PDF_LINE_HEIGHT),
                         C_TQDM_ASCII)
    # Draw PDF
    create_pdf(dataset, svg_pages, output_file_name, job_name, C_PDF_LEFT_MARGIN,
               C_PDF_TOP_MARGIN, C_PDF_LINE_HEIGHT, C_PDF_FONT_FAMILY, C_PDF_FONT_SIZE,
               C_PDF_PAGE_HEIGHT, C_TQDM_ASCII)
    logging.info('Job finished')


# -----=====| DECODE MAIN |=====-----

def decode_main(masked_image_input, text_input, debug_dir, output_file_name): # pragma: no cover
    image_input = list()
    if masked_image_input is not None:
        for i in masked_image_input:
            image_input.extend([os.path.realpath(f) for f in glob.glob(i)])
        image_input = sorted(list(set(image_input)))
    if (not image_input) and (text_input is None):
        raise ValueError('Input is empty: no images, no text!')
    logging.info('pawpyrus %s Decoder', __version__)

    # -----DEBUG-----
    if debug_dir is not None:
        logging.info('DEBUG MODE ON')
        os.mkdir(debug_dir)
    # ---------------

    if image_input:
        logging.info('Image Input File(s): %s', ', '.join(image_input))
    if text_input is not None:
        logging.info('Text Input File: %s', os.path.realpath(text_input))
    logging.info('Output File: %s', os.path.realpath(output_file_name))
    annotated_blocks = list()
    for file_index, file_name in enumerate(image_input):
        logging.info('Processing "%s"', file_name)
        annotated_blocks.extend(read_page(file_name, debug_dir, file_index + 1, C_ARUCO_DICT,
                                          C_OPENCV_MIN_MARKER_PERIMETER_RATE, C_TQDM_ASCII))

    # -----DEBUG-----
    if debug_dir is not None:
        detection_stats = {
            'total': len(annotated_blocks),
            'pyzbar_only': [(not block['Detected']['opencv']) and block['Detected']['pyzbar']
                            for block in annotated_blocks].count(True),
            'opencv_only': [block['Detected']['opencv'] and (not block['Detected']['pyzbar'])
                            for block in annotated_blocks].count(True),
            'both': [block['Detected']['opencv'] and block['Detected']['pyzbar']
                     for block in annotated_blocks].count(True),
            'neither': [(not block['Detected']['opencv']) and (not block['Detected']['pyzbar'])
                        for block in annotated_blocks].count(True)
            }
        json.dump(detection_stats,
                  open(os.path.join(debug_dir, 'detection_stats.json'), 'wt'), indent=4)
    # ---------------

    blocks = [block['Contents'] for block in annotated_blocks]
    if text_input is not None:
        with open(text_input, 'rt') as text_file:
            blocks += [Line.rstrip('\n').rstrip(C_PADDING_CHAR) for Line in text_file.readlines()]
            blocks = [Line for Line in blocks if Line]

    # -----DEBUG-----
    if debug_dir is not None:
        with open(os.path.join(debug_dir, 'blocks.txt'), 'wt') as blocks_file:
            blocks_file.write('\n'.join(blocks))
    # ---------------

    encoder = AlphaEncoder(C_ALPHANUMERIC_STRING, C_PADDING_CHAR, C_ENCODER_CHAR_CHUNK_SIZE,
                           C_ENCODER_OFFSET_BLOCK_SIZE, C_ENCODER_RUNID_BLOCK_SIZE,
                           C_ENCODER_BLOCKNUM_BLOCK_SIZE)
    result = encoder.decode(blocks)
    logging.info('Run ID: %s', result['RunID'])
    logging.info('Blocks: %d', result['Blocks'])
    logging.info('SHA-256: %s', result['Hash'])
    with open(output_file_name, 'wb') as out:
        out.write(result['Data'])
    logging.info('Job finished')


## ------======| PARSER |======------

def create_parser(): # pragma: no cover
    default_parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=f'pawpyrus {__version__}: Minimalist paper data storage based on QR codes',
        epilog=f'Bug tracker: {__bugtracker__}'
        )
    default_parser.add_argument('-v', '--version', action='version', version=__version__)
    subparsers = default_parser.add_subparsers(title='Commands', dest='command')
    # Encode parser
    encode_parser = subparsers.add_parser('Encode', help='Encode data as paper storage PDF file')
    encode_parser.add_argument('-n', '--name', required=True, type=str, dest='job_name',
                               help='Job name. Will be printed in page header. Required.')
    encode_parser.add_argument('-i', '--input', required=True, type=str, dest='InputFile',
                               help='File to encode, or "-" to read from stdin. Required.')
    encode_parser.add_argument('-o', '--output', required=True, type=str, dest='output_file',
                               help='PDF file to save. Required.')
    # Decode parser
    decode_parser = subparsers.add_parser('Decode', help='Decode data from paper storage scans')
    decode_parser.add_argument('-i', '--image', nargs='*', type=str, dest='image_input',
                               help='Paper storage scans to decode.')
    decode_parser.add_argument('-t', '--text', type=str, default=None, dest='text_input',
                               help='Files with lists of QR codes content, gathered manually.')
    decode_parser.add_argument('-o', '--output', required=True, type=str, dest='output_file',
                               help='File to save decoded data. Required.')
    decode_parser.add_argument('-d', '--debug-dir', type=str, default=None, dest='debug_dir',
                               help='Directory where to collect debug data if necessary.')

    return default_parser


# -----=====| MAIN |=====-----

def main(): # pragma: no cover
    parser = create_parser()
    namespace = parser.parse_args(sys.argv[1:])
    if namespace.command == 'Encode':
        encode_main(input_file_name=namespace.InputFile,
                    job_name=namespace.job_name,
                    output_file_name=namespace.output_file)
    elif namespace.command == 'Decode':
        decode_main(masked_image_input=namespace.image_input,
                    text_input=namespace.text_input,
                    debug_dir=namespace.debug_dir,
                    output_file_name=namespace.output_file)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
