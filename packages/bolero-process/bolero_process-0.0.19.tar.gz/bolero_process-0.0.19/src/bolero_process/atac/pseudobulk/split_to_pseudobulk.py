import pathlib
import pysam
import ray
import pandas as pd
import subprocess
from functools import partial


def touch_bai_files(bam_paths):
    """Touch to update the timestamp of the bai files."""
    for path in bam_paths:
        bai_path = pathlib.Path(f"{path}.bai")
        if bai_path.exists():
            bai_path.touch()


@ray.remote
class BamWriter:
    """
    Bam writer class to write reads to bam file and able to filter reads by barcodes.
    """
    def __init__(self, path, header, barcodes=None):
        """
        
        Parameters
        ----------
        path : str
            The output bam file path.
        header : dict
            The header of the bam file in OrderedDict format.
        barcodes : list
            The list of barcodes to keep. If None, all reads will be written.
        """
        header = pysam.AlignmentHeader.from_dict(header)
        self.path = path
        self.bam = pysam.AlignmentFile(path, header=header, mode="wb")
        self.header = header

        self.barcodes = None
        if barcodes is not None:
            self.barcodes = set(barcodes)

    def write(self, reads, bc_tag_key="CB"):
        """
        Write reads to the bam file.
        
        Parameters
        ----------
        reads : list of str
            The list of reads to write.
        bc_tag_key : str
            The barcode tag key in the read.
        """
        # print(f"Writing {len(reads)} to {self.path}")
        for read in reads:
            read = pysam.AlignedSegment.fromstring(read, header=self.header)

            if self.barcodes is not None:
                bc = read.get_tag(bc_tag_key)
                if bc not in self.barcodes:
                    continue

            self.bam.write(read)

    def close(self):
        """Close the bam file."""
        self.bam.close()


@ray.remote
class TsvWriter:
    """
    Tsv writer class to write reads to tsv file and able to filter reads by barcodes.
    """
    def __init__(self, path, barcodes=None):
        """
        
        Parameters
        ----------
        path : str
            The output tsv file path.
        barcodes : list
            The list of barcodes to keep. If None, all reads will be written.
        """
        self.path = path
        # Use subprocess to create a popen object to write to the file with bgzip
        # force create if file exists
        self.f = subprocess.Popen(
            ["bgzip", "-f", "-c", ">", path],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            shell=True,
        )
        self.barcodes = None
        if barcodes is not None:
            self.barcodes = set(barcodes)

    def write(self, chunk: pd.DataFrame, barcode_icol=3):
        """
        Write reads to the tsv file.

        Parameters
        ----------
        chunk : pd.DataFrame
            The chunk of reads to write.
        barcode_icol : int
            The barcode column index in the tsv file.
        """
        if isinstance(chunk, list):
            chunk = pd.concat(chunk)

        if self.barcodes is not None:
            # the fourth column is the barcode column
            chunk = chunk[chunk.iloc[:, barcode_icol].isin(self.barcodes)]
        chunk.to_csv(self.f.stdin, sep="\t", index=False, header=False)

    def close(self):
        """Close the tsv file."""
        self.f.stdin.close()
        self.f.wait()


def add_id_to_read(read, file_id, key="CB"):
    """Add file_id to the barcode tag of the read."""
    bc = read.get_tag(key)
    bc = f"{file_id}:{bc}"
    read.set_tag(key, bc)
    return read


def add_id_to_bc(bc, file_id):
    """Add file_id to the barcode."""
    bc = f"{file_id}:{bc}"
    return bc


def _prepare_iter(file_path, file_id, barcode_modify_func):
    if file_id is None:
        barcode_modify_func = None
    if barcode_modify_func is not None:
        barcode_modify_func = partial(barcode_modify_func, file_id=file_id)

    if isinstance(file_path, (str, pathlib.Path)):
        file_path_list = [file_path]
        if file_id is not None:
            file_id = [file_id]
    else:
        file_path_list = list(file_path)
        if file_id is not None:
            if isinstance(file_id, list):
                file_id = list(file_id)
            assert len(file_id) == len(
                file_path_list
            ), f"file_id must have the same length as tsv_path {file_path_list}, got {file_id}"

    return file_path_list, file_id, barcode_modify_func


def _tsv_iter(
    file_path,
    chunk_size,
    file_id=None,
    barcode_icol=3,
    barcode_modify_func=add_id_to_bc,
):
    """
    Iterate over tsv files and yield chunks.
    
    Parameters
    ----------
    file_path : str or list of str
        The path to the tsv file or list of paths.
    chunk_size : int
        The chunk size to yield.
    file_id : str or list of str
        The file id to add to the barcode. If None, no id will be added. 
        If list, must have the same length as file_path.
    barcode_icol : int
        The barcode column index in the tsv file.
    barcode_modify_func : callable
        The function to modify the barcode. If None, no modification will be done.
    """
    file_path_list, file_id, barcode_modify_func = _prepare_iter(
        file_path, file_id, barcode_modify_func
    )

    for idx, file_path in enumerate(file_path_list):
        if file_id is not None:
            file_id = file_id[idx]
            if barcode_modify_func is not None:
                _barcode_modify_func = partial(barcode_modify_func, file_id=file_id)

        chunks = pd.read_csv(file_path, sep="\t", chunksize=chunk_size, header=None)
        for chunk in chunks:
            if barcode_modify_func is not None:
                chunk.iloc[:, barcode_icol] = chunk.iloc[:, barcode_icol].apply(
                    _barcode_modify_func
                )
            yield [chunk]


def _bam_iter(bam_path, chunk_size, file_id=None, barcode_modify_func=add_id_to_read):
    """
    Iterate over bam files and yield chunks.
    
    Parameters
    ----------
    bam_path : str or list of str
        The path to the bam file or list of paths.
    chunk_size : int
        The chunk size to yield.
    file_id : str or list of str
        The file id to add to the barcode. If None, no id will be added. 
        If list, must have the same length as file_path.
    barcode_modify_func : callable
        The function to modify the barcode. If None, no modification will be done.
    """
    file_path_list, file_id, barcode_modify_func = _prepare_iter(
        bam_path, file_id, barcode_modify_func
    )
    for idx, file_path in enumerate(file_path_list):
        if file_id is not None:
            file_id = file_id[idx]
            if barcode_modify_func is not None:
                _barcode_modify_func = partial(barcode_modify_func, file_id=file_id)

        with pysam.AlignmentFile(file_path) as bam:
            reads = []
            for i, read in enumerate(bam):

                if barcode_modify_func is not None:
                    read = _barcode_modify_func(read)

                # pysam.AlignedSegment is not pickleble
                # to_string is 5 times faster than to_dict
                reads.append(read.to_string())
                if (i + 1) % chunk_size == 0:
                    # print(f"Yielding next {chunk_size} reads")
                    yield reads
                    reads = []

            if len(reads) > 0:
                # yield last batch
                yield reads


def _create_bam_writer(bam_path, output_dir, cell_group_dict):
    writers = []
    with pysam.AlignmentFile(bam_path) as bam:
        header = bam.header.to_dict()
        for name, cells in cell_group_dict.items():
            path = f"{output_dir}/{name}.bam"
            writer = BamWriter.remote(path=path, header=header, barcodes=cells)
            writers.append(writer)
    return writers


def _create_tsv_writer(output_dir, cell_group_dict):
    writers = []
    for name, cells in cell_group_dict.items():
        path = f"{output_dir}/{name}.tsv.gz"
        writer = TsvWriter.remote(path=path, barcodes=cells)
        writers.append(writer)
    return writers


def _split(input_iter, writers, chunk_size, **write_kwargs):
    remaining_ids = []
    cur_reads = []
    running = True
    while running:
        # this allows async read from the input bam while writer are writing
        while remaining_ids:
            # Use ray.wait to get the object ref of the first task that completes.
            _, remaining_ids = ray.wait(remaining_ids)
            if len(cur_reads) >= chunk_size:
                continue
            else:
                try:
                    data = next(input_iter)
                    cur_reads.extend(data)
                except StopIteration:
                    running = False

        remote_cur_reads = ray.put(cur_reads)
        remaining_ids = [
            writer.write.remote(remote_cur_reads, **write_kwargs) for writer in writers
        ]
        cur_reads = []

    # make sure all writer done
    if len(remaining_ids) > 0:
        _ = ray.get(remaining_ids)
        remaining_ids = []

    # close all writer
    fs = []
    for writer in writers:
        fs.append(writer.close.remote())
    _ = ray.get(fs)
    return


def split_bam(
    bam_path,
    output_dir,
    cell_group_dict,
    bam_id=None,
    bc_tag="CB",
    chunk_size=1000000,
    barcode_modify_func=add_id_to_read,
):
    """
    Split bam file to multiple bam files based on cell group.
    
    Parameters
    ----------
    bam_path : str, pathlib.Path, or list of str
        The input bam file path or list of paths.
    output_dir : str
        The output directory to save the splitted bam files.
    cell_group_dict : dict
        The cell group dictionary with cell group name as key and cell barcodes as value.
    bam_id : str
        The bam file id to add to the barcode. If None, no id will be added.
    bc_tag : str
        The barcode tag key in the bam file.
    chunk_size : int
        The chunk size to read from the bam file.
    barcode_modify_func : callable
        The function to modify the barcode. If None, no modification will be done.
    """
    output_dir = pathlib.Path(output_dir)
    output_dir.mkdir(exist_ok=True, parents=True)
    writers = _create_bam_writer(bam_path, output_dir, cell_group_dict)
    input_iter = _bam_iter(
        bam_path,
        chunk_size=chunk_size,
        file_id=bam_id,
        barcode_modify_func=barcode_modify_func,
    )

    _split(input_iter, writers, chunk_size, bc_tag_key=bc_tag)
    return


def split_fragments(
    frag_path,
    output_dir,
    cell_group_dict,
    frag_id=None,
    barcode_icol=3,
    chunk_size=1000000,
    barcode_modify_func=add_id_to_bc,
):
    """
    Split fragment file to multiple tsv files based on cell group.
    
    Parameters
    ----------
    frag_path : str, pathlib.Path, or list of str
        The input fragment file path or list of paths.
    output_dir : str
        The output directory to save the splitted tsv files.
    cell_group_dict : dict
        The cell group dictionary with cell group name as key and cell barcodes as value.
    frag_id : str
        The fragment file id to add to the barcode. If None, no id will be added.
    barcode_icol : int
        The barcode column index in the tsv file.
    chunk_size : int
        The chunk size to read from the tsv file.
    barcode_modify_func : callable
        The function to modify the barcode. If None, no modification will be done.
    """
    output_dir = pathlib.Path(output_dir)
    output_dir.mkdir(exist_ok=True, parents=True)
    writers = _create_tsv_writer(output_dir, cell_group_dict)
    input_iter = _tsv_iter(
        frag_path,
        file_id=frag_id,
        chunk_size=chunk_size,
        barcode_modify_func=barcode_modify_func,
        barcode_icol=barcode_icol,
    )
    _split(input_iter, writers, chunk_size, barcode_icol=barcode_icol)
    return
